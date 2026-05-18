"""Write a local AutoDL readiness report for AUDIT-SID."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import pandas as pd


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def count_rows(path: Path) -> int:
    return int(pd.read_parquet(path).shape[0])


def main() -> None:
    parser = argparse.ArgumentParser(description="Write AUDIT-SID AutoDL readiness report.")
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--matrix", type=Path, default=Path("tools/autodl_audit_sid/gate0_experiment_matrix.tsv"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    item_metadata = Path("_gate0_artifacts/resid_musical_normalized/item_metadata.parquet")
    interactions = Path("_gate0_artifacts/resid_musical_normalized/interactions.parquet")
    matrix = pd.read_csv(args.matrix, sep="\t")

    lines = [
        "# AUDIT-SID AutoDL Readiness Report",
        "",
        "**Status**: TRANSFER_READY / RUNNER_READY / FULL_REPRO_BLOCKED_NO_GPU",
        "",
        "## Bundle",
        "",
        f"- Path: `{args.bundle}`",
        f"- Size bytes: `{args.bundle.stat().st_size}`",
        f"- SHA256: `{sha256(args.bundle)}`",
        "",
        "## Input Artifacts",
        "",
        f"- item_metadata rows: `{count_rows(item_metadata)}`",
        f"- interactions rows: `{count_rows(interactions)}`",
        f"- item_metadata SHA256: `{sha256(item_metadata)}`",
        f"- interactions SHA256: `{sha256(interactions)}`",
        "",
        "## Experiment Matrix",
        "",
        "| Queue | Priority | Runs |",
        "|---|---:|---:|",
    ]

    for (queue, priority), group in matrix.groupby(["queue", "priority"], sort=False):
        lines.append(f"| `{queue}` | `{priority}` | {len(group)} |")

    lines.extend(
        [
            "",
            "## Queue Details",
            "",
            "| Queue | Priority | Exp ID | Runner | Purpose |",
            "|---|---|---|---|---|",
        ]
    )
    for row in matrix.itertuples(index=False):
        lines.append(
            f"| `{row.queue}` | `{row.priority}` | `{row.exp_id}` | `{row.runner}` | {row.purpose} |"
        )

    lines.extend(
        [
            "",
            "## Launch Command",
            "",
            "Preferred robust runner:",
            "",
            "```bash",
            "cd /root/autodl-tmp/Sec_phrase",
            "QUEUE_MODE=robust DEVICE=cuda:0 NUM_WORKERS=8 PYTHON_BIN=python3 \\",
            "bash tools/autodl_audit_sid/run_remote_audit_sid.sh",
            "```",
            "",
            "Use `QUEUE_MODE=sweep` only after quick or robust passes.",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
