#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
PYTHON_BIN="${PYTHON_BIN:-/root/miniconda3/bin/python}"
DATA_ROOT="${DATA_ROOT:-/root/autodl-tmp/amazon_2023}"
MODEL_PATH="${MODEL_PATH:-/root/autodl-tmp/hf_models/all_MiniLM_L6_v2}"
DATASET_NAME="${DATASET_NAME:-All_Beauty}"
META_JSONL_GZ="${META_JSONL_GZ:-$DATA_ROOT/meta_${DATASET_NAME}.jsonl.gz}"
REVIEWS_JSONL_GZ="${REVIEWS_JSONL_GZ:-$DATA_ROOT/${DATASET_NAME}.jsonl.gz}"
GRID_DIR="${GRID_DIR:-$ROOT_DIR/_gate0_repos/GRID}"

echo "[GATE0A preflight] root=$ROOT_DIR"
echo "[GATE0A preflight] dataset=$DATASET_NAME"
echo "[GATE0A preflight] python=$PYTHON_BIN"

missing=0
for path in \
  "$PYTHON_BIN" \
  "$ROOT_DIR/tools/autodl_audit_sid/run_grid_cluster_a_smoke.sh" \
  "$ROOT_DIR/tools/autodl_audit_sid/prepare_amazon_text_grid_inputs.py" \
  "$ROOT_DIR/tools/autodl_audit_sid/run_grid_rqkmeans_direct_export.py" \
  "$ROOT_DIR/src/audit_sid/metrics.py" \
  "$GRID_DIR" \
  "$META_JSONL_GZ" \
  "$REVIEWS_JSONL_GZ" \
  "$MODEL_PATH"; do
  if [ -e "$path" ]; then
    echo "OK $path"
  else
    echo "MISS $path"
    missing=1
  fi
done

if command -v nvidia-smi >/dev/null 2>&1; then
  echo "[GATE0A preflight] nvidia-smi:"
  nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader || true
else
  echo "[GATE0A preflight] nvidia-smi unavailable"
fi

if [ -d "$GRID_DIR/.git" ]; then
  echo "[GATE0A preflight] GRID commit:"
  if ! git -C "$GRID_DIR" rev-parse HEAD 2>/dev/null; then
    head_file="$GRID_DIR/.git/HEAD"
    if [ -f "$head_file" ]; then
      head_ref="$(cat "$head_file")"
      case "$head_ref" in
        ref:\ *)
          ref_path="$GRID_DIR/.git/${head_ref#ref: }"
          [ -f "$ref_path" ] && cat "$ref_path" || true
          ;;
        *)
          echo "$head_ref"
          ;;
      esac
    fi
  fi
fi

if [ "$missing" != "0" ]; then
  echo "[GATE0A preflight] MISSING_INPUTS"
  exit 2
fi

PYTHONPATH="$ROOT_DIR/src:$GRID_DIR" "$PYTHON_BIN" - <<'PY'
from pathlib import Path
import importlib

for name in ["torch", "pandas", "numpy", "sentence_transformers"]:
    importlib.import_module(name)
print("python_imports=OK")
PY

echo "[GATE0A preflight] READY"
