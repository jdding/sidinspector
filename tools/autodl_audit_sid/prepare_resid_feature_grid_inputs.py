"""Prepare ReSID item-feature text embeddings for same-dataset GRID export.

This is a controlled same-item-universe bridge for AUDIT-SID diagnostics. It
uses ReSID's public processed item features and interactions, not raw Amazon
titles/reviews, then feeds row-aligned embeddings into the official GRID
MiniBatchKMeans exporter.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch


def item_feature_text(row: pd.Series) -> str:
    parts = [f"item {int(row['item_id'])}"]
    if "store_id" in row and pd.notna(row["store_id"]):
        parts.append(f"store {int(row['store_id'])}")
    for source, label in (
        ("category_l1", "category level 1"),
        ("category_l2", "category level 2"),
        ("category_l3", "category level 3"),
        ("category", "category"),
        ("cate1_id", "category level 1"),
        ("cate2_id", "category level 2"),
        ("cate3_id", "category level 3"),
    ):
        if source in row and pd.notna(row[source]):
            parts.append(f"{label} {int(row[source])}")
    return " ".join(parts)


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
    parser.add_argument("--item-metadata", type=Path, required=True)
    parser.add_argument("--interactions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="Musical_Instruments")
    parser.add_argument("--model-path", default="/Volumes/TU280Pro/Research/LLMs/all_MiniLM_L6_v2")
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--max-items", type=int, default=None)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    metadata = pd.read_parquet(args.item_metadata).copy()
    interactions = pd.read_parquet(args.interactions).copy()
    if "item_id" not in metadata.columns:
        raise ValueError("item metadata must include item_id")
    if "item_id" not in interactions.columns:
        raise ValueError("interactions must include item_id")

    metadata = metadata.sort_values("item_id").reset_index(drop=True)
    if args.max_items is not None:
        metadata = metadata.head(args.max_items).copy()
        keep = set(metadata["item_id"].astype(int).tolist())
        interactions = interactions[interactions["item_id"].astype(int).isin(keep)].copy()

    metadata["dataset"] = args.dataset_name
    metadata["text"] = metadata.apply(item_feature_text, axis=1)
    embeddings = encode_texts(metadata["text"].tolist(), args.model_path, args.batch_size, args.device)
    if embeddings.shape[0] != len(metadata):
        raise RuntimeError(f"Embedding rows {embeddings.shape[0]} != metadata rows {len(metadata)}")

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
                "source_item_metadata": str(args.item_metadata),
                "source_interactions": str(args.interactions),
                "input_type": "resid_processed_feature_text",
            },
            handle,
            indent=2,
        )


if __name__ == "__main__":
    main()
