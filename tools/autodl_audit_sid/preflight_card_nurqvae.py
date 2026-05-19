#!/usr/bin/env python3
"""CPU preflight for CARD's original ``nu-rq-vae`` export path.

The official CARD clone stores the NU-RQ-VAE source under a hyphenated
directory (``nu-rq-vae``), while its scripts import ``nu_rqvae4``.  This
preflight creates a temporary import-only package overlay so the original
source can be loaded without editing the method implementation.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import numpy as np
import pandas as pd
import torch


class CardNuRQVAEPreflightError(RuntimeError):
    """Raised when the official CARD NU-RQ-VAE path is not locally preflightable."""


def _required_paths(card_dir: Path) -> dict[str, Path]:
    return {
        "card_readme": card_dir / "README.md",
        "rqvae4_package": card_dir / "rqvae4",
        "rqvae4_dataset": card_dir / "rqvae4/datasets.py",
        "rqvae4_trainer": card_dir / "rqvae4/trainer.py",
        "rqvae4_rq": card_dir / "rqvae4/models/rq.py",
        "rqvae4_vq": card_dir / "rqvae4/models/vq.py",
        "nu_dir": card_dir / "nu-rq-vae",
        "nu_main": card_dir / "nu-rq-vae/main.py",
        "nu_generate_code": card_dir / "nu-rq-vae/generate_code.py",
        "nu_model": card_dir / "nu-rq-vae/models/nu_rqvae.py",
    }


def check_required_paths(card_dir: Path) -> dict[str, Any]:
    paths = _required_paths(card_dir)
    missing = {name: str(path) for name, path in paths.items() if not path.exists()}
    if missing:
        raise CardNuRQVAEPreflightError(f"missing CARD NU-RQ-VAE source paths: {missing}")
    return {name: str(path) for name, path in paths.items()}


def create_import_overlay(card_dir: Path, overlay_dir: Path) -> Path:
    """Create a temporary ``nu_rqvae4`` package that points at official source."""

    source_models = card_dir / "nu-rq-vae/models"
    package_dir = overlay_dir / "nu_rqvae4"
    models_dir = package_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "__init__.py").write_text(
        '"""Import overlay for CARD official nu-rq-vae source."""\n',
        encoding="utf-8",
    )
    (models_dir / "__init__.py").write_text("", encoding="utf-8")
    shutil.copy2(source_models / "nu_rqvae.py", models_dir / "nu_rqvae.py")
    return package_dir


def _drop_imported_card_modules() -> None:
    for name in list(sys.modules):
        if name == "rqvae4" or name.startswith("rqvae4.") or name == "nu_rqvae4" or name.startswith("nu_rqvae4."):
            sys.modules.pop(name, None)


def run_import_smoke(card_dir: Path, overlay_dir: Path) -> dict[str, Any]:
    """Import and execute the official NU-RQ-VAE class on a tiny CPU tensor."""

    _drop_imported_card_modules()
    sys.path.insert(0, str(overlay_dir.resolve()))
    sys.path.insert(0, str(card_dir.resolve()))
    try:
        from nu_rqvae4.models.nu_rqvae import NURQVAE
        from rqvae4.datasets import EmbDataset

        model = NURQVAE(
            in_dim=8,
            num_emb_list=[4, 5],
            e_dim=3,
            layers=[6],
            sk_epsilons=[0.0, 0.0],
            kmeans_init=False,
            nvq_hidden_dim=3,
        )
        x = torch.randn(7, 8)
        out, loss, indices = model(x, use_sk=False)
        if out.shape != x.shape:
            raise CardNuRQVAEPreflightError(f"unexpected model output shape: {tuple(out.shape)}")
        if indices.shape != (7, 2):
            raise CardNuRQVAEPreflightError(f"unexpected code shape: {tuple(indices.shape)}")
        if not torch.isfinite(loss):
            raise CardNuRQVAEPreflightError("NU-RQ-VAE tiny CPU loss is not finite")
        return {
            "status": "passed",
            "imported": ["nu_rqvae4.models.nu_rqvae.NURQVAE", "rqvae4.datasets.EmbDataset"],
            "model_class": f"{NURQVAE.__module__}.{NURQVAE.__name__}",
            "dataset_class": f"{EmbDataset.__module__}.{EmbDataset.__name__}",
            "tiny_forward": {
                "input_shape": list(x.shape),
                "output_shape": list(out.shape),
                "indices_shape": list(indices.shape),
            },
        }
    finally:
        for entry in (str(card_dir.resolve()), str(overlay_dir.resolve())):
            while entry in sys.path:
                sys.path.remove(entry)
        _drop_imported_card_modules()


def check_generate_code_contract(card_dir: Path) -> dict[str, Any]:
    """Static check for the official generate_code export contract."""

    source = (card_dir / "nu-rq-vae/generate_code.py").read_text(encoding="utf-8")
    checks = {
        "imports_official_nurqvae": "from nu_rqvae4.models.nu_rqvae import NURQVAE" in source,
        "accepts_data_path": "parser.add_argument('--data_path'" in source,
        "accepts_out_path": "parser.add_argument('--out_path'" in source,
        "loads_checkpoint": "torch.load(ckpt_path" in source,
        "uses_nurqvae_class": "model = NURQVAE(" in source,
        "exports_codes_npy": "np.save(cli.out_path, codes_array)" in source,
        "exports_sibling_item_ids": '"_item_ids.npy"' in source and "np.save(ids_out, item_ids)" in source,
        "preserves_itemid_when_present": '"ItemID" in df_ids.columns' in source,
        "uses_collision_reassignment_loop": "model.get_indices(d, use_sk=True)" in source,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise CardNuRQVAEPreflightError(f"generate_code.py export contract checks failed: {failed}")
    return {"status": "passed", "checks": checks}


def _write_tiny_checkpoint(card_dir: Path, overlay_dir: Path, ckpt_path: Path, in_dim: int) -> None:
    _drop_imported_card_modules()
    sys.path.insert(0, str(overlay_dir.resolve()))
    sys.path.insert(0, str(card_dir.resolve()))
    try:
        from nu_rqvae4.models.nu_rqvae import NURQVAE

        args = SimpleNamespace(
            num_emb_list=[4, 5],
            e_dim=3,
            layers=[6],
            dropout_prob=0.0,
            bn=False,
            loss_type="mse",
            quant_loss_weight=1.0,
            beta=0.25,
            kmeans_init=False,
            kmeans_iters=1,
            sk_epsilons=[0.0, 0.0],
            sk_iters=1,
            nvq_hidden_dim=3,
            nvq_loss_weight=1.0,
            nvq_nonlinearity="kumaraswamy",
            num_workers=0,
        )
        model = NURQVAE(
            in_dim=in_dim,
            num_emb_list=args.num_emb_list,
            e_dim=args.e_dim,
            layers=args.layers,
            dropout_prob=args.dropout_prob,
            bn=args.bn,
            loss_type=args.loss_type,
            quant_loss_weight=args.quant_loss_weight,
            beta=args.beta,
            kmeans_init=args.kmeans_init,
            kmeans_iters=args.kmeans_iters,
            sk_epsilons=args.sk_epsilons,
            sk_iters=args.sk_iters,
            nvq_hidden_dim=args.nvq_hidden_dim,
            nvq_loss_weight=args.nvq_loss_weight,
            nvq_nonlinearity=args.nvq_nonlinearity,
        )
        torch.save({"args": args, "state_dict": model.state_dict()}, ckpt_path)
    finally:
        for entry in (str(card_dir.resolve()), str(overlay_dir.resolve())):
            while entry in sys.path:
                sys.path.remove(entry)
        _drop_imported_card_modules()


def run_synthetic_export(card_dir: Path, overlay_dir: Path, work_dir: Path, device: str = "cpu") -> dict[str, Any]:
    """Run official ``nu-rq-vae/generate_code.py`` on a tiny synthetic checkpoint."""

    data_path = work_dir / "item_emb.parquet"
    ckpt_path = work_dir / "tiny_nurqvae.pth"
    out_path = work_dir / "card_nurqvae_codes.npy"
    item_ids = np.array([101, 103, 107, 109, 113, 127], dtype=np.int64)
    embeddings = [np.linspace(i, i + 0.7, 8, dtype=np.float32) for i in range(len(item_ids))]
    pd.DataFrame({"ItemID": item_ids, "embedding": embeddings}).to_parquet(data_path, index=False)
    _write_tiny_checkpoint(card_dir, overlay_dir, ckpt_path, in_dim=8)

    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        [str(overlay_dir.resolve()), str(card_dir.resolve()), env.get("PYTHONPATH", "")]
    )
    env["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"
    cmd = [
        sys.executable,
        str((card_dir / "nu-rq-vae/generate_code.py").resolve()),
        "--ckpt_path",
        str(ckpt_path),
        "--data_path",
        str(data_path),
        "--out_path",
        str(out_path),
        "--device",
        device,
        "--batch_size",
        "3",
    ]
    completed = subprocess.run(cmd, cwd=work_dir, env=env, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise CardNuRQVAEPreflightError(
            "synthetic generate_code export failed\n"
            f"cmd={' '.join(cmd)}\nstdout={completed.stdout}\nstderr={completed.stderr}"
        )

    ids_path = out_path.with_name(f"{out_path.stem}_item_ids.npy")
    if not out_path.exists() or not ids_path.exists():
        raise CardNuRQVAEPreflightError("generate_code did not emit both codes.npy and sibling *_item_ids.npy")
    codes = np.load(out_path)
    exported_ids = np.load(ids_path)
    if codes.shape != (len(item_ids), 2):
        raise CardNuRQVAEPreflightError(f"unexpected synthetic code shape: {codes.shape}")
    if not np.array_equal(exported_ids, item_ids):
        raise CardNuRQVAEPreflightError("generate_code did not preserve ItemID values from parquet")
    return {
        "status": "passed",
        "command": cmd,
        "runner_repairs": {
            "PYTHONPATH_overlay": str(overlay_dir),
            "TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD": "1",
        },
        "outputs": {
            "codes_path": str(out_path),
            "item_ids_path": str(ids_path),
            "codes_shape": list(codes.shape),
            "item_ids": exported_ids.astype(int).tolist(),
        },
        "stdout_tail": completed.stdout.strip().splitlines()[-12:],
    }


def preflight_card_nurqvae(
    card_dir: Path,
    *,
    run_export: bool = False,
    work_dir: Path | None = None,
    keep_work_dir: bool = False,
    device: str = "cpu",
) -> dict[str, Any]:
    card_dir = card_dir.resolve()
    required = check_required_paths(card_dir)

    temp_context = None
    if work_dir is None:
        if keep_work_dir:
            root = Path(tempfile.mkdtemp(prefix="card_nurqvae_preflight_"))
        else:
            temp_context = tempfile.TemporaryDirectory(prefix="card_nurqvae_preflight_")
            root = Path(temp_context.name)
    else:
        root = work_dir.resolve()
        root.mkdir(parents=True, exist_ok=True)
    overlay_dir = root / "import_overlay"
    package_dir = create_import_overlay(card_dir, overlay_dir)

    try:
        result: dict[str, Any] = {
            "status": "passed",
            "card_dir": str(card_dir),
            "faithfulness": {
                "official_code_skeleton": True,
                "original_model_file": str(card_dir / "nu-rq-vae/models/nu_rqvae.py"),
                "core_algorithm_patched": False,
                "quantizer_replaced": False,
                "repair_scope": [
                    "temporary nu_rqvae4 import package overlay for hyphenated official directory",
                    "runner env TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1 for PyTorch checkpoint compatibility",
                ],
            },
            "required_paths": required,
            "overlay_package": str(package_dir),
            "import_smoke": run_import_smoke(card_dir, overlay_dir),
            "generate_code_contract": check_generate_code_contract(card_dir),
        }
        if run_export:
            export_work = root / "synthetic_export"
            export_work.mkdir(parents=True, exist_ok=True)
            result["synthetic_export"] = run_synthetic_export(card_dir, overlay_dir, export_work, device=device)
            result["next_step_ready"] = True
        else:
            result["next_step_ready"] = False
        return result
    finally:
        if temp_context is not None and not keep_work_dir:
            temp_context.cleanup()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preflight CARD official nu-rq-vae source/import/export path on CPU.")
    parser.add_argument("--card-dir", type=Path, default=Path("_gate0_repos/CARD"))
    parser.add_argument("--run-synthetic-export", action="store_true")
    parser.add_argument("--work-dir", type=Path)
    parser.add_argument("--keep-work-dir", action="store_true")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--output-json", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    result = preflight_card_nurqvae(
        args.card_dir,
        run_export=args.run_synthetic_export,
        work_dir=args.work_dir,
        keep_work_dir=args.keep_work_dir,
        device=args.device,
    )
    payload = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
