"""Mapping-first SIDInspector diagnostic metrics.

The public paper uses D1--D5 names: utilization, aliasing, neighborhood
alignment, popularity allocation, and structural cost. Function and CSV names
retain earlier internal labels (for example, ``collision`` and
``d5a_deployment_cost.csv``) so previously generated artifacts remain
reproducible.
"""

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
    if "split" not in interactions.columns:
        return interactions
    train = interactions[interactions["split"] == "train"]
    return train if not train.empty else interactions


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


def _category_alignment(sid: pd.DataFrame, item_metadata: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if "category" not in item_metadata.columns:
        for group_key, group in sid.groupby(_group_cols(sid)):
            if not isinstance(group_key, tuple):
                group_key = (group_key,)
            key_values = dict(zip(_group_cols(sid), group_key))
            rows.append(
                {
                    **key_values,
                    "level0_category_purity_mean": np.nan,
                    "level0_non_singleton_buckets": 0,
                }
            )
        return pd.DataFrame(rows)
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


def _collaborative_neighbor_edges(
    interactions: pd.DataFrame,
    item_ids: set[int],
    top_k: int,
    max_pair_events: int,
    max_user_items: int,
) -> tuple[pd.DataFrame, dict[str, int]]:
    events = _train_events(interactions)[["user_id", "item_id"]].drop_duplicates()
    events = events[events["item_id"].astype(int).isin(item_ids)]
    if events.empty:
        return pd.DataFrame(columns=["item_id", "neighbor_item_id", "co_count", "rank"]), {
            "users_used": 0,
            "pair_events": 0,
            "collab_items": 0,
        }

    user_sizes = events.groupby("user_id").size()
    eligible = user_sizes[(user_sizes >= 2) & (user_sizes <= max_user_items)].sort_index()
    selected_users = []
    pair_events = 0
    for user_id, size in eligible.items():
        user_pairs = int(size * (size - 1) // 2)
        if selected_users and pair_events + user_pairs > max_pair_events:
            break
        selected_users.append(user_id)
        pair_events += user_pairs
    if not selected_users:
        return pd.DataFrame(columns=["item_id", "neighbor_item_id", "co_count", "rank"]), {
            "users_used": 0,
            "pair_events": 0,
            "collab_items": 0,
        }

    selected = events[events["user_id"].isin(selected_users)]
    pairs = selected.merge(selected, on="user_id", suffixes=("_i", "_j"))
    pairs = pairs[pairs["item_id_i"] < pairs["item_id_j"]]
    if pairs.empty:
        return pd.DataFrame(columns=["item_id", "neighbor_item_id", "co_count", "rank"]), {
            "users_used": len(selected_users),
            "pair_events": pair_events,
            "collab_items": 0,
        }

    counts = (
        pairs.groupby(["item_id_i", "item_id_j"])
        .size()
        .rename("co_count")
        .reset_index()
        .sort_values(["item_id_i", "co_count", "item_id_j"], ascending=[True, False, True])
    )
    forward = counts.rename(columns={"item_id_i": "item_id", "item_id_j": "neighbor_item_id"})
    backward = counts.rename(columns={"item_id_j": "item_id", "item_id_i": "neighbor_item_id"})
    directed = pd.concat([forward, backward], ignore_index=True)
    directed = directed.sort_values(["item_id", "co_count", "neighbor_item_id"], ascending=[True, False, True])
    directed["rank"] = directed.groupby("item_id").cumcount() + 1
    directed = directed[directed["rank"] <= top_k]
    return directed, {
        "users_used": len(selected_users),
        "pair_events": pair_events,
        "collab_items": int(directed["item_id"].nunique()),
    }


def alignment(
    sid: pd.DataFrame,
    item_metadata: pd.DataFrame,
    interactions: pd.DataFrame,
    top_k: int = 20,
    max_pair_events: int = 2_000_000,
    max_user_items: int = 200,
) -> pd.DataFrame:
    category = _category_alignment(sid, item_metadata)
    rows = []
    for group_key, group in sid.groupby(_group_cols(sid)):
        if not isinstance(group_key, tuple):
            group_key = (group_key,)
        key_values = dict(zip(_group_cols(sid), group_key))
        group_interactions = _filter_dataset(interactions, key_values.get("dataset"))
        item_ids = set(group["item_id"].astype(int))
        edges, stats = _collaborative_neighbor_edges(
            group_interactions,
            item_ids=item_ids,
            top_k=top_k,
            max_pair_events=max_pair_events,
            max_user_items=max_user_items,
        )
        level_cols = _level_cols(group)
        prefix_frame = group[["item_id", *level_cols]].copy()
        prefix_frame["item_id"] = prefix_frame["item_id"].astype(int)
        if edges.empty:
            for depth in range(1, len(level_cols) + 1):
                rows.append(
                    {
                        **key_values,
                        "prefix_depth": depth,
                        "collab_reference": "cooccurrence",
                        "collab_top_k": top_k,
                        **stats,
                        "mean_collab_prefix_recall": 0.0,
                        "weighted_collab_prefix_recall": 0.0,
                        "collab_edges_same_prefix_rate": 0.0,
                    }
                )
            continue

        for depth in range(1, len(level_cols) + 1):
            prefix_cols = level_cols[:depth]
            prefixes = prefix_frame[["item_id"]].copy()
            prefixes["prefix"] = prefix_frame[prefix_cols].astype(str).agg("-".join, axis=1)
            item_prefix = prefixes.rename(columns={"prefix": "item_prefix"})
            neighbor_prefix = prefixes.rename(columns={"item_id": "neighbor_item_id", "prefix": "neighbor_prefix"})
            scored = edges.merge(item_prefix, on="item_id", how="left").merge(
                neighbor_prefix, on="neighbor_item_id", how="left"
            )
            same_prefix = scored["item_prefix"] == scored["neighbor_prefix"]
            per_item = same_prefix.groupby(scored["item_id"]).agg(["sum", "count"])
            item_recall = per_item["sum"] / per_item["count"]
            rows.append(
                {
                    **key_values,
                    "prefix_depth": depth,
                    "collab_reference": "cooccurrence",
                    "collab_top_k": top_k,
                    **stats,
                    "mean_collab_prefix_recall": float(item_recall.mean()) if not item_recall.empty else 0.0,
                    "weighted_collab_prefix_recall": float(same_prefix.sum() / len(scored)) if len(scored) else 0.0,
                    "collab_edges_same_prefix_rate": float(same_prefix.mean()) if len(scored) else 0.0,
                }
            )

    collab = pd.DataFrame(rows)
    return collab.merge(category, on=_group_cols(sid), how="left")


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
    parser = argparse.ArgumentParser(description="Run SIDInspector mapping-first diagnostic probes.")
    parser.add_argument("--sid-assignments", type=Path, required=True)
    parser.add_argument("--item-metadata", type=Path, required=True)
    parser.add_argument("--interactions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--allow-partial-coverage", action="store_true")
    parser.add_argument("--d3-top-k", type=int, default=20)
    parser.add_argument("--d3-max-pair-events", type=int, default=2_000_000)
    parser.add_argument("--d3-max-user-items", type=int, default=200)
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
        "d3_alignment.csv": alignment(
            sid,
            item_metadata,
            interactions,
            top_k=args.d3_top_k,
            max_pair_events=args.d3_max_pair_events,
            max_user_items=args.d3_max_user_items,
        ),
        "d4_head_tail.csv": head_tail_capacity(sid, interactions),
        "d5a_deployment_cost.csv": deployment_cost(sid),
    }
    for name, table in tables.items():
        table.to_csv(args.output_dir / name, index=False)


if __name__ == "__main__":
    main()
