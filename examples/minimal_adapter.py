#!/usr/bin/env python3
"""Minimal SIDInspector adapter for an existing item-to-code export.

The adapter assumes the tokenizer has already produced one row per item. It
does not train or reproduce a tokenizer; it only normalizes an item-to-code
table into SIDInspector's mapping contract.

Input CSV columns:
  item_id, sid_0, sid_1, ... sid_L

Output:
  sid_assignments.parquet with item_id, sid_level_*, sid, method, dataset.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sidinspector.interface import validate_columns


def normalize_sid_export(input_csv: Path, method: str, dataset: str) -> pd.DataFrame:
    raw = pd.read_csv(input_csv)
    sid_cols = sorted(
        [col for col in raw.columns if col.startswith("sid_")],
        key=lambda col: int(col.rsplit("_", 1)[1]),
    )
    if "item_id" not in raw.columns or not sid_cols:
        raise ValueError("input CSV must contain item_id and at least one sid_<level> column")

    out = raw[["item_id", *sid_cols]].copy()
    rename = {col: f"sid_level_{idx}" for idx, col in enumerate(sid_cols)}
    out = out.rename(columns=rename)
    level_cols = [rename[col] for col in sid_cols]
    out["sid"] = out[level_cols].astype(str).agg("-".join, axis=1)
    out["method"] = method
    out["dataset"] = dataset
    validate_columns("sid_assignments", out.columns)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize a tokenizer item-to-code CSV for SIDInspector.")
    parser.add_argument("--input-csv", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--method", required=True)
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    sid_assignments = normalize_sid_export(args.input_csv, args.method, args.dataset)
    sid_assignments.to_parquet(args.output_dir / "sid_assignments.parquet", index=False)
    print(f"wrote {len(sid_assignments)} rows to {args.output_dir / 'sid_assignments.parquet'}")


if __name__ == "__main__":
    main()
