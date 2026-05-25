#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
RUN_ROOT="${RUN_ROOT:-$ROOT_DIR/_gate0_artifacts/grid_same_dataset_runs}"
DATASET_NAME="${DATASET_NAME:-Musical_Instruments}"
EXP_ID="${EXP_ID:-grid_official_rqkmeans_${DATASET_NAME}_resid_feature_text_cpu_max${MAX_ITEMS:-23742}_$(date +%Y%m%d_%H%M%S)}"
OUT_DIR="$RUN_ROOT/$EXP_ID"
INPUT_DIR="$OUT_DIR/input"
GRID_OUT="$OUT_DIR/grid_export"

ITEM_METADATA="${ITEM_METADATA:-$ROOT_DIR/_gate0_artifacts/resid_musical_normalized/item_metadata.parquet}"
INTERACTIONS="${INTERACTIONS:-$ROOT_DIR/_gate0_artifacts/resid_musical_normalized/interactions.parquet}"
MODEL_PATH="${MODEL_PATH:-/Volumes/TU280Pro/Research/LLMs/all_MiniLM_L6_v2}"
MAX_ITEMS="${MAX_ITEMS:-23742}"
EMBED_BATCH_SIZE="${EMBED_BATCH_SIZE:-256}"
CODEBOOK_WIDTH="${CODEBOOK_WIDTH:-64}"
NUM_HIERARCHIES="${NUM_HIERARCHIES:-3}"
GRID_BATCH_SIZE="${GRID_BATCH_SIZE:-4096}"
STEPS_PER_LAYER="${STEPS_PER_LAYER:-40}"
INIT_BUFFER_SIZE="${INIT_BUFFER_SIZE:-4096}"
SEED="${SEED:-42}"

mkdir -p "$INPUT_DIR" "$GRID_OUT" "$OUT_DIR/logs"

echo "[SIDInspector GRID-MUSICAL] root=$ROOT_DIR"
echo "[SIDInspector GRID-MUSICAL] exp_id=$EXP_ID"
echo "[SIDInspector GRID-MUSICAL] item_metadata=$ITEM_METADATA"
echo "[SIDInspector GRID-MUSICAL] interactions=$INTERACTIONS"
echo "[SIDInspector GRID-MUSICAL] model_path=$MODEL_PATH"
echo "[SIDInspector GRID-MUSICAL] max_items=$MAX_ITEMS codebook_width=$CODEBOOK_WIDTH hierarchies=$NUM_HIERARCHIES"
echo "[SIDInspector GRID-MUSICAL] device=cpu"

for required in "$ITEM_METADATA" "$INTERACTIONS" "$MODEL_PATH" "$ROOT_DIR/_gate0_repos/GRID"; do
  if [ ! -e "$required" ]; then
    echo "Missing required path: $required" >&2
    exit 2
  fi
done

export MPLCONFIGDIR="${MPLCONFIGDIR:-/tmp/audit_sid_mpl}"
mkdir -p "$MPLCONFIGDIR"

"$PYTHON_BIN" "$ROOT_DIR/tools/autodl_audit_sid/prepare_resid_feature_grid_inputs.py" \
  --item-metadata "$ITEM_METADATA" \
  --interactions "$INTERACTIONS" \
  --output-dir "$INPUT_DIR" \
  --dataset-name "$DATASET_NAME" \
  --model-path "$MODEL_PATH" \
  --batch-size "$EMBED_BATCH_SIZE" \
  --device cpu \
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
  --method grid_official_rqkmeans_resid_feature_text \
  --codebook-width "$CODEBOOK_WIDTH" \
  --num-hierarchies "$NUM_HIERARCHIES" \
  --batch-size "$GRID_BATCH_SIZE" \
  --steps-per-layer "$STEPS_PER_LAYER" \
  --init-buffer-size "$INIT_BUFFER_SIZE" \
  --device cpu \
  --seed "$SEED" \
  2>&1 | tee "$OUT_DIR/logs/grid_export.log"

echo "[SIDInspector GRID-MUSICAL] DONE: $GRID_OUT"
find "$GRID_OUT" -maxdepth 3 -type f | sort
