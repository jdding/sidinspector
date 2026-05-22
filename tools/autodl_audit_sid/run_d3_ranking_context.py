#!/usr/bin/env python3
"""Bounded prefix-retrieval ranking context for D3 SID alignment.

This is a proxy evaluator, not a downstream recommender benchmark.  It treats a
SID prefix bucket as a lightweight retrieval neighborhood: for each user's train
history, retrieve items sharing a SID prefix with history items and check whether
held-out validation/test items appear in the top-k candidates.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from audit_sid.metrics import alignment


DEFAULT_DATASET = "Musical_Instruments"
DEFAULT_ITEM_METADATA = Path("_gate0_artifacts/resid_musical_normalized/item_metadata.parquet")
DEFAULT_INTERACTIONS = Path("_gate0_artifacts/resid_musical_normalized/interactions.parquet")
DEFAULT_SID_PATHS = [
    Path("_gate0_artifacts/resid_real_runs/combined_resid_sanity/sid_assignments.parquet"),
    Path(
        "_gate0_artifacts/grid_same_dataset_runs/"
        "grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/"
        "grid_export/normalized/sid_assignments.parquet"
    ),
    Path(
        "_gate0_artifacts/grid_same_dataset_runs/"
        "matched_capacity_grid_32_1280_1280_seed42_20260520/"
        "grid_export/normalized/sid_assignments.parquet"
    ),
]


def _read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"required input not found: {path}")
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    if path.suffix == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"unsupported table suffix for {path}; expected .parquet or .csv")


def _level_cols(frame: pd.DataFrame) -> list[str]:
    cols = []
    for col in frame.columns:
        if not col.startswith("sid_level_"):
            continue
        if frame[col].isna().all():
            continue
        cols.append(col)
    return sorted(cols, key=lambda name: int(name.rsplit("_", 1)[1]))


def _require_columns(name: str, frame: pd.DataFrame, columns: Iterable[str]) -> None:
    missing = [col for col in columns if col not in frame.columns]
    if missing:
        raise ValueError(f"{name} is missing required columns: {', '.join(missing)}")


def _train_events(interactions: pd.DataFrame) -> pd.DataFrame:
    if "split" not in interactions.columns:
        return interactions
    train = interactions[interactions["split"] == "train"]
    return train if not train.empty else interactions


def _eval_events(interactions: pd.DataFrame, eval_splits: set[str]) -> pd.DataFrame:
    if "split" in interactions.columns:
        out = interactions[interactions["split"].astype(str).isin(eval_splits)].copy()
        if not out.empty:
            return out
    if "timestamp" in interactions.columns:
        ordered = interactions.sort_values(["user_id", "timestamp", "item_id"])
        return ordered.groupby("user_id", sort=True).tail(1).copy()
    return interactions.drop_duplicates(["user_id", "item_id"]).copy()


def _sort_events(frame: pd.DataFrame) -> pd.DataFrame:
    cols = ["user_id"]
    if "timestamp" in frame.columns:
        cols.append("timestamp")
    cols.append("item_id")
    return frame.sort_values(cols)


def _filter_items(
    item_metadata: pd.DataFrame,
    interactions: pd.DataFrame,
    sid: pd.DataFrame,
    max_items: int | None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if not max_items:
        return item_metadata, interactions, sid
    keep = set(item_metadata.sort_values("item_id")["item_id"].astype(int).head(max_items))
    item_metadata = item_metadata[item_metadata["item_id"].astype(int).isin(keep)].copy()
    interactions = interactions[interactions["item_id"].astype(int).isin(keep)].copy()
    sid = sid[sid["item_id"].astype(int).isin(keep)].copy()
    return item_metadata, interactions, sid


def load_sid_assignments(paths: list[Path], dataset_name: str, methods: set[str] | None = None) -> pd.DataFrame:
    frames = []
    for path in paths:
        frame = _read_table(path).copy()
        _require_columns(str(path), frame, ["item_id", "method"])
        if "dataset" not in frame.columns:
            frame["dataset"] = dataset_name
        frames.append(frame)
    if not frames:
        raise ValueError("no sid assignment paths provided")
    sid = pd.concat(frames, ignore_index=True)
    if methods:
        sid = sid[sid["method"].astype(str).isin(methods)].copy()
    if sid.empty:
        raise ValueError("no SID rows remain after method filtering")
    duplicate = sid.duplicated(["dataset", "method", "item_id"])
    if duplicate.any():
        examples = sid.loc[duplicate, ["dataset", "method", "item_id"]].head(5).to_dict("records")
        raise ValueError(f"duplicate SID rows across inputs; examples={examples}")
    if not _level_cols(sid):
        raise ValueError("SID assignments must include at least one sid_level_* column")
    return sid


def _bounded_train_histories(
    interactions: pd.DataFrame,
    eligible_users: set[int],
    max_history_items: int,
) -> dict[int, list[int]]:
    train = _sort_events(_train_events(interactions))
    train = train[train["user_id"].astype(int).isin(eligible_users)]
    histories: dict[int, list[int]] = {}
    for user_id, group in train.groupby("user_id", sort=True):
        values = group["item_id"].astype(int).drop_duplicates().tolist()
        if max_history_items > 0:
            values = values[-max_history_items:]
        histories[int(user_id)] = values
    return histories


def _bounded_targets(
    interactions: pd.DataFrame,
    eval_splits: set[str],
    max_users: int,
    max_targets_per_user: int,
) -> pd.DataFrame:
    eval_frame = _sort_events(_eval_events(interactions, eval_splits))
    eval_frame = eval_frame.drop_duplicates(["user_id", "item_id"])
    train_users = set(_train_events(interactions)["user_id"].astype(int))
    eval_frame = eval_frame[eval_frame["user_id"].astype(int).isin(train_users)]
    if max_targets_per_user > 0:
        eval_frame = eval_frame.groupby("user_id", sort=True).head(max_targets_per_user).reset_index(drop=True)
    if max_users > 0:
        users = sorted(eval_frame["user_id"].astype(int).unique())[:max_users]
        eval_frame = eval_frame[eval_frame["user_id"].astype(int).isin(users)]
    return eval_frame.reset_index(drop=True)


def _prefix_key(frame: pd.DataFrame, level_cols: list[str], depth: int) -> pd.Series:
    return frame[level_cols[:depth]].astype(int).astype(str).agg("-".join, axis=1)


def _build_prefix_index(
    sid_group: pd.DataFrame,
    interactions: pd.DataFrame,
    depth: int,
    max_candidates_per_prefix: int,
) -> tuple[dict[int, str], dict[str, list[int]], dict[int, int]]:
    level_cols = _level_cols(sid_group)
    if depth > len(level_cols):
        raise ValueError(f"depth {depth} exceeds available SID levels {len(level_cols)} for {sid_group['method'].iloc[0]}")
    group = sid_group[["item_id", *level_cols]].copy()
    group["item_id"] = group["item_id"].astype(int)
    group["prefix"] = _prefix_key(group, level_cols, depth)
    popularity = _train_events(interactions).groupby("item_id").size().rename("popularity").reset_index()
    ranked = group.merge(popularity, on="item_id", how="left").fillna({"popularity": 0})
    ranked["popularity"] = ranked["popularity"].astype(int)
    ranked = ranked.sort_values(["prefix", "popularity", "item_id"], ascending=[True, False, True])
    item_to_prefix = dict(zip(ranked["item_id"].astype(int), ranked["prefix"].astype(str)))
    item_popularity = dict(zip(ranked["item_id"].astype(int), ranked["popularity"].astype(int)))
    prefix_to_items: dict[str, list[int]] = {}
    for prefix, bucket in ranked.groupby("prefix", sort=True):
        items = bucket["item_id"].astype(int).tolist()
        if max_candidates_per_prefix > 0:
            items = items[:max_candidates_per_prefix]
        prefix_to_items[str(prefix)] = items
    return item_to_prefix, prefix_to_items, item_popularity


def evaluate_prefix_retrieval(
    sid: pd.DataFrame,
    interactions: pd.DataFrame,
    *,
    eval_splits: set[str],
    top_k: int,
    max_users: int,
    max_history_items: int,
    max_targets_per_user: int,
    max_candidates_per_prefix: int,
    depths: list[int],
) -> pd.DataFrame:
    _require_columns("interactions", interactions, ["user_id", "item_id"])
    _require_columns("sid_assignments", sid, ["dataset", "method", "item_id", "sid"])
    targets = _bounded_targets(interactions, eval_splits, max_users, max_targets_per_user)
    if targets.empty:
        raise ValueError("no eligible evaluation targets after split/user bounds")
    eligible_users = set(targets["user_id"].astype(int))
    histories = _bounded_train_histories(interactions, eligible_users, max_history_items)
    rows = []
    for (dataset, method), group in sid.groupby(["dataset", "method"], sort=True):
        group_items = set(group["item_id"].astype(int))
        group_targets = targets[targets["item_id"].astype(int).isin(group_items)].copy()
        if group_targets.empty:
            continue
        for depth in depths:
            if depth > len(_level_cols(group)):
                continue
            item_to_prefix, prefix_to_items, item_popularity = _build_prefix_index(
                group,
                interactions,
                depth,
                max_candidates_per_prefix,
            )
            hits = 0
            covered = 0
            reciprocal_rank = 0.0
            candidate_counts = []
            prefix_counts = []
            evaluated = 0
            users_with_candidates: set[int] = set()
            for row in group_targets.itertuples(index=False):
                user_id = int(row.user_id)
                target_item = int(row.item_id)
                history = [item for item in histories.get(user_id, []) if item in item_to_prefix]
                if not history:
                    continue
                history_set = set(history)
                query_prefixes = sorted({item_to_prefix[item] for item in history})
                scores: dict[int, int] = defaultdict(int)
                for prefix in query_prefixes:
                    for candidate in prefix_to_items.get(prefix, []):
                        if candidate not in history_set:
                            scores[candidate] += 1
                if not scores:
                    continue
                evaluated += 1
                users_with_candidates.add(user_id)
                candidate_counts.append(len(scores))
                prefix_counts.append(len(query_prefixes))
                if target_item in scores:
                    covered += 1
                ranked = sorted(scores, key=lambda item: (-scores[item], -item_popularity.get(item, 0), item))
                top_items = ranked[:top_k]
                if target_item in top_items:
                    rank = top_items.index(target_item) + 1
                    hits += 1
                    reciprocal_rank += 1.0 / rank
            rows.append(
                {
                    "dataset": dataset,
                    "method": method,
                    "prefix_depth": depth,
                    "top_k": top_k,
                    "users_with_eval_targets": int(group_targets["user_id"].nunique()),
                    "users_with_candidates": len(users_with_candidates),
                    "targets_seen": int(len(group_targets)),
                    "targets_evaluated": evaluated,
                    "candidate_coverage_rate": float(covered / evaluated) if evaluated else 0.0,
                    "hit_rate_at_k": float(hits / evaluated) if evaluated else 0.0,
                    "mrr_at_k": float(reciprocal_rank / evaluated) if evaluated else 0.0,
                    "mean_candidate_count": float(pd.Series(candidate_counts).mean()) if candidate_counts else 0.0,
                    "median_candidate_count": float(pd.Series(candidate_counts).median()) if candidate_counts else 0.0,
                    "mean_query_prefix_count": float(pd.Series(prefix_counts).mean()) if prefix_counts else 0.0,
                }
            )
    if not rows:
        raise ValueError("no ranking rows produced; check SID item coverage and depth bounds")
    return pd.DataFrame(rows)


def compute_d3_context(
    sid: pd.DataFrame,
    item_metadata: pd.DataFrame,
    interactions: pd.DataFrame,
    *,
    d3_top_k: int,
    d3_max_pair_events: int,
    d3_max_user_items: int,
) -> pd.DataFrame:
    d3 = alignment(
        sid,
        item_metadata,
        interactions,
        top_k=d3_top_k,
        max_pair_events=d3_max_pair_events,
        max_user_items=d3_max_user_items,
    )
    return d3[
        [
            "dataset",
            "method",
            "prefix_depth",
            "mean_collab_prefix_recall",
            "weighted_collab_prefix_recall",
            "collab_edges_same_prefix_rate",
            "users_used",
            "pair_events",
            "collab_items",
        ]
    ].copy()


def run_context(
    *,
    sid_paths: list[Path],
    item_metadata_path: Path,
    interactions_path: Path,
    dataset_name: str,
    methods: set[str] | None,
    output_dir: Path,
    top_k: int,
    max_users: int,
    max_items: int | None,
    max_history_items: int,
    max_targets_per_user: int,
    max_candidates_per_prefix: int,
    depths: list[int],
    eval_splits: set[str],
    d3_top_k: int,
    d3_max_pair_events: int,
    d3_max_user_items: int,
    skip_d3: bool = False,
) -> tuple[pd.DataFrame, dict[str, object]]:
    item_metadata = _read_table(item_metadata_path)
    interactions = _read_table(interactions_path)
    sid = load_sid_assignments(sid_paths, dataset_name, methods)
    _require_columns("item_metadata", item_metadata, ["item_id"])
    _require_columns("interactions", interactions, ["user_id", "item_id"])
    item_metadata, interactions, sid = _filter_items(item_metadata, interactions, sid, max_items)

    ranking = evaluate_prefix_retrieval(
        sid,
        interactions,
        eval_splits=eval_splits,
        top_k=top_k,
        max_users=max_users,
        max_history_items=max_history_items,
        max_targets_per_user=max_targets_per_user,
        max_candidates_per_prefix=max_candidates_per_prefix,
        depths=depths,
    )
    if skip_d3:
        summary = ranking
    else:
        d3 = compute_d3_context(
            sid,
            item_metadata,
            interactions,
            d3_top_k=d3_top_k,
            d3_max_pair_events=d3_max_pair_events,
            d3_max_user_items=d3_max_user_items,
        )
        summary = ranking.merge(d3, on=["dataset", "method", "prefix_depth"], how="left")

    output_dir.mkdir(parents=True, exist_ok=True)
    summary_csv = output_dir / "d3_ranking_context_summary.csv"
    summary_json = output_dir / "d3_ranking_context_summary.json"
    summary.to_csv(summary_csv, index=False)
    records = summary.to_dict(orient="records")
    summary_json.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = {
        "dataset": dataset_name,
        "sid_assignments": [str(path) for path in sid_paths],
        "item_metadata": str(item_metadata_path),
        "interactions": str(interactions_path),
        "output_dir": str(output_dir),
        "summary_csv": str(summary_csv),
        "summary_json": str(summary_json),
        "methods": sorted(summary["method"].astype(str).unique()),
        "bounds": {
            "top_k": top_k,
            "max_users": max_users,
            "max_items": max_items,
            "max_history_items": max_history_items,
            "max_targets_per_user": max_targets_per_user,
            "max_candidates_per_prefix": max_candidates_per_prefix,
            "prefix_depths": depths,
            "eval_splits": sorted(eval_splits),
        },
        "d3": None
        if skip_d3
        else {
            "top_k": d3_top_k,
            "max_pair_events": d3_max_pair_events,
            "max_user_items": d3_max_user_items,
        },
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary, manifest


def _parse_csv_set(value: str | None) -> set[str] | None:
    if not value:
        return None
    return {part.strip() for part in value.split(",") if part.strip()}


def _parse_int_list(value: str) -> list[int]:
    out = [int(part.strip()) for part in value.split(",") if part.strip()]
    if not out:
        raise ValueError("expected at least one integer")
    if any(depth <= 0 for depth in out):
        raise ValueError("prefix depths must be positive")
    return sorted(set(out))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sid-assignments", type=Path, action="append", default=None)
    parser.add_argument("--item-metadata", type=Path, default=DEFAULT_ITEM_METADATA)
    parser.add_argument("--interactions", type=Path, default=DEFAULT_INTERACTIONS)
    parser.add_argument("--dataset-name", default=DEFAULT_DATASET)
    parser.add_argument("--methods", default=None, help="Comma-separated method filter.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--prefix-depths", default="1,2")
    parser.add_argument("--eval-splits", default="valid,test")
    parser.add_argument("--max-users", type=int, default=1000)
    parser.add_argument("--max-items", type=int, default=None)
    parser.add_argument("--max-history-items", type=int, default=50)
    parser.add_argument("--max-targets-per-user", type=int, default=2)
    parser.add_argument("--max-candidates-per-prefix", type=int, default=5000)
    parser.add_argument("--d3-top-k", type=int, default=20)
    parser.add_argument("--d3-max-pair-events", type=int, default=250_000)
    parser.add_argument("--d3-max-user-items", type=int, default=200)
    parser.add_argument("--skip-d3", action="store_true")
    args = parser.parse_args()

    sid_paths = args.sid_assignments if args.sid_assignments else DEFAULT_SID_PATHS
    summary, manifest = run_context(
        sid_paths=sid_paths,
        item_metadata_path=args.item_metadata,
        interactions_path=args.interactions,
        dataset_name=args.dataset_name,
        methods=_parse_csv_set(args.methods),
        output_dir=args.output_dir,
        top_k=args.top_k,
        max_users=args.max_users,
        max_items=args.max_items,
        max_history_items=args.max_history_items,
        max_targets_per_user=args.max_targets_per_user,
        max_candidates_per_prefix=args.max_candidates_per_prefix,
        depths=_parse_int_list(args.prefix_depths),
        eval_splits=_parse_csv_set(args.eval_splits) or {"valid", "test"},
        d3_top_k=args.d3_top_k,
        d3_max_pair_events=args.d3_max_pair_events,
        d3_max_user_items=args.d3_max_user_items,
        skip_d3=args.skip_d3,
    )
    print(summary.to_string(index=False))
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
