"""Normalize DACT code artifacts bundled with the public DACT release."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from sidinspector.interface import validate_columns


def normalize_dact_codes(
    codes_path: Path,
    method: str,
    dataset: str,
    item_ids: np.ndarray | None = None,
    item_id_offset: int = 1,
) -> pd.DataFrame:
    codes = np.load(codes_path, allow_pickle=False)
    if codes.ndim != 2:
        raise ValueError(f"Expected DACT codes to be 2D, got shape {codes.shape}")
    codes = codes.astype(np.int64)
    if item_ids is None:
        item_ids = np.arange(codes.shape[0], dtype=np.int64) + item_id_offset
    if len(item_ids) != codes.shape[0]:
        raise ValueError(f"item_ids length {len(item_ids)} does not match code rows {codes.shape[0]}")

    out = pd.DataFrame({"item_id": item_ids.astype(int), "method": method, "dataset": dataset})
    for level in range(codes.shape[1]):
        out[f"sid_level_{level}"] = codes[:, level].astype(int)
    level_cols = [f"sid_level_{level}" for level in range(codes.shape[1])]
    out["sid"] = out[level_cols].astype(str).agg("-".join, axis=1)
    validate_columns("sid_assignments", out.columns)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize public DACT SID code arrays.")
    parser.add_argument("--codes-path", type=Path, required=True)
    parser.add_argument("--item-ids", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="Tools")
    parser.add_argument("--method", default="dact")
    parser.add_argument("--item-id-offset", type=int, default=1)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    item_ids = np.load(args.item_ids, allow_pickle=False) if args.item_ids else None
    sid = normalize_dact_codes(
        codes_path=args.codes_path,
        method=args.method,
        dataset=args.dataset_name,
        item_ids=item_ids,
        item_id_offset=args.item_id_offset,
    )
    sid.to_parquet(args.output_dir / "sid_assignments.parquet", index=False)


if __name__ == "__main__":
    main()
