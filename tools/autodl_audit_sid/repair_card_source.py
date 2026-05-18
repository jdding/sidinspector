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
    statuses = []

    old = "ckpt = torch.load(ckpt_path, map_location=torch.device('cpu'))"
    new = "ckpt = torch.load(ckpt_path, map_location=torch.device('cpu'), weights_only=False)"
    if new in text:
        statuses.append("weights_only_exists")
    elif old in text:
        text = text.replace(old, new)
        statuses.append("weights_only_patched")
    else:
        statuses.append("weights_only_unmatched")

    old = "tt = 0\n#There are often duplicate items in the dataset, and we no longer differentiate them\nwhile True:\n    if tt >= 30 or check_collision(all_indices_str):\n        break\n\n    collision_item_groups = get_collision_item(all_indices_str)\n    print(collision_item_groups)\n    print(len(collision_item_groups))\n"
    new = "tt = 0\nmax_collision_rounds = int(os.environ.get('CARD_GENERATE_MAX_COLLISION_ROUNDS', '30'))\nprint_collision_groups = os.environ.get('CARD_GENERATE_PRINT_COLLISIONS', '1') == '1'\n#There are often duplicate items in the dataset, and we no longer differentiate them\nwhile True:\n    if tt >= max_collision_rounds or check_collision(all_indices_str):\n        break\n\n    collision_item_groups = get_collision_item(all_indices_str)\n    if print_collision_groups:\n        print(collision_item_groups)\n    print(len(collision_item_groups))\n"
    if "max_collision_rounds = int(os.environ.get('CARD_GENERATE_MAX_COLLISION_ROUNDS'" in text:
        statuses.append("collision_controls_exist")
    elif old in text:
        text = text.replace(old, new)
        statuses.append("collision_controls_patched")
    else:
        statuses.append("collision_controls_unmatched")

    path.write_text(text)
    return ",".join(statuses)


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
    print(f"[CARD repair] generate_code patches: {status}")


if __name__ == "__main__":
    main()
