#!/usr/bin/env python3
"""Validate SIDInspector release integrity, manifest hashes, and core workflows."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_manifest() -> int:
    manifest_path = ROOT / "PACKAGE_MANIFEST.json"
    checksums_path = ROOT / "CHECKSUMS.sha256"
    if not manifest_path.is_file() or not checksums_path.is_file():
        raise FileNotFoundError("PACKAGE_MANIFEST.json or CHECKSUMS.sha256 is missing.")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = manifest.get("files", [])
    if len(entries) != manifest.get("file_count"):
        raise ValueError("PACKAGE_MANIFEST.json file_count mismatch.")

    manifest_map: dict[str, str] = {}
    for row in entries:
        rel = row["path"]
        target = ROOT / rel
        if not target.is_file():
            raise FileNotFoundError(f"Manifest entry missing on disk: {rel}")
        actual = sha256_file(target)
        if actual != row["sha256"]:
            raise ValueError(f"SHA-256 mismatch for {rel}: expected {row['sha256']}, got {actual}")
        manifest_map[rel] = actual

    checksum_map: dict[str, str] = {}
    for line in checksums_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        checksum_map[rel] = digest

    if checksum_map != manifest_map:
        raise ValueError("CHECKSUMS.sha256 does not match PACKAGE_MANIFEST.json.")
    return len(entries)


def main() -> None:
    verified = verify_manifest()
    print(f"Verified SHA-256 integrity for {verified} manifest files.")

    # Verify browser_example.py runs purely on standard library
    proc = subprocess.run(
        [sys.executable, "-B", str(ROOT / "demo" / "browser_example.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(proc.stdout)
    if payload.get("status") != "pass" or len(payload.get("table2", [])) != 7 or len(payload.get("table3", [])) != 3:
        raise RuntimeError("demo/browser_example.py returned unexpected payload.")
    print("Verified pure-Python browser workbench payload (7 Table 2 rows, 3 Table 3 rows).")

    # Run v1.0 package verifier (covers quickstart, toy diagnostic, table rebuild, and tests)
    subprocess.run([sys.executable, "-B", str(ROOT / "tools" / "verify_package.py")], cwd=ROOT, check=True)
    print("PASS_SIDINSPECTOR_RELEASE_VALIDATION")


if __name__ == "__main__":
    main()
