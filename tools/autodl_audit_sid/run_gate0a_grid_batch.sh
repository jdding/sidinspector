#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
PYTHON_BIN="${PYTHON_BIN:-/root/miniconda3/bin/python}"
DATASET_NAME="${DATASET_NAME:-All_Beauty}"
MAX_ITEMS="${MAX_ITEMS:-50000}"
CODEBOOK_WIDTH="${CODEBOOK_WIDTH:-128}"
NUM_HIERARCHIES="${NUM_HIERARCHIES:-3}"
STEPS_PER_LAYER="${STEPS_PER_LAYER:-40}"
GRID_BATCH_SIZE="${GRID_BATCH_SIZE:-4096}"
INIT_BUFFER_SIZE="${INIT_BUFFER_SIZE:-8192}"
EMBED_BATCH_SIZE="${EMBED_BATCH_SIZE:-256}"
SEED="${SEED:-42}"
DEVICE="${DEVICE:-cuda}"
RUN_ROOT="${RUN_ROOT:-$ROOT_DIR/_gate0_artifacts/grid_cluster_a_runs}"
EXP_ID="${EXP_ID:-grid_official_rqkmeans_${DATASET_NAME}_text_${MAX_ITEMS}_cuda_seed${SEED}}"

bash "$ROOT_DIR/tools/autodl_audit_sid/preflight_gate0a_grid.sh"

if [ "$DEVICE" = "cuda" ]; then
  if ! nvidia-smi --query-gpu=index,memory.used,memory.total --format=csv,noheader | awk -F',' '{gsub(/ /,"",$2); if ($2 < 500) ok=1} END{exit ok?0:1}'; then
    echo "[GATE0A grid] no idle GPU; refusing to launch CUDA run" >&2
    exit 3
  fi
fi

ROOT_DIR="$ROOT_DIR" \
PYTHON_BIN="$PYTHON_BIN" \
SKIP_PIP_INSTALL=1 \
DATASET_NAME="$DATASET_NAME" \
MAX_ITEMS="$MAX_ITEMS" \
CODEBOOK_WIDTH="$CODEBOOK_WIDTH" \
NUM_HIERARCHIES="$NUM_HIERARCHIES" \
STEPS_PER_LAYER="$STEPS_PER_LAYER" \
GRID_BATCH_SIZE="$GRID_BATCH_SIZE" \
INIT_BUFFER_SIZE="$INIT_BUFFER_SIZE" \
GRID_DEVICE="$DEVICE" \
EMBED_DEVICE="$DEVICE" \
EMBED_BATCH_SIZE="$EMBED_BATCH_SIZE" \
SEED="$SEED" \
RUN_ROOT="$RUN_ROOT" \
EXP_ID="$EXP_ID" \
  bash "$ROOT_DIR/tools/autodl_audit_sid/run_grid_cluster_a_smoke.sh"

echo "[GATE0A grid] DONE run=$RUN_ROOT/$EXP_ID"
