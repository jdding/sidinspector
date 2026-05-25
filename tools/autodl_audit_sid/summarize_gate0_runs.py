"""Summarize SIDInspector AutoDL Gate 0 run directories."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


REQUIRED_METRIC_FILES = (
    "coverage_report.csv",
    "d1_utilization.csv",
    "d2_collision.csv",
    "d3_alignment.csv",
    "d4_head_tail.csv",
    "d5a_deployment_cost.csv",
)

AUXILIARY_DIRS = {"configs", "logs"}


def _read_csv(path: Path, errors: list[str], required: bool = False) -> pd.DataFrame:
    if not path.exists():
        if required:
            errors.append(f"missing {path}")
        return pd.DataFrame()
    return pd.read_csv(path)


def _identity_cols(frame: pd.DataFrame) -> list[str]:
    return ["dataset", "method"] if "dataset" in frame.columns else ["method"]


def _filter_identity(frame: pd.DataFrame, identity: dict[str, object]) -> pd.DataFrame:
    out = frame
    for col, value in identity.items():
        if col in out.columns:
            out = out[out[col] == value]
    return out


def summarize_run(run_dir: Path, errors: list[str], strict: bool = False) -> list[dict[str, object]]:
    skipped = run_dir / "SKIPPED.txt"
    if skipped.exists():
        return [
            {
                "run": run_dir.name,
                "method": "SKIPPED",
                "run_dir": str(run_dir),
                "status": skipped.read_text().strip().splitlines()[0],
            }
        ]

    metrics_dir = run_dir / "metrics"
    if not metrics_dir.exists():
        normalized_metrics = run_dir / "normalized" / "metrics"
        metrics_dir = normalized_metrics if normalized_metrics.exists() else metrics_dir
    if strict:
        for name in REQUIRED_METRIC_FILES:
            if not (metrics_dir / name).exists():
                errors.append(f"{run_dir.name}: missing {metrics_dir / name}")

    coverage = _read_csv(metrics_dir / "coverage_report.csv", errors, required=strict)
    d2 = _read_csv(metrics_dir / "d2_collision.csv", errors, required=strict)
    d3 = _read_csv(metrics_dir / "d3_alignment.csv", errors, required=strict)
    d5 = _read_csv(metrics_dir / "d5a_deployment_cost.csv", errors, required=strict)

    identities: list[dict[str, object]] = []
    if not coverage.empty:
        for _, row in coverage[_identity_cols(coverage)].drop_duplicates().iterrows():
            identities.append(row.to_dict())
    else:
        for frame in (d2, d3, d5):
            if "method" in frame.columns:
                for _, row in frame[_identity_cols(frame)].drop_duplicates().iterrows():
                    identities.append(row.to_dict())

    rows: list[dict[str, object]] = []
    for identity in identities:
        method = str(identity["method"])
        row: dict[str, object] = {"run": run_dir.name, **identity, "run_dir": str(run_dir)}

        if not coverage.empty:
            c = _filter_identity(coverage, identity)
            if not c.empty:
                first = c.iloc[0]
                for col in ("sid_items", "metadata_items", "interaction_items", "metadata_without_sid", "interaction_without_sid"):
                    if col in c.columns:
                        row[col] = first[col]

        if not d2.empty:
            m = _filter_identity(d2, identity)
            if not m.empty:
                first = m.iloc[0]
                for col in ("full_collision_rate", "full_collision_groups", "full_collision_items"):
                    if col in m.columns:
                        row[col] = first[col]
                if "prefix_depth" in m.columns:
                    last = m.sort_values("prefix_depth").iloc[-1]
                    for col in ("prefix_collision_rate", "prefix_collision_groups", "prefix_collision_items"):
                        if col in m.columns:
                            row[f"last_{col}"] = last[col]

        if not d3.empty:
            m = _filter_identity(d3, identity)
            if not m.empty:
                first = m.iloc[0]
                for col in ("level0_category_purity_mean", "level0_non_singleton_buckets"):
                    if col in m.columns:
                        row[col] = first[col]

        if not d5.empty:
            m = _filter_identity(d5, identity)
            if not m.empty:
                first = m.iloc[0]
                for col in ("sid_length", "unique_sid", "duplicate_sid_rate", "prefix_counts"):
                    if col in m.columns:
                        row[col] = first[col]

        rows.append(row)

    if strict and not rows:
        errors.append(f"{run_dir.name}: no summarizable metric rows")

    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize SIDInspector Gate 0 run metrics.")
    parser.add_argument("--run-root", type=Path, default=Path("_gate0_artifacts/autodl_runs"))
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    rows: list[dict[str, object]] = []
    errors: list[str] = []
    if args.run_root.exists():
        for run_dir in sorted(path for path in args.run_root.iterdir() if path.is_dir()):
            if run_dir.name in AUXILIARY_DIRS:
                continue
            rows.extend(summarize_run(run_dir, errors, strict=args.strict))
    elif args.strict:
        errors.append(f"missing run root: {args.run_root}")

    summary = pd.DataFrame(rows)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(args.output, index=False)

    if summary.empty:
        print("No Gate 0 metrics found.")
    else:
        print(summary.to_string(index=False))
    if errors:
        print("\nSummary errors:")
        for error in errors:
            print(f"- {error}")
        if args.strict:
            raise SystemExit(6)


if __name__ == "__main__":
    main()
