#!/usr/bin/env python3
"""Profile SIDInspector D1-D5 diagnostics on a local artifact bundle."""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from audit_sid import metrics


DEFAULT_SID_PATHS = [
    ROOT / "_gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/grid_export/normalized/sid_assignments.parquet",
    ROOT / "_gate0_artifacts/grid_same_dataset_runs/matched_capacity_grid_32_1280_1280_seed42_20260520/grid_export/normalized/sid_assignments.parquet",
    ROOT / "methods/rqvae_minimal_reference/outputs/cpu_full_23742_seed42/normalized/sid_assignments.parquet",
    ROOT / "_gate0_artifacts/resid_real_runs/normalized_resid_gaoq_1epoch/sid_assignments.parquet",
    ROOT / "_gate0_artifacts/sanity_musical/sid_assignments.parquet",
]
DEFAULT_METADATA = ROOT / "_gate0_artifacts/resid_musical_normalized/item_metadata.parquet"
DEFAULT_INTERACTIONS = ROOT / "_gate0_artifacts/resid_musical_normalized/interactions.parquet"


def timed(label: str, fn):
    start = time.perf_counter()
    result = fn()
    return label, time.perf_counter() - start, result


def main() -> None:
    parser = argparse.ArgumentParser(description="Profile D1-D5 runtime for SIDInspector local artifacts.")
    parser.add_argument("--sid-assignments", type=Path, nargs="*", default=DEFAULT_SID_PATHS)
    parser.add_argument("--item-metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--interactions", type=Path, default=DEFAULT_INTERACTIONS)
    parser.add_argument("--output-csv", type=Path, default=ROOT / "paper_assets/tables/table16_runtime_profile.csv")
    parser.add_argument("--output-md", type=Path, default=ROOT / "paper_assets/tables/table16_runtime_profile.md")
    parser.add_argument("--d3-top-k", type=int, default=20)
    parser.add_argument("--d3-max-pair-events", type=int, default=2_000_000)
    parser.add_argument("--d3-max-user-items", type=int, default=200)
    args = parser.parse_args()

    missing = [path for path in [*args.sid_assignments, args.item_metadata, args.interactions] if not path.exists()]
    if missing:
        raise FileNotFoundError("missing local runtime artifact(s): " + ", ".join(map(str, missing)))

    load_start = time.perf_counter()
    sid = pd.concat([pd.read_parquet(path) for path in args.sid_assignments], ignore_index=True)
    item_metadata = pd.read_parquet(args.item_metadata)
    interactions = pd.read_parquet(args.interactions)
    load_seconds = time.perf_counter() - load_start

    runs = [
        timed("input_load", lambda: None),
        timed("validation", lambda: metrics.validate_inputs(sid, item_metadata, interactions, allow_partial_coverage=True)),
        timed("D1_utilization", lambda: metrics.utilization(sid)),
        timed("D2_aliasing", lambda: metrics.collision(sid, interactions)),
        timed(
            "D3_neighborhood_alignment",
            lambda: metrics.alignment(
                sid,
                item_metadata,
                interactions,
                top_k=args.d3_top_k,
                max_pair_events=args.d3_max_pair_events,
                max_user_items=args.d3_max_user_items,
            ),
        ),
        timed("D4_popularity_allocation", lambda: metrics.head_tail_capacity(sid, interactions)),
        timed("D5_structural_cost", lambda: metrics.deployment_cost(sid)),
    ]
    rows = []
    for probe, seconds, result in runs:
        if probe == "input_load":
            seconds = load_seconds
            output_rows = 0
        elif isinstance(result, pd.DataFrame):
            output_rows = len(result)
        else:
            output_rows = 0
        rows.append(
            {
                "probe": probe,
                "seconds": round(seconds, 4),
                "sid_rows": len(sid),
                "items_per_method": int(sid.groupby(["dataset", "method"]).size().max()),
                "methods": int(sid.groupby(["dataset", "method"]).ngroups),
                "interaction_rows": len(interactions),
                "output_rows": output_rows,
                "notes": "dominant interaction-neighborhood step" if probe == "D3_neighborhood_alignment" else "mapping-level preflight",
            }
        )

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(args.output_csv, index=False)
    args.output_md.write_text(
        "# D1-D5 Runtime Profile\n\n"
        "Measured on the local Musical artifact bundle used by the paper-facing verifier. "
        "The table profiles five SID/profile rows plus sanity controls over the same "
        "23,742-item universe; timings are wall-clock seconds on the local development machine.\n\n"
        + df.to_markdown(index=False)
        + "\n\n"
        + "Environment:\n\n"
        + "```json\n"
        + json.dumps(
            {
                "python": platform.python_version(),
                "platform": platform.platform(),
            },
            indent=2,
        )
        + "\n```\n",
        encoding="utf-8",
    )
    print(f"wrote {args.output_csv}")
    print(f"wrote {args.output_md}")


if __name__ == "__main__":
    main()
