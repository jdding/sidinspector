#!/usr/bin/env python3
"""Run a reviewer-facing SIDInspector quickstart on a small music-like export.

The script intentionally uses the public command-line path:
minimal adapter -> preflight -> D1-D5 metrics. It is a small usability example,
not paper-result reproduction.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "examples" / "reviewer_quickstart_data"
DEFAULT_OUT = ROOT / "examples" / "reviewer_quickstart_output"


def run(cmd: list[str]) -> None:
    print("+ " + " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the SIDInspector reviewer quickstart.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out = args.output_dir.resolve()
    normalized = out / "normalized"
    diagnostics = out / "diagnostics"
    normalized.mkdir(parents=True, exist_ok=True)
    diagnostics.mkdir(parents=True, exist_ok=True)

    run(
        [
            sys.executable,
            "examples/minimal_adapter.py",
            "--input-csv",
            str(DATA / "sid_codes.csv"),
            "--output-dir",
            str(normalized),
            "--method",
            "mini_music_export",
            "--dataset",
            "mini_music",
        ]
    )

    metadata_path = normalized / "item_metadata.parquet"
    interactions_path = normalized / "interactions.parquet"
    pd.read_csv(DATA / "item_metadata.csv").to_parquet(metadata_path, index=False)
    pd.read_csv(DATA / "interactions.csv").to_parquet(interactions_path, index=False)

    sid_path = normalized / "sid_assignments.parquet"
    preflight_json = out / "preflight_summary.json"
    run(
        [
            sys.executable,
            "-m",
            "sidinspector.preflight",
            "--sid-assignments",
            str(sid_path),
            "--item-metadata",
            str(metadata_path),
            "--interactions",
            str(interactions_path),
            "--output-json",
            str(preflight_json),
            "--run-metric-smoke",
            "--d3-top-k",
            "2",
            "--d3-max-pair-events",
            "1000",
        ]
    )

    run(
        [
            sys.executable,
            "-m",
            "sidinspector.metrics",
            "--sid-assignments",
            str(sid_path),
            "--item-metadata",
            str(metadata_path),
            "--interactions",
            str(interactions_path),
            "--output-dir",
            str(diagnostics),
            "--d3-top-k",
            "2",
            "--d3-max-pair-events",
            "1000",
        ]
    )

    d2 = pd.read_csv(diagnostics / "d2_collision.csv")
    d3 = pd.read_csv(diagnostics / "d3_alignment.csv")
    d5 = pd.read_csv(diagnostics / "d5a_deployment_cost.csv")
    d2_depth3 = d2[d2["prefix_depth"] == 3].iloc[0]
    d3_depth1 = d3[d3["prefix_depth"] == 1].iloc[0]
    d5_row = d5.iloc[0]

    print("\nReviewer quickstart summary")
    print(f"- preflight: {preflight_json}")
    print(f"- D1-D5 reports: {diagnostics}")
    print(f"- D2 full aliasing rate: {d2_depth3['full_collision_rate']:.3f}")
    print(f"- D3 depth-1 weighted co-occurrence recall: {d3_depth1['weighted_collab_prefix_recall']:.3f}")
    print(f"- D5 active prefix counts: {d5_row['prefix_counts']}")


if __name__ == "__main__":
    main()
