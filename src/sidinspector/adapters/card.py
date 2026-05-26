"""Normalize CARD RQ-VAE/NU-RQ-VAE generated code artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from sidinspector.interface import validate_columns


def _default_item_ids_path(codes_path: Path) -> Path:
    return codes_path.with_name(f"{codes_path.stem}_item_ids.npy")


def _read_item_ids(path: Path) -> np.ndarray:
    if path.suffix == ".npy":
        return np.load(path).astype(np.int64)
    if path.suffix == ".parquet":
        frame = pd.read_parquet(path)
    else:
        frame = pd.read_csv(path)
    for column in ("item_id", "ItemID"):
        if column in frame.columns:
            return frame[column].to_numpy(dtype=np.int64)
    raise ValueError(f"{path} must contain item_id or ItemID")


def normalize_card_codes(
    codes_path: Path,
    method: str,
    dataset: str,
    item_ids_path: Path | None = None,
    item_id_offset: int = 1,
    unsafe_assume_dense_item_ids: bool = False,
) -> pd.DataFrame:
    codes = np.load(codes_path)
    if codes.ndim != 2:
        raise ValueError(f"Expected CARD codes to be a 2D array, got shape {codes.shape}")
    codes = codes.astype(np.int64)

    if item_ids_path is None:
        default_path = _default_item_ids_path(codes_path)
        if default_path.exists():
            item_ids_path = default_path

    if item_ids_path is not None:
        item_ids = _read_item_ids(item_ids_path)
    else:
        if not unsafe_assume_dense_item_ids:
            raise ValueError(
                "CARD code artifacts require --item-ids or a sibling *_item_ids.npy "
                "unless --unsafe-assume-dense-item-ids is explicitly set."
            )
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
    parser = argparse.ArgumentParser(description="Normalize CARD generated SID code artifacts.")
    parser.add_argument("--codes-path", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="unknown")
    parser.add_argument("--method", default="card_rqvae")
    parser.add_argument("--item-ids", type=Path, default=None)
    parser.add_argument("--item-id-offset", type=int, default=1)
    parser.add_argument("--unsafe-assume-dense-item-ids", action="store_true")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    sid_assignments = normalize_card_codes(
        codes_path=args.codes_path,
        method=args.method,
        dataset=args.dataset_name,
        item_ids_path=args.item_ids,
        item_id_offset=args.item_id_offset,
        unsafe_assume_dense_item_ids=args.unsafe_assume_dense_item_ids,
    )
    sid_assignments.to_parquet(args.output_dir / "sid_assignments.parquet", index=False)


if __name__ == "__main__":
    main()
