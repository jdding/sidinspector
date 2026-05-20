#!/usr/bin/env python3
"""Bounded local preflight for AUDIT-SID metric-runner inputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from audit_sid.interface import CONTRACTS, validate_columns
from audit_sid.metrics import alignment, collision, deployment_cost, head_tail_capacity, validate_inputs


def read_table(path: Path) -> pd.DataFrame:
    """Read a small local table format supported by the preflight script."""

    suffix = path.suffix.lower()
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".json", ".jsonl", ".ndjson"}:
        lines = suffix in {".jsonl", ".ndjson"}
        return pd.read_json(path, lines=lines)
    raise ValueError(f"unsupported table format for {path}; expected parquet, csv, json, or jsonl")


def _table_summary(name: str, path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    contract = CONTRACTS[name]
    return {
        "path": str(path),
        "rows": int(len(frame)),
        "columns": list(frame.columns),
        "required_columns": list(contract.required_columns),
        "optional_columns_present": [col for col in contract.optional_columns if col in frame.columns],
    }


def _key_cols(frame: pd.DataFrame) -> list[str]:
    return ["dataset", "method"] if "dataset" in frame.columns else ["method"]


def _select_row(frame: pd.DataFrame, key_values: dict[str, Any]) -> pd.Series | None:
    selected = frame
    for col, value in key_values.items():
        if col in selected.columns:
            selected = selected[selected[col] == value]
    if selected.empty:
        return None
    return selected.iloc[0]


def _d4_bucket_map(d4: pd.DataFrame, key_values: dict[str, Any]) -> dict[str, float]:
    selected = d4
    for col, value in key_values.items():
        if col in selected.columns:
            selected = selected[selected[col] == value]
    return {str(row["bucket"]): float(row["sid_unique_ratio"]) for _, row in selected.iterrows()}


def build_metric_smoke_summary(
    sid: pd.DataFrame,
    item_metadata: pd.DataFrame,
    interactions: pd.DataFrame,
    top_k: int,
    max_pair_events: int,
    max_user_items: int,
) -> list[dict[str, Any]]:
    """Run bounded D1-D5a smoke metrics and return compact finding rows."""

    d2 = collision(sid, interactions)
    d3 = alignment(
        sid,
        item_metadata,
        interactions,
        top_k=top_k,
        max_pair_events=max_pair_events,
        max_user_items=max_user_items,
    )
    d4 = head_tail_capacity(sid, interactions)
    d5 = deployment_cost(sid)

    rows: list[dict[str, Any]] = []
    for _, d5_row in d5.iterrows():
        keys = {col: d5_row[col] for col in _key_cols(d5)}
        d2_row = _select_row(d2, keys)
        d3_depth1 = _select_row(d3[d3["prefix_depth"] == 1], keys)
        d4_buckets = _d4_bucket_map(d4, keys)
        rows.append(
            {
                **keys,
                "sid_length": int(d5_row["sid_length"]),
                "unique_sid": int(d5_row["unique_sid"]),
                "duplicate_sid_rate": float(d5_row["duplicate_sid_rate"]),
                "prefix_counts": str(d5_row["prefix_counts"]),
                "full_collision_rate": float(d2_row["full_collision_rate"]) if d2_row is not None else None,
                "d3_depth1_weighted_collab_recall": float(d3_depth1["weighted_collab_prefix_recall"])
                if d3_depth1 is not None
                else None,
                "d3_depth1_mean_collab_recall": float(d3_depth1["mean_collab_prefix_recall"])
                if d3_depth1 is not None
                else None,
                "d4_head_sid_unique_ratio": d4_buckets.get("head"),
                "d4_mid_sid_unique_ratio": d4_buckets.get("mid"),
                "d4_tail_sid_unique_ratio": d4_buckets.get("tail"),
            }
        )
    return rows


def preflight_inputs(
    sid_assignments: Path,
    item_metadata: Path,
    interactions: Path,
    *,
    allow_partial_coverage: bool = False,
    run_metric_smoke: bool = False,
    max_metric_items: int = 50_000,
    top_k: int = 5,
    max_pair_events: int = 10_000,
    max_user_items: int = 50,
) -> dict[str, Any]:
    """Validate AUDIT-SID input contracts and optionally run bounded metrics."""

    paths = {
        "sid_assignments": sid_assignments,
        "item_metadata": item_metadata,
        "interactions": interactions,
    }
    tables = {name: read_table(path) for name, path in paths.items()}

    for name, frame in tables.items():
        validate_columns(name, frame.columns)
        if frame.empty:
            raise ValueError(f"{name} is empty")

    coverage = validate_inputs(
        tables["sid_assignments"],
        tables["item_metadata"],
        tables["interactions"],
        allow_partial_coverage=allow_partial_coverage,
    )
    result: dict[str, Any] = {
        "status": "passed",
        "tables": {name: _table_summary(name, paths[name], frame) for name, frame in tables.items()},
        "coverage": coverage.to_dict(orient="records"),
        "bounds": {
            "run_metric_smoke": run_metric_smoke,
            "max_metric_items": max_metric_items,
            "d3_top_k": top_k,
            "d3_max_pair_events": max_pair_events,
            "d3_max_user_items": max_user_items,
        },
    }

    if run_metric_smoke:
        sid_rows = len(tables["sid_assignments"])
        if sid_rows > max_metric_items:
            raise ValueError(
                f"metric smoke is bounded to {max_metric_items} SID rows; got {sid_rows}. "
                "Raise --max-metric-items only for an intentional local run."
            )
        result["metric_smoke_summary"] = build_metric_smoke_summary(
            tables["sid_assignments"],
            tables["item_metadata"],
            tables["interactions"],
            top_k=top_k,
            max_pair_events=max_pair_events,
            max_user_items=max_user_items,
        )

    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate sid_assignments/item_metadata/interactions contract before running AUDIT-SID metrics. "
            "Optionally emits a bounded D1-D5a JSON smoke summary for local follow-up experiments."
        )
    )
    parser.add_argument("--sid-assignments", type=Path, required=True)
    parser.add_argument("--item-metadata", type=Path, required=True)
    parser.add_argument("--interactions", type=Path, required=True)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--allow-partial-coverage", action="store_true")
    parser.add_argument("--run-metric-smoke", action="store_true")
    parser.add_argument("--max-metric-items", type=int, default=50_000)
    parser.add_argument("--d3-top-k", type=int, default=5)
    parser.add_argument("--d3-max-pair-events", type=int, default=10_000)
    parser.add_argument("--d3-max-user-items", type=int, default=50)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    result = preflight_inputs(
        args.sid_assignments,
        args.item_metadata,
        args.interactions,
        allow_partial_coverage=args.allow_partial_coverage,
        run_metric_smoke=args.run_metric_smoke,
        max_metric_items=args.max_metric_items,
        top_k=args.d3_top_k,
        max_pair_events=args.d3_max_pair_events,
        max_user_items=args.d3_max_user_items,
    )
    payload = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
