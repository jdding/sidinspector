"""Export GRID-style residual k-means SIDs using GRID's MiniBatchKMeans module.

This script avoids GRID's TFRecord/Hydra input stack but imports and uses the
official GRID `MiniBatchKMeans`, distance, and initializer classes from a local
GRID clone. It is intended as a bounded Cluster-A artifact export path.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch


def git_commit(repo: Path) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        head_path = repo / ".git" / "HEAD"
        try:
            head = head_path.read_text(encoding="utf-8").strip()
            if head.startswith("ref: "):
                ref_path = repo / ".git" / head.split(" ", 1)[1]
                return ref_path.read_text(encoding="utf-8").strip()
            return head
        except Exception:
            return "unknown"


def import_grid(grid_dir: Path):
    sys.path.insert(0, str(grid_dir))
    try:
        from src.components.clustering_initializers import KMeansPlusPlusInitInitializer
        from src.components.distance_functions import SquaredEuclideanDistance
        from src.models.modules.clustering.mini_batch_kmeans import MiniBatchKMeans
    except Exception as exc:  # pragma: no cover - preflight error path
        raise RuntimeError(
            "Could not import official GRID MiniBatchKMeans classes. Install the "
            "minimal GRID dependencies first: lightning, pytorch-lightning, "
            "torchmetrics."
        ) from exc
    return KMeansPlusPlusInitInitializer, SquaredEuclideanDistance, MiniBatchKMeans


def l2_normalize(x: torch.Tensor) -> torch.Tensor:
    return torch.nn.functional.normalize(x, dim=-1)


def train_one_layer(layer, residuals: torch.Tensor, batch_size: int, steps: int, seed: int) -> None:
    generator = torch.Generator(device=residuals.device)
    generator.manual_seed(seed)
    n_items = residuals.shape[0]
    layer.on_train_start()
    optimizer = None
    if not getattr(layer, "update_manually", False):
        optimizer = torch.optim.SGD([layer.centroids], lr=0.5)

    for step in range(steps):
        indices = torch.randint(0, n_items, (min(batch_size, n_items),), generator=generator, device=residuals.device)
        batch = residuals[indices]
        _assignments, _embeddings, loss = layer.model_step(batch)
        if optimizer is not None and loss is not None:
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()


def assign_layer(layer, residuals: torch.Tensor, batch_size: int) -> tuple[torch.Tensor, torch.Tensor]:
    assignments: list[torch.Tensor] = []
    embeddings: list[torch.Tensor] = []
    with torch.no_grad():
        for start in range(0, residuals.shape[0], batch_size):
            batch = residuals[start : start + batch_size]
            ids, emb = layer.predict_step(batch)
            assignments.append(ids.detach().cpu())
            embeddings.append(emb.detach())
    return torch.cat(assignments, dim=0), torch.cat(embeddings, dim=0)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grid-dir", type=Path, default=Path("_gate0_repos/GRID"))
    parser.add_argument("--embeddings", type=Path, required=True)
    parser.add_argument("--item-ids", type=Path, required=True)
    parser.add_argument("--item-metadata", type=Path, required=True)
    parser.add_argument("--interactions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="All_Beauty")
    parser.add_argument("--method", default="grid_official_rqkmeans")
    parser.add_argument("--codebook-width", type=int, default=128)
    parser.add_argument("--num-hierarchies", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=4096)
    parser.add_argument("--steps-per-layer", type=int, default=80)
    parser.add_argument("--init-buffer-size", type=int, default=4096)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    KMeansPlusPlusInitInitializer, SquaredEuclideanDistance, MiniBatchKMeans = import_grid(args.grid_dir)

    torch.manual_seed(args.seed)
    embeddings = torch.load(args.embeddings, map_location="cpu").float()
    item_ids = np.load(args.item_ids).astype(np.int64)
    if embeddings.ndim != 2:
        raise ValueError(f"Expected embeddings to be 2D, got {tuple(embeddings.shape)}")
    if len(item_ids) != embeddings.shape[0]:
        raise ValueError(f"item_ids length {len(item_ids)} != embedding rows {embeddings.shape[0]}")
    if args.codebook_width > embeddings.shape[0]:
        raise ValueError("codebook width cannot exceed number of items")

    device = torch.device(args.device if torch.cuda.is_available() or args.device == "cpu" else "cpu")
    embeddings = l2_normalize(embeddings.to(device))
    residuals = embeddings
    codes: list[np.ndarray] = []
    layer_summaries: list[dict] = []

    distance = SquaredEuclideanDistance()
    for level in range(args.num_hierarchies):
        layer = MiniBatchKMeans(
            n_clusters=args.codebook_width,
            n_features=embeddings.shape[1],
            distance_function=distance,
            initializer=KMeansPlusPlusInitInitializer(
                n_clusters=args.codebook_width,
                distance_function=distance,
                initialize_on_cpu=False,
            ),
            init_buffer_size=min(args.init_buffer_size, embeddings.shape[0]),
            update_manually=True,
        ).to(device)
        train_residuals = l2_normalize(residuals)
        train_one_layer(layer, train_residuals, args.batch_size, args.steps_per_layer, args.seed + level)
        ids, quantized = assign_layer(layer, train_residuals, args.batch_size)
        residuals = residuals - quantized
        codes.append(ids.numpy().astype(np.int64))
        unique = int(np.unique(codes[-1]).shape[0])
        layer_summaries.append({"level": level, "unique_codes": unique, "codebook_width": args.codebook_width})

    code_array = np.stack(codes, axis=1)
    np.save(args.output_dir / "grid_rqkmeans_codes.npy", code_array)
    np.save(args.output_dir / "grid_rqkmeans_item_ids.npy", item_ids)

    sid = pd.DataFrame({"item_id": item_ids, "method": args.method, "dataset": args.dataset_name})
    for level in range(code_array.shape[1]):
        sid[f"sid_level_{level}"] = code_array[:, level].astype(int)
    sid["sid"] = sid[[f"sid_level_{i}" for i in range(code_array.shape[1])]].astype(str).agg("-".join, axis=1)
    normalized_dir = args.output_dir / "normalized"
    normalized_dir.mkdir(exist_ok=True)
    sid.to_parquet(normalized_dir / "sid_assignments.parquet", index=False)

    with (args.output_dir / "grid_export_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "method": args.method,
                "dataset": args.dataset_name,
                "grid_dir": str(args.grid_dir),
                "grid_commit": git_commit(args.grid_dir),
                "num_items": int(embeddings.shape[0]),
                "embedding_dim": int(embeddings.shape[1]),
                "codebook_width": args.codebook_width,
                "num_hierarchies": args.num_hierarchies,
                "steps_per_layer": args.steps_per_layer,
                "device": str(device),
                "layers": layer_summaries,
            },
            handle,
            indent=2,
        )

    # Run AUDIT-SID metrics immediately so the export is join-validated.
    from audit_sid.metrics import (
        alignment,
        collision,
        deployment_cost,
        head_tail_capacity,
        utilization,
        validate_inputs,
    )

    item_metadata = pd.read_parquet(args.item_metadata)
    interactions = pd.read_parquet(args.interactions)
    metrics_dir = args.output_dir / "metrics"
    metrics_dir.mkdir(exist_ok=True)
    tables = {
        "coverage_report.csv": validate_inputs(sid, item_metadata, interactions),
        "d1_utilization.csv": utilization(sid),
        "d2_collision.csv": collision(sid, interactions),
        "d3_alignment.csv": alignment(sid, item_metadata),
        "d4_head_tail.csv": head_tail_capacity(sid, interactions),
        "d5a_deployment_cost.csv": deployment_cost(sid),
    }
    for name, table in tables.items():
        table.to_csv(metrics_dir / name, index=False)


if __name__ == "__main__":
    main()
