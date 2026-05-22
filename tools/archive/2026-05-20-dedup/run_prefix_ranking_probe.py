#!/usr/bin/env python3
"""Bounded prefix-neighborhood ranking probe for D3 context.

This is intentionally not a generator evaluation. It asks whether a user's
training-item SID prefixes retrieve the held-out next item under a simple
popularity-tiebroken prefix-neighborhood rule.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd


def level_columns(frame: pd.DataFrame) -> list[str]:
    cols = [c for c in frame.columns if c.startswith("sid_level_")]
    return sorted(cols, key=lambda c: int(c.rsplit("_", 1)[1]))


def prefix_frame(sid: pd.DataFrame, depth: int) -> pd.DataFrame:
    levels = level_columns(sid)
    if depth < 1 or depth > len(levels):
        raise ValueError(f"depth={depth} incompatible with levels={levels}")
    out = sid[["item_id", "method", "dataset", *levels[:depth]]].copy()
    out["prefix"] = out[levels[:depth]].astype(str).agg("-".join, axis=1)
    return out[["item_id", "method", "dataset", "prefix"]]


def topk_hit(
    prefixes: list[str],
    train_items: set[int],
    target: int,
    prefix_to_items: dict[str, list[int]],
    item_pop: dict[int, int],
    k: int,
) -> tuple[int, int]:
    scores: Counter[int] = Counter()
    for prefix in prefixes:
        for item in prefix_to_items.get(prefix, []):
            if item not in train_items:
                scores[item] += 1
    if not scores:
        return 0, 0
    ranked = sorted(scores, key=lambda item: (-scores[item], -item_pop.get(item, 0), item))[:k]
    return int(target in ranked), len(scores)


def evaluate(
    sid: pd.DataFrame,
    interactions: pd.DataFrame,
    *,
    depth: int,
    k: int,
    eval_split: str,
    max_users: int,
) -> pd.DataFrame:
    pref = prefix_frame(sid, depth)
    item_pop = interactions[interactions["split"] == "train"]["item_id"].value_counts().astype(int).to_dict()
    train_by_user = (
        interactions[interactions["split"] == "train"]
        .sort_values(["user_id", "timestamp"])
        .groupby("user_id")["item_id"]
        .apply(list)
        .to_dict()
    )
    eval_targets = (
        interactions[interactions["split"] == eval_split]
        .sort_values(["user_id", "timestamp"])
        .groupby("user_id")["item_id"]
        .first()
    )
    users = [u for u in eval_targets.index.tolist() if u in train_by_user]
    if max_users > 0:
        users = users[:max_users]

    rows = []
    for (dataset, method), method_pref in pref.groupby(["dataset", "method"], sort=True):
        item_to_prefix = dict(zip(method_pref["item_id"].astype(int), method_pref["prefix"].astype(str)))
        prefix_to_items: dict[str, list[int]] = defaultdict(list)
        for item, prefix in item_to_prefix.items():
            prefix_to_items[prefix].append(item)
        hits = 0
        covered = 0
        candidate_sizes = []
        for user in users:
            train_items = [int(i) for i in train_by_user[user] if int(i) in item_to_prefix]
            target = int(eval_targets.loc[user])
            if not train_items or target not in item_to_prefix:
                continue
            user_prefixes = [item_to_prefix[i] for i in train_items]
            hit, n_candidates = topk_hit(user_prefixes, set(train_items), target, prefix_to_items, item_pop, k)
            hits += hit
            covered += 1
            candidate_sizes.append(n_candidates)
        mean_candidates = sum(candidate_sizes) / len(candidate_sizes) if candidate_sizes else 0.0
        rows.append(
            {
                "dataset": dataset,
                "method": method,
                "prefix_depth": depth,
                "eval_split": eval_split,
                "users_evaluated": covered,
                "recall_at_k": hits / covered if covered else 0.0,
                "k": k,
                "mean_candidate_count": mean_candidates,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sid", type=Path, action="append", required=True, help="SID assignment parquet; can repeat")
    parser.add_argument("--interactions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--k", type=int, default=20)
    parser.add_argument("--eval-split", default="valid")
    parser.add_argument("--max-users", type=int, default=5000)
    args = parser.parse_args()

    sid = pd.concat([pd.read_parquet(p) for p in args.sid], ignore_index=True)
    interactions = pd.read_parquet(args.interactions)
    result = evaluate(
        sid,
        interactions,
        depth=args.depth,
        k=args.k,
        eval_split=args.eval_split,
        max_users=args.max_users,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output_dir / "prefix_ranking_probe.csv", index=False)
    (args.output_dir / "prefix_ranking_probe.md").write_text(result.to_markdown(index=False) + "\n", encoding="utf-8")
    manifest = {
        "sid_inputs": [str(p) for p in args.sid],
        "interactions": str(args.interactions),
        "depth": args.depth,
        "k": args.k,
        "eval_split": args.eval_split,
        "max_users": args.max_users,
        "claim_boundary": "prefix-neighborhood retrieval proxy; not Recall/NDCG from a trained generator",
    }
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(result.to_string(index=False))


if __name__ == "__main__":
    if sys.version_info < (3, 9):
        raise SystemExit("Python 3.9+ required")
    main()
