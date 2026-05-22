"""Local RQ-VAE-style residual quantization reference exporter.

This module intentionally implements a small reference path, not a reproduction
of TIGER, GRID, ReSID, or CARD.  It consumes item embeddings, learns residual
codebooks with MiniBatchKMeans, writes item_id -> SID assignments, and runs the
SIDInspector D1-D5 diagnostics through the shared metric functions.
"""

from __future__ import annotations

import json
import platform
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


METHOD_LABEL = "rqvae_minimal_reference"


@dataclass(frozen=True)
class RQReferenceConfig:
    dataset_name: str = "Musical_Instruments"
    method: str = METHOD_LABEL
    widths: tuple[int, ...] = (32, 128, 128)
    seed: int = 42
    batch_size: int = 512
    max_iter: int = 50
    max_items: int | None = 512
    l2_normalize: bool = True
    d3_top_k: int = 5
    d3_max_pair_events: int = 10_000
    d3_max_user_items: int = 50


@dataclass(frozen=True)
class RQReferenceResult:
    status: str
    gate_passed: bool
    output_dir: Path
    sid_assignments: Path
    metrics_dir: Path
    audit_json: Path
    missing_requirements: tuple[str, ...]
    gpu_worthy: bool


def _require_runtime() -> tuple[Any, type[Any], tuple[str, ...]]:
    missing: list[str] = []
    torch = None
    minibatch_kmeans = None
    try:
        import torch as torch_module

        torch = torch_module
    except Exception as exc:  # pragma: no cover - depends on environment
        missing.append(f"torch import failed: {exc}")
    try:
        from sklearn.cluster import MiniBatchKMeans as MiniBatchKMeansClass

        minibatch_kmeans = MiniBatchKMeansClass
    except Exception as exc:  # pragma: no cover - depends on environment
        missing.append(f"scikit-learn import failed: {exc}")
    return torch, minibatch_kmeans, tuple(missing)


def _load_embeddings(path: Path) -> np.ndarray:
    suffix = path.suffix.lower()
    if suffix == ".pt":
        torch, _, missing = _require_runtime()
        if missing:
            raise RuntimeError("; ".join(missing))
        obj = torch.load(path, map_location="cpu")
        if hasattr(obj, "detach"):
            arr = obj.detach().cpu().numpy()
        elif isinstance(obj, dict):
            for key in ("embeddings", "item_embeddings", "features"):
                if key in obj:
                    value = obj[key]
                    arr = value.detach().cpu().numpy() if hasattr(value, "detach") else np.asarray(value)
                    break
            else:
                raise ValueError(f"{path} dict must contain embeddings, item_embeddings, or features")
        else:
            arr = np.asarray(obj)
    elif suffix == ".npy":
        arr = np.load(path)
    elif suffix == ".parquet":
        frame = pd.read_parquet(path)
        if "embedding" in frame.columns:
            arr = np.stack(frame["embedding"].to_numpy()).astype(np.float32)
        else:
            numeric = frame.select_dtypes(include=[np.number]).drop(columns=["item_id", "ItemID"], errors="ignore")
            if numeric.empty:
                raise ValueError(f"{path} has no embedding column or numeric feature columns")
            arr = numeric.to_numpy(dtype=np.float32)
    else:
        raise ValueError(f"unsupported embedding format: {path}; expected .pt, .npy, or .parquet")
    arr = np.asarray(arr, dtype=np.float32)
    if arr.ndim != 2:
        raise ValueError(f"embeddings must be 2D, got shape {arr.shape}")
    if not np.isfinite(arr).all():
        raise ValueError("embeddings contain NaN or infinite values")
    return arr


def _load_item_ids(item_ids_path: Path | None, embeddings_path: Path, n_rows: int) -> np.ndarray:
    if item_ids_path is None:
        sibling = embeddings_path.with_name("item_ids.npy")
        if sibling.exists():
            item_ids_path = sibling
    if item_ids_path is None:
        raise ValueError("item ids are required; pass --item-ids or place item_ids.npy next to embeddings")
    if item_ids_path.suffix.lower() == ".npy":
        item_ids = np.load(item_ids_path).astype(np.int64)
    elif item_ids_path.suffix.lower() == ".parquet":
        frame = pd.read_parquet(item_ids_path)
        column = "item_id" if "item_id" in frame.columns else "ItemID"
        if column not in frame.columns:
            raise ValueError(f"{item_ids_path} must contain item_id or ItemID")
        item_ids = frame[column].to_numpy(dtype=np.int64)
    else:
        frame = pd.read_csv(item_ids_path)
        column = "item_id" if "item_id" in frame.columns else "ItemID"
        if column not in frame.columns:
            raise ValueError(f"{item_ids_path} must contain item_id or ItemID")
        item_ids = frame[column].to_numpy(dtype=np.int64)
    if len(item_ids) != n_rows:
        raise ValueError(f"item_ids length {len(item_ids)} != embedding rows {n_rows}")
    return item_ids


