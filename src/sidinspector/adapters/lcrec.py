"""Normalize LC-Rec released item-index artifacts.

LC-Rec releases item indices as JSON mappings from item ids to token strings
such as ``<a_128>``. The format is compatible with the LETTER JSON index
contract, but this module gives LC-Rec a method-specific CLI entry point and
default labels for reviewer-facing resource use.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from sidinspector.adapters.letter import (
    normalize_letter_index,
    normalize_letter_interactions,
    normalize_letter_metadata,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize LC-Rec JSON SID index artifacts.")
    parser.add_argument("--index-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="unknown")
    parser.add_argument("--method", default="lcrec_official_index")
    parser.add_argument("--item-json", type=Path, default=None)
    parser.add_argument("--inter-json", type=Path, default=None)
    parser.add_argument("--interaction-split", default="train")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    sid_assignments = normalize_letter_index(args.index_json, method=args.method, dataset=args.dataset_name)
    sid_assignments.to_parquet(args.output_dir / "sid_assignments.parquet", index=False)

    if args.item_json:
        item_metadata = normalize_letter_metadata(args.item_json, dataset=args.dataset_name)
        item_metadata.to_parquet(args.output_dir / "item_metadata.parquet", index=False)
    if args.inter_json:
        interactions = normalize_letter_interactions(args.inter_json, dataset=args.dataset_name, split=args.interaction_split)
        interactions.to_parquet(args.output_dir / "interactions.parquet", index=False)


if __name__ == "__main__":
    main()
