"""Generate deterministic sanity SID baselines."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from sidinspector.interface import validate_columns


def _sid_from_levels(frame: pd.DataFrame, level_cols: list[str]) -> pd.Series:
    return frame[level_cols].astype(int).astype(str).agg("-".join, axis=1)


def _metadata_col(item_metadata: pd.DataFrame, *candidates: str) -> pd.Series:
    for candidate in candidates:
        if candidate in item_metadata.columns:
            return item_metadata[candidate]
    raise ValueError(f"item_metadata must contain one of: {', '.join(candidates)}")


def mod_collision_sid(item_metadata: pd.DataFrame, dataset: str, width: int = 256, levels: int = 4) -> pd.DataFrame:
    # Deterministic arithmetic hash baseline, avoiding RNG/version differences.
    out = pd.DataFrame({"item_id": item_metadata["item_id"].astype(int)})
    for level in range(levels):
        out[f"sid_level_{level}"] = ((out["item_id"] * (1103515245 + level * 97) + 12345) % width) + 1
    out["sid"] = _sid_from_levels(out, [f"sid_level_{i}" for i in range(levels)])
    out["method"] = "sanity_mod_collision_hash"
    out["dataset"] = dataset
    validate_columns("sid_assignments", out.columns)
    return out


def category_prefix_sid(item_metadata: pd.DataFrame, dataset: str) -> pd.DataFrame:
    out = pd.DataFrame({"item_id": item_metadata["item_id"].astype(int)})
    out["sid_level_0"] = _metadata_col(item_metadata, "category_l1", "category").astype(int)
    out["sid_level_1"] = _metadata_col(item_metadata, "category_l2", "category").astype(int)
    out["sid_level_2"] = _metadata_col(item_metadata, "category_l3", "category").astype(int)
    out["sid_level_3"] = out.groupby(["sid_level_0", "sid_level_1", "sid_level_2"]).cumcount() + 1
    out["sid"] = _sid_from_levels(out, ["sid_level_0", "sid_level_1", "sid_level_2", "sid_level_3"])
    out["method"] = "sanity_category_prefix"
    out["dataset"] = dataset
    validate_columns("sid_assignments", out.columns)
    return out


def popularity_balanced_sid(
    item_metadata: pd.DataFrame,
    interactions: pd.DataFrame,
    dataset: str,
    width: int = 256,
) -> pd.DataFrame:
    event_source = interactions[interactions["split"] == "train"] if "split" in interactions.columns else interactions
    counts = event_source.groupby("item_id").size().rename("popularity").reset_index()
    out = item_metadata[["item_id"]].merge(counts, on="item_id", how="left").fillna({"popularity": 0})
    out = out.sort_values(["popularity", "item_id"], ascending=[False, True]).reset_index(drop=True)
    out["sid_level_0"] = pd.qcut(out.index, q=4, labels=False, duplicates="drop").astype(int) + 1
    out["sid_level_1"] = (out.groupby("sid_level_0").cumcount() % width) + 1
    out["sid_level_2"] = ((out["item_id"].astype(int) * 131) % width) + 1
    out["sid_level_3"] = ((out["item_id"].astype(int) * 17) % width) + 1
    out["sid"] = _sid_from_levels(out, ["sid_level_0", "sid_level_1", "sid_level_2", "sid_level_3"])
    out["method"] = "sanity_popularity_balanced"
    out["dataset"] = dataset
    validate_columns("sid_assignments", out.columns)
    return out.drop(columns=["popularity"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate SIDInspector sanity SID baselines.")
    parser.add_argument("--item-metadata", type=Path, required=True)
    parser.add_argument("--interactions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="Musical_Instruments")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    item_metadata = pd.read_parquet(args.item_metadata)
    interactions = pd.read_parquet(args.interactions)

    baselines = [
        mod_collision_sid(item_metadata, args.dataset_name),
        category_prefix_sid(item_metadata, args.dataset_name),
        popularity_balanced_sid(item_metadata, interactions, args.dataset_name),
    ]
    sid_assignments = pd.concat(baselines, ignore_index=True)
    sid_assignments.to_parquet(args.output_dir / "sid_assignments.parquet", index=False)


if __name__ == "__main__":
    main()
