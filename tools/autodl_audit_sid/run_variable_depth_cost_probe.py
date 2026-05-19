#!/usr/bin/env python3
"""Run controlled variable-depth SID cost probes."""

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

from audit_sid.metrics import collision, deployment_cost, head_tail_capacity, validate_inputs


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


def popularity_buckets(item_metadata: pd.DataFrame, interactions: pd.DataFrame) -> pd.DataFrame:
    counts = train_events(interactions).groupby("item_id").size().rename("popularity").reset_index()
    frame = item_metadata[["item_id"]].copy()
    frame["item_id"] = frame["item_id"].astype(int)
    frame = frame.merge(counts, on="item_id", how="left").fillna({"popularity": 0})
    frame["popularity"] = frame["popularity"].astype(int)
    pct_rank = frame["popularity"].rank(method="first", pct=True)
    frame["bucket"] = pd.Series("head", index=frame.index)
    frame.loc[pct_rank <= 1 / 3, "bucket"] = "tail"
    frame.loc[(pct_rank > 1 / 3) & (pct_rank <= 2 / 3), "bucket"] = "mid"
    return frame


def code_to_levels(code_id: int, width: int, depth: int) -> list[int]:
    levels = []
    value = int(code_id)
    for power in reversed(range(depth)):
        divisor = width**power
        levels.append((value // divisor) % width + 1)
    return levels


def length_for_bucket(bucket: str, policy: str) -> int:
    if policy == "head_short_tail_long":
        return {"head": 2, "mid": 3, "tail": 4}[bucket]
    if policy == "head_long_tail_short":
        return {"head": 4, "mid": 3, "tail": 2}[bucket]
    if policy == "uniform_depth3":
        return 3
    raise ValueError(f"unsupported variable-depth policy: {policy}")


def generate_variable_depth_sid(
    item_metadata: pd.DataFrame,
    interactions: pd.DataFrame,
    *,
    dataset: str,
    width: int,
    max_depth: int,
    policy: str,
) -> pd.DataFrame:
    buckets = popularity_buckets(item_metadata, interactions)
    rows: list[dict[str, Any]] = []
    if policy == "uniform_depth3":
        effective_depth = length_for_bucket("head", policy)
        ordered = buckets.sort_values(["popularity", "item_id"], ascending=[False, True]).reset_index(drop=True)
        capacity = width**effective_depth
        for rank, row in ordered.iterrows():
            active_levels = code_to_levels(rank % capacity, width, effective_depth)
            padded_levels = active_levels + [0] * (max_depth - effective_depth)
            out: dict[str, Any] = {
                "dataset": dataset,
                "method": f"controller_variable_depth_{policy}_w{width}_maxd{max_depth}",
                "item_id": int(row["item_id"]),
                "effective_depth": effective_depth,
            }
            for level_idx, level_value in enumerate(padded_levels):
                out[f"sid_level_{level_idx}"] = int(level_value)
            out["sid"] = "-".join(str(level) for level in active_levels)
            rows.append(out)
        return pd.DataFrame(rows)

    for bucket, bucket_frame in buckets.groupby("bucket", sort=True):
        effective_depth = length_for_bucket(str(bucket), policy)
        ordered = bucket_frame.sort_values(["popularity", "item_id"], ascending=[False, True]).reset_index(drop=True)
        capacity = width**effective_depth
        for rank, row in ordered.iterrows():
            active_levels = code_to_levels(rank % capacity, width, effective_depth)
            padded_levels = active_levels + [0] * (max_depth - effective_depth)
            out: dict[str, Any] = {
                "dataset": dataset,
                "method": f"controller_variable_depth_{policy}_w{width}_maxd{max_depth}",
                "item_id": int(row["item_id"]),
                "effective_depth": effective_depth,
            }
            for level_idx, level_value in enumerate(padded_levels):
                out[f"sid_level_{level_idx}"] = int(level_value)
            out["sid"] = "-".join(str(level) for level in active_levels)
            rows.append(out)
    return pd.DataFrame(rows)


def effective_prefix_counts(group: pd.DataFrame, max_depth: int) -> str:
    counts = []
    for depth in range(1, max_depth + 1):
        active = group[group["effective_depth"] >= depth]
        if active.empty:
            counts.append(0)
            continue
        level_cols = [f"sid_level_{idx}" for idx in range(depth)]
        counts.append(int(active[level_cols].drop_duplicates().shape[0]))
    return ";".join(map(str, counts))


def build_summary(sid: pd.DataFrame, interactions: pd.DataFrame, max_depth: int) -> pd.DataFrame:
    d2 = collision(sid.drop(columns=["effective_depth"]), interactions)
    d4 = head_tail_capacity(sid.drop(columns=["effective_depth"]), interactions)
    d5 = deployment_cost(sid.drop(columns=["effective_depth"]))
    rows = []
    for method, group in sid.groupby("method", sort=True):
        d2_row = d2[d2["method"] == method].iloc[0]
        d5_row = d5[d5["method"] == method].iloc[0]
        d4_rows = d4[d4["method"] == method]
        d4_map = {str(row["bucket"]): float(row["sid_unique_ratio"]) for _, row in d4_rows.iterrows()}
        rows.append(
            {
                "dataset": group["dataset"].iloc[0],
                "method": method,
                "width": int(method.rsplit("_w", 1)[1].split("_maxd", 1)[0]),
                "max_depth": max_depth,
                "items": int(group["item_id"].nunique()),
                "unique_sid": int(d5_row["unique_sid"]),
                "duplicate_sid_rate": float(d5_row["duplicate_sid_rate"]),
                "full_collision_rate": float(d2_row["full_collision_rate"]),
                "mean_effective_depth": float(group["effective_depth"].mean()),
                "head_unique_ratio": d4_map.get("head", 0.0),
                "mid_unique_ratio": d4_map.get("mid", 0.0),
                "tail_unique_ratio": d4_map.get("tail", 0.0),
                "standard_prefix_counts": d5_row["prefix_counts"],
                "effective_prefix_counts": effective_prefix_counts(group, max_depth),
            }
        )
    return pd.DataFrame(rows).sort_values("method").reset_index(drop=True)


def run_probe(
    item_metadata_path: Path,
    interactions_path: Path,
    output_dir: Path,
    *,
    dataset: str,
    width: int,
    max_depth: int,
    policies: list[str],
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    item_metadata = read_table(item_metadata_path)
    interactions = read_table(interactions_path)
    sid = pd.concat(
        [
            generate_variable_depth_sid(
                item_metadata,
                interactions,
                dataset=dataset,
                width=width,
                max_depth=max_depth,
                policy=policy,
            )
            for policy in policies
        ],
        ignore_index=True,
    )
    validate_inputs(sid.drop(columns=["effective_depth"]), item_metadata, interactions, allow_partial_coverage=False)
    sid.to_parquet(output_dir / "sid_assignments.parquet", index=False)
    collision(sid.drop(columns=["effective_depth"]), interactions).to_csv(output_dir / "d2_collision.csv", index=False)
    head_tail_capacity(sid.drop(columns=["effective_depth"]), interactions).to_csv(
        output_dir / "d4_head_tail.csv", index=False
    )
    deployment_cost(sid.drop(columns=["effective_depth"])).to_csv(output_dir / "d5a_deployment_cost.csv", index=False)
    summary = build_summary(sid, interactions, max_depth)
    summary.to_csv(output_dir / "variable_depth_cost_summary.csv", index=False)
    manifest = {
        "status": "passed",
        "item_metadata": str(item_metadata_path),
        "interactions": str(interactions_path),
        "output_dir": str(output_dir),
        "dataset": dataset,
        "width": width,
        "max_depth": max_depth,
        "policies": policies,
        "summary_rows": summary.to_dict(orient="records"),
    }
    (output_dir / "variable_depth_cost_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def parse_str_list(value: str) -> list[str]:
    out = [part.strip() for part in value.split(",") if part.strip()]
    if not out:
        raise argparse.ArgumentTypeError("expected at least one value")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AUDIT-SID variable-depth cost controller.")
    parser.add_argument("--item-metadata", type=Path, required=True)
    parser.add_argument("--interactions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="Musical_Instruments")
    parser.add_argument("--width", type=int, default=64)
    parser.add_argument("--max-depth", type=int, default=4)
    parser.add_argument(
        "--policies",
        type=parse_str_list,
        default=parse_str_list("head_short_tail_long,head_long_tail_short,uniform_depth3"),
    )
    args = parser.parse_args()
    manifest = run_probe(
        item_metadata_path=args.item_metadata,
        interactions_path=args.interactions,
        output_dir=args.output_dir,
        dataset=args.dataset_name,
        width=args.width,
        max_depth=args.max_depth,
        policies=args.policies,
    )
    print(json.dumps({"status": manifest["status"], "output_dir": manifest["output_dir"]}, indent=2))


if __name__ == "__main__":
    main()
