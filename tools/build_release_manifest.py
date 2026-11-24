#!/usr/bin/env python3
"""Build PACKAGE_MANIFEST.json and CHECKSUMS.sha256 for SIDInspector."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {"PACKAGE_MANIFEST.json", "CHECKSUMS.sha256"}
SKIP_PREFIXES = (".git/", "__pycache__/", ".pytest_cache/", "examples/toy_output/", "examples/reviewer_quickstart_output/")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_files() -> list[Path]:
    # Include git-tracked files plus untracked non-ignored files so newly created release files are indexed cleanly.
    tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
    untracked = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True
    ).splitlines()
    rel_paths = sorted(set(tracked) | set(untracked))
    files: list[Path] = []
    for rel in rel_paths:
        if rel in EXCLUDED or any(rel.startswith(prefix) for prefix in SKIP_PREFIXES):
            continue
        if rel.endswith(".pyc") or Path(rel).name == ".DS_Store":
            continue
        full = ROOT / rel
        if full.is_file():
            files.append(full)
    return files


def main() -> None:
    status = json.loads((ROOT / "RELEASE_STATUS.json").read_text(encoding="utf-8"))
    files = collect_files()
    entries = []
    checksum_lines = []
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        digest = sha256_file(path)
        size = path.stat().st_size
        entries.append({"path": rel, "sha256": digest, "bytes": size})
        checksum_lines.append(f"{digest}  {rel}")

    manifest = {
        "schema": "sidinspector.package_manifest.v1",
        "name": status["name"],
        "version": status["version"],
        "file_count": len(entries),
        "files": entries,
    }
    (ROOT / "PACKAGE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / "CHECKSUMS.sha256").write_text(
        "\n".join(checksum_lines) + "\n", encoding="utf-8"
    )
    print(f"Wrote PACKAGE_MANIFEST.json and CHECKSUMS.sha256 ({len(entries)} files)")


if __name__ == "__main__":
    main()
