"""Optional fixed-reranker probe for SID prefix utility.

This module is intentionally outside the core D1-D5 diagnostics. It asks
whether SID prefix buckets can recover held-out targets under a fixed,
train-only candidate/reranking protocol. It is not a trained generator
evaluation and should not be reported as downstream system quality.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def _level_cols(frame: pd.DataFrame) -> list[str]:
    cols = [col for col in frame.columns if col.startswith("sid_level_")]
    return sorted(cols, key=lambda col: int(col.rsplit("_", 1)[1]))


def _split_train_eval(interactions: pd.DataFrame, strategy: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = interactions.copy()
    frame["item_id"] = frame["item_id"].astype(int)
    if strategy == "auto":
        if "split" in frame.columns and (frame["split"].astype(str) == "train").any():
            strategy = "explicit"
        else:
            strategy = "leave_last"

    if strategy == "explicit":
        if "split" not in frame.columns:
            raise ValueError("explicit split strategy requires a split column")
        train = frame[frame["split"].astype(str) == "train"].copy()
        eval_events = frame[frame["split"].astype(str) != "train"].copy()
        return train, eval_events

    if strategy != "leave_last":
        raise ValueError(f"Unknown eval strategy: {strategy}")

    order_cols = ["user_id"]
    if "timestamp" in frame.columns:
        order_cols.append("timestamp")
    elif "position" in frame.columns:
        order_cols.append("position")
    frame = frame.sort_values(order_cols, kind="stable").copy()
    frame["_rank"] = frame.groupby("user_id").cumcount()
    frame["_count"] = frame.groupby("user_id")["item_id"].transform("size")
    eligible = frame["_count"] >= 2
    eval_events = frame[eligible & (frame["_rank"] == frame["_count"] - 1)].copy()
    train = frame[eligible & (frame["_rank"] < frame["_count"] - 1)].copy()
    return train.drop(columns=["_rank", "_count"]), eval_events.drop(columns=["_rank", "_count"])


def _bounded_train(train: pd.DataFrame, max_user_items: int) -> pd.DataFrame:
    events = train[["user_id", "item_id"]].drop_duplicates()
    sizes = events.groupby("user_id").size()
    keep = sizes[(sizes >= 2) & (sizes <= max_user_items)].index
    return events[events["user_id"].isin(keep)].copy()


def _cooccurrence_counts(train: pd.DataFrame, max_pair_events: int, max_user_items: int) -> dict[tuple[int, int], int]:
    events = _bounded_train(train, max_user_items=max_user_items)
    sizes = events.groupby("user_id").size().sort_index()
    selected_users = []
    pair_events = 0
    for user_id, size in sizes.items():
        user_pairs = int(size * (size - 1) // 2)
        if selected_users and pair_events + user_pairs > max_pair_events:
            break
        selected_users.append(user_id)
        pair_events += user_pairs
    selected = events[events["user_id"].isin(selected_users)]
    counts: dict[tuple[int, int], int] = defaultdict(int)
    for _, group in selected.groupby("user_id", sort=False):
        items = sorted(group["item_id"].astype(int).unique())
        for pos, left in enumerate(items):
            for right in items[pos + 1 :]:
                counts[(left, right)] += 1
                counts[(right, left)] += 1
    return counts


def _d3_weighted(
    sid: pd.DataFrame,
    train: pd.DataFrame,
    depth: int,
    top_k: int,
    max_pair_events: int,
    max_user_items: int,
) -> tuple[float, int, int]:
    level_cols = _level_cols(sid)
    item_prefix = {
        int(row.item_id): tuple(getattr(row, col) for col in level_cols[:depth])
        for row in sid[["item_id", *level_cols]].itertuples(index=False)
    }
    train = _bounded_train(train, max_user_items=max_user_items)
    sizes = train.groupby("user_id").size().sort_index()
    selected_users = []
    pair_events = 0
    for user_id, size in sizes.items():
        user_pairs = int(size * (size - 1) // 2)
        if selected_users and pair_events + user_pairs > max_pair_events:
            break
        selected_users.append(user_id)
        pair_events += user_pairs
    selected = train[train["user_id"].isin(selected_users)]

    neighbor_counts: dict[int, Counter[int]] = defaultdict(Counter)
    for _, group in selected.groupby("user_id", sort=False):
        items = sorted(set(int(item) for item in group["item_id"] if int(item) in item_prefix))
        for pos, left in enumerate(items):
            for right in items[pos + 1 :]:
                neighbor_counts[left][right] += 1
                neighbor_counts[right][left] += 1

    total = 0
    same = 0
    for item, counts in neighbor_counts.items():
        for neighbor, _ in counts.most_common(top_k):
            if neighbor not in item_prefix:
                continue
            total += 1
            same += int(item_prefix[item] == item_prefix[neighbor])
    return (float(same / total) if total else 0.0, len(selected_users), pair_events)


def _build_prefix_index(sid: pd.DataFrame, depth: int) -> tuple[dict[int, tuple[Any, ...]], dict[tuple[Any, ...], np.ndarray]]:
    level_cols = _level_cols(sid)
    if depth < 1 or depth > len(level_cols):
        raise ValueError(f"Invalid prefix depth {depth}; SID has {len(level_cols)} levels")
    item_prefix: dict[int, tuple[Any, ...]] = {}
    buckets: dict[tuple[Any, ...], list[int]] = defaultdict(list)
    for row in sid[["item_id", *level_cols[:depth]]].itertuples(index=False):
        item_id = int(row.item_id)
        prefix = tuple(getattr(row, col) for col in level_cols[:depth])
        item_prefix[item_id] = prefix
        buckets[prefix].append(item_id)
    bucket_arrays = {prefix: np.asarray(sorted(items), dtype=np.int64) for prefix, items in buckets.items()}
    return item_prefix, bucket_arrays


def _rank_candidates(
    candidates: set[int],
    history: set[int],
    popularity: dict[int, int],
    co_counts: dict[tuple[int, int], int],
    ranker: str,
) -> list[int]:
    if ranker == "popularity":
        return sorted(candidates, key=lambda item: (-popularity.get(item, 0), item))
    if ranker == "cooccurrence_popularity":
        return sorted(
            candidates,
            key=lambda item: (
                -sum(co_counts.get((item, hist), 0) for hist in history),
                -popularity.get(item, 0),
                item,
            ),
        )
    raise ValueError(f"Unknown ranker: {ranker}")


def _dcg(ranks: list[int]) -> float:
    return float(sum(1.0 / np.log2(rank + 1) for rank in ranks))


def _evaluate_one(
    sid: pd.DataFrame,
    interactions: pd.DataFrame,
    depth: int,
    ranker: str,
    rec_k: int,
    d3_top_k: int,
    max_users: int,
    max_pair_events: int,
    max_user_items: int,
    eval_strategy: str,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    train, eval_events = _split_train_eval(interactions, strategy=eval_strategy)
    item_ids = set(int(item) for item in sid["item_id"])
    train = train[train["item_id"].astype(int).isin(item_ids)]
    eval_events = eval_events[eval_events["item_id"].astype(int).isin(item_ids)]
    if max_users > 0:
        users = sorted(set(train["user_id"]).intersection(set(eval_events["user_id"])))[:max_users]
        train = train[train["user_id"].isin(users)]
        eval_events = eval_events[eval_events["user_id"].isin(users)]

    item_prefix, buckets = _build_prefix_index(sid, depth=depth)
    popularity = train.groupby("item_id").size().astype(int).to_dict()
    co_counts = _cooccurrence_counts(train, max_pair_events=max_pair_events, max_user_items=max_user_items)
    d3_weighted, users_used, pair_events = _d3_weighted(
        sid,
        train,
        depth=depth,
        top_k=d3_top_k,
        max_pair_events=max_pair_events,
        max_user_items=max_user_items,
    )

    train_by_user = {
        user: set(int(item) for item in group["item_id"])
        for user, group in train.groupby("user_id", sort=False)
    }
    eval_by_user = {
        user: [int(item) for item in group["item_id"]]
        for user, group in eval_events.groupby("user_id", sort=False)
    }

    rows = []
    for user in sorted(set(train_by_user).intersection(eval_by_user)):
        history = {item for item in train_by_user[user] if item in item_prefix}
        targets = [item for item in eval_by_user[user] if item in item_prefix]
        if not history or not targets:
            continue
        candidate_set: set[int] = set()
        for item in history:
            candidate_set.update(int(cand) for cand in buckets[item_prefix[item]])
        candidate_set.difference_update(history)
        if not candidate_set:
            continue
        target_set = set(targets)
        candidate_hits = target_set.intersection(candidate_set)
        ranked = _rank_candidates(candidate_set, history, popularity, co_counts, ranker=ranker)
        top = ranked[:rec_k]
        top_pos = {item: pos + 1 for pos, item in enumerate(top)}
        hit_ranks = [top_pos[item] for item in targets if item in top_pos]
        ideal_hits = min(len(targets), rec_k)
        ideal_dcg = _dcg(list(range(1, ideal_hits + 1))) if ideal_hits else 0.0
        rows.append(
            {
                "user_id": user,
                "targets": len(targets),
                "candidate_count": len(candidate_set),
                "candidate_hits": len(candidate_hits),
                "candidate_recall": len(candidate_hits) / len(targets),
                "recall_at_k": len(hit_ranks) / len(targets),
                "ndcg_at_k": _dcg(hit_ranks) / ideal_dcg if ideal_dcg else 0.0,
                "mrr_at_k": 1.0 / min(hit_ranks) if hit_ranks else 0.0,
            }
        )
    user_metrics = pd.DataFrame(rows)
    stats = {
        "d3_weighted": d3_weighted,
        "users_used_for_d3": users_used,
        "pair_events_for_d3": pair_events,
        "train_events": len(train),
        "eval_events": len(eval_events),
    }
    return user_metrics, stats


def _prepare_context(
    sid: pd.DataFrame,
    interactions: pd.DataFrame,
    depth: int,
    d3_top_k: int,
    max_users: int,
    max_pair_events: int,
    max_user_items: int,
    eval_strategy: str,
) -> dict[str, Any]:
    train, eval_events = _split_train_eval(interactions, strategy=eval_strategy)
    item_ids = set(int(item) for item in sid["item_id"])
    train = train[train["item_id"].astype(int).isin(item_ids)]
    eval_events = eval_events[eval_events["item_id"].astype(int).isin(item_ids)]
    if max_users > 0:
        users = sorted(set(train["user_id"]).intersection(set(eval_events["user_id"])))[:max_users]
        train = train[train["user_id"].isin(users)]
        eval_events = eval_events[eval_events["user_id"].isin(users)]

    item_prefix, buckets = _build_prefix_index(sid, depth=depth)
    popularity = train.groupby("item_id").size().astype(int).to_dict()
    co_counts = _cooccurrence_counts(train, max_pair_events=max_pair_events, max_user_items=max_user_items)
    d3_weighted, users_used, pair_events = _d3_weighted(
        sid,
        train,
        depth=depth,
        top_k=d3_top_k,
        max_pair_events=max_pair_events,
        max_user_items=max_user_items,
    )
    train_by_user = {
        user: set(int(item) for item in group["item_id"])
        for user, group in train.groupby("user_id", sort=False)
    }
    eval_by_user = {
        user: [int(item) for item in group["item_id"]]
        for user, group in eval_events.groupby("user_id", sort=False)
    }
    return {
        "item_prefix": item_prefix,
        "buckets": buckets,
        "popularity": popularity,
        "co_counts": co_counts,
        "train_by_user": train_by_user,
        "eval_by_user": eval_by_user,
        "stats": {
            "d3_weighted": d3_weighted,
            "users_used_for_d3": users_used,
            "pair_events_for_d3": pair_events,
            "train_events": len(train),
            "eval_events": len(eval_events),
        },
    }


def _evaluate_context_for_ranker(
    context: dict[str, Any],
    ranker: str,
    rec_ks: list[int],
) -> dict[int, pd.DataFrame]:
    max_k = max(rec_ks)
    rows_by_k: dict[int, list[dict[str, Any]]] = {rec_k: [] for rec_k in rec_ks}
    item_prefix = context["item_prefix"]
    buckets = context["buckets"]
    popularity = context["popularity"]
    co_counts = context["co_counts"]
    train_by_user = context["train_by_user"]
    eval_by_user = context["eval_by_user"]

    for user in sorted(set(train_by_user).intersection(eval_by_user)):
        history = {item for item in train_by_user[user] if item in item_prefix}
        targets = [item for item in eval_by_user[user] if item in item_prefix]
        if not history or not targets:
            continue
        candidate_set: set[int] = set()
        for item in history:
            candidate_set.update(int(cand) for cand in buckets[item_prefix[item]])
        candidate_set.difference_update(history)
        if not candidate_set:
            continue
        target_set = set(targets)
        candidate_hits = target_set.intersection(candidate_set)
        ranked = _rank_candidates(candidate_set, history, popularity, co_counts, ranker=ranker)[:max_k]
        for rec_k in rec_ks:
            top = ranked[:rec_k]
            top_pos = {item: pos + 1 for pos, item in enumerate(top)}
            hit_ranks = [top_pos[item] for item in targets if item in top_pos]
            ideal_hits = min(len(targets), rec_k)
            ideal_dcg = _dcg(list(range(1, ideal_hits + 1))) if ideal_hits else 0.0
            rows_by_k[rec_k].append(
                {
                    "user_id": user,
                    "targets": len(targets),
                    "candidate_count": len(candidate_set),
                    "candidate_hits": len(candidate_hits),
                    "candidate_recall": len(candidate_hits) / len(targets),
                    "recall_at_k": len(hit_ranks) / len(targets),
                    "ndcg_at_k": _dcg(hit_ranks) / ideal_dcg if ideal_dcg else 0.0,
                    "mrr_at_k": 1.0 / min(hit_ranks) if hit_ranks else 0.0,
                }
            )
    return {rec_k: pd.DataFrame(rows) for rec_k, rows in rows_by_k.items()}


def _bootstrap_ci(values: np.ndarray, rng: np.random.Generator, samples: int) -> tuple[float, float, float]:
    if len(values) == 0:
        return 0.0, 0.0, 0.0
    mean = float(np.mean(values))
    if samples <= 0 or len(values) < 2:
        return mean, mean, mean
    draws = rng.choice(values, size=(samples, len(values)), replace=True).mean(axis=1)
    return mean, float(np.quantile(draws, 0.025)), float(np.quantile(draws, 0.975))


def _summarize_user_metrics(
    user_metrics: pd.DataFrame,
    base: dict[str, Any],
    bootstrap_samples: int,
    seed: int,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    summary = {
        **base,
        "users_with_eval_targets": int(len(user_metrics)),
        "targets_evaluated": int(user_metrics["targets"].sum()) if not user_metrics.empty else 0,
        "mean_candidate_count": float(user_metrics["candidate_count"].mean()) if not user_metrics.empty else 0.0,
        "median_candidate_count": float(user_metrics["candidate_count"].median()) if not user_metrics.empty else 0.0,
    }
    for metric in ("candidate_recall", "recall_at_k", "ndcg_at_k", "mrr_at_k"):
        values = user_metrics[metric].to_numpy(float) if metric in user_metrics.columns else np.asarray([], dtype=float)
        mean, lo, hi = _bootstrap_ci(values, rng, bootstrap_samples)
        summary[metric] = mean
        summary[f"{metric}_ci_low"] = lo
        summary[f"{metric}_ci_high"] = hi
    return summary


def _correlations(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    group_cols = ["dataset", "prefix_depth", "ranker", "rec_k"]
    for group_key, group in summary.groupby(group_cols, dropna=False):
        if len(group) < 3:
            continue
        key_values = dict(zip(group_cols, group_key))
        for metric in ("candidate_recall", "recall_at_k", "ndcg_at_k", "mrr_at_k"):
            rows.append(
                {
                    **key_values,
                    "metric": metric,
                    "pearson_with_d3_weighted": group["d3_weighted"].corr(group[metric], method="pearson"),
                    "spearman_with_d3_weighted": group["d3_weighted"].corr(group[metric], method="spearman"),
                    "rows": len(group),
                }
            )
    return pd.DataFrame(rows)


def run_probe(
    manifest: pd.DataFrame,
    output_dir: Path,
    depths: list[int],
    rec_ks: list[int],
    rankers: list[str],
    d3_top_k: int,
    max_users: int,
    max_pair_events: int,
    max_user_items: int,
    eval_strategy: str,
    bootstrap_samples: int,
    seed: int,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_rows = []
    user_frames = []
    for row_idx, row in manifest.iterrows():
        sid = pd.read_parquet(row["sid_assignments"])
        interactions = pd.read_parquet(row["interactions"])
        requested_method = _manifest_value(row, "method")
        requested_dataset = _manifest_value(row, "dataset")
        if requested_method is not None and "method" in sid.columns:
            sid = sid[sid["method"].astype(str) == str(requested_method)].copy()
        if requested_dataset is not None and "dataset" in sid.columns:
            sid = sid[sid["dataset"].astype(str) == str(requested_dataset)].copy()
            if "dataset" in interactions.columns:
                interactions = interactions[interactions["dataset"].astype(str) == str(requested_dataset)].copy()
        if sid.empty:
            raise ValueError(f"Manifest row {row_idx} selects no SID rows")
        method = str(requested_method or sid["method"].iloc[0])
        dataset = str(requested_dataset or sid["dataset"].iloc[0])
        label = str(_manifest_value(row, "label") or method)
        for depth in depths:
            context = _prepare_context(
                sid=sid,
                interactions=interactions,
                depth=depth,
                d3_top_k=d3_top_k,
                max_users=max_users,
                max_pair_events=max_pair_events,
                max_user_items=max_user_items,
                eval_strategy=eval_strategy,
            )
            for ranker in rankers:
                user_metrics_by_k = _evaluate_context_for_ranker(context, ranker=ranker, rec_ks=rec_ks)
                for rec_k in rec_ks:
                    user_metrics = user_metrics_by_k[rec_k]
                    base = {
                        "dataset": dataset,
                        "label": label,
                        "method": method,
                        "manifest_row": int(row_idx),
                        "prefix_depth": depth,
                        "ranker": ranker,
                        "rec_k": rec_k,
                        **context["stats"],
                    }
                    summary_rows.append(
                        _summarize_user_metrics(
                            user_metrics,
                            base=base,
                            bootstrap_samples=bootstrap_samples,
                            seed=seed + int(row_idx) * 1009 + depth * 101 + rec_k,
                        )
                    )
                    if not user_metrics.empty:
                        user_frame = user_metrics.assign(**base)
                        user_frames.append(user_frame)

    summary = pd.DataFrame(summary_rows)
    correlations = _correlations(summary)
    summary.to_csv(output_dir / "downstream_probe_summary.csv", index=False)
    correlations.to_csv(output_dir / "downstream_probe_correlations.csv", index=False)
    if user_frames:
        pd.concat(user_frames, ignore_index=True).to_csv(output_dir / "downstream_probe_user_metrics.csv", index=False)
    manifest.to_csv(output_dir / "downstream_probe_manifest_resolved.csv", index=False)
    metadata = {
        "depths": depths,
        "rec_ks": rec_ks,
        "rankers": rankers,
        "d3_top_k": d3_top_k,
        "max_users": max_users,
        "max_pair_events": max_pair_events,
        "max_user_items": max_user_items,
        "eval_strategy": eval_strategy,
        "bootstrap_samples": bootstrap_samples,
        "seed": seed,
        "rows": len(summary),
    }
    (output_dir / "downstream_probe_run.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata


def _parse_int_list(text: str) -> list[int]:
    return [int(part) for part in text.split(",") if part.strip()]


def _parse_str_list(text: str) -> list[str]:
    return [part.strip() for part in text.split(",") if part.strip()]


def _manifest_value(row: pd.Series, key: str) -> Any | None:
    if key not in row:
        return None
    value = row[key]
    if pd.isna(value):
        return None
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="Run optional SID prefix downstream probe.")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--depths", default="1,2")
    parser.add_argument("--rec-ks", default="10,20,50")
    parser.add_argument("--rankers", default="cooccurrence_popularity,popularity")
    parser.add_argument("--d3-top-k", type=int, default=20)
    parser.add_argument("--max-users", type=int, default=5000)
    parser.add_argument("--max-pair-events", type=int, default=2_000_000)
    parser.add_argument("--max-user-items", type=int, default=200)
    parser.add_argument("--eval-strategy", choices=("auto", "explicit", "leave_last"), default="auto")
    parser.add_argument("--bootstrap-samples", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    manifest = pd.read_csv(args.manifest)
    required = {"sid_assignments", "interactions"}
    missing = sorted(required - set(manifest.columns))
    if missing:
        raise ValueError(f"Manifest missing columns: {missing}")
    metadata = run_probe(
        manifest=manifest,
        output_dir=args.output_dir,
        depths=_parse_int_list(args.depths),
        rec_ks=_parse_int_list(args.rec_ks),
        rankers=_parse_str_list(args.rankers),
        d3_top_k=args.d3_top_k,
        max_users=args.max_users,
        max_pair_events=args.max_pair_events,
        max_user_items=args.max_user_items,
        eval_strategy=args.eval_strategy,
        bootstrap_samples=args.bootstrap_samples,
        seed=args.seed,
    )
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
