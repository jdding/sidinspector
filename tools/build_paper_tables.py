#!/usr/bin/env python3
"""Rebuild the paper-facing Table 2 and Table 3 CSV snapshots.

This command starts from the compact metric summaries and manifests released
under ``docs/reproducibility/sources``. It reconstructs the reported tables; it
does not retrain or rerun the upstream tokenizers.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "docs" / "reproducibility" / "sources"

TABLE2_FIELDS = [
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
]
TABLE3_FIELDS = ["probe", "d", "without_probe", "with_probe", "source_evidence"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def one(rows: list[dict[str, str]], **criteria: str) -> dict[str, str]:
    matches = [row for row in rows if all(row.get(key) == value for key, value in criteria.items())]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one row for {criteria}, found {len(matches)}")
    return matches[0]


def build_table2() -> list[dict[str, str]]:
    grid_seeds = read_csv(SOURCE_DIR / "grid_ft_seed_summary.csv")
    grid_resid = read_csv(SOURCE_DIR / "grid_resid_comparison.csv")
    controls = read_csv(SOURCE_DIR / "control_summary.csv")
    rqmin = read_csv(SOURCE_DIR / "rqmin_reference.csv")[0]

    grid_ft = one(grid_seeds, seed="42")
    resid = one(grid_resid, method="resid_gaoq")
    category = one(controls, method="sanity_category_prefix")
    popularity = one(controls, method="sanity_popularity_balanced")
    hashed = one(controls, method="sanity_mod_collision_hash")

    cap_coverage = read_csv(SOURCE_DIR / "grid_cap_metrics" / "coverage_report.csv")[0]
    cap_d2 = one(read_csv(SOURCE_DIR / "grid_cap_metrics" / "d2_collision.csv"), prefix_depth="1")
    cap_d3 = one(read_csv(SOURCE_DIR / "grid_cap_metrics" / "d3_alignment.csv"), prefix_depth="1")
    cap_d4 = one(read_csv(SOURCE_DIR / "grid_cap_metrics" / "d4_head_tail.csv"), bucket="tail")
    cap_d5 = read_csv(SOURCE_DIR / "grid_cap_metrics" / "d5a_deployment_cost.csv")[0]

    source = "docs/reproducibility/sources/"
    return [
        {
            "artifact": "GRID-style ft",
            "group": "RQ-style exports",
            "items": "23742",
            "seeds": "3 (seed 42 shown)",
            "unique_sids": grid_ft["unique_sid"],
            "d2_aliasing_rate": grid_ft["full_collision_rate"],
            "d3_l1_weighted": grid_ft["d3_level1_weighted_recall"],
            "d4_tail_unique_ratio": grid_ft["d4_tail_sid_unique_ratio"],
            "d5_active_prefix_counts": grid_ft["prefix_counts"].replace(";", "/"),
            "source_evidence": source + "grid_ft_seed_summary.csv",
        },
        {
            "artifact": "GRID-style cap",
            "group": "RQ-style exports",
            "items": cap_coverage["sid_items"],
            "seeds": "1",
            "unique_sids": cap_d5["unique_sid"],
            "d2_aliasing_rate": cap_d2["full_collision_rate"],
            "d3_l1_weighted": cap_d3["weighted_collab_prefix_recall"],
            "d4_tail_unique_ratio": cap_d4["sid_unique_ratio"],
            "d5_active_prefix_counts": cap_d5["prefix_counts"].replace(";", "/"),
            "source_evidence": source + "grid_cap_metrics/*.csv",
        },
        {
            "artifact": "RQ-min ref",
            "group": "RQ-style exports",
            "items": rqmin["items"],
            "seeds": "1",
            "unique_sids": rqmin["unique_sid"],
            "d2_aliasing_rate": rqmin["full_collision_rate"],
            "d3_l1_weighted": rqmin["d3_l1_weighted"],
            "d4_tail_unique_ratio": rqmin["d4_tail_unique_ratio"],
            "d5_active_prefix_counts": rqmin["prefix_counts"],
            "source_evidence": source + "rqmin_reference.csv",
        },
        {
            "artifact": "ReSID",
            "group": "Named contrast",
            "items": resid["sid_items"],
            "seeds": "1",
            "unique_sids": resid["unique_sid"],
            "d2_aliasing_rate": resid["full_collision_rate"],
            "d3_l1_weighted": resid["d3_level1_weighted_recall"],
            "d4_tail_unique_ratio": resid["d4_tail_sid_unique_ratio"],
            "d5_active_prefix_counts": resid["prefix_counts"].replace(";", "/"),
            "source_evidence": source + "grid_resid_comparison.csv",
        },
        *[
            {
                "artifact": label,
                "group": "Controls",
                "items": "23742",
                "seeds": "n/a",
                "unique_sids": row["unique_sid"],
                "d2_aliasing_rate": row["full_collision_rate"],
                "d3_l1_weighted": row["d3_depth1_collab_recall"],
                "d4_tail_unique_ratio": row["tail_sid_unique_ratio"],
                "d5_active_prefix_counts": row["prefix_counts"].replace(";", "/"),
                "source_evidence": source + "control_summary.csv",
            }
            for label, row in [
                ("Cat-prefix", category),
                ("Pop-balanced", popularity),
                ("Hash-collide", hashed),
            ]
        ],
    ]


def build_table3() -> list[dict[str, str]]:
    aliasing = read_csv(SOURCE_DIR / "controller_qualified_aliasing.csv")
    capacity = read_csv(SOURCE_DIR / "controller_capacity_budget.csv")
    variable = read_csv(SOURCE_DIR / "controller_variable_depth.csv")

    hash_row = one(aliasing, method="sanity_mod_collision_hash")
    cooccur_row = one(aliasing, method="grid_official_rqkmeans_resid_feature_text")
    budget_row = one(capacity, method="controller_capacity_head_reserved_w24_d3")
    depth_row = one(variable, method="controller_variable_depth_head_long_tail_short_w64_maxd4")
    source = "docs/reproducibility/sources/"
    return [
        {
            "probe": "Qualified aliasing",
            "d": "D2",
            "without_probe": f"hash {float(hash_row['interaction_qualified_collision_lift']):.2f}x",
            "with_probe": f"co-occur {float(cooccur_row['interaction_qualified_collision_lift']):.2f}x",
            "source_evidence": source + "controller_qualified_aliasing.csv",
        },
        {
            "probe": "Capacity budget",
            "d": "D1/D4",
            "without_probe": f"head {float(budget_row['head_unique_ratio']):.3f}",
            "with_probe": f"tail {float(budget_row['tail_unique_ratio']):.3f}",
            "source_evidence": source + "controller_capacity_budget.csv",
        },
        {
            "probe": "Variable depth",
            "d": "D5",
            "without_probe": f"max-depth {int(depth_row['standard_prefix_counts'].split(';')[2]):,}",
            "with_probe": f"active {int(depth_row['effective_prefix_counts'].split(';')[2]):,}",
            "source_evidence": source + "controller_variable_depth.csv",
        },
    ]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    write_csv(args.output_dir / "table2_musical_diagnostic.csv", TABLE2_FIELDS, build_table2())
    write_csv(args.output_dir / "table3_probe_calibration.csv", TABLE3_FIELDS, build_table3())
    print(f"Rebuilt paper table snapshots in {args.output_dir}")


if __name__ == "__main__":
    main()
