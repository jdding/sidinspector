#!/usr/bin/env python3
"""Run a bounded D3 replication panel for one learned SID row plus controls."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from audit_sid.adapters.sanity import mod_collision_sid, popularity_balanced_sid
from audit_sid.metrics import alignment, collision, deployment_cost, head_tail_capacity, utilization, validate_inputs


def _sid_from_levels(frame: pd.DataFrame, level_cols: list[str]) -> pd.Series:
    return frame[level_cols].astype(int).astype(str).agg("-".join, axis=1)


def category_prefix_with_fallback(item_metadata: pd.DataFrame, dataset: str) -> tuple[pd.DataFrame, dict[str, object]]:
    """Build category-prefix SIDs even when only coarse category strings exist."""

    out = pd.DataFrame({"item_id": item_metadata["item_id"].astype(int)})
    meta = item_metadata.copy()
    used_cols: list[str] = []
    if {"category_l1", "category_l2", "category_l3"}.issubset(meta.columns):
        for level, col in enumerate(["category_l1", "category_l2", "category_l3"]):
            out[f"sid_level_{level}"] = meta[col].astype(int)
            used_cols.append(col)
        coarse = False
    elif "category" in meta.columns:
        codes, uniques = pd.factorize(meta["category"].astype(str), sort=True)
        stable = codes.astype(int) + 1
        out["sid_level_0"] = stable
        out["sid_level_1"] = stable
        out["sid_level_2"] = stable
        used_cols.append("category")
        coarse = len(uniques) <= 2
    else:
        out["sid_level_0"] = 1
        out["sid_level_1"] = 1
        out["sid_level_2"] = 1
        coarse = True
    out["sid_level_3"] = out.groupby(["sid_level_0", "sid_level_1", "sid_level_2"]).cumcount() + 1
    out["sid"] = _sid_from_levels(out, ["sid_level_0", "sid_level_1", "sid_level_2", "sid_level_3"])
    out["method"] = "sanity_category_prefix"
    out["dataset"] = dataset
    return out, {
        "used_category_columns": used_cols,
        "coarse_category_levels": coarse,
        "level0_unique": int(out["sid_level_0"].nunique()),
    }


def write_metrics(
    sid: pd.DataFrame,
    item_metadata: pd.DataFrame,
    interactions: pd.DataFrame,
    output_dir: Path,
    *,
    top_k: int,
    max_pair_events: int,
    max_user_items: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    tables = {
        "coverage_report.csv": validate_inputs(sid, item_metadata, interactions),
        "d1_utilization.csv": utilization(sid),
        "d2_collision.csv": collision(sid, interactions),
        "d3_alignment.csv": alignment(
            sid,
            item_metadata,
            interactions,
            top_k=top_k,
            max_pair_events=max_pair_events,
            max_user_items=max_user_items,
        ),
        "d4_head_tail.csv": head_tail_capacity(sid, interactions),
        "d5a_deployment_cost.csv": deployment_cost(sid),
    }
    for name, table in tables.items():
        table.to_csv(output_dir / name, index=False)


def summarize(metrics_dir: Path, output_csv: Path) -> pd.DataFrame:
    d2 = pd.read_csv(metrics_dir / "d2_collision.csv")
    d3 = pd.read_csv(metrics_dir / "d3_alignment.csv")
    d4 = pd.read_csv(metrics_dir / "d4_head_tail.csv")
    d5 = pd.read_csv(metrics_dir / "d5a_deployment_cost.csv")
    rows = []
    for _, row in d5.iterrows():
        dataset = row["dataset"]
        method = row["method"]
        d2_row = d2[(d2["dataset"] == dataset) & (d2["method"] == method)].iloc[0]
        d3_l1 = d3[(d3["dataset"] == dataset) & (d3["method"] == method) & (d3["prefix_depth"] == 1)].iloc[0]
        d4_method = d4[(d4["dataset"] == dataset) & (d4["method"] == method)]
        d4_map = dict(zip(d4_method["bucket"], d4_method["sid_unique_ratio"]))
        rows.append(
            {
                "dataset": dataset,
                "method": method,
                "unique_sid": int(row["unique_sid"]),
                "duplicate_sid_rate": float(row["duplicate_sid_rate"]),
                "full_collision_rate": float(d2_row["full_collision_rate"]),
                "d3_l1_weighted": float(d3_l1["weighted_collab_prefix_recall"]),
                "d3_l1_mean": float(d3_l1["mean_collab_prefix_recall"]),
                "level0_category_purity_mean": float(d3_l1.get("level0_category_purity_mean", 0.0)),
                "d4_tail": float(d4_map.get("tail", 0.0)),
                "prefix_counts": row["prefix_counts"],
            }
        )
    table = pd.DataFrame(rows).sort_values("method")
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(output_csv, index=False)
    return table


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--learned-sid", type=Path, required=True)
    parser.add_argument("--item-metadata", type=Path, required=True)
    parser.add_argument("--interactions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--learned-label", default=None)
    parser.add_argument("--d3-top-k", type=int, default=20)
    parser.add_argument("--d3-max-pair-events", type=int, default=2_000_000)
    parser.add_argument("--d3-max-user-items", type=int, default=200)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    item_metadata = pd.read_parquet(args.item_metadata)
    interactions = pd.read_parquet(args.interactions)
    learned = pd.read_parquet(args.learned_sid)
    if args.learned_label:
        learned = learned.copy()
        learned["method"] = args.learned_label
    category_sid, category_info = category_prefix_with_fallback(item_metadata, args.dataset_name)
    controls = [
        category_sid,
        mod_collision_sid(item_metadata, args.dataset_name),
        popularity_balanced_sid(item_metadata, interactions, args.dataset_name),
    ]
    combined = pd.concat([learned, *controls], ignore_index=True)
    sid_path = args.output_dir / "sid_assignments.parquet"
    combined.to_parquet(sid_path, index=False)
    metrics_dir = args.output_dir / "metrics"
    write_metrics(
        combined,
        item_metadata,
        interactions,
        metrics_dir,
        top_k=args.d3_top_k,
        max_pair_events=args.d3_max_pair_events,
        max_user_items=args.d3_max_user_items,
    )
    summary = summarize(metrics_dir, args.output_dir / "vertical_d3_summary.csv")
    (args.output_dir / "vertical_d3_summary.md").write_text(summary.to_markdown(index=False) + "\n", encoding="utf-8")
    manifest = {
        "dataset": args.dataset_name,
        "learned_sid": str(args.learned_sid),
        "item_metadata": str(args.item_metadata),
        "interactions": str(args.interactions),
        "sid_assignments": str(sid_path),
        "metrics_dir": str(metrics_dir),
        "category_prefix": category_info,
        "d3": {
            "top_k": args.d3_top_k,
            "max_pair_events": args.d3_max_pair_events,
            "max_user_items": args.d3_max_user_items,
        },
    }
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(summary.to_string(index=False))
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
