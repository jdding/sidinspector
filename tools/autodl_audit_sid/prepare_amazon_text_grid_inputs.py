"""Prepare Amazon-2023 text embeddings for a GRID RQ-KMeans export.

This prepares public raw Amazon review data into the SIDInspector schema plus a
row-aligned embedding tensor. It intentionally does not train a tokenizer.
The tokenizer/export step is handled by `run_grid_rqkmeans_direct_export.py`.
"""

from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import torch


def iter_jsonl_gz(path: Path) -> Iterable[dict]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def text_from_meta(row: dict) -> str:
    parts: list[str] = []
    for key in ("title", "store", "main_category"):
        value = row.get(key)
        if value:
            parts.append(str(value))
    for key in ("categories", "features", "description"):
        value = row.get(key)
        if isinstance(value, list):
            flat: list[str] = []
            for item in value:
                if isinstance(item, list):
                    flat.extend(str(x) for x in item if x)
                elif item:
                    flat.append(str(item))
            if flat:
                parts.append(" ".join(flat[:32]))
        elif value:
            parts.append(str(value))
    text = " ".join(parts).strip()
    return text or str(row.get("parent_asin", ""))


def load_metadata(meta_path: Path, max_items: int | None) -> pd.DataFrame:
    rows: list[dict] = []
    seen: set[str] = set()
    for raw in iter_jsonl_gz(meta_path):
        parent_asin = raw.get("parent_asin")
        if not parent_asin or parent_asin in seen:
            continue
        seen.add(parent_asin)
        rows.append(
            {
                "parent_asin": parent_asin,
                "title": raw.get("title") or "",
                "store": raw.get("store") or "",
                "category": raw.get("main_category") or "",
                "text": text_from_meta(raw),
            }
        )
        if max_items is not None and len(rows) >= max_items:
            break
    if not rows:
        raise ValueError(f"No metadata rows loaded from {meta_path}")
    frame = pd.DataFrame(rows)
    frame.insert(0, "item_id", np.arange(len(frame), dtype=np.int64))
    return frame


def load_interactions(reviews_path: Path | None, asin_to_item: dict[str, int]) -> pd.DataFrame:
    if reviews_path is None:
        return pd.DataFrame(columns=["user_id", "item_id", "timestamp", "split"])

    user_to_id: dict[str, int] = {}
    rows: list[tuple[int, int, int, str]] = []
    for raw in iter_jsonl_gz(reviews_path):
        parent_asin = raw.get("parent_asin")
        if parent_asin not in asin_to_item:
            continue
        user = raw.get("user_id")
        if not user:
            continue
        if user not in user_to_id:
            user_to_id[user] = len(user_to_id)
        timestamp = raw.get("timestamp")
        rows.append((user_to_id[user], asin_to_item[parent_asin], int(timestamp or 0), "all"))
    return pd.DataFrame(rows, columns=["user_id", "item_id", "timestamp", "split"])


def encode_texts(texts: list[str], model_path: str, batch_size: int, device: str) -> np.ndarray:
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_path, device=device)
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    return embeddings.astype(np.float32)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--meta-jsonl-gz", type=Path, required=True)
    parser.add_argument("--reviews-jsonl-gz", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="All_Beauty")
    parser.add_argument("--model-path", default="/Volumes/TU280Pro/Research/LLMs/all_MiniLM_L6_v2")
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--max-items", type=int, default=None)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    metadata = load_metadata(args.meta_jsonl_gz, args.max_items)
    asin_to_item = dict(zip(metadata["parent_asin"], metadata["item_id"]))
    interactions = load_interactions(args.reviews_jsonl_gz, asin_to_item)
    embeddings = encode_texts(metadata["text"].tolist(), args.model_path, args.batch_size, args.device)

    if embeddings.shape[0] != len(metadata):
        raise RuntimeError(f"Embedding rows {embeddings.shape[0]} != metadata rows {len(metadata)}")

    metadata["dataset"] = args.dataset_name
    metadata.to_parquet(args.output_dir / "item_metadata.parquet", index=False)
    interactions.to_parquet(args.output_dir / "interactions.parquet", index=False)
    np.save(args.output_dir / "item_ids.npy", metadata["item_id"].to_numpy(dtype=np.int64))
    torch.save(torch.from_numpy(embeddings), args.output_dir / "item_embeddings.pt")
    with (args.output_dir / "manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "dataset": args.dataset_name,
                "num_items": int(len(metadata)),
                "num_interactions": int(len(interactions)),
                "embedding_dim": int(embeddings.shape[1]),
                "model_path": args.model_path,
                "meta_jsonl_gz": str(args.meta_jsonl_gz),
                "reviews_jsonl_gz": str(args.reviews_jsonl_gz) if args.reviews_jsonl_gz else None,
            },
            handle,
            indent=2,
        )


if __name__ == "__main__":
    main()
