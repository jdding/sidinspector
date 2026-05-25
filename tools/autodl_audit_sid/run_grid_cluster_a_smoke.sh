#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
RUN_ROOT="${RUN_ROOT:-$ROOT_DIR/_gate0_artifacts/grid_cluster_a_runs}"
DATASET_NAME="${DATASET_NAME:-All_Beauty}"
EXP_ID="${EXP_ID:-grid_official_rqkmeans_${DATASET_NAME}_text_max${MAX_ITEMS:-5000}_$(date +%Y%m%d_%H%M%S)}"
OUT_DIR="$RUN_ROOT/$EXP_ID"
INPUT_DIR="$OUT_DIR/input"
GRID_OUT="$OUT_DIR/grid_export"

META_JSONL_GZ="${META_JSONL_GZ:-/root/autodl-tmp/amazon_2023/meta_All_Beauty.jsonl.gz}"
REVIEWS_JSONL_GZ="${REVIEWS_JSONL_GZ:-/root/autodl-tmp/amazon_2023/All_Beauty.jsonl.gz}"
MODEL_PATH="${MODEL_PATH:-/root/autodl-tmp/hf_models/all_MiniLM_L6_v2}"
MAX_ITEMS="${MAX_ITEMS:-5000}"
EMBED_BATCH_SIZE="${EMBED_BATCH_SIZE:-256}"
EMBED_DEVICE="${EMBED_DEVICE:-cuda}"
GRID_DEVICE="${GRID_DEVICE:-cuda}"
CODEBOOK_WIDTH="${CODEBOOK_WIDTH:-64}"
NUM_HIERARCHIES="${NUM_HIERARCHIES:-3}"
GRID_BATCH_SIZE="${GRID_BATCH_SIZE:-4096}"
STEPS_PER_LAYER="${STEPS_PER_LAYER:-40}"
INIT_BUFFER_SIZE="${INIT_BUFFER_SIZE:-4096}"
SEED="${SEED:-42}"
SKIP_PIP_INSTALL="${SKIP_PIP_INSTALL:-0}"

mkdir -p "$INPUT_DIR" "$GRID_OUT" "$OUT_DIR/logs"

echo "[SIDInspector GRID] root=$ROOT_DIR"
echo "[SIDInspector GRID] exp_id=$EXP_ID"
echo "[SIDInspector GRID] meta=$META_JSONL_GZ"
echo "[SIDInspector GRID] reviews=$REVIEWS_JSONL_GZ"
echo "[SIDInspector GRID] model_path=$MODEL_PATH"
echo "[SIDInspector GRID] max_items=$MAX_ITEMS codebook_width=$CODEBOOK_WIDTH hierarchies=$NUM_HIERARCHIES"

for required in "$META_JSONL_GZ" "$REVIEWS_JSONL_GZ" "$MODEL_PATH" "$ROOT_DIR/_gate0_repos/GRID"; do
  if [ ! -e "$required" ]; then
    echo "Missing required path: $required" >&2
    exit 2
  fi
done

if [ "$SKIP_PIP_INSTALL" != "1" ]; then
  "$PYTHON_BIN" -m pip install -q sentence-transformers lightning pytorch-lightning torchmetrics pandas pyarrow numpy
else
  echo "[SIDInspector GRID] SKIP_PIP_INSTALL=1; using existing Python environment"
fi

export MPLCONFIGDIR="${MPLCONFIGDIR:-/tmp/audit_sid_mpl}"
mkdir -p "$MPLCONFIGDIR"

"$PYTHON_BIN" "$ROOT_DIR/tools/autodl_audit_sid/prepare_amazon_text_grid_inputs.py" \
  --meta-jsonl-gz "$META_JSONL_GZ" \
  --reviews-jsonl-gz "$REVIEWS_JSONL_GZ" \
  --output-dir "$INPUT_DIR" \
  --dataset-name "$DATASET_NAME" \
  --model-path "$MODEL_PATH" \
  --batch-size "$EMBED_BATCH_SIZE" \
  --device "$EMBED_DEVICE" \
  --max-items "$MAX_ITEMS" \
  2>&1 | tee "$OUT_DIR/logs/prepare_inputs.log"

PYTHONPATH="$ROOT_DIR/src" "$PYTHON_BIN" "$ROOT_DIR/tools/autodl_audit_sid/run_grid_rqkmeans_direct_export.py" \
  --grid-dir "$ROOT_DIR/_gate0_repos/GRID" \
  --embeddings "$INPUT_DIR/item_embeddings.pt" \
  --item-ids "$INPUT_DIR/item_ids.npy" \
  --item-metadata "$INPUT_DIR/item_metadata.parquet" \
  --interactions "$INPUT_DIR/interactions.parquet" \
  --output-dir "$GRID_OUT" \
  --dataset-name "$DATASET_NAME" \
  --method grid_official_rqkmeans \
  --codebook-width "$CODEBOOK_WIDTH" \
  --num-hierarchies "$NUM_HIERARCHIES" \
  --batch-size "$GRID_BATCH_SIZE" \
  --steps-per-layer "$STEPS_PER_LAYER" \
  --init-buffer-size "$INIT_BUFFER_SIZE" \
  --device "$GRID_DEVICE" \
  --seed "$SEED" \
  2>&1 | tee "$OUT_DIR/logs/grid_export.log"

echo "[SIDInspector GRID] DONE: $GRID_OUT"
find "$GRID_OUT" -maxdepth 3 -type f | sort
