#!/usr/bin/env python3
"""Verify the public SIDInspector/AUDIT-SID artifact without private local caches."""

from __future__ import annotations

import csv
import math
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
    "paper_assets/tables/table3_mechanism_probes.csv",
    "paper_assets/tables/table3_mechanism_probes.md",
    "paper_assets/tables/table3_mechanism_probes.tex",
    "paper_assets/tables/table4_grid_scale.csv",
    "paper_assets/tables/table5_dact_d6_churn.csv",
    "paper_assets/tables/table6_movielens_portability.csv",
    "paper_assets/tables/table7_grid_musical_3seed.csv",
    "paper_assets/tables/table8_qualified_collision_probe.csv",
    "paper_assets/tables/table9_capacity_budget_sweep.csv",
    "paper_assets/tables/table10_variable_depth_cost_probe.csv",
    "paper_assets/tables/table11_d3_ranking_validation.csv",
    "paper_assets/tables/table12_sports_grid_vertical.csv",
    "paper_assets/tables/table13_all_beauty_vertical_d3.csv",
    "paper_assets/tables/table14_all_beauty_d3_ranking_validation.csv",
    "paper_assets/tables/table15_rqvae_minimal_reference.csv",
    "paper_assets/tables/table16_runtime_profile.csv",
    "paper_assets/tables/table16_runtime_profile.md",
    "paper_assets/references/audit_sid_references.bib",
    "examples/minimal_adapter.py",
    "tools/autodl_audit_sid/preflight_metric_inputs.py",
    "tools/autodl_audit_sid/preflight_card_nurqvae.py",
    "tools/profile_diagnostics_runtime.py",
    "tools/autodl_audit_sid/run_d3_ranking_context.py",
    "tools/autodl_audit_sid/run_d3_ranking_validation.py",
    "tools/autodl_audit_sid/run_rqvae_minimal_reference.py",
    "tools/autodl_audit_sid/run_grid_rqkmeans_direct_export.py",
    "tools/autodl_audit_sid/run_qualified_collision_probe.py",
    "tools/autodl_audit_sid/run_capacity_budget_sweep.py",
    "tools/autodl_audit_sid/run_variable_depth_cost_probe.py",
    "tests/test_preflight_metric_inputs.py",
    "tests/test_preflight_card_nurqvae.py",
    "tests/test_qualified_collision_probe.py",
    "tests/test_capacity_budget_sweep.py",
    "tests/test_variable_depth_cost_probe.py",
    "tests/test_d3_ranking_context.py",
    "tests/test_d3_ranking_validation.py",
    "tests/test_rqvae_minimal_reference.py",
    "methods/rqvae_minimal_reference/IMPL_NOTES.md",
    "methods/rqvae_minimal_reference/exporter.py",
    "docs/THIRD_METHOD_EVIDENCE_GATE.md",
    "docs/METHOD_RELEASE_SCOUT.md",
    "docs/CARD_ORIGINAL_NURQVAE_EVIDENCE_GATE.md",
    "docs/DIAGNOSTIC_PROBE_TAXONOMY.md",
    "docs/CONTROLLED_STRESSOR_SELECTION.md",
    "docs/QUALIFIED_COLLISION_PROBE.md",
    "docs/CAPACITY_BUDGET_SWEEP.md",
    "docs/VARIABLE_DEPTH_COST_PROBE.md",
    "docs/D3_RANKING_VALIDATION_MUSICAL.md",
    "docs/D3_RANKING_VALIDATION_ALL_BEAUTY.md",
    "docs/RQVAE_MINIMAL_REFERENCE_GATE.md",
    "docs/SPORTS_GRID_THIRD_VERTICAL.md",
    "docs/ADAPTER_TEMPLATE.md",
    "docs/PAPER_CONTROLLER_INTEGRATION.md",
    "docs/PAPER_STRICT_CLAIM_AUDIT.md",
]


