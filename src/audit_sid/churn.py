"""D6 SID refresh/churn diagnostics."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def level_cols(frame: pd.DataFrame) -> list[str]:
    """Return SID level columns sorted by level index."""

    return sorted([c for c in frame.columns if c.startswith("sid_level_")], key=lambda c: int(c.rsplit("_", 1)[1]))


def _prefix_key(frame: pd.DataFrame, cols: list[str]) -> pd.Series:
    return frame[cols].astype(str).agg("-".join, axis=1)


def _collision_stats(frame: pd.DataFrame, cols: list[str], label: str) -> dict[str, int | float]:
    keys = _prefix_key(frame, cols)
    sizes = keys.value_counts()
    collision_groups = int((sizes > 1).sum())
    collision_items = int(sizes[sizes > 1].sum())
    return {
        f"{label}_unique_prefixes": int(sizes.shape[0]),
        f"{label}_prefix_collision_groups": collision_groups,
        f"{label}_prefix_collision_items": collision_items,
        f"{label}_prefix_collision_rate": float(collision_items / len(frame)) if len(frame) else 0.0,
    }


def _key_cols(old_sid: pd.DataFrame, new_sid: pd.DataFrame) -> list[str]:
    old_has_dataset = "dataset" in old_sid.columns
    new_has_dataset = "dataset" in new_sid.columns
    if old_has_dataset != new_has_dataset:
        raise ValueError("old_sid and new_sid must either both contain dataset or both omit it")
    return ["dataset", "item_id"] if old_has_dataset else ["item_id"]


def _validate_sid(frame: pd.DataFrame, name: str, key_cols: list[str]) -> None:
    if "item_id" not in frame.columns:
        raise ValueError(f"{name} must contain item_id")
    for col in key_cols:
        if col not in frame.columns:
            raise ValueError(f"{name} must contain {col}")
        if frame[col].isna().any():
            raise ValueError(f"{name} contains null {col} values")
    if frame["item_id"].isna().any():
        raise ValueError(f"{name} contains null item_id values")
    if frame.duplicated(key_cols).any():
        raise ValueError(f"{name} contains duplicate rows for key {key_cols}")
    if not level_cols(frame):
        raise ValueError(f"{name} must contain at least one sid_level_* column")


def compute_churn(old_sid: pd.DataFrame, new_sid: pd.DataFrame) -> pd.DataFrame:
    """Compare two SID assignment tables and report prefix churn by depth."""

    key_cols = _key_cols(old_sid, new_sid)
    _validate_sid(old_sid, "old_sid", key_cols)
    _validate_sid(new_sid, "new_sid", key_cols)
    old_levels = level_cols(old_sid)
    new_levels = level_cols(new_sid)
    max_depth = min(len(old_levels), len(new_levels))
    old = old_sid[[*key_cols, *old_levels[:max_depth]]].copy()
    new = new_sid[[*key_cols, *new_levels[:max_depth]]].copy()
    group_values = [None]
    if "dataset" in key_cols:
        group_values = sorted(set(old["dataset"].astype(str)) | set(new["dataset"].astype(str)))
    rows = []
    for dataset in group_values:
        if dataset is None:
            old_group = old
            new_group = new
            key_values = {}
            item_key = "item_id"
        else:
            old_group = old[old["dataset"].astype(str) == dataset]
            new_group = new[new["dataset"].astype(str) == dataset]
            key_values = {"dataset": dataset}
            item_key = "item_id"
        merged = old_group.merge(new_group, on=key_cols, suffixes=("_old", "_new"))
        old_items = set(old_group[item_key].astype(int))
        new_items = set(new_group[item_key].astype(int))
        for depth in range(1, max_depth + 1):
            old_cols = [f"{old_levels[i]}_old" for i in range(depth)]
            new_cols = [f"{new_levels[i]}_new" for i in range(depth)]
            changed = (merged[old_cols].to_numpy() != merged[new_cols].to_numpy()).any(axis=1)
            rows.append(
                {
                    **key_values,
                    "prefix_depth": depth,
                    "old_items": int(len(old_items)),
                    "new_items": int(len(new_items)),
                    "common_items": int(len(merged)),
                    "old_only_items": int(len(old_items - new_items)),
                    "new_only_items": int(len(new_items - old_items)),
                    "common_rate_old": float(len(merged) / len(old_items)) if old_items else 0.0,
                    "common_rate_new": float(len(merged) / len(new_items)) if new_items else 0.0,
                    "changed_items": int(changed.sum()),
                    "stable_items": int((~changed).sum()),
                    "churn_rate_common": float(changed.mean()) if len(merged) else 0.0,
                    **_collision_stats(old_group, old_levels[:depth], "old"),
                    **_collision_stats(new_group, new_levels[:depth], "new"),
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old-sid", type=Path, required=True)
    parser.add_argument("--new-sid", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    old_sid = pd.read_parquet(args.old_sid)
    new_sid = pd.read_parquet(args.new_sid)
    table = compute_churn(old_sid, new_sid)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(args.output, index=False)
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
