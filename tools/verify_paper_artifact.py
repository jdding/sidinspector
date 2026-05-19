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
    "paper_assets/tables/table8_qualified_collision_probe.csv",
    "paper_assets/tables/table9_capacity_budget_sweep.csv",
    "paper_assets/tables/table10_variable_depth_cost_probe.csv",
    "paper_assets/references/audit_sid_references.bib",
    "tools/autodl_audit_sid/preflight_metric_inputs.py",
    "tools/autodl_audit_sid/preflight_card_nurqvae.py",
    "tools/autodl_audit_sid/run_qualified_collision_probe.py",
    "tools/autodl_audit_sid/run_capacity_budget_sweep.py",
    "tools/autodl_audit_sid/run_variable_depth_cost_probe.py",
    "tests/test_preflight_metric_inputs.py",
    "tests/test_preflight_card_nurqvae.py",
    "tests/test_qualified_collision_probe.py",
    "tests/test_capacity_budget_sweep.py",
    "tests/test_variable_depth_cost_probe.py",
    "docs/THIRD_METHOD_EVIDENCE_GATE.md",
    "docs/METHOD_RELEASE_SCOUT.md",
    "docs/CARD_ORIGINAL_NURQVAE_EVIDENCE_GATE.md",
    "docs/CONTROLLED_STRESSOR_SELECTION.md",
    "docs/QUALIFIED_COLLISION_PROBE.md",
    "docs/CAPACITY_BUDGET_SWEEP.md",
    "docs/VARIABLE_DEPTH_COST_PROBE.md",
    "docs/PAPER_CONTROLLER_INTEGRATION.md",
    "docs/PAPER_STRICT_CLAIM_AUDIT.md",
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


EXPECTED_TABLE3 = {
    "sanity_category_prefix": {
        "unique_sid": "23742.0",
        "full_collision_rate": "0.0",
        "D3 L1 collab": "0.447",
        "D4 tail": "1.0",
    },
    "sanity_mod_collision_hash": {
        "unique_sid": "256.0",
        "full_collision_rate": "1.0",
        "D3 L1 collab": "0.0037",
        "D4 tail": "0.0322",
    },
    "sanity_popularity_balanced": {
        "unique_sid": "22707.0",
        "full_collision_rate": "0.086",
        "D3 L1 collab": "0.3026",
        "D4 tail": "0.9619",
    },
}


EXPECTED_TABLE8 = {
    "grid_official_rqkmeans_resid_feature_text": {
        "interaction_qualified_collision_lift": "3.8631578947368426",
    },
    "sanity_mod_collision_hash": {
        "interaction_qualified_collision_lift": "1.1851851851851851",
    },
}


EXPECTED_TABLE9_WIDTH24 = {
    "head_unique_ratio": "1.0",
    "tail_unique_ratio": "0.0281902844198338",
}


EXPECTED_TABLE10 = {
    "controller_variable_depth_head_long_tail_short_w64_maxd4": {
        "standard_prefix_counts": "64;4096;12010;19924",
        "effective_prefix_counts": "64;4096;7914;7914",
    }
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


def load_csv(rel_path: str, key: str) -> dict[str, dict[str, str]]:
    path = ROOT / rel_path
    with path.open(newline="", encoding="utf-8") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


def check_expected_rows(table: dict[str, dict[str, str]], expected: dict[str, dict[str, str]], label: str) -> None:
    missing = sorted(set(expected) - set(table))
    if missing:
        raise ValueError(f"missing {label} rows: {missing}")
    for row_key, expected_cols in expected.items():
        row = table[row_key]
        for col, expected_value in expected_cols.items():
            actual = row[col]
            if actual != expected_value:
                raise ValueError(f"{label} {row_key} {col}: expected {expected_value}, got {actual}")


def check_table3() -> None:
    check_expected_rows(
        load_csv("paper_assets/tables/table3_sanity_controls.csv", "method"),
        EXPECTED_TABLE3,
        "Table 3 sanity",
    )


def check_table8() -> None:
    check_expected_rows(
        load_csv("paper_assets/tables/table8_qualified_collision_probe.csv", "method"),
        EXPECTED_TABLE8,
        "Table 8 collision probe",
    )


def check_table9() -> None:
    rows = []
    with (ROOT / "paper_assets/tables/table9_capacity_budget_sweep.csv").open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle)]
    matches = [row for row in rows if row["policy"] == "head_reserved" and row["width"] == "24"]
    if len(matches) != 1:
        raise ValueError("missing Table 9 head_reserved width 24 row")
    for col, expected_value in EXPECTED_TABLE9_WIDTH24.items():
        actual = matches[0][col]
        if actual != expected_value:
            raise ValueError(f"Table 9 head_reserved width 24 {col}: expected {expected_value}, got {actual}")


def check_table10() -> None:
    check_expected_rows(
        load_csv("paper_assets/tables/table10_variable_depth_cost_probe.csv", "method"),
        EXPECTED_TABLE10,
        "Table 10 variable depth",
    )


def main() -> None:
    for rel_path in REQUIRED_FILES:
        require_file(rel_path)
    check_table2()
    check_table7()
    check_table3()
    check_table8()
    check_table9()
    check_table10()
    print("AUDIT-SID public artifact verification passed.")


if __name__ == "__main__":
    main()