EXPECTED_TABLE1 = {
    "GRID ft": {
        "type": "named (A)",
        "items": "23,742",
        "seeds": "3",
        "d_coverage": "D1-D5",
    },
    "GRID ft-cap": {
        "type": "named (A, capacity ablation)",
        "items": "23,742",
        "seeds": "1",
        "d_coverage": "D1-D5",
    },
    "RQ-min ref": {
        "type": "reference adapter",
        "items": "23,742",
        "seeds": "1",
        "d_coverage": "D1-D5",
    },
    "ReSID†": {
        "type": "named (B)",
        "items": "23,742",
        "seeds": "1",
        "d_coverage": "D1-D5",
    },
    "Cat-prefix, Pop-bal, Hash-coll": {
        "type": "controls",
        "items": "23,742",
        "seeds": "n/a",
        "d_coverage": "D1-D5",
    },
    "Mechanism probes (3)": {
        "type": "controlled",
        "items": "synth.",
        "seeds": "n/a",
        "d_coverage": "D2,D4,D5",
    },
    "All_Beauty, Sports, MovieLens, DACT": {
        "type": "portability/extension",
        "items": "varies",
        "seeds": "varies",
        "d_coverage": "D1-D5, D6",
    },
}


EXPECTED_TABLE2 = {
    "GRID feature-text": {
        "items": "23742.0",
        "unique_sid": "3749.0",
        "full_collision_rate": "0.9769",
        "D3 L1 collab": "0.0552",
        "D4 tail": "0.3695",
        "prefix_counts": "64;3440;3749",
    },
    "GRID ft-cap": {
        "items": "23742.0",
        "unique_sid": "9874.0",
        "full_collision_rate": "0.7785",
        "D3 L1 collab": "0.0796",
        "D4 tail": "0.6391",
        "prefix_counts": "32;9300;9874",
    },
    "RQ-min reference": {
        "items": "23742.0",
        "unique_sid": "17247.0",
        "full_collision_rate": "0.4401",
        "D3 L1 collab": "0.0650",
        "D4 tail": "0.8831",
        "prefix_counts": "32;2368;17247",
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


EXPECTED_TABLE3_MECHANISM = {
    "Qualified aliasing": {
        "d": "D2",
        "without_probe": "hash 1.19x",
        "with_probe": "co-occur 3.86x",
    },
    "Capacity budget": {
        "d": "D1/D4",
        "without_probe": "head 1.000",
        "with_probe": "tail 0.028",
    },
    "Variable depth": {
        "d": "D5",
        "without_probe": "max-depth 12,010",
        "with_probe": "active 7,914",
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

EXPECTED_TABLE11_ROWS = {
    "sanity_category_prefix": {
        "D3 L1 collab": 0.438287,
        "candidate_recall": 0.612558,
        "fixed_reranker_recall_at_20": 0.061787,
        "fixed_reranker_ndcg_at_20": 0.029202,
    },
    "resid_gaoq": {
        "D3 L1 collab": 0.135273,
        "candidate_recall": 0.360104,
        "fixed_reranker_recall_at_20": 0.052774,
        "fixed_reranker_ndcg_at_20": 0.025177,
    },
    "grid_official_rqkmeans_resid_feature_text": {
        "D3 L1 collab": 0.052332,
        "candidate_recall": 0.18586,
        "fixed_reranker_recall_at_20": 0.034048,
        "fixed_reranker_ndcg_at_20": 0.017148,
    },
}

EXPECTED_TABLE11_SPEARMAN = {
    "candidate_recall": 0.942857142857143,
    "fixed_reranker_recall_at_20": 0.8857142857142858,
    "fixed_reranker_ndcg_at_20": 0.942857142857143,
}

EXPECTED_TABLE12_20K = {
    "metadata_without_sid": "0.0",
    "interaction_without_sid": "0.0",
    "unique_sid": "8165.0",
    "duplicate_sid_rate": "0.59175",
    "D3 L1 collab": "0.054982",
    "D4 tail": "0.65284",
    "prefix_counts": "128;7986;8165",
}

EXPECTED_TABLE13_ROWS = {
    "seed42:grid_official_rqkmeans_all_beauty_20k_seed42": {
        "D3 L1 collab": "0.081147",
        "category_metadata_scope": "coarse category fallback",
    },
    "seed42:sanity_category_prefix": {
        "D3 L1 collab": "0.968438",
        "category_metadata_scope": "coarse category fallback",
    },
    "seed43:grid_rqkmeans_seed43": {
        "D3 L1 collab": "0.08724",
        "category_metadata_scope": "coarse category fallback",
    },
    "seed44:grid_rqkmeans_seed44": {
        "D3 L1 collab": "0.089778",
        "category_metadata_scope": "coarse category fallback",
    },
}

EXPECTED_TABLE14_ROWS = {
    "category-prefix sanity": {
        "D3 L1 collab": 0.9531972265023112,
        "candidate_recall": 0.514,
        "fixed_reranker_recall_at_20": 0.048,
        "fixed_reranker_ndcg_at_20": 0.0222885132480993,
    },
    "GRID RQ-KMeans 20k seed42": {
        "D3 L1 collab": 0.0597072419106317,
        "candidate_recall": 0.085,
        "fixed_reranker_recall_at_20": 0.029,
        "fixed_reranker_ndcg_at_20": 0.016183396290365,
    },
}

EXPECTED_TABLE14_SPEARMAN = {
    "candidate_recall": 1.0,
    "fixed_reranker_recall_at_20": 0.8,
    "fixed_reranker_ndcg_at_20": 0.8,
}

EXPECTED_TABLE15_ROWS = {
    "rqvae_minimal_reference": {
        "items": 23742.0,
        "unique_sid": 17247.0,
        "duplicate_sid_rate": 0.2736,
        "full_collision_rate": 0.4401,
        "D3 L1 collab": 0.0650,
        "D4 tail": 0.8831,
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


def check_table1() -> None:
    table = load_csv("paper_assets/tables/table1_method_coverage.csv", "row")
    if len(table) != len(EXPECTED_TABLE1):
        raise ValueError(f"Table 1 should contain {len(EXPECTED_TABLE1)} rows, got {len(table)}")
    check_expected_rows(table, EXPECTED_TABLE1, "Table 1 evidence catalog")


def check_table3_mechanism() -> None:
    check_expected_rows(
        load_csv("paper_assets/tables/table3_mechanism_probes.csv", "probe"),
        EXPECTED_TABLE3_MECHANISM,
        "Table 3 mechanism probes",
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


def _as_float(row: dict[str, str], col: str) -> float:
    return float(row[col])


def _assert_close(actual: float, expected: float, label: str, tolerance: float = 1e-6) -> None:
    if math.isnan(actual) or abs(actual - expected) > tolerance:
        raise ValueError(f"{label}: expected {expected}, got {actual}")


def _rank(values: list[float]) -> list[float]:
    # Current verifier inputs have no ties.  Keep tie handling deterministic in
    # case a future rounded table introduces one.
    order = sorted(range(len(values)), key=lambda idx: values[idx])
    ranks = [0.0] * len(values)
    pos = 0
    while pos < len(order):
        end = pos + 1
        while end < len(order) and values[order[end]] == values[order[pos]]:
            end += 1
        avg_rank = (pos + 1 + end) / 2.0
        for idx in order[pos:end]:
            ranks[idx] = avg_rank
        pos = end
    return ranks


def _pearson(left: list[float], right: list[float]) -> float:
    if len(left) != len(right) or len(left) < 2:
        raise ValueError("correlation requires matching vectors with at least two rows")
    left_mean = sum(left) / len(left)
    right_mean = sum(right) / len(right)
    numerator = sum((x - left_mean) * (y - right_mean) for x, y in zip(left, right))
    left_norm = math.sqrt(sum((x - left_mean) ** 2 for x in left))
    right_norm = math.sqrt(sum((y - right_mean) ** 2 for y in right))
    if left_norm == 0 or right_norm == 0:
        raise ValueError("correlation vector has zero variance")
    return numerator / (left_norm * right_norm)


def _spearman(left: list[float], right: list[float]) -> float:
    return _pearson(_rank(left), _rank(right))


def check_table11() -> None:
    table = load_csv("paper_assets/tables/table11_d3_ranking_validation.csv", "method")
    if len(table) != 6:
        raise ValueError(f"Table 11 should contain six artifact/control rows, got {len(table)}")
    check_expected_float_rows(table, EXPECTED_TABLE11_ROWS, "Table 11 D3 validation")
    rows = list(table.values())
    if {row["ranker"] for row in rows} != {"cooccurrence_popularity"}:
        raise ValueError("Table 11 must fix the reranker to cooccurrence_popularity")
    if {row["prefix_depth"] for row in rows} != {"1.0"}:
        raise ValueError("Table 11 must use prefix depth 1")
    d3 = [_as_float(row, "D3 L1 collab") for row in rows]
    for metric, expected in EXPECTED_TABLE11_SPEARMAN.items():
        actual = _spearman(d3, [_as_float(row, metric) for row in rows])
        _assert_close(actual, expected, f"Table 11 Spearman D3 vs {metric}", tolerance=1e-12)


def check_expected_float_rows(
    table: dict[str, dict[str, str]],
    expected: dict[str, dict[str, float]],
    label: str,
) -> None:
    missing = sorted(set(expected) - set(table))
    if missing:
        raise ValueError(f"missing {label} rows: {missing}")
    for row_key, expected_cols in expected.items():
        row = table[row_key]
        for col, expected_value in expected_cols.items():
            _assert_close(_as_float(row, col), expected_value, f"{label} {row_key} {col}")


def check_table12() -> None:
    table = load_csv("paper_assets/tables/table12_sports_grid_vertical.csv", "run_size")
    if sorted(table) != ["20000.0", "5000.0"]:
        raise ValueError(f"Table 12 should contain 5k and 20k Sports rows, got {sorted(table)}")
    row = table["20000.0"]
    for col, expected_value in EXPECTED_TABLE12_20K.items():
        actual = row[col]
        if actual != expected_value:
            raise ValueError(f"Table 12 Sports 20k {col}: expected {expected_value}, got {actual}")


def check_table13() -> None:
    rows = []
    with (ROOT / "paper_assets/tables/table13_all_beauty_vertical_d3.csv").open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle)]
    table = {f"{row['seed']}:{row['method']}": row for row in rows}
    check_expected_rows(table, EXPECTED_TABLE13_ROWS, "Table 13 All_Beauty D3")


def check_table14() -> None:
    table = load_csv("paper_assets/tables/table14_all_beauty_d3_ranking_validation.csv", "method")
    if len(table) != 4:
        raise ValueError(f"Table 14 should contain four All_Beauty artifact/control rows, got {len(table)}")
    check_expected_float_rows(table, EXPECTED_TABLE14_ROWS, "Table 14 All_Beauty D3 validation")
    rows = list(table.values())
    if {row["ranker"] for row in rows} != {"cooccurrence_popularity"}:
        raise ValueError("Table 14 must fix the reranker to cooccurrence_popularity")
    if {row["prefix_depth"] for row in rows} != {"1"}:
        raise ValueError("Table 14 must use prefix depth 1")
    d3 = [_as_float(row, "D3 L1 collab") for row in rows]
    for metric, expected in EXPECTED_TABLE14_SPEARMAN.items():
        actual = _spearman(d3, [_as_float(row, metric) for row in rows])
        _assert_close(actual, expected, f"Table 14 Spearman D3 vs {metric}", tolerance=1e-12)


def check_table15() -> None:
    table = load_csv("paper_assets/tables/table15_rqvae_minimal_reference.csv", "method")
    check_expected_float_rows(table, EXPECTED_TABLE15_ROWS, "Table 15 RQ-min reference")


def main() -> None:
    for rel_path in REQUIRED_FILES:
        require_file(rel_path)
    check_table1()
    check_table2()
    check_table7()
    check_table3()
    check_table3_mechanism()
    check_table8()
    check_table9()
    check_table10()
    check_table11()
    check_table12()
    check_table13()
    check_table14()
    check_table15()
    print("SIDInspector/AUDIT-SID public artifact verification passed.")


if __name__ == "__main__":
    main()
