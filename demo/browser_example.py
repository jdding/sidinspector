"""Run SIDInspector's diagnostic workflows in pure Python (Pyodide or local)."""

from __future__ import annotations

import contextlib
import csv
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from sidinspector.pure_diagnostics import (  # noqa: E402
    compute_churn_pure,
    parse_interactions_csv_text,
    parse_metadata_csv_text,
    parse_sid_csv_text,
    run_mapping_diagnostics,
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _run_mechanism_checks(
    base_rows: list[dict[str, Any]],
    interactions: list[dict[str, str]],
    metadata: dict[str, dict[str, str]],
) -> dict[str, Any]:
    """Run live controlled mechanism perturbations (collision injection + D6 refresh churn)."""
    base_diag = run_mapping_diagnostics(base_rows, interactions=interactions, metadata=metadata)

    # Perturbation 1: collapse half of items onto shared leaves to verify D2 + D4 reaction
    aliased_rows = []
    for idx, row in enumerate(base_rows):
        lvls = list(row["levels"])
        if idx % 2 == 1 and idx > 0:
            lvls = list(base_rows[idx - 1]["levels"])
        aliased_rows.append({**row, "levels": lvls, "sid": "-".join(lvls)})
    aliased_diag = run_mapping_diagnostics(aliased_rows, interactions=interactions, metadata=metadata)

    # Perturbation 2: simulate a tokenizer refresh changing 25% of items (3 of 12)
    refreshed_rows = []
    for idx, row in enumerate(base_rows):
        lvls = list(row["levels"])
        if idx % 4 == 0:
            lvls[-1] = str(int(lvls[-1]) + 50)
        if idx == 0:
            lvls[0] = str(int(lvls[0]) + 10)
        refreshed_rows.append({**row, "levels": lvls, "sid": "-".join(lvls)})
    churn_rows = compute_churn_pure(base_rows, refreshed_rows)

    return {
        "collision_injection": {
            "baseline_d2": base_diag["d2"][0]["full_collision_rate"],
            "injected_d2": aliased_diag["d2"][0]["full_collision_rate"],
            "baseline_unique_sids": base_diag["d5"]["unique_sid"],
            "injected_unique_sids": aliased_diag["d5"]["unique_sid"],
            "baseline_d4_tail_singleton": next(
                r["global_singleton_ratio"] for r in base_diag["d4"] if r["bucket"] == "tail"
            ),
            "injected_d4_tail_singleton": next(
                r["global_singleton_ratio"] for r in aliased_diag["d4"] if r["bucket"] == "tail"
            ),
        },
        "d6_refresh_churn": churn_rows,
    }


def _verify_cikm_tables() -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    steps: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="sidinspector-tables-") as tmp_dir:
        out = Path(tmp_dir)
        previous_argv = sys.argv
        buf = io.StringIO()
        sys.argv = ["build_paper_tables.py", "--output-dir", str(out)]
        try:
            with contextlib.redirect_stdout(buf):
                runpy.run_path(str(ROOT / "tools" / "build_paper_tables.py"), run_name="__main__")
        finally:
            sys.argv = previous_argv

        rebuilt_t2 = _read_csv(out / "table2_musical_diagnostic.csv")
        frozen_t2 = _read_csv(ROOT / "docs" / "reproducibility" / "table2_musical_diagnostic.csv")
        if rebuilt_t2 != frozen_t2:
            raise ValueError("Rebuilt Table 2 does not match frozen CIKM 2026 snapshot.")

        rebuilt_t3 = _read_csv(out / "table3_probe_calibration.csv")
        frozen_t3 = _read_csv(ROOT / "docs" / "reproducibility" / "table3_probe_calibration.csv")
        if rebuilt_t3 != frozen_t3:
            raise ValueError("Rebuilt Table 3 does not match frozen CIKM 2026 snapshot.")

        steps.append(
            {
                "script": "tools/build_paper_tables.py",
                "output": f"Exact match: Table 2 ({len(rebuilt_t2)} rows) & Table 3 ({len(rebuilt_t3)} rows)",
            }
        )
        return rebuilt_t2, rebuilt_t3, steps


def audit_custom_csv(
    sid_csv_text: str,
    interactions_csv_text: str = "",
    metadata_csv_text: str = "",
) -> dict[str, Any]:
    """Audit user-provided CSV text strictly client-side (no uploads)."""
    parsed = parse_sid_csv_text(sid_csv_text)
    interactions = parse_interactions_csv_text(interactions_csv_text) if interactions_csv_text.strip() else []
    metadata = parse_metadata_csv_text(metadata_csv_text) if metadata_csv_text.strip() else {}
    report = run_mapping_diagnostics(parsed["rows"], interactions=interactions, metadata=metadata)
    return {
        "status": "pass",
        "custom": True,
        "report": report,
        "python": sys.version.split()[0],
    }


def run_example() -> dict[str, Any]:
    """Run all built-in SIDInspector diagnostic workflows and CIKM table verification."""
    qs_dir = ROOT / "examples" / "reviewer_quickstart_data"
    parsed = parse_sid_csv_text((qs_dir / "sid_codes.csv").read_text(encoding="utf-8"))
    interactions = parse_interactions_csv_text((qs_dir / "interactions.csv").read_text(encoding="utf-8"))
    metadata = parse_metadata_csv_text((qs_dir / "item_metadata.csv").read_text(encoding="utf-8"))

    quickstart_diag = run_mapping_diagnostics(parsed["rows"], interactions=interactions, metadata=metadata)
    mechanisms = _run_mechanism_checks(parsed["rows"], interactions, metadata)
    table2_rows, table3_rows, steps = _verify_cikm_tables()

    steps.insert(
        0,
        {
            "script": "src/sidinspector/pure_diagnostics.py",
            "output": (
                f"Audited {quickstart_diag['d5']['items']} items, depth {quickstart_diag['d5']['sid_length']}, "
                f"{quickstart_diag['d5']['unique_sid']} unique SIDs, D2={quickstart_diag['d2'][0]['full_collision_rate']:.3f}"
            ),
        },
    )
    steps.append(
        {
            "script": "demo/browser_example.py (mechanism + D6 churn)",
            "output": (
                f"Collision lift {mechanisms['collision_injection']['baseline_d2']:.3f} -> "
                f"{mechanisms['collision_injection']['injected_d2']:.3f}; "
                f"D6 depth-3 churn={mechanisms['d6_refresh_churn'][-1]['churn_rate_common']:.3f}"
            ),
        }
    )

    official_adapters = _read_csv(ROOT / "docs" / "reproducibility" / "official_adapter_metrics_snapshot.csv")
    extensions = _read_csv(ROOT / "docs" / "reproducibility" / "extension_checks_snapshot.csv")
    release_meta = json.loads((ROOT / "RELEASE_STATUS.json").read_text(encoding="utf-8"))

    return {
        "status": "pass",
        "version": release_meta["version"],
        "paper_doi": release_meta["paper_doi"],
        "quickstart": quickstart_diag,
        "mechanisms": mechanisms,
        "table2": table2_rows,
        "table3": table3_rows,
        "official_adapters": official_adapters,
        "extensions": extensions,
        "steps": steps,
        "python": sys.version.split()[0],
    }


if __name__ == "__main__":
    print(json.dumps(run_example()))
