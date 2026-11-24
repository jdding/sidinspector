"""Standard-library-only D1--D6 diagnostic engine for SIDInspector.

This module mirrors the mathematical definitions in :mod:`sidinspector.metrics`
and :mod:`sidinspector.churn` without requiring pandas, numpy, or pyarrow. It
powers the zero-install browser workbench (Pyodide), the local HTTP demo, and
lightweight CSV audits.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import io
import math
from pathlib import Path
from typing import Any


def _entropy_from_counts(counts: list[int]) -> float:
    total = sum(counts)
    if total <= 0:
        return 0.0
    entropy = 0.0
    for count in counts:
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    return entropy


def _gini_from_counts(counts: list[int]) -> float:
    ordered = sorted(float(c) for c in counts if c > 0)
    total = sum(ordered)
    n = len(ordered)
    if n == 0 or total <= 0.0:
        return 0.0
    weighted = sum((idx + 1) * val for idx, val in enumerate(ordered))
    return (2.0 * weighted) / (n * total) - (n + 1.0) / n


def _detect_level_columns(fieldnames: list[str]) -> list[str]:
    sid_level = [c for c in fieldnames if c.startswith("sid_level_")]
    if sid_level:
        return sorted(sid_level, key=lambda c: int(c.rsplit("_", 1)[1]))
    sid_short = [c for c in fieldnames if c.startswith("sid_") and c != "sid" and c.rsplit("_", 1)[1].isdigit()]
    if sid_short:
        return sorted(sid_short, key=lambda c: int(c.rsplit("_", 1)[1]))
    return []


def parse_sid_csv_text(text: str, max_rows: int = 50_000) -> dict[str, Any]:
    """Parse an item-to-SID CSV string into normalized records."""
    reader = csv.DictReader(io.StringIO(text.strip()))
    if not reader.fieldnames:
        raise ValueError("SID CSV is empty or missing a header row.")
    fieldnames = [name.strip() for name in reader.fieldnames if name is not None]
    if "item_id" not in fieldnames:
        raise ValueError("SID CSV must include an `item_id` column.")

    level_cols = _detect_level_columns(fieldnames)
    has_sid_string = "sid" in fieldnames
    if not level_cols and not has_sid_string:
        raise ValueError(
            "SID CSV must include level columns (`sid_0,sid_1,...` or `sid_level_0,...`) or a `sid` column."
        )

    rows: list[dict[str, Any]] = []
    seen_items: set[str] = set()
    expected_depth: int | None = None

    for idx, raw in enumerate(reader, start=2):
        if len(rows) >= max_rows:
            raise ValueError(f"Row limit exceeded ({max_rows} items).")
        cleaned = {k.strip(): (v.strip() if isinstance(v, str) else "") for k, v in raw.items() if k is not None}
        item_id = cleaned.get("item_id", "")
        if not item_id:
            raise ValueError(f"Line {idx}: empty item_id.")
        if item_id in seen_items:
            raise ValueError(f"Line {idx}: duplicate item_id `{item_id}`.")
        seen_items.add(item_id)

        if level_cols:
            levels = []
            for col in level_cols:
                val = cleaned.get(col, "")
                if val == "":
                    raise ValueError(f"Line {idx}: missing value in `{col}` for item `{item_id}`.")
                levels.append(val)
        else:
            raw_sid = cleaned.get("sid", "")
            if not raw_sid:
                raise ValueError(f"Line {idx}: empty `sid` for item `{item_id}`.")
            sep = "-" if "-" in raw_sid else ("|" if "|" in raw_sid else ",")
            levels = [part.strip() for part in raw_sid.split(sep) if part.strip() != ""]

        if expected_depth is None:
            expected_depth = len(levels)
        elif len(levels) != expected_depth:
            raise ValueError(
                f"Line {idx}: inconsistent SID depth ({len(levels)} vs expected {expected_depth}) for item `{item_id}`."
            )

        sid_str = "-".join(levels)
        rows.append(
            {
                "item_id": item_id,
                "levels": levels,
                "sid": sid_str,
                "dataset": cleaned.get("dataset") or "user_dataset",
                "method": cleaned.get("method") or "user_mapping",
            }
        )

    if not rows:
        raise ValueError("SID CSV contains a header but zero item rows.")

    return {
        "rows": rows,
        "depth": expected_depth or 0,
        "level_names": [f"sid_level_{i}" for i in range(expected_depth or 0)],
    }


def parse_interactions_csv_text(text: str, max_rows: int = 200_000) -> list[dict[str, str]]:
    """Parse an optional interactions CSV string (`user_id,item_id[,split]`)."""
    stripped = text.strip()
    if not stripped:
        return []
    reader = csv.DictReader(io.StringIO(stripped))
    if not reader.fieldnames:
        return []
    fieldnames = [name.strip() for name in reader.fieldnames if name is not None]
    if "user_id" not in fieldnames or "item_id" not in fieldnames:
        raise ValueError("Interactions CSV must include `user_id` and `item_id` columns.")
    events: list[dict[str, str]] = []
    for idx, raw in enumerate(reader, start=2):
        if len(events) >= max_rows:
            raise ValueError(f"Interaction row limit exceeded ({max_rows} rows).")
        cleaned = {k.strip(): (v.strip() if isinstance(v, str) else "") for k, v in raw.items() if k is not None}
        if not cleaned.get("user_id") or not cleaned.get("item_id"):
            raise ValueError(f"Interactions line {idx}: missing user_id or item_id.")
        events.append(
            {
                "user_id": cleaned["user_id"],
                "item_id": cleaned["item_id"],
                "split": cleaned.get("split", ""),
            }
        )
    return events


def parse_metadata_csv_text(text: str, max_rows: int = 50_000) -> dict[str, dict[str, str]]:
    """Parse an optional item metadata CSV string (`item_id[,category,title]`)."""
    stripped = text.strip()
    if not stripped:
        return {}
    reader = csv.DictReader(io.StringIO(stripped))
    if not reader.fieldnames:
        return {}
    fieldnames = [name.strip() for name in reader.fieldnames if name is not None]
    if "item_id" not in fieldnames:
        raise ValueError("Metadata CSV must include an `item_id` column.")
    meta: dict[str, dict[str, str]] = {}
    for idx, raw in enumerate(reader, start=2):
        if len(meta) >= max_rows:
            raise ValueError(f"Metadata row limit exceeded ({max_rows} rows).")
        cleaned = {k.strip(): (v.strip() if isinstance(v, str) else "") for k, v in raw.items() if k is not None}
        item_id = cleaned.get("item_id", "")
        if not item_id:
            raise ValueError(f"Metadata line {idx}: empty item_id.")
        if item_id in meta:
            raise ValueError(f"Metadata line {idx}: duplicate item_id `{item_id}`.")
        meta[item_id] = {
            "category": cleaned.get("category", ""),
            "title": cleaned.get("title", ""),
        }
    return meta


def _sort_item_key(item_id: str) -> tuple[int, int | str]:
    try:
        return (0, int(item_id))
    except ValueError:
        return (1, item_id)


_UNSPLIT_LABELS = {"", "all", "full", "reference"}


def _select_train_events(interactions: list[dict[str, str]]) -> tuple[list[dict[str, str]], str]:
    """Select training interactions without ever falling back to held-out valid/test splits."""
    if not interactions:
        return [], "none"
    non_empty_splits = {
        e.get("split", "").strip().lower()
        for e in interactions
        if e.get("split", "").strip()
    }
    if not non_empty_splits or non_empty_splits <= _UNSPLIT_LABELS:
        return interactions, "unsplit_reference"
    train = [e for e in interactions if e.get("split", "").strip().lower() == "train"]
    if not train:
        labels = ", ".join(sorted(non_empty_splits))
        raise ValueError(
            f"Interactions declare explicit split labels ({labels}) with zero 'train' rows; "
            "held-out splits (valid/test) cannot be used for training-only D3/D4 diagnostics."
        )
    return train, "train_only"


def run_mapping_diagnostics(
    sid_rows: list[dict[str, Any]],
    interactions: list[dict[str, str]] | None = None,
    metadata: dict[str, dict[str, str]] | None = None,
    *,
    d3_top_k: int = 20,
    d3_max_pair_events: int = 2_000_000,
    d3_max_user_items: int = 200,
) -> dict[str, Any]:
    """Compute D1--D5 diagnostics, prefix/alias inspectors, and triage signals."""
    interactions = interactions or []
    metadata = metadata or {}
    if not sid_rows:
        raise ValueError("At least one SID assignment row is required.")

    depth = len(sid_rows[0]["levels"])
    n_items = len(sid_rows)
    item_map = {row["item_id"]: row for row in sid_rows}
    sid_item_ids = set(item_map)

    # Coverage summary
    meta_ids = set(metadata)
    inter_ids = {e["item_id"] for e in interactions}
    coverage = {
        "sid_items": n_items,
        "metadata_items": len(meta_ids),
        "interaction_items": len(inter_ids),
        "metadata_without_sid": len(meta_ids - sid_item_ids) if meta_ids else 0,
        "interaction_without_sid": len(inter_ids - sid_item_ids) if inter_ids else 0,
        "sid_without_metadata": len(sid_item_ids - meta_ids) if meta_ids else 0,
        "sid_depth": depth,
    }

    # Train interaction popularity (strict train-only when split labels are declared)
    train, split_mode = _select_train_events(interactions)
    coverage["interaction_split_mode"] = split_mode
    coverage["train_events_used"] = len(train)
    pop_counts: Counter[str] = Counter()
    for ev in train:
        if ev["item_id"] in sid_item_ids:
            pop_counts[ev["item_id"]] += 1

    # D1: Utilization per level
    d1_rows = []
    for level_idx in range(depth):
        counts = Counter(row["levels"][level_idx] for row in sid_rows)
        val_counts = list(counts.values())
        numeric_codes = []
        for code in counts:
            try:
                numeric_codes.append(int(code))
            except ValueError:
                pass
        d1_rows.append(
            {
                "level": f"sid_level_{level_idx}",
                "level_index": level_idx,
                "items": n_items,
                "unique_codes": len(counts),
                "entropy": _entropy_from_counts(val_counts),
                "gini": _gini_from_counts(val_counts),
                "max_code": max(numeric_codes) if numeric_codes else None,
            }
        )

    # D2: Aliasing / Collision profile by depth
    full_groups: dict[str, list[str]] = defaultdict(list)
    for row in sid_rows:
        full_groups[row["sid"]].append(row["item_id"])
    full_collision_groups = [sid for sid, members in full_groups.items() if len(members) > 1]
    full_collision_item_set = {
        item_id for sid in full_collision_groups for item_id in full_groups[sid]
    }
    full_collision_items = len(full_collision_item_set)
    full_collision_rate = full_collision_items / n_items
    mean_pop_full = (
        sum(pop_counts.get(i, 0) for i in full_collision_item_set) / full_collision_items
        if full_collision_items
        else 0.0
    )

    d2_rows = []
    prefix_counts_by_depth: list[int] = []
    for d in range(1, depth + 1):
        pref_groups: dict[str, list[str]] = defaultdict(list)
        for row in sid_rows:
            pref = "-".join(row["levels"][:d])
            pref_groups[pref].append(row["item_id"])
        prefix_counts_by_depth.append(len(pref_groups))
        pref_col_groups = [p for p, members in pref_groups.items() if len(members) > 1]
        pref_col_items_set = {i for p in pref_col_groups for i in pref_groups[p]}
        pref_col_items = len(pref_col_items_set)
        mean_pop_pref = (
            sum(pop_counts.get(i, 0) for i in pref_col_items_set) / pref_col_items
            if pref_col_items
            else 0.0
        )
        d2_rows.append(
            {
                "prefix_depth": d,
                "active_prefixes": len(pref_groups),
                "full_collision_groups": len(full_collision_groups),
                "full_collision_items": full_collision_items,
                "full_collision_rate": full_collision_rate,
                "prefix_collision_groups": len(pref_col_groups),
                "prefix_collision_items": pref_col_items,
                "prefix_collision_rate": pref_col_items / n_items,
                "mean_popularity_full_collision_items": mean_pop_full,
                "mean_popularity_prefix_collision_items": mean_pop_pref,
            }
        )

    # Category purity at level 0
    has_category = bool(metadata) and all(bool(metadata.get(r["item_id"], {}).get("category")) for r in sid_rows)
    level0_purity: float | None = None
    level0_non_singleton = 0
    if has_category:
        buckets: dict[str, list[str]] = defaultdict(list)
        for row in sid_rows:
            buckets[row["levels"][0]].append(metadata[row["item_id"]]["category"])
        purities = []
        for cats in buckets.values():
            if len(cats) <= 1:
                continue
            top = Counter(cats).most_common(1)[0][1]
            purities.append(top / len(cats))
        level0_non_singleton = len(purities)
        level0_purity = (sum(purities) / len(purities)) if purities else 1.0

    # D3: Collaborative neighborhood alignment (exact match with metrics.py)
    user_items: dict[str, set[str]] = defaultdict(set)
    for ev in train:
        if ev["item_id"] in sid_item_ids:
            user_items[ev["user_id"]].add(ev["item_id"])

    eligible_users = sorted(
        (u for u, items in user_items.items() if 2 <= len(items) <= d3_max_user_items)
    )
    selected_users: list[str] = []
    pair_events = 0
    for u in eligible_users:
        sz = len(user_items[u])
        u_pairs = sz * (sz - 1) // 2
        if selected_users and pair_events + u_pairs > d3_max_pair_events:
            break
        selected_users.append(u)
        pair_events += u_pairs

    co_counts: Counter[tuple[str, str]] = Counter()
    for u in selected_users:
        items_sorted = sorted(user_items[u], key=_sort_item_key)
        for idx_i in range(len(items_sorted)):
            for idx_j in range(idx_i + 1, len(items_sorted)):
                co_counts[(items_sorted[idx_i], items_sorted[idx_j])] += 1

    directed_by_item: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for (i_id, j_id), cnt in co_counts.items():
        directed_by_item[i_id].append((j_id, cnt))
        directed_by_item[j_id].append((i_id, cnt))

    retained_edges: list[tuple[str, str, int]] = []
    for i_id in sorted(directed_by_item, key=_sort_item_key):
        neighbors = sorted(
            directed_by_item[i_id],
            key=lambda pair: (-pair[1], _sort_item_key(pair[0])),
        )[:d3_top_k]
        for n_id, cnt in neighbors:
            retained_edges.append((i_id, n_id, cnt))

    collab_items = len({edge[0] for edge in retained_edges})
    d3_rows = []
    for d in range(1, depth + 1):
        prefix_of = {row["item_id"]: "-".join(row["levels"][:d]) for row in sid_rows}
        if not retained_edges:
            d3_rows.append(
                {
                    "prefix_depth": d,
                    "users_used": len(selected_users),
                    "pair_events": pair_events,
                    "collab_items": collab_items,
                    "retained_edges": 0,
                    "weighted_collab_prefix_recall": 0.0,
                    "mean_collab_prefix_recall": 0.0,
                    "freq_weighted_collab_prefix_recall": 0.0,
                    "level0_category_purity_mean": level0_purity,
                    "level0_non_singleton_buckets": level0_non_singleton,
                }
            )
            continue

        hits_total = 0
        freq_hits = 0
        freq_total = 0
        per_item_hits: dict[str, list[int]] = defaultdict(list)
        for src, dst, cnt in retained_edges:
            same = 1 if prefix_of[src] == prefix_of[dst] else 0
            hits_total += same
            freq_hits += same * cnt
            freq_total += cnt
            per_item_hits[src].append(same)

        item_recalls = [sum(vals) / len(vals) for vals in per_item_hits.values()]
        d3_rows.append(
            {
                "prefix_depth": d,
                "users_used": len(selected_users),
                "pair_events": pair_events,
                "collab_items": collab_items,
                "retained_edges": len(retained_edges),
                "weighted_collab_prefix_recall": hits_total / len(retained_edges),
                "mean_collab_prefix_recall": sum(item_recalls) / len(item_recalls),
                "freq_weighted_collab_prefix_recall": (freq_hits / freq_total) if freq_total else 0.0,
                "level0_category_purity_mean": level0_purity,
                "level0_non_singleton_buckets": level0_non_singleton,
            }
        )

    # D4: Head/Mid/Tail popularity allocation + global singleton addressability
    observed_items = sorted(pop_counts.keys(), key=lambda iid: (pop_counts[iid], _sort_item_key(iid)))
    bucket_of: dict[str, str] = {}
    n_obs = len(observed_items)
    for rank_idx, iid in enumerate(observed_items, start=1):
        pct = rank_idx / n_obs
        if pct <= 1.0 / 3.0:
            bucket_of[iid] = "tail"
        elif pct <= 2.0 / 3.0:
            bucket_of[iid] = "mid"
        else:
            bucket_of[iid] = "head"
    for row in sid_rows:
        bucket_of.setdefault(row["item_id"], "tail")

    d4_rows = []
    for bucket in ("head", "mid", "tail"):
        members = [row for row in sid_rows if bucket_of[row["item_id"]] == bucket]
        if not members:
            continue
        unique_sids = len({row["sid"] for row in members})
        global_singletons = sum(1 for row in members if len(full_groups[row["sid"]]) == 1)
        lvl0_counts = list(Counter(row["levels"][0] for row in members).values())
        d4_rows.append(
            {
                "bucket": bucket,
                "items": len(members),
                "unique_sids": unique_sids,
                "sid_unique_ratio": unique_sids / len(members),
                "global_singleton_ratio": global_singletons / len(members),
                "level0_entropy": _entropy_from_counts(lvl0_counts),
            }
        )

    # D5: Structural cost
    unique_full_sids = len(full_groups)
    d5_summary = {
        "items": n_items,
        "sid_length": depth,
        "unique_sid": unique_full_sids,
        "duplicate_sid_rate": 1.0 - (unique_full_sids / n_items),
        "prefix_counts": "/".join(str(c) for c in prefix_counts_by_depth),
        "prefix_counts_list": prefix_counts_by_depth,
        "mean_branching_factor": [
            round(
                prefix_counts_by_depth[i] / (1 if i == 0 else max(1, prefix_counts_by_depth[i - 1])),
                3,
            )
            for i in range(depth)
        ],
    }

    # Interactive prefix inspector (depth 1 buckets)
    prefix_buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in sorted(sid_rows, key=lambda r: _sort_item_key(r["item_id"])):
        p1 = row["levels"][0]
        is_aliased = len(full_groups[row["sid"]]) > 1
        meta = metadata.get(row["item_id"], {})
        prefix_buckets[p1].append(
            {
                "item_id": row["item_id"],
                "sid": row["sid"],
                "category": meta.get("category") or "—",
                "title": meta.get("title") or row["item_id"],
                "train_events": pop_counts.get(row["item_id"], 0),
                "bucket": bucket_of[row["item_id"]],
                "aliased": is_aliased,
                "alias_group_size": len(full_groups[row["sid"]]),
            }
        )

    prefix_inspector = []
    for p1 in sorted(prefix_buckets, key=_sort_item_key):
        members = prefix_buckets[p1]
        cat_counts = Counter(m["category"] for m in members if m["category"] != "—")
        purity = (cat_counts.most_common(1)[0][1] / sum(cat_counts.values())) if cat_counts else None
        prefix_inspector.append(
            {
                "prefix": f"L0={p1}",
                "code": p1,
                "items": len(members),
                "unique_sids": len({m["sid"] for m in members}),
                "aliased_items": sum(1 for m in members if m["aliased"]),
                "dominant_category": cat_counts.most_common(1)[0][0] if cat_counts else "—",
                "category_purity": purity,
                "members": members[:40],
            }
        )

    alias_inspector = []
    for sid in sorted(full_collision_groups, key=lambda s: (-len(full_groups[s]), s))[:30]:
        members = []
        for iid in sorted(full_groups[sid], key=_sort_item_key):
            meta = metadata.get(iid, {})
            members.append(
                {
                    "item_id": iid,
                    "category": meta.get("category") or "—",
                    "title": meta.get("title") or iid,
                    "train_events": pop_counts.get(iid, 0),
                    "bucket": bucket_of[iid],
                }
            )
        alias_inspector.append({"sid": sid, "size": len(members), "members": members})

    # Triage guidance mapped directly to CIKM Table 1
    triage = build_triage_cards(d1_rows, d2_rows, d3_rows, d4_rows, d5_summary, has_interactions=bool(train))

    return {
        "coverage": coverage,
        "d1": d1_rows,
        "d2": d2_rows,
        "d3": d3_rows,
        "d4": d4_rows,
        "d5": d5_summary,
        "prefix_inspector": prefix_inspector,
        "alias_inspector": alias_inspector,
        "triage": triage,
    }


def compute_churn_pure(
    old_rows: list[dict[str, Any]],
    new_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Compute D6 paired refresh churn by prefix depth in pure Python."""
    old_map = {r["item_id"]: r["levels"] for r in old_rows}
    new_map = {r["item_id"]: r["levels"] for r in new_rows}
    common_ids = sorted(set(old_map) & set(new_map), key=_sort_item_key)
    max_depth = min(len(old_rows[0]["levels"]), len(new_rows[0]["levels"]))
    rows = []
    for d in range(1, max_depth + 1):
        changed = sum(1 for iid in common_ids if old_map[iid][:d] != new_map[iid][:d])
        old_prefs = Counter("-".join(lvls[:d]) for lvls in old_map.values())
        new_prefs = Counter("-".join(lvls[:d]) for lvls in new_map.values())
        old_col_items = sum(c for c in old_prefs.values() if c > 1)
        new_col_items = sum(c for c in new_prefs.values() if c > 1)
        rows.append(
            {
                "prefix_depth": d,
                "old_items": len(old_map),
                "new_items": len(new_map),
                "common_items": len(common_ids),
                "old_only_items": len(set(old_map) - set(new_map)),
                "new_only_items": len(set(new_map) - set(old_map)),
                "changed_items": changed,
                "stable_items": len(common_ids) - changed,
                "churn_rate_common": (changed / len(common_ids)) if common_ids else 0.0,
                "old_prefix_collision_rate": old_col_items / len(old_map) if old_map else 0.0,
                "new_prefix_collision_rate": new_col_items / len(new_map) if new_map else 0.0,
            }
        )
    return rows


