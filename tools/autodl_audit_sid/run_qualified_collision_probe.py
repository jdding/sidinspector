#!/usr/bin/env python3
"""Run an interaction-qualified collision probe for SID artifacts."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from audit_sid.metrics import validate_inputs


def read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".json", ".jsonl", ".ndjson"}:
        return pd.read_json(path, lines=suffix in {".jsonl", ".ndjson"})
    raise ValueError(f"unsupported table format for {path}")


def train_events(interactions: pd.DataFrame) -> pd.DataFrame:
    if "split" in interactions.columns:
        train = interactions[interactions["split"] == "train"]
        if not train.empty:
            return train
    return interactions


def pair_key(left: int, right: int) -> str:
    a, b = sorted((int(left), int(right)))
    return f"{a}-{b}"


def build_popularity_frame(item_ids: set[int], interactions: pd.DataFrame, bins: int) -> pd.DataFrame:
    counts = train_events(interactions).groupby("item_id").size().rename("popularity").reset_index()
    frame = pd.DataFrame({"item_id": sorted(item_ids)})
    frame = frame.merge(counts, on="item_id", how="left").fillna({"popularity": 0})
    frame["popularity"] = frame["popularity"].astype(int)
    if len(frame) <= 1:
        frame["popularity_bucket"] = 0
        return frame
    q = max(1, min(int(bins), len(frame)))
    ranks = frame["popularity"].rank(method="first")
    frame["popularity_bucket"] = pd.qcut(ranks, q=q, labels=False, duplicates="drop").astype(int)
    return frame


def bounded_cooccurrence_pairs(
    interactions: pd.DataFrame,
    item_ids: set[int],
    *,
    max_user_items: int,
    max_pair_events: int,
) -> tuple[pd.DataFrame, dict[str, int]]:
    events = train_events(interactions)[["user_id", "item_id"]].drop_duplicates()
    events = events[events["item_id"].astype(int).isin(item_ids)]
    if events.empty:
        return pd.DataFrame(columns=["item_i", "item_j", "co_count", "pair_key"]), {
            "users_used": 0,
            "pair_events": 0,
            "cooccurrence_pairs": 0,
        }

    user_sizes = events.groupby("user_id").size()
    eligible = user_sizes[(user_sizes >= 2) & (user_sizes <= max_user_items)].sort_index()
    selected_users: list[Any] = []
    pair_events = 0
    for user_id, size in eligible.items():
        next_pairs = int(size * (size - 1) // 2)
        if selected_users and pair_events + next_pairs > max_pair_events:
            break
        selected_users.append(user_id)
        pair_events += next_pairs

    if not selected_users:
        return pd.DataFrame(columns=["item_i", "item_j", "co_count", "pair_key"]), {
            "users_used": 0,
            "pair_events": 0,
            "cooccurrence_pairs": 0,
        }

    selected = events[events["user_id"].isin(selected_users)]
    pairs = selected.merge(selected, on="user_id", suffixes=("_i", "_j"))
    pairs = pairs[pairs["item_id_i"] < pairs["item_id_j"]]
    if pairs.empty:
        return pd.DataFrame(columns=["item_i", "item_j", "co_count", "pair_key"]), {
            "users_used": len(selected_users),
            "pair_events": pair_events,
            "cooccurrence_pairs": 0,
        }

    counts = pairs.groupby(["item_id_i", "item_id_j"]).size().rename("co_count").reset_index()
    counts = counts.rename(columns={"item_id_i": "item_i", "item_id_j": "item_j"})
    counts["item_i"] = counts["item_i"].astype(int)
    counts["item_j"] = counts["item_j"].astype(int)
    counts["pair_key"] = [pair_key(a, b) for a, b in zip(counts["item_i"], counts["item_j"])]
    return counts, {
        "users_used": len(selected_users),
        "pair_events": pair_events,
        "cooccurrence_pairs": int(len(counts)),
    }


def sample_collision_pairs(group: pd.DataFrame, max_pairs: int, rng: np.random.Generator) -> tuple[pd.DataFrame, int]:
    rows: list[dict[str, Any]] = []
    total_possible = 0
    for sid_value, sid_group in group.groupby("sid", sort=True):
        items = sorted(sid_group["item_id"].astype(int).tolist())
        n_items = len(items)
        if n_items <= 1:
            continue
        group_pairs = n_items * (n_items - 1) // 2
        total_possible += group_pairs
        remaining = max_pairs - len(rows)
        if remaining <= 0:
            continue
        if group_pairs <= remaining:
            for left_pos in range(n_items):
                for right_pos in range(left_pos + 1, n_items):
                    rows.append(
                        {
                            "item_i": items[left_pos],
                            "item_j": items[right_pos],
                            "shared_sid": sid_value,
                            "collision_group_size": n_items,
                        }
                    )
        else:
            seen: set[tuple[int, int]] = set()
            attempts = 0
            while len(seen) < remaining and attempts < remaining * 50:
                a, b = rng.choice(items, size=2, replace=False)
                left, right = sorted((int(a), int(b)))
                seen.add((left, right))
                attempts += 1
            for left, right in sorted(seen):
                rows.append(
                    {
                        "item_i": left,
                        "item_j": right,
                        "shared_sid": sid_value,
                        "collision_group_size": n_items,
                    }
                )
    return pd.DataFrame(rows), int(total_possible)


def sample_matched_noncollision_pairs(
    collision_pairs: pd.DataFrame,
    pop: pd.DataFrame,
    sid_by_item: dict[int, str],
    rng: np.random.Generator,
    attempts_per_pair: int,
) -> pd.DataFrame:
    if collision_pairs.empty:
        return pd.DataFrame(columns=["item_i", "item_j", "shared_sid", "collision_group_size"])

    item_bucket = pop.set_index("item_id")["popularity_bucket"].to_dict()
    bucket_items = {
        int(bucket): values["item_id"].astype(int).to_numpy()
        for bucket, values in pop.groupby("popularity_bucket", sort=True)
    }
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for _, row in collision_pairs.iterrows():
        bucket_i = int(item_bucket[int(row["item_i"])])
        bucket_j = int(item_bucket[int(row["item_j"])])
        left_candidates = bucket_items.get(bucket_i, np.array([], dtype=int))
        right_candidates = bucket_items.get(bucket_j, np.array([], dtype=int))
        if left_candidates.size == 0 or right_candidates.size == 0:
            continue
        for _ in range(attempts_per_pair):
            left = int(rng.choice(left_candidates))
            right = int(rng.choice(right_candidates))
            if left == right:
                continue
            key = pair_key(left, right)
            if key in seen:
                continue
            if sid_by_item[left] == sid_by_item[right]:
                continue
            seen.add(key)
            a, b = sorted((left, right))
            rows.append({"item_i": a, "item_j": b, "shared_sid": "", "collision_group_size": 0})
            break
    return pd.DataFrame(rows)


def annotate_pairs(
    pairs: pd.DataFrame,
    *,
    pair_type: str,
    method: str,
    dataset: str,
    sid_by_item: dict[int, str],
    pop: pd.DataFrame,
    cooccurrence: pd.DataFrame,
    category_by_item: dict[int, Any],
) -> pd.DataFrame:
    if pairs.empty:
        return pd.DataFrame(
            columns=[
                "dataset",
                "method",
                "pair_type",
                "item_i",
                "item_j",
                "sid_i",
                "sid_j",
                "same_sid",
                "popularity_i",
                "popularity_j",
                "popularity_bucket_i",
                "popularity_bucket_j",
                "co_count",
                "shares_user",
                "same_category",
                "collision_group_size",
            ]
        )
    out = pairs.copy()
    out["dataset"] = dataset
    out["method"] = method
    out["pair_type"] = pair_type
    out["pair_key"] = [pair_key(a, b) for a, b in zip(out["item_i"], out["item_j"])]
    out["sid_i"] = out["item_i"].map(sid_by_item)
    out["sid_j"] = out["item_j"].map(sid_by_item)
    out["same_sid"] = out["sid_i"] == out["sid_j"]

    pop_cols = pop.set_index("item_id")[["popularity", "popularity_bucket"]]
    out = out.merge(pop_cols.add_suffix("_i"), left_on="item_i", right_index=True, how="left")
    out = out.merge(pop_cols.add_suffix("_j"), left_on="item_j", right_index=True, how="left")
    co_map = cooccurrence.set_index("pair_key")["co_count"] if not cooccurrence.empty else pd.Series(dtype=int)
    out["co_count"] = out["pair_key"].map(co_map).fillna(0).astype(int)
    out["shares_user"] = out["co_count"] > 0
    out["same_category"] = out["item_i"].map(category_by_item) == out["item_j"].map(category_by_item)
    out["collision_group_size"] = out["collision_group_size"].fillna(0).astype(int)
    return out[
        [
            "dataset",
            "method",
            "pair_type",
            "item_i",
            "item_j",
            "sid_i",
            "sid_j",
            "same_sid",
            "popularity_i",
            "popularity_j",
            "popularity_bucket_i",
            "popularity_bucket_j",
            "co_count",
            "shares_user",
            "same_category",
            "collision_group_size",
        ]
    ]


def summarize_pairs(
    *,
    dataset: str,
    method: str,
    full_collision_groups: int,
    full_collision_items: int,
    collision_pairs_possible: int,
    pair_details: pd.DataFrame,
    cooccurrence_stats: dict[str, int],
) -> dict[str, Any]:
    rows: dict[str, Any] = {
        "dataset": dataset,
        "method": method,
        "full_collision_groups": full_collision_groups,
        "full_collision_items": full_collision_items,
        "collision_pairs_possible": collision_pairs_possible,
        **cooccurrence_stats,
    }
    for pair_type in ["collision", "matched_noncollision"]:
        subset = pair_details[pair_details["pair_type"] == pair_type]
        prefix = "collision" if pair_type == "collision" else "matched"
        rows[f"{prefix}_pairs_sampled"] = int(len(subset))
        rows[f"{prefix}_shares_user_rate"] = float(subset["shares_user"].mean()) if len(subset) else 0.0
        rows[f"{prefix}_mean_co_count"] = float(subset["co_count"].mean()) if len(subset) else 0.0
        rows[f"{prefix}_same_category_rate"] = float(subset["same_category"].mean()) if len(subset) else 0.0
    matched_rate = rows["matched_shares_user_rate"]
    rows["interaction_qualified_collision_lift"] = (
        float(rows["collision_shares_user_rate"] / matched_rate) if matched_rate > 0 else math.nan
    )
    rows["status"] = "no_full_sid_collisions" if collision_pairs_possible == 0 else "ok"
    return rows


def run_probe(
    sid_paths: list[Path],
    item_metadata_path: Path,
    interactions_path: Path,
    output_dir: Path,
    *,
    max_collision_pairs: int,
    max_pair_events: int,
    max_user_items: int,
    popularity_bins: int,
    seed: int,
    methods: set[str] | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sid = pd.concat([read_table(path) for path in sid_paths], ignore_index=True)
    if methods:
        sid = sid[sid["method"].isin(methods)].copy()
        if sid.empty:
            raise ValueError(f"no SID rows left after method filter: {sorted(methods)}")
    item_metadata = read_table(item_metadata_path)
    interactions = read_table(interactions_path)
    validate_inputs(sid, item_metadata, interactions, allow_partial_coverage=False)

    rng = np.random.default_rng(seed)
    detail_frames: list[pd.DataFrame] = []
    summary_rows: list[dict[str, Any]] = []

    category_col = "category" if "category" in item_metadata.columns else None
    category_by_item = (
        item_metadata.set_index("item_id")[category_col].to_dict() if category_col is not None else {}
    )

    group_cols = ["dataset", "method"] if "dataset" in sid.columns else ["method"]
    for group_key, group in sid.groupby(group_cols, sort=True):
        if not isinstance(group_key, tuple):
            group_key = (group_key,)
        key_values = dict(zip(group_cols, group_key))
        method = str(key_values["method"])
        dataset = str(key_values.get("dataset", ""))
        item_ids = set(group["item_id"].astype(int))
        sid_by_item = group.set_index("item_id")["sid"].astype(str).to_dict()
        pop = build_popularity_frame(item_ids, interactions, popularity_bins)
        cooccurrence, co_stats = bounded_cooccurrence_pairs(
            interactions,
            item_ids,
            max_user_items=max_user_items,
            max_pair_events=max_pair_events,
        )
        sid_sizes = group.groupby("sid").size()
        collision_pairs, collision_pairs_possible = sample_collision_pairs(group, max_collision_pairs, rng)
        matched_pairs = sample_matched_noncollision_pairs(
            collision_pairs,
            pop,
            sid_by_item,
            rng,
            attempts_per_pair=25,
        )
        annotated = pd.concat(
            [
                annotate_pairs(
                    collision_pairs,
                    pair_type="collision",
                    method=method,
                    dataset=dataset,
                    sid_by_item=sid_by_item,
                    pop=pop,
                    cooccurrence=cooccurrence,
                    category_by_item=category_by_item,
                ),
                annotate_pairs(
                    matched_pairs,
                    pair_type="matched_noncollision",
                    method=method,
                    dataset=dataset,
                    sid_by_item=sid_by_item,
                    pop=pop,
                    cooccurrence=cooccurrence,
                    category_by_item=category_by_item,
                ),
            ],
            ignore_index=True,
        )
        detail_frames.append(annotated)
        summary_rows.append(
            summarize_pairs(
                dataset=dataset,
                method=method,
                full_collision_groups=int((sid_sizes > 1).sum()),
                full_collision_items=int(sid_sizes[sid_sizes > 1].sum()),
                collision_pairs_possible=collision_pairs_possible,
                pair_details=annotated,
                cooccurrence_stats=co_stats,
            )
        )

    pair_details = pd.concat(detail_frames, ignore_index=True) if detail_frames else pd.DataFrame()
    summary = pd.DataFrame(summary_rows)
    pair_details.to_csv(output_dir / "qualified_collision_pairs.csv", index=False)
    summary.to_csv(output_dir / "qualified_collision_summary.csv", index=False)
    manifest = {
        "status": "passed",
        "sid_assignments": [str(path) for path in sid_paths],
        "item_metadata": str(item_metadata_path),
        "interactions": str(interactions_path),
        "output_dir": str(output_dir),
        "bounds": {
            "max_collision_pairs_per_method": max_collision_pairs,
            "max_pair_events": max_pair_events,
            "max_user_items": max_user_items,
            "popularity_bins": popularity_bins,
            "seed": seed,
        },
        "summary_rows": summary.to_dict(orient="records"),
    }
    (output_dir / "qualified_collision_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SIDInspector qualified collision controller.")
    parser.add_argument("--sid-assignments", type=Path, action="append", required=True)
    parser.add_argument("--item-metadata", type=Path, required=True)
    parser.add_argument("--interactions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--method", action="append", default=None, help="Optional method filter; repeatable.")
    parser.add_argument("--max-collision-pairs", type=int, default=50_000)
    parser.add_argument("--max-pair-events", type=int, default=500_000)
    parser.add_argument("--max-user-items", type=int, default=80)
    parser.add_argument("--popularity-bins", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    manifest = run_probe(
        sid_paths=args.sid_assignments,
        item_metadata_path=args.item_metadata,
        interactions_path=args.interactions,
        output_dir=args.output_dir,
        max_collision_pairs=args.max_collision_pairs,
        max_pair_events=args.max_pair_events,
        max_user_items=args.max_user_items,
        popularity_bins=args.popularity_bins,
        seed=args.seed,
        methods=set(args.method) if args.method else None,
    )
    print(json.dumps({"status": manifest["status"], "output_dir": manifest["output_dir"]}, indent=2))


if __name__ == "__main__":
    main()
