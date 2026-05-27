#!/usr/bin/env python3
"""Run a complete SIDInspector diagnostic pass on bundled toy data."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from minimal_adapter import normalize_sid_export
from sidinspector.metrics import alignment, collision, deployment_cost, head_tail_capacity, utilization, validate_inputs
from sidinspector.preflight import preflight_inputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run SIDInspector on the bundled toy data.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "examples" / "toy_output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sample_dir = Path(__file__).resolve().parent / "sample_data"
    out_dir = args.output_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    sid = normalize_sid_export(sample_dir / "sid_codes.csv", method="toy_tokenizer", dataset="toy")
    metadata = pd.read_csv(sample_dir / "item_metadata.csv")
    interactions = pd.read_csv(sample_dir / "interactions.csv")

    sid_path = out_dir / "sid_assignments.parquet"
    metadata_path = out_dir / "item_metadata.parquet"
    interactions_path = out_dir / "interactions.parquet"
    sid.to_parquet(sid_path, index=False)
    metadata.to_parquet(metadata_path, index=False)
    interactions.to_parquet(interactions_path, index=False)

    preflight = preflight_inputs(
        sid_path,
        metadata_path,
        interactions_path,
        run_metric_smoke=True,
        top_k=1,
        max_pair_events=100,
    )
    (out_dir / "preflight_summary.json").write_text(str(preflight) + "\n", encoding="utf-8")

    tables = {
        "coverage_report.csv": validate_inputs(sid, metadata, interactions),
        "d1_utilization.csv": utilization(sid),
        "d2_collision.csv": collision(sid, interactions),
        "d3_alignment.csv": alignment(sid, metadata, interactions, top_k=1, max_pair_events=100),
        "d4_head_tail.csv": head_tail_capacity(sid, interactions),
        "d5a_deployment_cost.csv": deployment_cost(sid),
    }
    for name, table in tables.items():
        table.to_csv(out_dir / name, index=False)

    print(f"Wrote SIDInspector toy diagnostic outputs to {out_dir}")
    print(tables["d5a_deployment_cost.csv"].to_string(index=False))


if __name__ == "__main__":
    main()
