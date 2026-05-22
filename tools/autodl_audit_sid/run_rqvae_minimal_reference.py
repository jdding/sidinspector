#!/usr/bin/env python3
"""Run the local rqvae_minimal_reference SIDInspector gate.

This is a CPU/local orchestration script.  It does not start AutoDL and does
not claim TIGER/GRID/ReSID/CARD equivalence.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from methods.rqvae_minimal_reference import METHOD_LABEL, RQReferenceConfig, export_rqvae_minimal_reference


FULL_INPUT_ROOT = (
    ROOT
    / "_gate0_artifacts/grid_same_dataset_runs/"
    "grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/input"
)
SMOKE_INPUT_ROOT = (
    ROOT
    / "_gate0_artifacts/grid_same_dataset_runs/"
    "grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max512_20260519_110703/input"
)
DEFAULT_INPUT_ROOT = FULL_INPUT_ROOT if FULL_INPUT_ROOT.exists() else SMOKE_INPUT_ROOT


def _parse_widths(text: str) -> tuple[int, ...]:
    widths = tuple(int(part.strip()) for part in text.split(",") if part.strip())
    if not widths:
        raise argparse.ArgumentTypeError("widths must contain at least one integer")
    return widths


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--embeddings", type=Path, default=DEFAULT_INPUT_ROOT / "item_embeddings.pt")
    parser.add_argument("--item-ids", type=Path, default=DEFAULT_INPUT_ROOT / "item_ids.npy")
    parser.add_argument("--item-metadata", type=Path, default=DEFAULT_INPUT_ROOT / "item_metadata.parquet")
    parser.add_argument("--interactions", type=Path, default=DEFAULT_INPUT_ROOT / "interactions.parquet")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--dataset-name", default="Musical_Instruments")
    parser.add_argument("--method", default=METHOD_LABEL)
    parser.add_argument("--widths", type=_parse_widths, default=(32, 128, 128))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--batch-size", type=int, default=512)
    parser.add_argument("--max-iter", type=int, default=50)
    parser.add_argument("--max-items", type=int, default=512, help="Use 512 for default smoke; use 2000 for 2k gate.")
    parser.add_argument("--d3-top-k", type=int, default=5)
    parser.add_argument("--d3-max-pair-events", type=int, default=10_000)
    parser.add_argument("--d3-max-user-items", type=int, default=50)
    parser.add_argument("--no-l2-normalize", action="store_true")
    parser.add_argument("--write-doc", action="store_true")
    return parser.parse_args(argv)


def _check_paths(paths: dict[str, Path]) -> list[str]:
    return [f"{name}: {path}" for name, path in paths.items() if not path.exists()]


def _write_doc(result_path: Path, output_dir: Path, result_payload: dict) -> tuple[Path, Path]:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    doc_latest = ROOT / "docs/RQVAE_MINIMAL_REFERENCE_GATE.md"
    doc_versioned = ROOT / f"docs/RQVAE_MINIMAL_REFERENCE_GATE_{timestamp}.md"
    lines = [
        "# RQ-VAE Minimal Reference Gate",
        "",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"状态：{'PASSED' if result_payload.get('gate_passed') else 'BLOCKED'}",
        f"方法标签：`{result_payload.get('method', METHOD_LABEL)}`",
        "",
        "## 边界",
        "",
        "这是本地 residual-quantization/RQ-VAE-style reference exporter；不冒充 TIGER、GRID、ReSID 或 CARD。",
        "",
        "## 产物",
        "",
        f"- gate JSON: `{result_path}`",
        f"- output dir: `{output_dir}`",
        f"- sid_assignments: `{result_payload.get('outputs', {}).get('sid_assignments', 'not_written')}`",
        f"- metrics: `{result_payload.get('outputs', {}).get('metrics_dir', 'not_written')}`",
        "",
        "## 结论",
        "",
        f"- items: `{result_payload.get('items', 'n/a')}`",
        f"- GPU-worthy: `{result_payload.get('gpu_worthy', False)}`",
        f"- condition: {result_payload.get('gpu_worthy_condition', '依赖或数据缺口先补齐。')}",
        "",
    ]
    content = "\n".join(lines)
    doc_versioned.write_text(content, encoding="utf-8")
    doc_latest.write_text(content, encoding="utf-8")
    return doc_versioned, doc_latest


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.method != METHOD_LABEL:
        raise SystemExit(f"--method must remain {METHOD_LABEL!r}; do not relabel this reference as another method")
    output_dir = args.output_dir
    if output_dir is None:
        size = "full" if args.max_items is None else str(args.max_items)
        output_dir = ROOT / "methods/rqvae_minimal_reference/outputs" / f"cpu_smoke_{size}_seed{args.seed}"
    paths = {
        "embeddings": args.embeddings,
        "item_ids": args.item_ids,
        "item_metadata": args.item_metadata,
        "interactions": args.interactions,
    }
    missing_paths = _check_paths(paths)
    if missing_paths:
        output_dir.mkdir(parents=True, exist_ok=True)
        audit_path = output_dir / "audit_result.json"
        payload = {
            "status": "blocked_missing_data",
            "gate_passed": False,
            "method": METHOD_LABEL,
            "missing_requirements": missing_paths,
            "gpu_worthy": False,
            "gpu_worthy_condition": "Do not start GPU/AutoDL until local embeddings, item_ids, metadata, and interactions exist.",
        }
        audit_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(payload, indent=2, sort_keys=True))
        raise SystemExit(2)

    config = RQReferenceConfig(
        dataset_name=args.dataset_name,
        method=args.method,
        widths=args.widths,
        seed=args.seed,
        batch_size=args.batch_size,
        max_iter=args.max_iter,
        max_items=args.max_items,
        l2_normalize=not args.no_l2_normalize,
        d3_top_k=args.d3_top_k,
        d3_max_pair_events=args.d3_max_pair_events,
        d3_max_user_items=args.d3_max_user_items,
    )
    result = export_rqvae_minimal_reference(
        embeddings_path=args.embeddings,
        item_ids_path=args.item_ids,
        item_metadata_path=args.item_metadata,
        interactions_path=args.interactions,
        output_dir=output_dir,
        config=config,
    )
    payload = json.loads(result.audit_json.read_text(encoding="utf-8"))
    if args.write_doc:
        versioned, latest = _write_doc(result.audit_json, output_dir, payload)
        payload["docs"] = {"versioned": str(versioned), "latest": str(latest)}
        result.audit_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    if not result.gate_passed:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