def _take_prefix(
    embeddings: np.ndarray,
    item_ids: np.ndarray,
    item_metadata: pd.DataFrame,
    interactions: pd.DataFrame,
    max_items: int | None,
) -> tuple[np.ndarray, np.ndarray, pd.DataFrame, pd.DataFrame]:
    if max_items is None or max_items >= len(item_ids):
        return embeddings, item_ids, item_metadata, interactions
    keep_item_ids = set(item_ids[:max_items].astype(int))
    metadata_small = item_metadata[item_metadata["item_id"].astype(int).isin(keep_item_ids)].copy()
    interactions_small = interactions[interactions["item_id"].astype(int).isin(keep_item_ids)].copy()
    return embeddings[:max_items], item_ids[:max_items], metadata_small, interactions_small


def _normalize_rows(x: np.ndarray) -> np.ndarray:
    denom = np.linalg.norm(x, axis=1, keepdims=True)
    return x / np.maximum(denom, 1e-12)


def residual_quantize(
    embeddings: np.ndarray,
    widths: tuple[int, ...],
    *,
    seed: int,
    batch_size: int,
    max_iter: int,
    l2_normalize: bool = True,
) -> tuple[np.ndarray, list[dict[str, Any]]]:
    _, MiniBatchKMeans, missing = _require_runtime()
    if missing:
        raise RuntimeError("; ".join(missing))
    if not widths:
        raise ValueError("widths must contain at least one codebook width")
    if embeddings.shape[0] < 2:
        raise ValueError("at least two items are required for residual quantization")
    residual = _normalize_rows(embeddings) if l2_normalize else embeddings.astype(np.float32, copy=True)
    codes: list[np.ndarray] = []
    summaries: list[dict[str, Any]] = []
    for level, requested_width in enumerate(widths):
        if requested_width <= 0:
            raise ValueError(f"codebook width must be positive, got {requested_width}")
        n_clusters = min(int(requested_width), int(residual.shape[0]))
        model = MiniBatchKMeans(
            n_clusters=n_clusters,
            random_state=seed + level,
            batch_size=min(batch_size, residual.shape[0]),
            n_init=5,
            max_iter=max_iter,
            reassignment_ratio=0.0,
        )
        labels = model.fit_predict(residual)
        quantized = model.cluster_centers_[labels]
        residual = residual - quantized
        codes.append(labels.astype(np.int64) + 1)
        summaries.append(
            {
                "level": level,
                "requested_width": int(requested_width),
                "effective_width": int(n_clusters),
                "unique_codes": int(np.unique(labels).shape[0]),
                "inertia": float(model.inertia_),
                "residual_l2_mean": float(np.linalg.norm(residual, axis=1).mean()),
            }
        )
    return np.stack(codes, axis=1), summaries


def _sid_frame(item_ids: np.ndarray, codes: np.ndarray, config: RQReferenceConfig) -> pd.DataFrame:
    sid = pd.DataFrame({"item_id": item_ids.astype(int), "method": config.method, "dataset": config.dataset_name})
    for level in range(codes.shape[1]):
        sid[f"sid_level_{level}"] = codes[:, level].astype(int)
    level_cols = [f"sid_level_{level}" for level in range(codes.shape[1])]
    sid["sid"] = sid[level_cols].astype(str).agg("-".join, axis=1)
    return sid


