"""Normalize LETTER-style JSON semantic-ID artifacts.

LETTER and LC-Rec style releases store item indices as a JSON mapping from
dense item ids to token strings such as ``<a_128>``. This adapter preserves the
released item keys and converts each token position into a SID level.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

from sidinspector.interface import validate_columns


TOKEN_RE = re.compile(r"<[A-Za-z]+_(-?\d+)>")


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _parse_token(token: Any) -> int:
    if isinstance(token, int):
        return token
    text = str(token)
    match = TOKEN_RE.fullmatch(text)
    if match:
        return int(match.group(1))
    try:
        return int(text)
    except ValueError as exc:
        raise ValueError(f"Cannot parse SID token: {token!r}") from exc


def normalize_letter_index(index_path: Path, method: str, dataset: str) -> pd.DataFrame:
    mapping = _read_json(index_path)
    if not isinstance(mapping, dict):
        raise ValueError(f"Expected JSON object in {index_path}")

    rows: list[dict[str, Any]] = []
    expected_depth: int | None = None
    for raw_item_id, raw_codes in sorted(mapping.items(), key=lambda kv: int(kv[0])):
        if not isinstance(raw_codes, list) or not raw_codes:
            raise ValueError(f"Item {raw_item_id!r} has invalid SID code list")
        codes = [_parse_token(token) for token in raw_codes]
        if expected_depth is None:
            expected_depth = len(codes)
        elif len(codes) != expected_depth:
            raise ValueError(f"Inconsistent SID depth for item {raw_item_id!r}")
        row: dict[str, Any] = {
            "item_id": int(raw_item_id),
            "method": method,
            "dataset": dataset,
        }
        for level, code in enumerate(codes):
            row[f"sid_level_{level}"] = code
        row["sid"] = "-".join(str(code) for code in codes)
        rows.append(row)

    out = pd.DataFrame(rows)
    validate_columns("sid_assignments", out.columns)
    return out


def normalize_letter_metadata(item_path: Path, dataset: str) -> pd.DataFrame:
    mapping = _read_json(item_path)
    if not isinstance(mapping, dict):
        raise ValueError(f"Expected JSON object in {item_path}")

    rows: list[dict[str, Any]] = []
    for raw_item_id, value in sorted(mapping.items(), key=lambda kv: int(kv[0])):
        if not isinstance(value, dict):
            value = {"raw": value}
        row = {"item_id": int(raw_item_id), "dataset": dataset}
        if "title" in value:
            row["title"] = value["title"]
        if "brand" in value:
            row["brand"] = value["brand"]
        categories = value.get("categories") or value.get("category")
        if categories:
            if isinstance(categories, list):
                row["category"] = " > ".join(str(part) for part in categories)
            else:
                row["category"] = str(categories)
        rows.append(row)

    out = pd.DataFrame(rows)
    if "category" not in out.columns:
        out["category"] = "unknown"
    else:
        out["category"] = out["category"].fillna("unknown")
    validate_columns("item_metadata", out.columns)
    return out


def normalize_letter_interactions(inter_path: Path, dataset: str, split: str = "train") -> pd.DataFrame:
    mapping = _read_json(inter_path)
    if not isinstance(mapping, dict):
        raise ValueError(f"Expected JSON object in {inter_path}")

    rows: list[dict[str, Any]] = []
    for raw_user_id, raw_items in sorted(mapping.items(), key=lambda kv: int(kv[0])):
        if not isinstance(raw_items, list):
            raise ValueError(f"User {raw_user_id!r} has invalid interaction list")
        for position, raw_item_id in enumerate(raw_items):
            rows.append(
                {
                    "user_id": int(raw_user_id),
                    "item_id": int(raw_item_id),
                    "dataset": dataset,
                    "split": split,
                    "position": position,
                }
            )
    out = pd.DataFrame(rows)
    validate_columns("interactions", out.columns)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize LETTER-style JSON SID artifacts.")
    parser.add_argument("--index-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="unknown")
    parser.add_argument("--method", default="letter")
    parser.add_argument("--item-json", type=Path, default=None)
    parser.add_argument("--inter-json", type=Path, default=None)
    parser.add_argument("--interaction-split", default="train")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    sid_assignments = normalize_letter_index(args.index_json, method=args.method, dataset=args.dataset_name)
    sid_assignments.to_parquet(args.output_dir / "sid_assignments.parquet", index=False)

    if args.item_json:
        item_metadata = normalize_letter_metadata(args.item_json, dataset=args.dataset_name)
        item_metadata.to_parquet(args.output_dir / "item_metadata.parquet", index=False)
    if args.inter_json:
        interactions = normalize_letter_interactions(args.inter_json, dataset=args.dataset_name, split=args.interaction_split)
        interactions.to_parquet(args.output_dir / "interactions.parquet", index=False)


if __name__ == "__main__":
    main()
