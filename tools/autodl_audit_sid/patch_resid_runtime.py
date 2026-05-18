#!/usr/bin/env python3
"""Apply auditable runtime patches to the vendored ReSID checkout."""

from __future__ import annotations

import argparse
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> tuple[str, bool]:
    if new in text:
        return text, False
    if old not in text:
        raise RuntimeError(f"Patch context not found for {label}")
    return text.replace(old, new, 1), True


def patch_utils(resid_dir: Path) -> list[str]:
    path = resid_dir / "utils.py"
    text = path.read_text()
    changed = []

    new_text = text.replace(
        "num_workers=4,",
        'num_workers=getattr(args, "num_workers", 4),',
    )
    if new_text != text:
        changed.append("utils.num_workers")
        text = new_text

    new_text = text.replace(
        "pin_memory=True,",
        "pin_memory=torch.cuda.is_available(),",
    )
    if new_text != text:
        changed.append("utils.pin_memory")
        text = new_text

    if changed:
        path.write_text(text)
    return changed


def patch_gaoq(resid_dir: Path) -> list[str]:
    path = resid_dir / "model" / "gaoq.py"
    text = path.read_text()
    changed = []

    old = '        use_balanced = getattr(self.args, "use_balancedkmeans", False)\n'
    new = (
        '        use_balanced = getattr(self.args, "use_balancedkmeans", False)\n'
        '        kmeans_n_jobs = int(os.environ.get("GAOQ_KMEANS_N_JOBS", "1"))\n'
    )
    text, did_change = replace_once(text, old, new, "gaoq.kmeans_n_jobs")
    if did_change:
        changed.append("gaoq.kmeans_n_jobs")

    old = (
        "                random_state=random_state,\n"
        "                n_init=3,\n"
        "            )\n"
    )
    new = (
        "                random_state=random_state,\n"
        "                n_init=3,\n"
        "                n_jobs=kmeans_n_jobs,\n"
        "            )\n"
    )
    text, did_change = replace_once(text, old, new, "gaoq.kmeans_constrained_n_jobs")
    if did_change:
        changed.append("gaoq.kmeans_constrained_n_jobs")

    if changed:
        path.write_text(text)
    return changed


def patch_custom_t5(resid_dir: Path) -> list[str]:
    path = resid_dir / "model" / "module" / "custom_t5.py"
    text = path.read_text()
    changed = []

    old = (
        "from transformers.pytorch_utils import (\n"
        "    find_pruneable_heads_and_indices,\n"
        "    prune_linear_layer,\n"
        ")\n"
    )
    new = (
        "from transformers.pytorch_utils import prune_linear_layer\n"
        "try:\n"
        "    from transformers.pytorch_utils import find_pruneable_heads_and_indices\n"
        "except ImportError:\n"
        "    def find_pruneable_heads_and_indices(heads, n_heads, head_size, already_pruned_heads):\n"
        "        mask = torch.ones(n_heads, head_size)\n"
        "        heads = set(heads) - already_pruned_heads\n"
        "        for head in heads:\n"
        "            head = head - sum(1 if h < head else 0 for h in already_pruned_heads)\n"
        "            mask[head] = 0\n"
        "        mask = mask.view(-1).contiguous().eq(1)\n"
        "        index = torch.arange(len(mask))[mask].long()\n"
        "        return heads, index\n"
    )
    text, did_change = replace_once(text, old, new, "custom_t5.prune_heads_fallback")
    if did_change:
        changed.append("custom_t5.prune_heads_fallback")

    if changed:
        path.write_text(text)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resid-dir", type=Path, required=True)
    args = parser.parse_args()

    if not args.resid_dir.exists():
        raise SystemExit(f"Missing ReSID directory: {args.resid_dir}")

    changed = []
    changed.extend(patch_utils(args.resid_dir))
    changed.extend(patch_gaoq(args.resid_dir))
    changed.extend(patch_custom_t5(args.resid_dir))

    if changed:
        print("RESID_RUNTIME_PATCHED " + ",".join(changed))
    else:
        print("RESID_RUNTIME_PATCHED none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
