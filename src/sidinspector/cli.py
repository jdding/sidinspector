"""Unified command-line entry point for SIDInspector workflows."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import subprocess
import sys

from sidinspector import __version__
from sidinspector.pure_diagnostics import load_csv_bundle


REPO_ROOT = Path(__file__).resolve().parents[2]

SCRIPT_COMMANDS: dict[str, tuple[str, str]] = {
    "quickstart": (
        "examples/run_reviewer_quickstart.py",
        "Run the bundled reviewer quickstart (normalize, preflight, D1-D5 CSVs).",
    ),
    "verify-tables": (
        "tools/verify_reproducibility_matrix.py",
        "Rebuild CIKM 2026 Tables 2 & 3 from compact sources and verify row-by-row.",
    ),
    "validate": (
        "tools/validate_release.py",
        "Verify SHA-256 manifest integrity and run the full package verification suite.",
    ),
    "demo": (
        "tools/serve_demo.py",
        "Launch the local browser workbench for SIDInspector workflows.",
    ),
}

MODULE_COMMANDS: dict[str, tuple[str, str]] = {
    "preflight": (
        "sidinspector.preflight",
        "Validate normalized sid_assignments, item_metadata, and interactions parquet tables.",
    ),
    "metrics": (
        "sidinspector.metrics",
        "Compute D1-D5 diagnostic CSV reports on normalized parquet inputs.",
    ),
    "churn": (
        "sidinspector.churn",
        "Compute D6 paired refresh churn between two normalized SID assignment tables.",
    ),
    "probe": (
        "sidinspector.downstream_probe",
        "Run the optional fixed-reranker candidate-exposure probe from a manifest.",
    ),
}


def _resolve_script(rel_path: str) -> Path:
    script = (REPO_ROOT / rel_path).resolve()
    if not script.is_file():
        raise FileNotFoundError(
            f"SIDInspector script not found at {script}. Install editable from a tagged checkout "
            "(`pip install -e .`) or run from the repository root."
        )
    return script


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _run_csv_audit(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="sidinspector audit",
        description="Run D1-D5 mapping diagnostics directly on CSV inputs without manual normalization.",
    )
    parser.add_argument("--sid-csv", type=Path, required=True, help="CSV with item_id and sid_0..sid_L (or sid).")
    parser.add_argument("--interactions-csv", type=Path, default=None, help="Optional CSV with user_id,item_id[,split].")
    parser.add_argument("--metadata-csv", type=Path, default=None, help="Optional CSV with item_id[,category,title].")
    parser.add_argument("--output-dir", type=Path, default=None, help="Optional directory to write JSON and CSV reports.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON summary to stdout.")
    args = parser.parse_args(argv)

    report = load_csv_bundle(args.sid_csv, args.interactions_csv, args.metadata_csv)
    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "audit_summary.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        _write_csv(args.output_dir / "d1_utilization.csv", report["d1"])
        _write_csv(args.output_dir / "d2_collision.csv", report["d2"])
        _write_csv(args.output_dir / "d3_alignment.csv", report["d3"])
        _write_csv(args.output_dir / "d4_head_tail.csv", report["d4"])
        _write_csv(args.output_dir / "d5a_deployment_cost.csv", [
            {k: v for k, v in report["d5"].items() if not isinstance(v, list)}
        ])

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    d5 = report["d5"]
    d2_l1 = report["d2"][0]
    d3_l1 = report["d3"][0]
    tail = next((row for row in report["d4"] if row["bucket"] == "tail"), None)
    print(f"SIDInspector {__version__} · CSV Audit Summary")
    print(f"  Items: {d5['items']} | Depth: {d5['sid_length']} | Unique SIDs: {d5['unique_sid']}")
    print(
        f"  D2 full aliasing: {d2_l1['full_collision_rate']:.4f} "
        f"({d2_l1['full_collision_items']} items in {d2_l1['full_collision_groups']} shared leaves)"
    )
    print(
        f"  D3 depth-1 recall: {d3_l1['weighted_collab_prefix_recall']:.4f} "
        f"(edges={d3_l1['retained_edges']}, users={d3_l1['users_used']})"
    )
    if tail is not None:
        print(
            f"  D4 tail unique ratio: {tail['sid_unique_ratio']:.4f} | "
            f"tail global singleton: {tail['global_singleton_ratio']:.4f}"
        )
    print(f"  D5 active prefixes: {d5['prefix_counts']}")
    if args.output_dir is not None:
        print(f"  Reports written to: {args.output_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    epilog_lines = ["Available subcommands:"]
    epilog_lines.append("  audit           Run D1-D5 mapping diagnostics directly on CSV inputs.")
    for name, (_, desc) in SCRIPT_COMMANDS.items():
        epilog_lines.append(f"  {name:<15s} {desc}")
    for name, (_, desc) in MODULE_COMMANDS.items():
        epilog_lines.append(f"  {name:<15s} {desc}")
    epilog_lines.append("")
    epilog_lines.append("Pass `-h` after a subcommand to see its options (e.g. `sidinspector audit -h`).")

    all_commands = sorted({"audit", *SCRIPT_COMMANDS, *MODULE_COMMANDS})
    parser = argparse.ArgumentParser(
        prog="sidinspector",
        description="SIDInspector CLI: Mapping-first diagnostics for Semantic-ID tokenizers (CIKM 2026).",
        epilog="\n".join(epilog_lines),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"SIDInspector {__version__}")
    parser.add_argument("command", choices=all_commands, help="Workflow subcommand to execute.")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments forwarded to the subcommand.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    parsed = parser.parse_args(argv)
    forwarded = list(parsed.args)
    if forwarded and forwarded[0] == "--":
        forwarded = forwarded[1:]

    if parsed.command == "audit":
        return _run_csv_audit(forwarded)
    if parsed.command in SCRIPT_COMMANDS:
        rel_path, _ = SCRIPT_COMMANDS[parsed.command]
        script = _resolve_script(rel_path)
        proc = subprocess.run([sys.executable, "-B", str(script), *forwarded], check=False)
        return proc.returncode
    module_name, _ = MODULE_COMMANDS[parsed.command]
    proc = subprocess.run([sys.executable, "-B", "-m", module_name, *forwarded], check=False)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
