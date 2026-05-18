"""Summarize AUDIT-SID AutoDL Gate 0 run directories."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def summarize_run(run_dir: Path) -> list[dict[str, object]]:
    metrics_dir = run_dir / "metrics"
    if not metrics_dir.exists():
        normalized_metrics = run_dir / "normalized" / "metrics"
        metrics_dir = normalized_metrics if normalized_metrics.exists() else metrics_dir

    coverage = _read_csv(metrics_dir / "coverage_report.csv")
    d2 = _read_csv(metrics_dir / "d2_collision.csv")
    d3 = _read_csv(metrics_dir / "d3_alignment.csv")
    d5 = _read_csv(metrics_dir / "d5a_deployment_cost.csv")

    methods: set[str] = set()
    for frame in (coverage, d2, d3, d5):
        if "method" in frame.columns:
            methods.update(frame["method"].dropna().astype(str))

    rows: list[dict[str, object]] = []
    for method in sorted(methods):
        row: dict[str, object] = {"run": run_dir.name, "method": method, "run_dir": str(run_dir)}

        if not coverage.empty:
            c = coverage[coverage["method"] == method]
            if not c.empty:
                first = c.iloc[0]
                for col in ("sid_items", "metadata_items", "interaction_items", "metadata_without_sid", "interaction_without_sid"):
                    if col in c.columns:
                        row[col] = first[col]

        if not d2.empty:
            m = d2[d2["method"] == method]
            full = m[m.get("collision_type", "") == "full"] if "collision_type" in m.columns else pd.DataFrame()
            if not full.empty:
                first = full.iloc[0]
                for col in ("collision_rate", "num_collision_groups", "mean_group_size"):
                    if col in full.columns:
                        row[f"full_{col}"] = first[col]
            prefix = m[m.get("collision_type", "") == "prefix"] if "collision_type" in m.columns else pd.DataFrame()
            if not prefix.empty and "depth" in prefix.columns:
                last = prefix.sort_values("depth").iloc[-1]
                if "collision_rate" in prefix.columns:
                    row["last_prefix_collision_rate"] = last["collision_rate"]

        if not d3.empty:
            m = d3[d3["method"] == method]
            if not m.empty:
                first = m.iloc[0]
                for col in ("category_purity", "mean_same_category_knn"):
                    if col in m.columns:
                        row[col] = first[col]

        if not d5.empty:
            m = d5[d5["method"] == method]
            if not m.empty:
                first = m.iloc[0]
                for col in ("sid_length", "unique_sid", "duplicate_sid_rate", "prefix_counts"):
                    if col in m.columns:
                        row[col] = first[col]

        rows.append(row)

    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize AUDIT-SID Gate 0 run metrics.")
    parser.add_argument("--run-root", type=Path, default=Path("_gate0_artifacts/autodl_runs"))
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    rows: list[dict[str, object]] = []
    if args.run_root.exists():
        for run_dir in sorted(path for path in args.run_root.iterdir() if path.is_dir()):
            rows.extend(summarize_run(run_dir))

    summary = pd.DataFrame(rows)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(args.output, index=False)

    if summary.empty:
        print("No Gate 0 metrics found.")
    else:
        print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
