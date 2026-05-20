#!/usr/bin/env python3
"""Fixed-reranker validation for D3 SID prefix alignment.

This evaluator is still bounded and lightweight, but it is stricter than the
prefix-scoring context probe: SID mappings only define candidate sets.  The
final ranking is produced by the same train-only co-occurrence/popularity
reranker for every method row.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from tools.autodl_audit_sid.run_d3_ranking_context import (  # noqa: E402
    DEFAULT_DATASET,
    DEFAULT_INTERACTIONS,
    DEFAULT_ITEM_METADATA,
    DEFAULT_SID_PATHS,
    _bounded_targets,
    _bounded_train_histories,
    _build_prefix_index,
    _filter_items,
    _level_cols,
    _parse_csv_set,
    _parse_int_list,
    _read_table,
    _require_columns,
    _sort_events,
    _train_events,
    compute_d3_context,
    load_sid_assignments,
)


def _ordered_unique(values: Iterable[int]) -> list[int]:
    seen: set[int] = set()
    out: list[int] = []
    for value in values:
        item = int(value)
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def build_train_cooccurrence(
    interactions: pd.DataFrame,
    *,
    eligible_items: set[int],
    max_users: int,
    max_user_items: int,
) -> dict[int, dict[int, int]]:
    """Build a bounded symmetric item co-occurrence table from train histories."""

    train = _sort_events(_train_events(interactions))
    if max_users > 0:
        users = sorted(train["user_id"].astype(int).unique())[:max_users]
        train = train[train["user_id"].astype(int).isin(users)]

    cooc: dict[int, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    for _, group in train.groupby("user_id", sort=True):
        items = [item for item in _ordered_unique(group["item_id"].astype(int)) if item in eligible_items]
        if max_user_items > 0:
            items = items[-max_user_items:]
        for i, left in enumerate(items):
            for right in items[i + 1 :]:
                if left == right:
                    continue
                cooc[left][right] += 1
                cooc[right][left] += 1
    return {left: dict(rights) for left, rights in cooc.items()}


def _validate_split_protocol(interactions: pd.DataFrame, eval_splits: set[str], allow_splitless_proxy: bool) -> None:
    if allow_splitless_proxy:
        return
    _require_columns("interactions", interactions, ["split"])
    split_values = set(interactions["split"].astype(str))
    if "train" not in split_values:
        raise ValueError("fixed-reranker validation requires a train split; use --allow-splitless-proxy for proxy-only data")
    missing_eval = sorted(eval_splits - split_values)
    if missing_eval and not (eval_splits & split_values):
        raise ValueError(
            "fixed-reranker validation requires at least one requested eval split "
            f"to exist; requested={sorted(eval_splits)} available={sorted(split_values)}"
        )


def _score_cooccurrence(
    candidate: int,
    history: list[int],
    cooccurrence: dict[int, dict[int, int]],
) -> int:
    return sum(cooccurrence.get(item, {}).get(candidate, 0) for item in history)


def _rank_candidates(
    candidate_prefix_hits: dict[int, int],
    history: list[int],
    item_popularity: dict[int, int],
    cooccurrence: dict[int, dict[int, int]],
    ranker: str,
) -> list[int]:
    candidates = list(candidate_prefix_hits)
    if ranker == "cooccurrence_popularity":
        return sorted(
            candidates,
            key=lambda item: (
                -_score_cooccurrence(item, history, cooccurrence),
                -item_popularity.get(item, 0),
                item,
            ),
        )
    if ranker == "popularity":
        return sorted(candidates, key=lambda item: (-item_popularity.get(item, 0), item))
    if ranker == "prefix_popularity":
        return sorted(
            candidates,
            key=lambda item: (
                -candidate_prefix_hits.get(item, 0),
                -item_popularity.get(item, 0),
                item,
            ),
        )
    raise ValueError(f"unsupported ranker: {ranker}")


def evaluate_fixed_reranker(
    sid: pd.DataFrame,
    interactions: pd.DataFrame,
    *,
    eval_splits: set[str],
    top_k: int,
    max_users: int,
    max_history_items: int,
    max_targets_per_user: int,
    max_candidates_per_prefix: int,
    max_cooccurrence_users: int,
    max_cooccurrence_user_items: int,
    depths: list[int],
    rankers: list[str],
    allow_splitless_proxy: bool = False,
) -> pd.DataFrame:
    _require_columns("interactions", interactions, ["user_id", "item_id"])
    _require_columns("sid_assignments", sid, ["dataset", "method", "item_id", "sid"])
    _validate_split_protocol(interactions, eval_splits, allow_splitless_proxy)

    eligible_items = set(sid["item_id"].astype(int))
    cooccurrence = build_train_cooccurrence(
        interactions,
        eligible_items=eligible_items,
        max_users=max_cooccurrence_users,
        max_user_items=max_cooccurrence_user_items,
    )
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
            accum = {
                ranker: {
                    "hits": 0,
                    "mrr": 0.0,
                    "ndcg": 0.0,
                    "covered": 0,
                    "evaluated": 0,
                    "candidate_counts": [],
                    "prefix_counts": [],
                    "users_with_candidates": set(),
                }
                for ranker in rankers
            }
            for row in group_targets.itertuples(index=False):
                user_id = int(row.user_id)
                target_item = int(row.item_id)
                history = [item for item in histories.get(user_id, []) if item in item_to_prefix]
                candidate_prefix_hits: dict[int, int] = defaultdict(int)
                query_prefixes: list[str] = []
                if history:
                    history_set = set(history)
                    query_prefixes = sorted({item_to_prefix[item] for item in history})
                    for prefix in query_prefixes:
                        for candidate in prefix_to_items.get(prefix, []):
                            if candidate not in history_set:
                                candidate_prefix_hits[candidate] += 1
                if not candidate_prefix_hits:
                    for ranker in rankers:
                        bucket = accum[ranker]
                        bucket["evaluated"] += 1
                        bucket["candidate_counts"].append(0)
                        bucket["prefix_counts"].append(len(query_prefixes))
                    continue
                covered = target_item in candidate_prefix_hits
                for ranker in rankers:
                    bucket = accum[ranker]
                    bucket["evaluated"] += 1
                    bucket["candidate_counts"].append(len(candidate_prefix_hits))
                    bucket["prefix_counts"].append(len(query_prefixes))
                    bucket["users_with_candidates"].add(user_id)
                    if covered:
                        bucket["covered"] += 1
                    ranked = _rank_candidates(
                        candidate_prefix_hits,
                        history,
                        item_popularity,
                        cooccurrence,
                        ranker,
                    )
                    top_items = ranked[:top_k]
                    if target_item in top_items:
                        rank = top_items.index(target_item) + 1
                        bucket["hits"] += 1
                        bucket["mrr"] += 1.0 / rank
                        bucket["ndcg"] += 1.0 / math.log2(rank + 1)
            for ranker, bucket in accum.items():
                evaluated = int(bucket["evaluated"])
                candidate_counts = bucket["candidate_counts"]
                prefix_counts = bucket["prefix_counts"]
                rows.append(
                    {
                        "dataset": dataset,
                        "method": method,
                        "prefix_depth": depth,
                        "ranker": ranker,
                        "top_k": top_k,
                        "users_with_eval_targets": int(group_targets["user_id"].nunique()),
                        "users_with_candidates": len(bucket["users_with_candidates"]),
                        "targets_seen": int(len(group_targets)),
                        "targets_evaluated": evaluated,
                        "candidate_recall": float(bucket["covered"] / evaluated) if evaluated else 0.0,
                        "recall_at_k": float(bucket["hits"] / evaluated) if evaluated else 0.0,
                        "ndcg_at_k": float(bucket["ndcg"] / evaluated) if evaluated else 0.0,
                        "mrr_at_k": float(bucket["mrr"] / evaluated) if evaluated else 0.0,
                        "mean_candidate_count": float(pd.Series(candidate_counts).mean()) if candidate_counts else 0.0,
                        "median_candidate_count": float(pd.Series(candidate_counts).median()) if candidate_counts else 0.0,
                        "mean_query_prefix_count": float(pd.Series(prefix_counts).mean()) if prefix_counts else 0.0,
                    }
                )
    if not rows:
        raise ValueError("no validation rows produced; check SID item coverage and depth bounds")
    return pd.DataFrame(rows)


def _correlations(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    metrics = ["candidate_recall", "recall_at_k", "ndcg_at_k", "mrr_at_k"]
    for (dataset, prefix_depth, ranker), group in summary.groupby(["dataset", "prefix_depth", "ranker"], sort=True):
        if group["weighted_collab_prefix_recall"].notna().sum() < 2:
            continue
        for metric in metrics:
            rows.append(
                {
                    "dataset": dataset,
                    "prefix_depth": int(prefix_depth),
                    "ranker": ranker,
                    "metric": metric,
                    "pearson_with_d3_weighted": float(
                        group["weighted_collab_prefix_recall"].corr(group[metric], method="pearson")
                    ),
                    "spearman_with_d3_weighted": float(
                        group["weighted_collab_prefix_recall"].corr(group[metric], method="spearman")
                    ),
                    "rows": int(len(group)),
                }
            )
    return pd.DataFrame(rows)


def run_validation(
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
    max_cooccurrence_users: int,
    max_cooccurrence_user_items: int,
    depths: list[int],
    eval_splits: set[str],
    rankers: list[str],
    d3_top_k: int,
    d3_max_pair_events: int,
    d3_max_user_items: int,
    allow_splitless_proxy: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, object]]:
    item_metadata = _read_table(item_metadata_path)
    interactions = _read_table(interactions_path)
    sid = load_sid_assignments(sid_paths, dataset_name, methods)
    _require_columns("item_metadata", item_metadata, ["item_id"])
    item_metadata, interactions, sid = _filter_items(item_metadata, interactions, sid, max_items)

    validation = evaluate_fixed_reranker(
        sid,
        interactions,
        eval_splits=eval_splits,
        top_k=top_k,
        max_users=max_users,
        max_history_items=max_history_items,
        max_targets_per_user=max_targets_per_user,
        max_candidates_per_prefix=max_candidates_per_prefix,
        max_cooccurrence_users=max_cooccurrence_users,
        max_cooccurrence_user_items=max_cooccurrence_user_items,
        depths=depths,
        rankers=rankers,
        allow_splitless_proxy=allow_splitless_proxy,
    )
    d3 = compute_d3_context(
        sid,
        item_metadata,
        interactions,
        d3_top_k=d3_top_k,
        d3_max_pair_events=d3_max_pair_events,
        d3_max_user_items=d3_max_user_items,
    )
    summary = validation.merge(d3, on=["dataset", "method", "prefix_depth"], how="left")
    correlations = _correlations(summary)

    output_dir.mkdir(parents=True, exist_ok=True)
    summary_csv = output_dir / "d3_ranking_validation_summary.csv"
    summary_json = output_dir / "d3_ranking_validation_summary.json"
    corr_csv = output_dir / "d3_ranking_validation_correlations.csv"
    manifest_path = output_dir / "manifest.json"
    summary.to_csv(summary_csv, index=False)
    summary_json.write_text(json.dumps(summary.to_dict(orient="records"), indent=2, sort_keys=True) + "\n")
    correlations.to_csv(corr_csv, index=False)
    manifest = {
        "dataset": dataset_name,
        "sid_assignments": [str(path) for path in sid_paths],
        "item_metadata": str(item_metadata_path),
        "interactions": str(interactions_path),
        "output_dir": str(output_dir),
        "summary_csv": str(summary_csv),
        "summary_json": str(summary_json),
        "correlations_csv": str(corr_csv),
        "methods": sorted(summary["method"].astype(str).unique()),
        "bounds": {
            "top_k": top_k,
            "max_users": max_users,
            "max_items": max_items,
            "max_history_items": max_history_items,
            "max_targets_per_user": max_targets_per_user,
            "max_candidates_per_prefix": max_candidates_per_prefix,
            "max_cooccurrence_users": max_cooccurrence_users,
            "max_cooccurrence_user_items": max_cooccurrence_user_items,
            "prefix_depths": depths,
            "eval_splits": sorted(eval_splits),
            "rankers": rankers,
            "allow_splitless_proxy": allow_splitless_proxy,
            "metric_denominator": "all eligible targets; no-history and no-candidate targets count as misses",
        },
        "d3": {
            "top_k": d3_top_k,
            "max_pair_events": d3_max_pair_events,
            "max_user_items": d3_max_user_items,
        },
        "interpretation_boundary": (
            "SID mappings define candidate sets; all rows share the same train-only reranker. "
            "This is a small ranking validation, not a trained generator benchmark."
        ),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return summary, correlations, manifest


def _parse_rankers(value: str) -> list[str]:
    allowed = {"cooccurrence_popularity", "popularity", "prefix_popularity"}
    rankers = [part.strip() for part in value.split(",") if part.strip()]
    if not rankers:
        raise ValueError("expected at least one ranker")
    unsupported = sorted(set(rankers) - allowed)
    if unsupported:
        raise ValueError(f"unsupported ranker(s): {', '.join(unsupported)}")
    return rankers


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
    parser.add_argument("--rankers", default="cooccurrence_popularity,popularity,prefix_popularity")
    parser.add_argument("--max-users", type=int, default=5000)
    parser.add_argument("--max-items", type=int, default=None)
    parser.add_argument("--max-history-items", type=int, default=50)
    parser.add_argument("--max-targets-per-user", type=int, default=2)
    parser.add_argument("--max-candidates-per-prefix", type=int, default=5000)
    parser.add_argument("--max-cooccurrence-users", type=int, default=20000)
    parser.add_argument("--max-cooccurrence-user-items", type=int, default=50)
    parser.add_argument("--d3-top-k", type=int, default=20)
    parser.add_argument("--d3-max-pair-events", type=int, default=500_000)
    parser.add_argument("--d3-max-user-items", type=int, default=200)
    parser.add_argument(
        "--allow-splitless-proxy",
        action="store_true",
        help="Allow missing split labels and use context-probe fallbacks. Off by default for validation.",
    )
    args = parser.parse_args()

    sid_paths = args.sid_assignments if args.sid_assignments else DEFAULT_SID_PATHS
    summary, correlations, manifest = run_validation(
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
        max_cooccurrence_users=args.max_cooccurrence_users,
        max_cooccurrence_user_items=args.max_cooccurrence_user_items,
        depths=_parse_int_list(args.prefix_depths),
        eval_splits=_parse_csv_set(args.eval_splits) or {"valid", "test"},
        rankers=_parse_rankers(args.rankers),
        d3_top_k=args.d3_top_k,
        d3_max_pair_events=args.d3_max_pair_events,
        d3_max_user_items=args.d3_max_user_items,
        allow_splitless_proxy=args.allow_splitless_proxy,
    )
    print(summary.to_string(index=False))
    if not correlations.empty:
        print(correlations.to_string(index=False))
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
