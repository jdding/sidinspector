"""Run AUDIT-SID metrics on public DACT bundled code artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from audit_sid.adapters.dact import normalize_dact_codes
from audit_sid.metrics import (
    alignment,
    collision,
    deployment_cost,
    head_tail_capacity,
    utilization,
    validate_inputs,
)
from compute_sid_churn import compute_churn


def sequence_interactions(path: Path, split: str, dataset: str) -> pd.DataFrame:
    frame = pd.read_parquet(path)
    rows: list[dict[str, object]] = []
    for row in frame.itertuples(index=False):
        user_id = int(getattr(row, "user"))
        target = int(getattr(row, "target"))
        history = list(getattr(row, "history"))
        for pos, item_id in enumerate(history):
            rows.append({"dataset": dataset, "user_id": user_id, "item_id": int(item_id), "timestamp": pos, "split": split})
        rows.append(
            {
                "dataset": dataset,
                "user_id": user_id,
                "item_id": target,
                "timestamp": len(history),
                "split": split,
            }
        )
    return pd.DataFrame(rows).drop_duplicates(["dataset", "user_id", "item_id", "split"])


def metadata_from_codes(sid: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({"dataset": sid["dataset"].iloc[0], "item_id": sid["item_id"].astype(int)})


def run_metrics(sid: pd.DataFrame, item_metadata: pd.DataFrame, interactions: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    tables = {
        "coverage_report.csv": validate_inputs(sid, item_metadata, interactions),
        "d1_utilization.csv": utilization(sid),
        "d2_collision.csv": collision(sid, interactions),
        "d3_alignment.csv": alignment(sid, item_metadata, interactions),
        "d4_head_tail.csv": head_tail_capacity(sid, interactions),
        "d5a_deployment_cost.csv": deployment_cost(sid),
    }
    for name, table in tables.items():
        table.to_csv(output_dir / name, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dact-data-dir", type=Path, default=Path("_gate0_repos/DACT/data/Tools"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="Tools")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    artifacts = [
        ("Tools_0.6_cf.npy", "dact_cf_0.6", "train_0.6.parquet"),
        ("Tools_0.7_dact.npy", "dact_0.7", "train_0.7.parquet"),
    ]
    normalized_sid: dict[str, pd.DataFrame] = {}
    for codes_name, method, interactions_name in artifacts:
        sid = normalize_dact_codes(args.dact_data_dir / codes_name, method=method, dataset=args.dataset_name)
        normalized_sid[method] = sid
        run_dir = args.output_dir / method
        normalized_dir = run_dir / "normalized"
        normalized_dir.mkdir(parents=True, exist_ok=True)
        sid.to_parquet(normalized_dir / "sid_assignments.parquet", index=False)
        item_metadata = metadata_from_codes(sid)
        item_metadata.to_parquet(normalized_dir / "item_metadata.parquet", index=False)
        interactions = sequence_interactions(args.dact_data_dir / interactions_name, split="train", dataset=args.dataset_name)
        interactions = interactions[interactions["item_id"].isin(set(sid["item_id"].astype(int)))]
        interactions.to_parquet(normalized_dir / "interactions.parquet", index=False)
        run_metrics(sid, item_metadata, interactions, run_dir / "metrics")
        print(f"[DACT smoke] {method}: items={len(sid)} interactions={len(interactions)} output={run_dir}")

    churn = compute_churn(normalized_sid["dact_cf_0.6"], normalized_sid["dact_0.7"])
    churn_path = args.output_dir / "d6_churn_0.6_to_0.7.csv"
    churn.to_csv(churn_path, index=False)
    print(f"[DACT smoke] D6 churn: output={churn_path}")


if __name__ == "__main__":
    main()
