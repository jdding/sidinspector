#!/usr/bin/env python3
"""Verify the public AUDIT-SID paper artifact without private local caches."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "ARTIFACT_QUICKSTART.md",
    "ARTIFACT_MANIFEST.md",
    "LICENSE",
    "paper/main.tex",
    "paper/main.pdf",
    "paper/figures/fig1_audit_sid_pipeline.pdf",
    "paper_assets/tables/table1_method_coverage.csv",
    "paper_assets/tables/table2_musical_diagnostic.csv",
    "paper_assets/tables/table3_sanity_controls.csv",
    "paper_assets/tables/table4_grid_scale.csv",
    "paper_assets/tables/table5_dact_d6_churn.csv",
    "paper_assets/tables/table6_movielens_portability.csv",
    "paper_assets/tables/table7_grid_musical_3seed.csv",
    "paper_assets/references/audit_sid_references.bib",
    "tools/autodl_audit_sid/preflight_metric_inputs.py",
    "tests/test_preflight_metric_inputs.py",
]


EXPECTED_TABLE2 = {
    "GRID feature-text": {
        "items": "23742.0",
        "unique_sid": "3749.0",
        "full_collision_rate": "0.9769",
        "D3 L1 collab": "0.0552",
        "D4 tail": "0.3695",
        "prefix_counts": "64;3440;3749",
    },
    "ReSID GAOQ": {
        "items": "23742.0",
        "unique_sid": "23742.0",
        "full_collision_rate": "0.0",
        "D3 L1 collab": "0.1535",
        "D4 tail": "1.0",
        "prefix_counts": "32;1280;23742",
    },
}


EXPECTED_TABLE7 = {
    "42": {"full_collision_rate": "0.9769", "duplicate_sid_rate": "0.8421"},
    "43": {"full_collision_rate": "0.9751", "duplicate_sid_rate": "0.8327"},
    "44": {"full_collision_rate": "0.9756", "duplicate_sid_rate": "0.8379"},
}


def require_file(rel_path: str) -> None:
    path = ROOT / rel_path
    if not path.exists():
        raise FileNotFoundError(rel_path)
    if path.is_file() and path.stat().st_size == 0:
        raise ValueError(f"{rel_path} is empty")


def load_table2() -> dict[str, dict[str, str]]:
    path = ROOT / "paper_assets/tables/table2_musical_diagnostic.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["system"]: row for row in csv.DictReader(handle)}


def check_table2() -> None:
    table = load_table2()
    missing = sorted(set(EXPECTED_TABLE2) - set(table))
    if missing:
        raise ValueError(f"missing Table 2 rows: {missing}")
    for system, expected_cols in EXPECTED_TABLE2.items():
        row = table[system]
        for col, expected in expected_cols.items():
            actual = row[col]
            if actual != expected:
                raise ValueError(f"{system} {col}: expected {expected}, got {actual}")


def load_table7() -> dict[str, dict[str, str]]:
    path = ROOT / "paper_assets/tables/table7_grid_musical_3seed.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["seed"]: row for row in csv.DictReader(handle)}


def check_table7() -> None:
    table = load_table7()
    missing = sorted(set(EXPECTED_TABLE7) - set(table))
    if missing:
        raise ValueError(f"missing Table 7 seed rows: {missing}")
    for seed, expected_cols in EXPECTED_TABLE7.items():
        row = table[seed]
        for col, expected in expected_cols.items():
            actual = row[col]
            if actual != expected:
                raise ValueError(f"Table 7 seed {seed} {col}: expected {expected}, got {actual}")


def main() -> None:
    for rel_path in REQUIRED_FILES:
        require_file(rel_path)
    check_table2()
    check_table7()
    print("AUDIT-SID public artifact verification passed.")


if __name__ == "__main__":
    main()
