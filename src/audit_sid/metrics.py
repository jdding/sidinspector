"""Mapping-first AUDIT-SID diagnostic metrics."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def _entropy(values: pd.Series) -> float:
    probs = values.value_counts(normalize=True)
    return float(-(probs * np.log2(probs)).sum())


def _gini(values: pd.Series) -> float:
    counts = np.sort(values.value_counts().to_numpy(dtype=float))
    if counts.size == 0 or counts.sum() == 0:
        return 0.0
    index = np.arange(1, counts.size + 1)
    return float((2 * (index * counts).sum()) / (counts.size * counts.sum()) - (counts.size + 1) / counts.size)


def _level_cols(frame: pd.DataFrame) -> list[str]:
    return sorted(
        [col for col in frame.columns if col.startswith("sid_level_") and not frame[col].isna().all()],
        key=lambda x: int(x.rsplit("_", 1)[1]),
    )


def _group_cols(frame: pd.DataFrame) -> list[str]:
    return ["dataset", "method"] if "dataset" in frame.columns else ["method"]


def _train_events(interactions: pd.DataFrame) -> pd.DataFrame:
    return interactions[interactions["split"] == "train"] if "split" in interactions.columns else interactions


def _filter_dataset(frame: pd.DataFrame, dataset: object) -> pd.DataFrame:
    if "dataset" not in frame.columns:
        return frame
    return frame[frame["dataset"] == dataset]


def validate_inputs(
    sid: pd.DataFrame,
    item_metadata: pd.DataFrame,
    interactions: pd.DataFrame,
    allow_partial_coverage: bool = False,
) -> pd.DataFrame:
    level_cols = _level_cols(sid)
    if not level_cols:
        raise ValueError("sid_assignments must contain at least one sid_level_* column")
    required_non_null = ["item_id", "sid", "method"]
    if "dataset" in sid.columns:
        required_non_null.append("dataset")
    for col in required_non_null:
        if sid[col].isna().any():
            raise ValueError(f"sid_assignments contains null values in {col}")
    metadata_unique_key = ["dataset", "item_id"] if "dataset" in item_metadata.columns else ["item_id"]
    if item_metadata.duplicated(metadata_unique_key).any():
        raise ValueError("item_metadata contains duplicate item_id values")
    if "dataset" in sid.columns and sid["dataset"].nunique() > 1:
        if "dataset" not in item_metadata.columns or "dataset" not in interactions.columns:
            raise ValueError(
                "Multi-dataset sid_assignments require dataset columns in item_metadata and interactions. "
                "Run metrics per dataset or add dataset-aware metadata/interactions."
            )

    duplicate_keys = sid.duplicated(_group_cols(sid) + ["item_id"])
    if duplicate_keys.any():
        raise ValueError("sid_assignments contains duplicate item_id rows within a dataset/method group")

    coverage_rows = []
    for group_key, group in sid.groupby(_group_cols(sid)):
        if not isinstance(group_key, tuple):
            group_key = (group_key,)
        key_values = dict(zip(_group_cols(sid), group_key))
        dataset = key_values.get("dataset")
        group_metadata = _filter_dataset(item_metadata, dataset)
        group_interactions = _filter_dataset(interactions, dataset)
        if group_metadata["item_id"].duplicated().any():
            raise ValueError(f"{key_values} has duplicate item_id values in item_metadata")
        group_level_cols = _level_cols(group)
        if not group_level_cols:
            raise ValueError(f"{key_values} has no non-null sid_level_* columns")
        for col in group_level_cols:
            if group[col].isna().any():
                raise ValueError(f"{key_values} contains null values in {col}")
        sid_items = set(group["item_id"].astype(int))
        meta_items = set(group_metadata["item_id"].astype(int))
        interaction_items = set(group_interactions["item_id"].astype(int))
        missing_metadata = sid_items - meta_items
        missing_sid_for_metadata = meta_items - sid_items
        missing_sid_for_interactions = interaction_items - sid_items
        if missing_metadata:
            raise ValueError(f"{key_values} has SID rows missing item metadata: {len(missing_metadata)}")
        if not allow_partial_coverage and missing_sid_for_metadata:
            raise ValueError(f"{key_values} is missing SID rows for metadata items: {len(missing_sid_for_metadata)}")
        if not allow_partial_coverage and missing_sid_for_interactions:
            raise ValueError(
                f"{key_values} is missing SID rows for interaction items: {len(missing_sid_for_interactions)}"
            )
        coverage_rows.append(
            {
                **key_values,
                "sid_items": len(sid_items),
                "metadata_items": len(meta_items),
                "interaction_items": len(interaction_items),
                "metadata_without_sid": len(missing_sid_for_metadata),
                "interaction_without_sid": len(missing_sid_for_interactions),
            }
        )
    return pd.DataFrame(coverage_rows)


def utilization(sid: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for group_key, group in sid.groupby(_group_cols(sid)):
        if not isinstance(group_key, tuple):
            group_key = (group_key,)
        key_values = dict(zip(_group_cols(sid), group_key))
        for col in _level_cols(group):
            rows.append(
                {
                    **key_values,
                    "level": col,
                    "items": len(group),
                    "unique_codes": int(group[col].nunique()),
                    "entropy": _entropy(group[col]),
                    "gini": _gini(group[col]),
                    "max_code": int(group[col].max()),
                }
            )
    return pd.DataFrame(rows)


def collision(sid: pd.DataFrame, interactions: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for group_key, group in sid.groupby(_group_cols(sid)):
        if not isinstance(group_key, tuple):
            group_key = (group_key,)
        key_values = dict(zip(_group_cols(sid), group_key))
        group_interactions = _filter_dataset(interactions, key_values.get("dataset"))
        popularity = _train_events(group_interactions).groupby("item_id").size().rename("popularity")
        merged = group.merge(popularity, on="item_id", how="left").fillna({"popularity": 0})
        full_sizes = merged.groupby("sid").size()
        full_collision_items = int(full_sizes[full_sizes > 1].sum())
        collided = merged["sid"].isin(full_sizes[full_sizes > 1].index)
        for depth in range(1, len(_level_cols(merged)) + 1):
            prefix_cols = _level_cols(merged)[:depth]
            prefix_key = merged[prefix_cols].astype(str).agg("-".join, axis=1)
            prefix_sizes = prefix_key.value_counts()
            rows.append(
                {
                    **key_values,
                    "prefix_depth": depth,
                    "full_collision_groups": int((full_sizes > 1).sum()),
                    "full_collision_items": full_collision_items,
                    "full_collision_rate": float((full_collision_items / len(merged)) if len(merged) else 0),
                    "prefix_collision_groups": int((prefix_sizes > 1).sum()),
                    "prefix_collision_items": int(prefix_sizes[prefix_sizes > 1].sum()),
                    "prefix_collision_rate": float(
                        (prefix_sizes[prefix_sizes > 1].sum() / len(merged)) if len(merged) else 0
                    ),
                    "mean_popularity_full_collision_items": float(merged.loc[collided, "popularity"].mean())
                    if collided.any()
                    else 0.0,
                    "mean_popularity_prefix_collision_items": float(
                        merged.loc[prefix_key.isin(prefix_sizes[prefix_sizes > 1].index), "popularity"].mean()
                    )
                    if (prefix_sizes > 1).any()
                    else 0.0,
                }
            )
    return pd.DataFrame(rows)


def alignment(sid: pd.DataFrame, item_metadata: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if item_metadata["category"].isna().any():
        raise ValueError("item_metadata contains null category values")
    for group_key, group in sid.groupby(_group_cols(sid)):
        if not isinstance(group_key, tuple):
            group_key = (group_key,)
        key_values = dict(zip(_group_cols(sid), group_key))
        meta = _filter_dataset(item_metadata, key_values.get("dataset"))[["item_id", "category"]].copy()
        merged = group.merge(meta, on="item_id", how="left")
        if merged["category"].isna().any():
            raise ValueError(f"{key_values} has SID rows without category metadata")
        first_level = _level_cols(merged)[0]
        purity_values = []
        for _, bucket in merged.groupby(first_level):
            if len(bucket) <= 1:
                continue
            purity_values.append(bucket["category"].value_counts(normalize=True).max())
        rows.append(
            {
                **key_values,
                "level0_category_purity_mean": float(np.mean(purity_values)) if purity_values else 1.0,
                "level0_non_singleton_buckets": len(purity_values),
            }
        )
    return pd.DataFrame(rows)


def head_tail_capacity(sid: pd.DataFrame, interactions: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for group_key, group in sid.groupby(_group_cols(sid)):
        if not isinstance(group_key, tuple):
            group_key = (group_key,)
        key_values = dict(zip(_group_cols(sid), group_key))
        group_interactions = _filter_dataset(interactions, key_values.get("dataset"))
        popularity = _train_events(group_interactions).groupby("item_id").size().rename("popularity").reset_index()
        if popularity.empty:
            popularity["bucket"] = pd.Series(dtype="object")
        else:
            pct_rank = popularity["popularity"].rank(method="first", pct=True)
            popularity["bucket"] = np.select(
                [pct_rank <= 1 / 3, pct_rank <= 2 / 3],
                ["tail", "mid"],
                default="head",
            )
        merged = group.merge(popularity[["item_id", "bucket"]], on="item_id", how="left").fillna({"bucket": "tail"})
        for bucket, bucket_df in merged.groupby("bucket", observed=False):
            rows.append(
                {
                    **key_values,
                    "bucket": bucket,
                    "items": len(bucket_df),
                    "sid_unique_ratio": float(bucket_df["sid"].nunique() / len(bucket_df)) if len(bucket_df) else 0,
                    "level0_entropy": _entropy(bucket_df[_level_cols(bucket_df)[0]]) if len(bucket_df) else 0,
                }
            )
    return pd.DataFrame(rows)


def deployment_cost(sid: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for group_key, group in sid.groupby(_group_cols(sid)):
        if not isinstance(group_key, tuple):
            group_key = (group_key,)
        key_values = dict(zip(_group_cols(sid), group_key))
        level_cols = _level_cols(group)
        prefix_counts = []
        for depth in range(1, len(level_cols) + 1):
            prefix_counts.append(group[level_cols[:depth]].drop_duplicates().shape[0])
        rows.append(
            {
                **key_values,
                "sid_length": len(level_cols),
                "unique_sid": int(group["sid"].nunique()),
                "duplicate_sid_rate": float(1 - group["sid"].nunique() / len(group)) if len(group) else 0,
                "prefix_counts": ";".join(map(str, prefix_counts)),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AUDIT-SID mapping-first metrics.")
    parser.add_argument("--sid-assignments", type=Path, required=True)
    parser.add_argument("--item-metadata", type=Path, required=True)
    parser.add_argument("--interactions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--allow-partial-coverage", action="store_true")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    sid = pd.read_parquet(args.sid_assignments)
    item_metadata = pd.read_parquet(args.item_metadata)
    interactions = pd.read_parquet(args.interactions)
    coverage = validate_inputs(sid, item_metadata, interactions, allow_partial_coverage=args.allow_partial_coverage)

    tables = {
        "coverage_report.csv": coverage,
        "d1_utilization.csv": utilization(sid),
        "d2_collision.csv": collision(sid, interactions),
        "d3_alignment.csv": alignment(sid, item_metadata),
        "d4_head_tail.csv": head_tail_capacity(sid, interactions),
        "d5a_deployment_cost.csv": deployment_cost(sid),
    }
    for name, table in tables.items():
        table.to_csv(args.output_dir / name, index=False)


if __name__ == "__main__":
    main()
