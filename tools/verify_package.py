#!/usr/bin/env python3
"""Verify that a clean SIDInspector checkout can run the core diagnostics."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED = [
    "README.md",
    "LICENSE",
    "pyproject.toml",
    "requirements.txt",
    "src/sidinspector/__init__.py",
    "src/sidinspector/metrics.py",
    "src/sidinspector/preflight.py",
    "src/sidinspector/churn.py",
    "src/sidinspector/adapters/grid.py",
    "src/sidinspector/baselines/rqkmeans.py",
    "examples/minimal_adapter.py",
    "examples/run_toy_diagnostic.py",
    "examples/run_reviewer_quickstart.py",
    "examples/sample_data/sid_codes.csv",
    "examples/sample_data/item_metadata.csv",
    "examples/sample_data/interactions.csv",
    "examples/reviewer_quickstart_data/sid_codes.csv",
    "examples/reviewer_quickstart_data/item_metadata.csv",
    "examples/reviewer_quickstart_data/interactions.csv",
    "docs/ADAPTER_TEMPLATE.md",
    "docs/DIAGNOSTICS.md",
]


FORBIDDEN_SUFFIXES = (".pdf", ".tex", ".pt", ".ckpt", ".tar.gz", ".zip")
FORBIDDEN_DIR_PARTS = {"archive", "logs", "cache"}


def require_file(path: str) -> None:
    if not (ROOT / path).is_file():
        raise FileNotFoundError(path)


def main() -> None:
    for path in REQUIRED:
        require_file(path)

    tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
    leaked = []
    for path in tracked:
        parts = set(Path(path).parts)
        if path.endswith(FORBIDDEN_SUFFIXES):
            leaked.append(path)
        elif parts & FORBIDDEN_DIR_PARTS:
            leaked.append(path)
    if leaked:
        formatted = "\n".join(f"  - {path}" for path in leaked[:40])
        raise RuntimeError(f"non-package files are still tracked:\n{formatted}")

    subprocess.run(
        [sys.executable, "-c", "import sidinspector; print(sidinspector.__name__)"],
        cwd=ROOT,
        check=True,
    )
    with tempfile.TemporaryDirectory(prefix="sidinspector-verify-") as tmp:
        tmp_path = Path(tmp)
        subprocess.run(
            [sys.executable, "examples/run_toy_diagnostic.py", "--output-dir", str(tmp_path / "toy_output")],
            cwd=ROOT,
            check=True,
        )
        subprocess.run(
            [
                sys.executable,
                "examples/run_reviewer_quickstart.py",
                "--output-dir",
                str(tmp_path / "reviewer_quickstart"),
            ],
            cwd=ROOT,
            check=True,
        )
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=ROOT, check=True)
    print("SIDInspector package verification passed.")
    print("Verified: package import, toy diagnostic, reviewer quickstart, and unit tests.")


if __name__ == "__main__":
    main()