def export_rqvae_minimal_reference(
    *,
    embeddings_path: Path,
    item_ids_path: Path | None,
    item_metadata_path: Path,
    interactions_path: Path,
    output_dir: Path,
    config: RQReferenceConfig,
) -> RQReferenceResult:
    from audit_sid.interface import validate_columns
    from audit_sid.metrics import (
        alignment,
        collision,
        deployment_cost,
        head_tail_capacity,
        utilization,
        validate_inputs,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    missing_requirements = _require_runtime()[2]
    audit_json = output_dir / "audit_result.json"
    normalized_dir = output_dir / "normalized"
    metrics_dir = output_dir / "metrics"
    normalized_dir.mkdir(exist_ok=True)
    metrics_dir.mkdir(exist_ok=True)
    sid_path = normalized_dir / "sid_assignments.parquet"

    if missing_requirements:
        audit_json.write_text(
            json.dumps(
                {
                    "status": "blocked_missing_dependency",
                    "gate_passed": False,
                    "method": config.method,
                    "missing_requirements": list(missing_requirements),
                    "gpu_worthy": False,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return RQReferenceResult(
            "blocked_missing_dependency",
            False,
            output_dir,
            sid_path,
            metrics_dir,
            audit_json,
            missing_requirements,
            False,
        )

    embeddings = _load_embeddings(embeddings_path)
    item_ids = _load_item_ids(item_ids_path, embeddings_path, embeddings.shape[0])
    item_metadata = pd.read_parquet(item_metadata_path)
    interactions = pd.read_parquet(interactions_path)
    embeddings, item_ids, item_metadata, interactions = _take_prefix(
        embeddings,
        item_ids,
        item_metadata,
        interactions,
        config.max_items,
    )
    if item_metadata.empty:
        raise ValueError("item_metadata has no rows after max_items filtering")
    if interactions.empty:
        raise ValueError("interactions has no rows after max_items filtering")

    codes, codebooks = residual_quantize(
        embeddings,
        config.widths,
        seed=config.seed,
        batch_size=config.batch_size,
        max_iter=config.max_iter,
        l2_normalize=config.l2_normalize,
    )
    sid = _sid_frame(item_ids, codes, config)
    validate_columns("sid_assignments", sid.columns)
    coverage = validate_inputs(sid, item_metadata, interactions)
    sid.to_parquet(sid_path, index=False)
    np.save(output_dir / "rqvae_minimal_reference_codes.npy", codes)
    np.save(output_dir / "rqvae_minimal_reference_item_ids.npy", item_ids)

    tables = {
        "coverage_report.csv": coverage,
        "d1_utilization.csv": utilization(sid),
        "d2_collision.csv": collision(sid, interactions),
        "d3_alignment.csv": alignment(
            sid,
            item_metadata,
            interactions,
            top_k=config.d3_top_k,
            max_pair_events=config.d3_max_pair_events,
            max_user_items=config.d3_max_user_items,
        ),
        "d4_head_tail.csv": head_tail_capacity(sid, interactions),
        "d5a_deployment_cost.csv": deployment_cost(sid),
    }
    for name, table in tables.items():
        table.to_csv(metrics_dir / name, index=False)

    d5 = tables["d5a_deployment_cost.csv"].iloc[0].to_dict()
    gpu_worthy = bool(config.max_items is not None and config.max_items >= 2000 and float(d5["duplicate_sid_rate"]) < 0.5)
    payload = {
        "status": "passed",
        "gate_passed": True,
        "method": config.method,
        "label_boundary": "minimal residual-quantization reference; not TIGER, GRID, ReSID, or CARD",
        "config": asdict(config),
        "inputs": {
            "embeddings": str(embeddings_path),
            "item_ids": str(item_ids_path) if item_ids_path else str(embeddings_path.with_name("item_ids.npy")),
            "item_metadata": str(item_metadata_path),
            "interactions": str(interactions_path),
        },
        "outputs": {
            "sid_assignments": str(sid_path),
            "codes": str(output_dir / "rqvae_minimal_reference_codes.npy"),
            "item_ids": str(output_dir / "rqvae_minimal_reference_item_ids.npy"),
            "metrics_dir": str(metrics_dir),
        },
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
        },
        "items": int(len(sid)),
        "embedding_dim": int(embeddings.shape[1]),
        "codebooks": codebooks,
        "coverage": coverage.to_dict(orient="records"),
        "d5_summary": d5,
        "gpu_worthy": gpu_worthy,
        "gpu_worthy_condition": "Run GPU/full-data only after 2k CPU smoke passes and duplicate_sid_rate < 0.5.",
    }
    audit_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return RQReferenceResult("passed", True, output_dir, sid_path, metrics_dir, audit_json, (), gpu_worthy)
