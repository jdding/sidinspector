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

    old = "from scipy.optimize import linear_sum_assignment\n"
    new = (
        "from scipy.optimize import linear_sum_assignment\n"
        "from joblib import Parallel, delayed\n"
    )
    text, did_change = replace_once(text, old, new, "gaoq.joblib_import")
    if did_change:
        changed.append("gaoq.joblib_import")

    old = '        use_balanced = getattr(self.args, "use_balancedkmeans", False)\n'
    new = (
        '        use_balanced = getattr(self.args, "use_balancedkmeans", False)\n'
        '        kmeans_n_jobs = int(os.environ.get("GAOQ_KMEANS_N_JOBS", "1"))\n'
        '        kmeans_n_init = int(os.environ.get("GAOQ_KMEANS_N_INIT", "3"))\n'
    )
    text, did_change = replace_once(text, old, new, "gaoq.kmeans_n_jobs")
    if did_change:
        changed.append("gaoq.kmeans_n_jobs")

    old = (
        "                random_state=random_state,\n"
        "                n_init=3,\n"
        "                n_jobs=kmeans_n_jobs,\n"
        "            )\n"
    )
    new = (
        "                random_state=random_state,\n"
        "                n_init=kmeans_n_init,\n"
        "                n_jobs=kmeans_n_jobs,\n"
        "            )\n"
    )
    if new not in text:
        if old not in text:
            old_without_n_jobs = (
                "                random_state=random_state,\n"
                "                n_init=3,\n"
                "            )\n"
            )
            new_with_n_jobs = (
                "                random_state=random_state,\n"
                "                n_init=kmeans_n_init,\n"
                "                n_jobs=kmeans_n_jobs,\n"
                "            )\n"
            )
            text, did_change = replace_once(
                text,
                old_without_n_jobs,
                new_with_n_jobs,
                "gaoq.kmeans_constrained_n_jobs",
            )
        else:
            text = text.replace(old, new, 1)
            did_change = True
        if did_change:
            changed.append("gaoq.kmeans_constrained_n_jobs")

    old = """        for i in np.unique(level1_labels):
            mask = level1_labels == i
            sub_x = x[mask]

            km_level2 = self._make_kmeans(self.b2, sub_x.shape[0], random_state=0)
            km_level2.fit(sub_x)

            sub_centers = km_level2.cluster_centers_
            sub_labels = km_level2.labels_

            level2_centers_per_item[mask] = sub_centers[sub_labels]

            residual_centers = sub_centers - level1_centers[i]

            global_id_mapping, _ = self.match_embeddings_hungarian(
                residual_centers, global2_centers
            )

            level2_ids[mask] = global_id_mapping[sub_labels]
"""
    new = """        level2_parallel_jobs = int(os.environ.get("GAOQ_LEVEL2_PARALLEL_JOBS", "1"))
        level2_parallel_backend = os.environ.get("GAOQ_LEVEL2_PARALLEL_BACKEND", "loky")
        level1_unique = np.unique(level1_labels)
        print(
            f"Level2 group count = {len(level1_unique)}, "
            f"parallel jobs = {level2_parallel_jobs}, backend = {level2_parallel_backend}"
        )

        def fit_level2_group(i):
            indices = np.flatnonzero(level1_labels == i)
            sub_x = x[indices]

            old_kmeans_n_jobs = os.environ.get("GAOQ_KMEANS_N_JOBS")
            if level2_parallel_jobs > 1:
                os.environ["GAOQ_KMEANS_N_JOBS"] = "1"
            try:
                km_level2 = self._make_kmeans(self.b2, sub_x.shape[0], random_state=0)
            finally:
                if level2_parallel_jobs > 1:
                    if old_kmeans_n_jobs is None:
                        os.environ.pop("GAOQ_KMEANS_N_JOBS", None)
                    else:
                        os.environ["GAOQ_KMEANS_N_JOBS"] = old_kmeans_n_jobs

            km_level2.fit(sub_x)

            sub_centers = km_level2.cluster_centers_
            sub_labels = km_level2.labels_
            sub_level2_centers = sub_centers[sub_labels]

            residual_centers = sub_centers - level1_centers[i]

            global_id_mapping, _ = self.match_embeddings_hungarian(
                residual_centers, global2_centers
            )

            sub_level2_ids = global_id_mapping[sub_labels]
            return indices, sub_level2_ids, sub_level2_centers

        if level2_parallel_jobs > 1 and len(level1_unique) > 1:
            level2_results = Parallel(
                n_jobs=level2_parallel_jobs,
                backend=level2_parallel_backend,
            )(
                delayed(fit_level2_group)(i) for i in level1_unique
            )
        else:
            level2_results = [fit_level2_group(i) for i in level1_unique]

        for indices, sub_level2_ids, sub_level2_centers in level2_results:
            level2_centers_per_item[indices] = sub_level2_centers
            level2_ids[indices] = sub_level2_ids
"""
    if new not in text:
        if old in text:
            text = text.replace(old, new, 1)
            did_change = True
        else:
            old_previous_parallel = """        level2_parallel_jobs = int(os.environ.get("GAOQ_LEVEL2_PARALLEL_JOBS", "1"))
        level1_unique = np.unique(level1_labels)
        print(f"Level2 group count = {len(level1_unique)}, parallel jobs = {level2_parallel_jobs}")

        def fit_level2_group(i):
            indices = np.flatnonzero(level1_labels == i)
            sub_x = x[indices]

            old_kmeans_n_jobs = os.environ.get("GAOQ_KMEANS_N_JOBS")
            if level2_parallel_jobs > 1:
                os.environ["GAOQ_KMEANS_N_JOBS"] = "1"
            try:
                km_level2 = self._make_kmeans(self.b2, sub_x.shape[0], random_state=0)
            finally:
                if level2_parallel_jobs > 1:
                    if old_kmeans_n_jobs is None:
                        os.environ.pop("GAOQ_KMEANS_N_JOBS", None)
                    else:
                        os.environ["GAOQ_KMEANS_N_JOBS"] = old_kmeans_n_jobs

            km_level2.fit(sub_x)

            sub_centers = km_level2.cluster_centers_
            sub_labels = km_level2.labels_
            sub_level2_centers = sub_centers[sub_labels]

            residual_centers = sub_centers - level1_centers[i]

            global_id_mapping, _ = self.match_embeddings_hungarian(
                residual_centers, global2_centers
            )

            sub_level2_ids = global_id_mapping[sub_labels]
            return indices, sub_level2_ids, sub_level2_centers

        if level2_parallel_jobs > 1 and len(level1_unique) > 1:
            level2_results = Parallel(n_jobs=level2_parallel_jobs, prefer="processes")(
                delayed(fit_level2_group)(i) for i in level1_unique
            )
        else:
            level2_results = [fit_level2_group(i) for i in level1_unique]

        for indices, sub_level2_ids, sub_level2_centers in level2_results:
            level2_centers_per_item[indices] = sub_level2_centers
            level2_ids[indices] = sub_level2_ids
"""
            text, did_change = replace_once(
                text,
                old_previous_parallel,
                new,
                "gaoq.level2_parallel",
            )
        if did_change:
            changed.append("gaoq.level2_parallel")

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
