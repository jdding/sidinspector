#!/usr/bin/env python3
"""Validate SIDInspector's resource reproducibility matrix.

The matrix intentionally mixes fully runnable release rows with tracked
evidence snapshots for paper-only experiments. This verifier checks the release
side of that contract: required files exist, CSV schemas are complete, and the
paper-facing snapshot values that anchor the main finding have not drifted.
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "reproducibility_matrix.csv"
SNAPSHOT_DIR = ROOT / "docs" / "reproducibility"
SOURCE_DIR = SNAPSHOT_DIR / "sources"


REQUIRED_MATRIX_COLUMNS = {
    "paper_evidence",
    "source_artifact",
    "command",
    "output",
    "runtime",
    "release_status",
}

REQUIRED_SNAPSHOTS = {
    "table1_evidence_catalog.csv": {"row", "role", "items", "seeds", "signal", "source_evidence", "release_status"},
    "table2_musical_diagnostic.csv": {
        "artifact",
        "group",
        "items",
        "seeds",
        "unique_sids",
        "d2_aliasing_rate",
        "d3_l1_weighted",
        "d4_tail_unique_ratio",
        "d5_active_prefix_counts",
        "source_evidence",
    },
    "table3_probe_calibration.csv": {"probe", "d", "without_probe", "with_probe", "source_evidence"},
    "official_adapter_metrics_snapshot.csv": {
        "adapter",
        "dataset",
        "items",
        "unique_sids",
        "d2_aliasing_rate",
        "d3_l1_weighted",
        "d4_tail_unique_ratio",
        "d5_active_prefix_counts",
        "source_evidence",
        "release_status",
    },
    "extension_checks_snapshot.csv": {"check", "dataset", "items", "key_signal", "source_evidence", "release_status"},
    "rqmin_reference_snapshot.csv": {
        "dataset",
        "method",
        "items",
        "unique_sid",
        "duplicate_sid_rate",
        "full_collision_rate",
        "d3_l1_weighted",
        "d4_head_unique_ratio",
        "d4_mid_unique_ratio",
        "d4_tail_unique_ratio",
        "prefix_counts",
        "evidence_role",
        "caveat",
        "source_config",
    },
}

REQUIRED_SOURCES = [
    "README.md",
    "grid_ft_seed_summary.csv",
    "grid_resid_comparison.csv",
    "control_summary.csv",
    "rqmin_reference.csv",
    "controller_qualified_aliasing.csv",
    "controller_capacity_budget.csv",
    "controller_variable_depth.csv",
    "grid_ft_manifest.json",
    "grid_cap_manifest.json",
    "grid_cap_metrics/coverage_report.csv",
    "grid_cap_metrics/d1_utilization.csv",
    "grid_cap_metrics/d2_collision.csv",
    "grid_cap_metrics/d3_alignment.csv",
    "grid_cap_metrics/d4_head_tail.csv",
    "grid_cap_metrics/d5a_deployment_cost.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require_columns(path: Path, required: set[str]) -> list[dict[str, str]]:
    rows = read_csv(path)
    if not rows:
        raise RuntimeError(f"{path} is empty")
    missing = required - set(rows[0])
    if missing:
        raise RuntimeError(f"{path} is missing columns: {sorted(missing)}")
    return rows


def require_close(label: str, observed: float, expected: float, tolerance: float = 0.0005) -> None:
    if abs(observed - expected) > tolerance:
        raise RuntimeError(f"{label} drifted: observed {observed}, expected {expected}")


def main() -> None:
    if not MATRIX.is_file():
        raise FileNotFoundError(MATRIX)
    if not SNAPSHOT_DIR.is_dir():
        raise FileNotFoundError(SNAPSHOT_DIR)

    matrix_rows = require_columns(MATRIX, REQUIRED_MATRIX_COLUMNS)
    if len(matrix_rows) < 8:
        raise RuntimeError(f"matrix has too few rows: {len(matrix_rows)}")
    runnable = [row for row in matrix_rows if "fully runnable from release repo" in row["release_status"]]
    if len(runnable) < 2:
        raise RuntimeError("matrix should include at least toy and reviewer quickstart runnable rows")

    for name, columns in REQUIRED_SNAPSHOTS.items():
        require_columns(SNAPSHOT_DIR / name, columns)

    for name in REQUIRED_SOURCES:
        path = SOURCE_DIR / name
        if not path.is_file():
            raise FileNotFoundError(path)

    with tempfile.TemporaryDirectory(prefix="sidinspector-paper-tables-") as tmp:
        output_dir = Path(tmp)
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / "build_paper_tables.py"), "--output-dir", str(output_dir)],
            cwd=ROOT,
            check=True,
        )
        for name in ["table2_musical_diagnostic.csv", "table3_probe_calibration.csv"]:
            rebuilt = read_csv(output_dir / name)
            tracked = read_csv(SNAPSHOT_DIR / name)
            if rebuilt != tracked:
                raise RuntimeError(f"{name} does not match its released source summaries")

    with (SOURCE_DIR / "grid_ft_manifest.json").open(encoding="utf-8") as handle:
        grid_ft_manifest = json.load(handle)
    with (SOURCE_DIR / "grid_cap_manifest.json").open(encoding="utf-8") as handle:
        grid_cap_manifest = json.load(handle)
    if grid_ft_manifest.get("num_hierarchies") != 3 or grid_ft_manifest.get("codebook_width") != 64:
        raise RuntimeError("GRID-style feature-text budget must be three width-64 levels")
    if grid_cap_manifest.get("per_level_widths") != [32, 1280, 1280]:
        raise RuntimeError("GRID-style capacity budget must be 32/1280/1280")

    table2 = {row["artifact"]: row for row in read_csv(SNAPSHOT_DIR / "table2_musical_diagnostic.csv")}
    for artifact in ["GRID-style ft", "ReSID", "Cat-prefix", "RQ-min ref"]:
        if artifact not in table2:
            raise RuntimeError(f"Table 2 snapshot missing {artifact}")
    require_close("GRID-style ft D2", float(table2["GRID-style ft"]["d2_aliasing_rate"]), 0.9768764215314631)
    require_close("GRID-style ft D3", float(table2["GRID-style ft"]["d3_l1_weighted"]), 0.0551755939778614)
    require_close("ReSID D3", float(table2["ReSID"]["d3_l1_weighted"]), 0.1535441362629664)
    require_close("Cat-prefix D3", float(table2["Cat-prefix"]["d3_l1_weighted"]), 0.4469788910982484)
    require_close("RQ-min D2", float(table2["RQ-min ref"]["d2_aliasing_rate"]), 0.4401, tolerance=0.001)
    require_close("RQ-min D3", float(table2["RQ-min ref"]["d3_l1_weighted"]), 0.0650, tolerance=0.001)

    rqmin = read_csv(SNAPSHOT_DIR / "rqmin_reference_snapshot.csv")[0]
    if rqmin["method"] != "rqvae_minimal_reference":
        raise RuntimeError(f"Unexpected RQ-min method label: {rqmin['method']}")
    require_close("RQ-min snapshot full_collision_rate", float(rqmin["full_collision_rate"]), 0.4401, tolerance=0.001)
    require_close("RQ-min snapshot D3", float(rqmin["d3_l1_weighted"]), 0.0650, tolerance=0.001)

    table3 = {row["probe"]: row for row in read_csv(SNAPSHOT_DIR / "table3_probe_calibration.csv")}
    expected_probe_values = {
        "Qualified aliasing": ("hash 1.19x", "co-occur 3.86x"),
        "Capacity budget": ("head 1.000", "tail 0.028"),
        "Variable depth": ("max-depth 12,010", "active 7,914"),
    }
    for probe, (without_probe, with_probe) in expected_probe_values.items():
        row = table3.get(probe)
        if row is None:
            raise RuntimeError(f"Table 3 snapshot missing {probe}")
        if row["without_probe"] != without_probe or row["with_probe"] != with_probe:
            raise RuntimeError(f"{probe} values drifted: {row}")

    print("SIDInspector reproducibility matrix verification passed.")
    print(
        f"Verified {len(matrix_rows)} matrix rows, {len(REQUIRED_SNAPSHOTS)} evidence snapshots, "
        f"and deterministic Table 2/3 reconstruction from {len(REQUIRED_SOURCES)} source files."
    )


if __name__ == "__main__":
    main()
