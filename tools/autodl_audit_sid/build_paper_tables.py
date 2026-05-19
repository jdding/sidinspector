"""Build paper-facing AUDIT-SID tables from local metric artifacts."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


GRID_ROOT = Path("_gate0_artifacts/grid_cluster_a_runs")
GRID_SCALE_RUNS = [
    "grid_official_rqkmeans_All_Beauty_text_20000_cuda_seed42",
    "grid_official_rqkmeans_All_Beauty_text_20000_cuda_seed43",
    "grid_official_rqkmeans_All_Beauty_text_20000_cuda_seed44",
    "grid_official_rqkmeans_All_Beauty_text_50000_cuda_seed42",
]


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def _round(value: object, digits: int = 4) -> object:
    if pd.isna(value):
        return value
    if isinstance(value, (float, int)):
        return round(float(value), digits)
    return value


def _format_table(df: pd.DataFrame, digits: int = 4) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if pd.api.types.is_numeric_dtype(out[col]):
            out[col] = out[col].map(lambda x: _round(x, digits))
    return out


def _markdown(df: pd.DataFrame) -> str:
    return df.to_markdown(index=False) + "\n"


def _latex(df: pd.DataFrame, caption: str, label: str) -> str:
    return df.to_latex(index=False, escape=True, caption=caption, label=label) + "\n"


def _write_table(df: pd.DataFrame, output_dir: Path, stem: str, caption: str, label: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    formatted = _format_table(df)
    formatted.to_csv(output_dir / f"{stem}.csv", index=False)
    (output_dir / f"{stem}.md").write_text(_markdown(formatted), encoding="utf-8")
    (output_dir / f"{stem}.tex").write_text(_latex(formatted, caption=caption, label=label), encoding="utf-8")


def method_coverage_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "line": "GRID/RQ-KMeans",
                "cluster": "A",
                "dataset": "All_Beauty; Musical_Instruments",
                "artifact": "real SID export",
                "diagnostics": "D1-D5a/D3v2",
                "paper_role": "main A evidence; same-item Musical row",
                "caveat": "Musical row uses processed feature text, not raw-text TIGER",
            },
            {
                "line": "ReSID/GAOQ",
                "cluster": "B",
                "dataset": "Musical_Instruments",
                "artifact": "real SID export",
                "diagnostics": "D1-D5a/D3v2",
                "paper_role": "main B evidence",
                "caveat": "bounded 1-epoch FAMAE; Sports balanced GAOQ stopped",
            },
            {
                "line": "Sanity tokenizers",
                "cluster": "control",
                "dataset": "Musical_Instruments; MovieLens-25M smoke",
                "artifact": "deterministic synthetic SIDs",
                "diagnostics": "D1-D5a/D3v2",
                "paper_role": "metric non-redundancy controls",
                "caveat": "not named SID methods",
            },
            {
                "line": "CARD compact",
                "cluster": "B/control",
                "dataset": "Musical_Instruments; Sports_and_Outdoors",
                "artifact": "proxy/stressor",
                "diagnostics": "D1-D5a",
                "paper_role": "backlog or stressor only",
                "caveat": "not faithful CARD evidence",
            },
            {
                "line": "DACT",
                "cluster": "drift",
                "dataset": "Tools",
                "artifact": "bundled code arrays",
                "diagnostics": "D6 optional",
                "paper_role": "optional churn demo",
                "caveat": "not a Cluster B replacement",
            },
            {
                "line": "DIGER/CapsID/AdaSID/AsymRec",
                "cluster": "future",
                "dataset": "not run",
                "artifact": "literature/code-screen only",
                "diagnostics": "not claimed",
                "paper_role": "coverage table context",
                "caveat": "verify public releases before submission",
            },
        ]
    )


def main_diagnostic_table() -> pd.DataFrame:
    path = Path("_gate0_artifacts/grid_same_dataset_runs/musical_same_dataset_grid_vs_resid_summary_20260519_110722.csv")
    raw = _read_csv(path)
    return raw[
        [
            "system",
            "method",
            "sid_items",
            "unique_sid",
            "duplicate_sid_rate",
            "full_collision_rate",
            "d3_level1_weighted_recall",
            "d4_head_sid_unique_ratio",
            "d4_mid_sid_unique_ratio",
            "d4_tail_sid_unique_ratio",
            "prefix_counts",
        ]
    ].rename(
        columns={
            "sid_items": "items",
            "d3_level1_weighted_recall": "D3 L1 collab",
            "d4_head_sid_unique_ratio": "D4 head",
            "d4_mid_sid_unique_ratio": "D4 mid",
            "d4_tail_sid_unique_ratio": "D4 tail",
        }
    )


def sanity_controls_table() -> pd.DataFrame:
    path = Path("_gate0_artifacts/case_study/resid_sanity_d3v2_summary.csv")
    raw = _read_csv(path)
    return raw[
        [
            "method",
            "unique_sid",
            "duplicate_sid_rate",
            "full_collision_rate",
            "d3_depth1_collab_recall",
            "d3_level0_category_purity",
            "head_sid_unique_ratio",
            "mid_sid_unique_ratio",
            "tail_sid_unique_ratio",
            "prefix_counts",
        ]
    ].rename(
        columns={
            "d3_depth1_collab_recall": "D3 L1 collab",
            "d3_level0_category_purity": "L0 category purity",
            "head_sid_unique_ratio": "D4 head",
            "mid_sid_unique_ratio": "D4 mid",
            "tail_sid_unique_ratio": "D4 tail",
        }
    )


def _grid_run_summary(run_name: str) -> dict[str, object]:
    run_dir = GRID_ROOT / run_name / "grid_export" / "metrics"
    coverage = _read_csv(run_dir / "coverage_report.csv").iloc[0]
    d2 = _read_csv(run_dir / "d2_collision.csv").iloc[0]
    d3 = _read_csv(run_dir / "d3_alignment.csv")
    d4 = _read_csv(run_dir / "d4_head_tail.csv")
    d5 = _read_csv(run_dir / "d5a_deployment_cost.csv").iloc[0]
    size_match = re.search(r"text_(\d+)_", run_name)
    seed_match = re.search(r"seed(\d+)", run_name)
    d3_depth1 = d3[d3["prefix_depth"] == 1].iloc[0] if "prefix_depth" in d3.columns else None
    d4_pivot = d4.pivot_table(columns="bucket", values="sid_unique_ratio", aggfunc="first")

    def d4_value(bucket: str) -> object:
        if d4_pivot.empty or bucket not in d4_pivot.columns:
            return pd.NA
        return float(d4_pivot[bucket].iloc[0])

    return {
        "dataset": coverage["dataset"],
        "items": int(coverage["sid_items"]),
        "run_size": int(size_match.group(1)) if size_match else int(coverage["sid_items"]),
        "seed": int(seed_match.group(1)) if seed_match else None,
        "unique_sid": int(d5["unique_sid"]),
        "duplicate_sid_rate": float(d5["duplicate_sid_rate"]),
        "full_collision_rate": float(d2["full_collision_rate"]),
        "D3 L1 collab": float(d3_depth1["weighted_collab_prefix_recall"]) if d3_depth1 is not None else pd.NA,
        "D4 head": d4_value("head"),
        "D4 mid": d4_value("mid"),
        "D4 tail": d4_value("tail"),
        "prefix_counts": d5["prefix_counts"],
    }


def grid_scale_table() -> pd.DataFrame:
    rows = [_grid_run_summary(run_name) for run_name in GRID_SCALE_RUNS]
    return pd.DataFrame(rows).sort_values(["run_size", "seed"]).reset_index(drop=True)


def d6_churn_table() -> pd.DataFrame:
    raw = _read_csv(Path("_gate0_artifacts/dact_tools_smoke/d6_churn_0.6_to_0.7.csv"))
    return raw[
        [
            "dataset",
            "prefix_depth",
            "old_items",
            "new_items",
            "common_items",
            "new_only_items",
            "changed_items",
            "churn_rate_common",
            "new_unique_prefixes",
            "new_prefix_collision_rate",
        ]
    ]


def movielens_portability_table() -> pd.DataFrame:
    root = Path("_gate0_artifacts/movielens_portability_smoke/ml25m_1mratings_10kitems/metrics")
    coverage = _read_csv(root / "coverage_report.csv")
    d5 = _read_csv(root / "d5a_deployment_cost.csv")
    d3 = _read_csv(root / "d3_alignment.csv")
    d3_depth1 = d3[d3["prefix_depth"] == 1][["dataset", "method", "weighted_collab_prefix_recall"]]
    merged = coverage.merge(d5, on=["dataset", "method"]).merge(d3_depth1, on=["dataset", "method"])
    return merged[
        [
            "dataset",
            "method",
            "sid_items",
            "metadata_without_sid",
            "interaction_without_sid",
            "unique_sid",
            "duplicate_sid_rate",
            "weighted_collab_prefix_recall",
            "prefix_counts",
        ]
    ].rename(columns={"weighted_collab_prefix_recall": "D3 L1 collab"})


def main() -> None:
    parser = argparse.ArgumentParser(description="Build AUDIT-SID paper-facing tables.")
    parser.add_argument("--output-dir", type=Path, default=Path("paper_assets/tables"))
    args = parser.parse_args()

    tables = [
        ("table1_method_coverage", method_coverage_table(), "AUDIT-SID method coverage.", "tab:method-coverage"),
        ("table2_musical_diagnostic", main_diagnostic_table(), "Same-item Musical diagnostic table.", "tab:musical-diagnostic"),
        ("table3_sanity_controls", sanity_controls_table(), "Sanity-control diagnostic non-redundancy.", "tab:sanity-controls"),
        ("table4_grid_scale", grid_scale_table(), "GRID scale and seed summary.", "tab:grid-scale"),
        ("table5_dact_d6_churn", d6_churn_table(), "DACT optional D6 churn.", "tab:d6-churn"),
        (
            "table6_movielens_portability",
            movielens_portability_table(),
            "MovieLens optional portability smoke.",
            "tab:movielens-portability",
        ),
    ]
    for stem, df, caption, label in tables:
        _write_table(df, args.output_dir, stem, caption, label)
        print(f"[paper-table] wrote {stem}: {len(df)} rows")


if __name__ == "__main__":
    main()
