"""Repair missing CARD RQ-VAE source files from tracked compatibility templates."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def copy_if_needed(src: Path, dst: Path, overwrite: bool) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and not overwrite:
        return "exists"
    shutil.copyfile(src, dst)
    return "written"


def patch_generate_code(card_dir: Path) -> str:
    path = card_dir / "rqvae4/generate_code.py"
    if not path.exists():
        return "missing"
    text = path.read_text()
    old = "ckpt = torch.load(ckpt_path, map_location=torch.device('cpu'))"
    new = "ckpt = torch.load(ckpt_path, map_location=torch.device('cpu'), weights_only=False)"
    if new in text:
        return "exists"
    if old not in text:
        return "unmatched"
    path.write_text(text.replace(old, new))
    return "patched"


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply tracked CARD RQ-VAE source repair templates.")
    parser.add_argument("--card-dir", type=Path, default=Path("_gate0_repos/CARD"))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    template_dir = Path(__file__).resolve().parent / "card_source_repair"
    targets = [
        (template_dir / "rq.py", args.card_dir / "rqvae4/models/rq.py"),
        (template_dir / "vq.py", args.card_dir / "rqvae4/models/vq.py"),
        (template_dir / "root_vq.py", args.card_dir / "rqvae4/vq.py"),
    ]
    for src, dst in targets:
        status = copy_if_needed(src, dst, args.overwrite)
        print(f"[CARD repair] {status}: {dst}")
    status = patch_generate_code(args.card_dir)
    print(f"[CARD repair] generate_code torch.load weights_only=False: {status}")


if __name__ == "__main__":
    main()
