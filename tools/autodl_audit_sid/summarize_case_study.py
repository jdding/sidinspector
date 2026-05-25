"""Build a compact paper-facing summary from SIDInspector metric CSVs."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def _read(metrics_dir: Path, name: str) -> pd.DataFrame:
    path = metrics_dir / name
    if not path.exists():
        raise FileNotFoundError(f"missing metric table: {path}")
    return pd.read_csv(path)


def summarize(metrics_dir: Path) -> pd.DataFrame:
    d2 = _read(metrics_dir, "d2_collision.csv")
    d3 = _read(metrics_dir, "d3_alignment.csv")
    d4 = _read(metrics_dir, "d4_head_tail.csv")
    d5 = _read(metrics_dir, "d5a_deployment_cost.csv")

    key_cols = ["dataset", "method"]
    rows = []
    for key, d5_group in d5.groupby(key_cols):
        if not isinstance(key, tuple):
            key = (key,)
        key_values = dict(zip(key_cols, key))
        method_filter = (d2["dataset"] == key_values["dataset"]) & (d2["method"] == key_values["method"])
        d2_group = d2[method_filter]
        d3_group = d3[(d3["dataset"] == key_values["dataset"]) & (d3["method"] == key_values["method"])]
        d4_group = d4[(d4["dataset"] == key_values["dataset"]) & (d4["method"] == key_values["method"])]
        d3_depth1 = d3_group[d3_group["prefix_depth"] == 1]
        d3_depth2 = d3_group[d3_group["prefix_depth"] == 2]
        d4_pivot = d4_group.pivot_table(index=key_cols, columns="bucket", values="sid_unique_ratio", aggfunc="first")
        d5_row = d5_group.iloc[0]
        d2_row = d2_group.iloc[0] if not d2_group.empty else pd.Series(dtype=object)
        d3_row = d3_depth1.iloc[0] if not d3_depth1.empty else pd.Series(dtype=object)
        d3_row2 = d3_depth2.iloc[0] if not d3_depth2.empty else pd.Series(dtype=object)
        rows.append(
            {
                **key_values,
                "sid_length": int(d5_row["sid_length"]),
                "unique_sid": int(d5_row["unique_sid"]),
                "duplicate_sid_rate": float(d5_row["duplicate_sid_rate"]),
                "prefix_counts": d5_row["prefix_counts"],
                "full_collision_rate": float(d2_row.get("full_collision_rate", 0.0)),
                "d3_depth1_collab_recall": float(d3_row.get("mean_collab_prefix_recall", 0.0)),
                "d3_depth2_collab_recall": float(d3_row2.get("mean_collab_prefix_recall", 0.0)),
                "d3_level0_category_purity": float(d3_row.get("level0_category_purity_mean", 0.0)),
                "head_sid_unique_ratio": float(d4_pivot.get("head", pd.Series([0.0])).iloc[0])
                if not d4_pivot.empty
                else 0.0,
                "mid_sid_unique_ratio": float(d4_pivot.get("mid", pd.Series([0.0])).iloc[0])
                if not d4_pivot.empty
                else 0.0,
                "tail_sid_unique_ratio": float(d4_pivot.get("tail", pd.Series([0.0])).iloc[0])
                if not d4_pivot.empty
                else 0.0,
            }
        )
    return pd.DataFrame(rows).sort_values(key_cols)


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize an SIDInspector case-study metrics directory.")
    parser.add_argument("--metrics-dir", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--output-md", type=Path)
    args = parser.parse_args()

    table = summarize(args.metrics_dir)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(args.output_csv, index=False)
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(table.to_markdown(index=False) + "\n", encoding="utf-8")
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
