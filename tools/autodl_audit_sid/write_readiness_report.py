"""Write a local AutoDL readiness report for AUDIT-SID."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import pandas as pd


def card_source_status(card_dir: Path = Path("_gate0_repos/CARD")) -> tuple[str, list[str]]:
    required = [
        card_dir / "rqvae4/main.py",
        card_dir / "rqvae4/generate_code.py",
        card_dir / "rqvae4/models/rqvae.py",
        card_dir / "rqvae4/models/layers.py",
        card_dir / "rqvae4/models/rq.py",
        card_dir / "rqvae4/models/vq.py",
    ]
    missing = [str(path) for path in required if not path.exists()]
    return ("OK" if not missing else "INCOMPLETE", missing)


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
    card_status, card_missing = card_source_status()

    if card_status == "OK":
        status = "TRANSFER_READY / RUNNER_READY / FULL_REPRO_BLOCKED_NO_GPU"
        preferred_label = "Preferred robust runner:"
        preferred_mode = "robust"
        followup = "Use `QUEUE_MODE=sweep` only after quick or robust passes."
    else:
        status = "QUICK_SMOKE_READY / FORMAL_GATE0_BLOCKED_CARD_SOURCE"
        preferred_label = "Only bounded quick smoke is recommended until CARD/Cluster-A source is repaired:"
        preferred_mode = "quick"
        followup = (
            "Do not run `robust`, `sweep`, or `quality` unless CARD source is repaired, "
            "or unless `ALLOW_RESID_ONLY=1` is intentionally set for ReSID-only debugging."
        )

    lines = [
        "# AUDIT-SID AutoDL Readiness Report",
        "",
        f"**Status**: {status}",
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
        "## Source Integrity",
        "",
        f"- CARD source status: `{card_status}`",
    ]
    if card_missing:
        lines.append("- CARD missing files:")
        for path in card_missing:
            lines.append(f"  - `{path}`")
        lines.append("- AutoDL queue default: `CARD_SOURCE_FAIL=skip`; ReSID runs continue and CARD runs write `SKIPPED.txt`.")

    lines.extend(
        [
        "",
        "## Experiment Matrix",
        "",
        "| Queue | Priority | Runs |",
        "|---|---:|---:|",
        ]
    )

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
            preferred_label,
            "",
            "```bash",
            "cd /root/autodl-tmp/Sec_phrase",
            f"QUEUE_MODE={preferred_mode} DEVICE=cuda:0 NUM_WORKERS=8 PYTHON_BIN=python3 \\",
            "bash tools/autodl_audit_sid/run_remote_audit_sid.sh",
            "```",
            "",
            followup,
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