def build_triage_cards(
    d1: list[dict[str, Any]],
    d2: list[dict[str, Any]],
    d3: list[dict[str, Any]],
    d4: list[dict[str, Any]],
    d5: dict[str, Any],
    *,
    has_interactions: bool,
) -> list[dict[str, str]]:
    """Map observed D1--D5 metrics to CIKM Table 1 inspection actions."""
    cards: list[dict[str, str]] = []
    max_gini = max((row["gini"] for row in d1), default=0.0)
    cards.append(
        {
            "probe": "D1 Utilization",
            "status": "watch" if max_gini > 0.35 else "ok",
            "signal": f"Level-0 uses {d1[0]['unique_codes']} symbols (H={d1[0]['entropy']:.2f} bits, max Gini={max_gini:.3f}).",
            "next_check": "Compare per-level occupied codes against intended codebook budgets and check for collapsed levels.",
        }
    )
    full_alias = d2[0]["full_collision_rate"]
    cards.append(
        {
            "probe": "D2 Aliasing",
            "status": "alert" if full_alias > 0.25 else ("watch" if full_alias > 0.0 else "ok"),
            "signal": f"Full-code aliasing = {full_alias:.3f} ({d2[0]['full_collision_items']} / {d5['items']} items in {d2[0]['full_collision_groups']} shared leaves).",
            "next_check": "Inspect alias groups by popularity and co-occurrence; shared leaves require an explicit downstream resolver."
            if full_alias > 0
            else "Every catalog item has a unique full code; verify prefix alignment separately.",
        }
    )
    if has_interactions and d3 and d3[0]["retained_edges"] > 0:
        d3_l1 = d3[0]["weighted_collab_prefix_recall"]
        cards.append(
            {
                "probe": "D3 Neighborhood alignment",
                "status": "watch" if d3_l1 < 0.15 else "ok",
                "signal": f"Depth-1 edge-micro recall = {d3_l1:.3f} across {d3[0]['retained_edges']} directed neighbor edges.",
                "next_check": "Compare against a same-dataset category-prefix control and run the fixed-reranker exposure probe if weak.",
            }
        )
    else:
        cards.append(
            {
                "probe": "D3 Neighborhood alignment",
                "status": "info",
                "signal": "No training interaction co-occurrence edges supplied.",
                "next_check": "Attach interactions.csv (`user_id,item_id,split`) to measure prefix co-occurrence recovery.",
            }
        )
    tail_row = next((r for r in d4 if r["bucket"] == "tail"), None)
    if tail_row:
        gap = tail_row["sid_unique_ratio"] - tail_row["global_singleton_ratio"]
        cards.append(
            {
                "probe": "D4 Popularity allocation",
                "status": "alert" if tail_row["global_singleton_ratio"] < 0.8 else ("watch" if gap > 0.05 else "ok"),
                "signal": (
                    f"Tail allocation = {tail_row['sid_unique_ratio']:.3f}; "
                    f"tail global singleton = {tail_row['global_singleton_ratio']:.3f}."
                ),
                "next_check": "Inspect cross-stratum collisions and compressed tail buckets before downstream training."
                if gap > 0.05 or tail_row["global_singleton_ratio"] < 0.8
                else "Head/mid/tail capacity allocation is balanced.",
            }
        )
    cards.append(
        {
            "probe": "D5 Structural cost",
            "status": "ok",
            "signal": f"Depth {d5['sid_length']}, {d5['unique_sid']} unique leaves, active prefixes {d5['prefix_counts']}.",
            "next_check": "Profile trie fan-out and constrained-decoding latency on your target serving stack.",
        }
    )
    return cards


def load_csv_bundle(
    sid_csv: Path,
    interactions_csv: Path | None = None,
    metadata_csv: Path | None = None,
) -> dict[str, Any]:
    """Load CSV files from disk and execute pure-Python D1--D5 diagnostics."""
    parsed = parse_sid_csv_text(sid_csv.read_text(encoding="utf-8"))
    interactions = (
        parse_interactions_csv_text(interactions_csv.read_text(encoding="utf-8"))
        if interactions_csv and interactions_csv.is_file()
        else []
    )
    metadata = (
        parse_metadata_csv_text(metadata_csv.read_text(encoding="utf-8"))
        if metadata_csv and metadata_csv.is_file()
        else {}
    )
    return run_mapping_diagnostics(parsed["rows"], interactions=interactions, metadata=metadata)
