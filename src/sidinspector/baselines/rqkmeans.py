"""Generate a local residual-kmeans SID baseline from item features.

This is a development baseline for toolkit and case-study plumbing. It is not a
replacement for auditing a public GRID/TIGER-style implementation.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler

from sidinspector.interface import validate_columns


def _feature_matrix(item_metadata: pd.DataFrame, feature_cols: list[str]) -> np.ndarray:
    missing = [col for col in feature_cols if col not in item_metadata.columns]
    if missing:
        raise ValueError(f"Missing feature columns: {', '.join(missing)}")
    features = item_metadata[feature_cols].astype(float).to_numpy()
    return StandardScaler().fit_transform(features)


def residual_kmeans_sid(
    item_metadata: pd.DataFrame,
    dataset: str,
    method: str,
    feature_cols: list[str],
    widths: list[int],
    seed: int,
) -> pd.DataFrame:
    item_ids = item_metadata["item_id"].astype(int).to_numpy()
    residual = _feature_matrix(item_metadata, feature_cols)
    assignments: dict[str, np.ndarray] = {}

    for level, width in enumerate(widths):
        n_clusters = min(width, len(item_metadata))
        model = MiniBatchKMeans(
            n_clusters=n_clusters,
            random_state=seed + level,
            batch_size=min(4096, len(item_metadata)),
            n_init=10,
        )
        labels = model.fit_predict(residual)
        assignments[f"sid_level_{level}"] = labels.astype(int) + 1
        residual = residual - model.cluster_centers_[labels]

    out = pd.DataFrame({"item_id": item_ids, "method": method, "dataset": dataset})
    for col, values in assignments.items():
        out[col] = values
    level_cols = list(assignments)
    out["sid"] = out[level_cols].astype(str).agg("-".join, axis=1)
    validate_columns("sid_assignments", out.columns)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a local residual-kmeans SID baseline.")
    parser.add_argument("--item-metadata", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="Musical_Instruments")
    parser.add_argument("--method", default="local_rqkmeans_feature_proxy")
    parser.add_argument("--feature-cols", default="store_id,category_l1,category_l2,category_l3")
    parser.add_argument("--widths", default="32,40,19")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    item_metadata = pd.read_parquet(args.item_metadata)
    feature_cols = [col.strip() for col in args.feature_cols.split(",") if col.strip()]
    widths = [int(width.strip()) for width in args.widths.split(",") if width.strip()]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    sid_assignments = residual_kmeans_sid(
        item_metadata=item_metadata,
        dataset=args.dataset_name,
        method=args.method,
        feature_cols=feature_cols,
        widths=widths,
        seed=args.seed,
    )
    sid_assignments.to_parquet(args.output_dir / "sid_assignments.parquet", index=False)


if __name__ == "__main__":
    main()
