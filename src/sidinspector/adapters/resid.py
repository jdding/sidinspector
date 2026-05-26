"""Normalize ReSID processed datasets and GAOQ mappings."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

from sidinspector.interface import validate_columns


def _read_parquet_dir(path: Path) -> pd.DataFrame:
    files = sorted(path.glob("part-*.parquet"))
    if not files:
        raise FileNotFoundError(f"No parquet part files found under {path}")
    return pd.concat((pd.read_parquet(file) for file in files), ignore_index=True)


def normalize_item_metadata(dataset_root: Path) -> pd.DataFrame:
    item_feature = _read_parquet_dir(dataset_root / "item_feature")
    item_feature = item_feature.rename(
        columns={
            "cate1_id": "category_l1",
            "cate2_id": "category_l2",
            "cate3_id": "category_l3",
        }
    )
    item_feature["category"] = item_feature["category_l3"]
    validate_columns("item_metadata", item_feature.columns)
    return item_feature


def normalize_interactions(dataset_root: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for split in ("train", "valid", "test"):
        split_df = _read_parquet_dir(dataset_root / split)
        frames.append(
            split_df[["user_id", "target", "timestamp"]]
            .rename(columns={"target": "item_id"})
            .assign(split=split, is_target=True)
        )
    interactions = pd.concat(frames, ignore_index=True)
    interactions["item_id"] = interactions["item_id"].astype(int)
    validate_columns("interactions", interactions.columns)
    return interactions


def normalize_gaoq_mapping(mapping_path: Path, method: str, dataset: str) -> pd.DataFrame:
    mapping = pd.read_parquet(mapping_path)
    matched_cols: list[tuple[int, str]] = []
    for col in mapping.columns:
        match = re.fullmatch(r"codebook(\d+)_id", col)
        if match:
            matched_cols.append((int(match.group(1)), col))
    matched_cols = sorted(matched_cols)
    code_cols = [col for _, col in matched_cols]
    if not code_cols:
        raise ValueError(f"No codebook columns found in {mapping_path}")
    expected = list(range(1, len(code_cols) + 1))
    actual = [level for level, _ in matched_cols]
    if actual != expected:
        raise ValueError(f"Non-contiguous ReSID codebook levels in {mapping_path}: {actual}")

    out = pd.DataFrame(
        {
            "item_id": mapping["item_id"].astype(int),
            "method": method,
            "dataset": dataset,
        }
    )
    for idx, col in enumerate(code_cols):
        out[f"sid_level_{idx}"] = mapping[col].astype(int)
    out["sid"] = out[[f"sid_level_{idx}" for idx in range(len(code_cols))]].astype(str).agg("-".join, axis=1)
    validate_columns("sid_assignments", out.columns)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize ReSID artifacts.")
    parser.add_argument("--dataset-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="Musical_Instruments")
    parser.add_argument("--gaoq-mapping", type=Path, default=None)
    parser.add_argument("--method", default="resid_gaoq")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    item_metadata = normalize_item_metadata(args.dataset_root)
    item_metadata.to_parquet(args.output_dir / "item_metadata.parquet", index=False)

    interactions = normalize_interactions(args.dataset_root)
    interactions.to_parquet(args.output_dir / "interactions.parquet", index=False)

    if args.gaoq_mapping:
        sid_assignments = normalize_gaoq_mapping(
            args.gaoq_mapping,
            method=args.method,
            dataset=args.dataset_name,
        )
        sid_assignments.to_parquet(args.output_dir / "sid_assignments.parquet", index=False)


if __name__ == "__main__":
    main()
