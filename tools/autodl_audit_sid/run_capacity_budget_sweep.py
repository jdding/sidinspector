#!/usr/bin/env python3
"""Run controlled capacity-budget stressors for SID artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from audit_sid.metrics import collision, deployment_cost, head_tail_capacity, utilization, validate_inputs


def read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".json", ".jsonl", ".ndjson"}:
        return pd.read_json(path, lines=suffix in {".jsonl", ".ndjson"})
    raise ValueError(f"unsupported table format for {path}")


def train_events(interactions: pd.DataFrame) -> pd.DataFrame:
    if "split" in interactions.columns:
        train = interactions[interactions["split"] == "train"]
        if not train.empty:
            return train
    return interactions


def code_to_levels(code_id: int, width: int, depth: int) -> list[int]:
    levels = []
    value = int(code_id)
    for power in reversed(range(depth)):
        divisor = width**power
        levels.append((value // divisor) % width + 1)
    return levels


def item_order(item_metadata: pd.DataFrame, interactions: pd.DataFrame, policy: str) -> pd.DataFrame:
    counts = train_events(interactions).groupby("item_id").size().rename("popularity").reset_index()
    frame = item_metadata[["item_id"]].copy()
    frame["item_id"] = frame["item_id"].astype(int)
    frame = frame.merge(counts, on="item_id", how="left").fillna({"popularity": 0})
    frame["popularity"] = frame["popularity"].astype(int)
    if policy == "rank_mod":
        return frame.sort_values(["item_id"]).reset_index(drop=True)
    if policy == "head_reserved":
        return frame.sort_values(["popularity", "item_id"], ascending=[False, True]).reset_index(drop=True)
    raise ValueError(f"unsupported capacity policy: {policy}")


def assign_code_id(rank: int, capacity: int, width: int, policy: str) -> int:
    if policy == "rank_mod":
        return rank % capacity
    if policy == "head_reserved":
        if rank < capacity:
            return rank
        overflow_width = max(1, min(width, capacity))
        return capacity - 1 - ((rank - capacity) % overflow_width)
    raise ValueError(f"unsupported capacity policy: {policy}")


def generate_capacity_sid(
    item_metadata: pd.DataFrame,
    interactions: pd.DataFrame,
    *,
    dataset: str,
    width: int,
    depth: int,
    policy: str,
) -> pd.DataFrame:
    ordered = item_order(item_metadata, interactions, policy)
    capacity = int(width**depth)
    rows: list[dict[str, Any]] = []
    for rank, item_id in enumerate(ordered["item_id"].astype(int).tolist()):
        levels = code_to_levels(assign_code_id(rank, capacity, width, policy), width, depth)
        row: dict[str, Any] = {
            "dataset": dataset,
            "method": f"controller_capacity_{policy}_w{width}_d{depth}",
            "item_id": item_id,
        }
        for level_idx, level_value in enumerate(levels):
            row[f"sid_level_{level_idx}"] = level_value
        row["sid"] = "-".join(str(level) for level in levels)
        rows.append(row)
    return pd.DataFrame(rows)


def _select_row(frame: pd.DataFrame, method: str) -> pd.Series:
    selected = frame[frame["method"] == method]
    if selected.empty:
        raise ValueError(f"missing metric row for {method}")
    return selected.iloc[0]


def _d4_bucket_values(d4: pd.DataFrame, method: str) -> dict[str, float]:
    selected = d4[d4["method"] == method]
    return {str(row["bucket"]): float(row["sid_unique_ratio"]) for _, row in selected.iterrows()}


def build_summary(sid: pd.DataFrame, interactions: pd.DataFrame, widths: list[int], depth: int) -> pd.DataFrame:
    d2 = collision(sid, interactions)
    d4 = head_tail_capacity(sid, interactions)
    d5 = deployment_cost(sid)
    rows = []
    for _, d5_row in d5.iterrows():
        method = str(d5_row["method"])
        parts = method.rsplit("_w", 1)
        width = int(parts[1].split("_d", 1)[0])
        policy = parts[0].replace("controller_capacity_", "")
        d2_row = _select_row(d2, method)
        d4_buckets = _d4_bucket_values(d4, method)
        rows.append(
            {
                "dataset": d5_row.get("dataset", ""),
                "method": method,
                "policy": policy,
                "width": width,
                "depth": depth,
                "nominal_capacity": int(width**depth),
                "items": int(sid[sid["method"] == method]["item_id"].nunique()),
                "unique_sid": int(d5_row["unique_sid"]),
                "duplicate_sid_rate": float(d5_row["duplicate_sid_rate"]),
                "full_collision_rate": float(d2_row["full_collision_rate"]),
                "head_unique_ratio": d4_buckets.get("head", 0.0),
                "mid_unique_ratio": d4_buckets.get("mid", 0.0),
                "tail_unique_ratio": d4_buckets.get("tail", 0.0),
                "prefix_counts": d5_row["prefix_counts"],
            }
        )
    return pd.DataFrame(rows).sort_values(["policy", "width"]).reset_index(drop=True)


def run_sweep(
    item_metadata_path: Path,
    interactions_path: Path,
    output_dir: Path,
    *,
    dataset: str,
    widths: list[int],
    depth: int,
    policies: list[str],
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    item_metadata = read_table(item_metadata_path)
    interactions = read_table(interactions_path)
    sid = pd.concat(
        [
            generate_capacity_sid(
                item_metadata,
                interactions,
                dataset=dataset,
                width=width,
                depth=depth,
                policy=policy,
            )
            for policy in policies
            for width in widths
        ],
        ignore_index=True,
    )
    validate_inputs(sid, item_metadata, interactions, allow_partial_coverage=False)
    metric_tables = {
        "sid_assignments.parquet": sid,
        "d1_utilization.csv": utilization(sid),
        "d2_collision.csv": collision(sid, interactions),
        "d4_head_tail.csv": head_tail_capacity(sid, interactions),
        "d5a_deployment_cost.csv": deployment_cost(sid),
    }
    summary = build_summary(sid, interactions, widths, depth)
    metric_tables["capacity_budget_summary.csv"] = summary
    for name, table in metric_tables.items():
        if name.endswith(".parquet"):
            table.to_parquet(output_dir / name, index=False)
        else:
            table.to_csv(output_dir / name, index=False)
    manifest = {
        "status": "passed",
        "item_metadata": str(item_metadata_path),
        "interactions": str(interactions_path),
        "output_dir": str(output_dir),
        "dataset": dataset,
        "widths": widths,
        "depth": depth,
        "policies": policies,
        "summary_rows": summary.to_dict(orient="records"),
    }
    (output_dir / "capacity_budget_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def parse_int_list(value: str) -> list[int]:
    out = [int(part.strip()) for part in value.split(",") if part.strip()]
    if not out:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return out


def parse_str_list(value: str) -> list[str]:
    out = [part.strip() for part in value.split(",") if part.strip()]
    if not out:
        raise argparse.ArgumentTypeError("expected at least one value")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SIDInspector capacity-budget controller sweep.")
    parser.add_argument("--item-metadata", type=Path, required=True)
    parser.add_argument("--interactions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="Musical_Instruments")
    parser.add_argument("--widths", type=parse_int_list, default=parse_int_list("8,12,16,24,32,48"))
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--policies", type=parse_str_list, default=parse_str_list("rank_mod,head_reserved"))
    args = parser.parse_args()
    manifest = run_sweep(
        item_metadata_path=args.item_metadata,
        interactions_path=args.interactions,
        output_dir=args.output_dir,
        dataset=args.dataset_name,
        widths=args.widths,
        depth=args.depth,
        policies=args.policies,
    )
    print(json.dumps({"status": manifest["status"], "output_dir": manifest["output_dir"]}, indent=2))


if __name__ == "__main__":
    main()
