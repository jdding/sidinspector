"""Download selected PIIR/ReSID-dataset categories for AUDIT-SID."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from huggingface_hub import hf_hub_download, list_repo_files


REPO_ID = "PIIR/ReSID-dataset"
REPO_TYPE = "dataset"
DEFAULT_REVISION = "main"
DEFAULT_CATEGORIES = ("Sports_and_Outdoors",)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def wanted_file(filename: str, category: str) -> bool:
    prefix = f"{category}/leave_one_out/dataset/"
    if not filename.startswith(prefix):
        return False
    name = Path(filename).name
    if name.startswith("."):
        return False
    return filename.endswith((".parquet", ".json"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Download ReSID processed category shards.")
    parser.add_argument("--categories", nargs="+", default=list(DEFAULT_CATEGORIES))
    parser.add_argument("--revision", default=DEFAULT_REVISION)
    parser.add_argument(
        "--local-dir",
        type=Path,
        default=Path(os.environ.get("RESID_DATASET_ROOT", "_gate0_repos/ReSID-dataset")),
    )
    parser.add_argument("--manifest", type=Path, default=Path("_gate0_artifacts/resid_dataset_download_manifest.json"))
    args = parser.parse_args()

    repo_files = list_repo_files(REPO_ID, repo_type=REPO_TYPE, revision=args.revision)
    downloaded: list[dict[str, object]] = []

    for category in args.categories:
        matches = sorted(filename for filename in repo_files if wanted_file(filename, category))
        if not matches:
            raise SystemExit(f"No downloadable dataset files found for category: {category}")
        for filename in matches:
            path = Path(
                hf_hub_download(
                    repo_id=REPO_ID,
                    repo_type=REPO_TYPE,
                    revision=args.revision,
                    filename=filename,
                    local_dir=args.local_dir,
                )
            )
            downloaded.append(
                {
                    "category": category,
                    "filename": filename,
                    "path": str(path),
                    "size_bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )
            print(path)

    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(downloaded, indent=2, sort_keys=True) + "\n")
    print(f"manifest={args.manifest}")


if __name__ == "__main__":
    main()
