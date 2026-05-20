"""Normalize GRID semantic-ID assignment artifacts."""

from __future__ import annotations

import argparse
import pickle
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from audit_sid.interface import validate_columns


def _read_pt(path: Path) -> np.ndarray:
    import torch

    tensor = torch.load(path, map_location="cpu")
    if hasattr(tensor, "detach"):
        tensor = tensor.detach().cpu().numpy()
    return np.asarray(tensor)


def _read_pkl(path: Path, item_key: str, value_key: str) -> tuple[np.ndarray, np.ndarray]:
    with path.open("rb") as handle:
        rows = pickle.load(handle)
    if not isinstance(rows, list):
        raise ValueError(f"Expected GRID pickle to contain a list of rows: {path}")

    item_ids: list[int] = []
    values: list[Any] = []
    for row in rows:
        if item_key not in row or value_key not in row:
            raise ValueError(f"Missing {item_key!r} or {value_key!r} in GRID row")
        item_ids.append(int(row[item_key]))
        values.append(row[value_key])
    return np.asarray(item_ids, dtype=np.int64), np.asarray(values, dtype=np.int64)


def _read_item_ids(path: Path) -> np.ndarray:
    if path.suffix == ".npy":
        return np.load(path).astype(np.int64)
    if path.suffix == ".parquet":
        return pd.read_parquet(path)["item_id"].to_numpy(dtype=np.int64)
    frame = pd.read_csv(path)
    if "item_id" not in frame.columns:
        raise ValueError(f"{path} must contain an item_id column")
    return frame["item_id"].to_numpy(dtype=np.int64)


def _orient_codes(codes: np.ndarray, layout: str) -> np.ndarray:
    if codes.ndim != 2:
        raise ValueError(f"Expected a 2D GRID SID tensor, got shape {codes.shape}")
    if layout == "item_rows":
        return codes
    if layout == "item_columns":
        return codes.T
    if layout != "auto":
        raise ValueError(f"Unknown layout: {layout}")

    # GRID post-processing may transpose `merged_predictions_tensor.pt` so that
    # rows are SID levels and columns are item ids. SID depth is normally small.
    if codes.shape[0] <= 16 and codes.shape[1] > codes.shape[0]:
        return codes.T
    return codes


def normalize_grid_mapping(
    artifact_path: Path,
    method: str,
    dataset: str,
    layout: str = "auto",
    item_ids_path: Path | None = None,
    item_id_offset: int = 0,
    unsafe_assume_dense_zero_indexed: bool = False,
    item_key: str = "item_id",
    value_key: str = "cluster_ids",
) -> pd.DataFrame:
    if artifact_path.suffix == ".pt":
        item_ids = None
        codes = _read_pt(artifact_path)
    elif artifact_path.suffix == ".pkl":
        item_ids, codes = _read_pkl(artifact_path, item_key=item_key, value_key=value_key)
    elif artifact_path.suffix == ".npy":
        item_ids = None
        codes = np.load(artifact_path)
    else:
        raise ValueError(f"Unsupported GRID artifact suffix: {artifact_path.suffix}")

    codes = _orient_codes(np.asarray(codes, dtype=np.int64), layout=layout)
    if item_ids_path is not None:
        item_ids = _read_item_ids(item_ids_path)
    if item_ids is None:
        if not unsafe_assume_dense_zero_indexed:
            raise ValueError(
                "GRID tensor artifacts require --item-ids unless "
                "--unsafe-assume-dense-zero-indexed is explicitly set."
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
    parser = argparse.ArgumentParser(description="Normalize GRID SID mapping artifacts.")
    parser.add_argument("--artifact-path", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="unknown")
    parser.add_argument("--method", default="grid_rqvae")
    parser.add_argument("--layout", choices=("auto", "item_rows", "item_columns"), default="auto")
    parser.add_argument("--item-ids", type=Path, default=None)
    parser.add_argument("--item-id-offset", type=int, default=0)
    parser.add_argument("--unsafe-assume-dense-zero-indexed", action="store_true")
    parser.add_argument("--item-key", default="item_id")
    parser.add_argument("--value-key", default="cluster_ids")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    sid_assignments = normalize_grid_mapping(
        artifact_path=args.artifact_path,
        method=args.method,
        dataset=args.dataset_name,
        layout=args.layout,
        item_ids_path=args.item_ids,
        item_id_offset=args.item_id_offset,
        unsafe_assume_dense_zero_indexed=args.unsafe_assume_dense_zero_indexed,
        item_key=args.item_key,
        value_key=args.value_key,
    )
    sid_assignments.to_parquet(args.output_dir / "sid_assignments.parquet", index=False)


if __name__ == "__main__":
    main()
