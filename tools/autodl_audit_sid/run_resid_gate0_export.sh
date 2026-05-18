#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
RESID_DIR="${RESID_DIR:-$ROOT_DIR/_gate0_repos/ReSID}"
DATASET_NAME="${DATASET_NAME:-Musical_Instruments}"
RESID_DATASET_ROOT="${RESID_DATASET_ROOT:-$ROOT_DIR/_gate0_repos/ReSID-dataset}"
DATASET_DIR="${DATASET_DIR:-$RESID_DATASET_ROOT/$DATASET_NAME/leave_one_out/dataset}"
RUN_ROOT="${RUN_ROOT:-$ROOT_DIR/_gate0_artifacts/autodl_runs}"
EXP_ID="${EXP_ID:-resid_${DATASET_NAME}_e${FAMAE_EPOCHS:-3}_seed${SEED:-42}_$(date +%Y%m%d_%H%M%S)}"
OUT_DIR="$RUN_ROOT/$EXP_ID"
CONFIG_DIR="$OUT_DIR/configs"
LOG_DIR="$OUT_DIR/logs"
FAMAE_EPOCHS="${FAMAE_EPOCHS:-3}"
SEED="${SEED:-42}"
DEVICE="${DEVICE:-cuda:0}"
GAOQ_DEVICE="${GAOQ_DEVICE:-cpu}"
NUM_WORKERS="${NUM_WORKERS:-4}"
BATCH_SIZE="${BATCH_SIZE:-2048}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
SKIP_PIP_INSTALL="${SKIP_PIP_INSTALL:-0}"
GAOQ_USE_BALANCED_KMEANS="${GAOQ_USE_BALANCED_KMEANS:-true}"
GAOQ_NUM_THREADS="${GAOQ_NUM_THREADS:-$NUM_WORKERS}"
GAOQ_KMEANS_N_JOBS="${GAOQ_KMEANS_N_JOBS:-$GAOQ_NUM_THREADS}"
STOP_AFTER_FAMAE="${STOP_AFTER_FAMAE:-0}"

case "$DATASET_NAME" in
  Musical_Instruments)
    DEFAULT_B1=32
    DEFAULT_B2=40
    ;;
  Video_Games)
    DEFAULT_B1=32
    DEFAULT_B2=64
    ;;
  Industrial_and_Scientific)
    DEFAULT_B1=24
    DEFAULT_B2=80
    ;;
  Baby_Products)
    DEFAULT_B1=32
    DEFAULT_B2=64
    ;;
  Arts_Crafts_and_Sewing)
    DEFAULT_B1=64
    DEFAULT_B2=96
    ;;
  Sports_and_Outdoors)
    DEFAULT_B1=128
    DEFAULT_B2=128
    ;;
  Toys_and_Games)
    DEFAULT_B1=192
    DEFAULT_B2=192
    ;;
  Health_and_Household)
    DEFAULT_B1=50
    DEFAULT_B2=512
    ;;
  Beauty_and_Personal_Care)
    DEFAULT_B1=96
    DEFAULT_B2=192
    ;;
  Books)
    DEFAULT_B1=256
    DEFAULT_B2=256
    ;;
  *)
    echo "Unknown ReSID DATASET_NAME=$DATASET_NAME; set B1/B2/G2 explicitly." >&2
    DEFAULT_B1="${B1:-32}"
    DEFAULT_B2="${B2:-40}"
    ;;
esac

B1="${B1:-$DEFAULT_B1}"
B2="${B2:-$DEFAULT_B2}"
G2="${G2:-$B2}"

mkdir -p "$CONFIG_DIR" "$LOG_DIR"

echo "[AUDIT-SID] root=$ROOT_DIR"
echo "[AUDIT-SID] exp_id=$EXP_ID"
echo "[AUDIT-SID] resid_dir=$RESID_DIR"
echo "[AUDIT-SID] dataset_name=$DATASET_NAME"
echo "[AUDIT-SID] dataset_dir=$DATASET_DIR"
echo "[AUDIT-SID] code_size B1=$B1 B2=$B2 G2=$G2"
echo "[AUDIT-SID] device=$DEVICE gaoq_device=$GAOQ_DEVICE"
echo "[AUDIT-SID] gaoq_use_balancedkmeans=$GAOQ_USE_BALANCED_KMEANS gaoq_num_threads=$GAOQ_NUM_THREADS gaoq_kmeans_n_jobs=$GAOQ_KMEANS_N_JOBS"

if [ ! -d "$RESID_DIR" ]; then
  echo "Missing ReSID repo: $RESID_DIR" >&2
  exit 2
fi
if [ ! -d "$DATASET_DIR" ]; then
  echo "Missing ReSID dataset: $DATASET_DIR" >&2
  exit 2
fi

if [ "$SKIP_PIP_INSTALL" != "1" ]; then
  "$PYTHON_BIN" -m pip install -q \
    pyyaml tqdm pandas pyarrow transformers scikit-learn scipy \
    numpy==1.26.4 k-means-constrained==0.7.3
else
  echo "[AUDIT-SID] SKIP_PIP_INSTALL=1; using existing Python environment"
fi

case "$GAOQ_USE_BALANCED_KMEANS" in
  true|false) ;;
  *)
    echo "GAOQ_USE_BALANCED_KMEANS must be true or false, got: $GAOQ_USE_BALANCED_KMEANS" >&2
    exit 2
    ;;
esac

"$PYTHON_BIN" "$ROOT_DIR/tools/autodl_audit_sid/patch_resid_runtime.py" \
  --resid-dir "$RESID_DIR"

cat > "$CONFIG_DIR/famae.yaml" <<YAML
batch_size: $BATCH_SIZE
dataset: $DATASET_DIR/
decay_rate: 0.8
device: $DEVICE
dim_feedforward: 512
dropout: 0.1
early_stop: 3
embed_proj: none
epochs: $FAMAE_EPOCHS
eval_step: 1
feature:
- item_id
- store_id
- cate1_id
- cate2_id
- cate3_id
feature_emb_dim: 128
feature_fusion: sum
feature_loss_weight: 1
ffn_activation: relu
hidden_size: 128
is_causal: false
log_dir_path: $LOG_DIR/
lr: 0.001
max_len: 32
metric_feature:
  fusion_feature:
  - 10
  mask_item_id_recall_item_id:
  - 10
model: famae
momentum: null
monitor_metric:
- mask_item_id_recall_item_id
- fusion_feature
norm_adjust_type: none
norm_first: true
num_heads: 4
num_layers: 2
num_workers: $NUM_WORKERS
optimizer: AdamW
per_feature_loss_weights:
  cate1_id: 1
  cate2_id: 1
  cate3_id: 1
  item_id: 1
  store_id: 1
random_seed: $SEED
save_model: true
similarity: cosine_scaled
train_type: normal
use_input_layernorm: false
use_output_layernorm: false
version: ${EXP_ID}_famae
weight_decay: 1.0e-05
YAML

pushd "$RESID_DIR" >/dev/null
PYTHONPATH="$ROOT_DIR/src:$RESID_DIR" PYTHONPYCACHEPREFIX=/tmp/audit_sid_pycache \
  "$PYTHON_BIN" main.py --config "$CONFIG_DIR/famae.yaml" --device "$DEVICE" \
  2>&1 | tee "$OUT_DIR/famae_stdout.log"
popd >/dev/null

FAMAE_CKPT="$(find "$LOG_DIR/famae" -name best_model.pth -print | sort | tail -1)"
if [ -z "$FAMAE_CKPT" ]; then
  echo "FAMAE best_model.pth not found under $LOG_DIR" >&2
  exit 3
fi
echo "[AUDIT-SID] FAMAE checkpoint: $FAMAE_CKPT"

if [ "$STOP_AFTER_FAMAE" = "1" ]; then
  echo "[AUDIT-SID] STOP_AFTER_FAMAE=1; checkpoint prepared, skipping GAOQ export"
  echo "$FAMAE_CKPT" > "$OUT_DIR/famae_checkpoint_path.txt"
  exit 0
fi

cat > "$CONFIG_DIR/gaoq.yaml" <<YAML
b1: $B1
b2: $B2
batch_size: $BATCH_SIZE
dataset: $DATASET_DIR/
device: $GAOQ_DEVICE
embed_proj: none
feature:
- item_id
- store_id
- cate1_id
- cate2_id
- cate3_id
feature_emb_dim: 128
feature_fusion: concat
g2: $G2
l2norm: false
log_dir_path: $LOG_DIR/
max_len: 32
model: gaoq
num_workers: $NUM_WORKERS
pretrained_model_path: $FAMAE_CKPT
random_seed: $SEED
train_type: direct
use_balancedkmeans: $GAOQ_USE_BALANCED_KMEANS
version: ${EXP_ID}_gaoq
YAML

export OMP_NUM_THREADS="$GAOQ_NUM_THREADS"
export MKL_NUM_THREADS="$GAOQ_NUM_THREADS"
export OPENBLAS_NUM_THREADS="$GAOQ_NUM_THREADS"
export NUMEXPR_NUM_THREADS="$GAOQ_NUM_THREADS"
export GAOQ_KMEANS_N_JOBS="$GAOQ_KMEANS_N_JOBS"
echo "[AUDIT-SID] GAOQ CPU-only export: device=$GAOQ_DEVICE balanced=$GAOQ_USE_BALANCED_KMEANS"
echo "[AUDIT-SID] GAOQ thread env: OMP=$OMP_NUM_THREADS MKL=$MKL_NUM_THREADS OPENBLAS=$OPENBLAS_NUM_THREADS NUMEXPR=$NUMEXPR_NUM_THREADS KMEANS_N_JOBS=$GAOQ_KMEANS_N_JOBS"

pushd "$RESID_DIR" >/dev/null
PYTHONPATH="$ROOT_DIR/src:$RESID_DIR" PYTHONPYCACHEPREFIX=/tmp/audit_sid_pycache \
  "$PYTHON_BIN" main.py --config "$CONFIG_DIR/gaoq.yaml" --device "$GAOQ_DEVICE" \
  2>&1 | tee "$OUT_DIR/gaoq_stdout.log"
popd >/dev/null

GAOQ_MAPPING="$(find "$LOG_DIR/gaoq" -path '*/item_feature/item_code_mapping.parquet' -print | sort | tail -1)"
if [ -z "$GAOQ_MAPPING" ]; then
  echo "GAOQ item_code_mapping.parquet not found under $LOG_DIR" >&2
  exit 4
fi
echo "[AUDIT-SID] GAOQ mapping: $GAOQ_MAPPING"

PYTHONPATH="$ROOT_DIR/src" PYTHONPYCACHEPREFIX=/tmp/audit_sid_pycache \
  "$PYTHON_BIN" -m audit_sid.adapters.resid \
  --dataset-root "$DATASET_DIR" \
  --output-dir "$OUT_DIR/normalized" \
  --dataset-name "$DATASET_NAME" \
  --gaoq-mapping "$GAOQ_MAPPING"

PYTHONPATH="$ROOT_DIR/src" PYTHONPYCACHEPREFIX=/tmp/audit_sid_pycache \
  "$PYTHON_BIN" -m audit_sid.metrics \
  --sid-assignments "$OUT_DIR/normalized/sid_assignments.parquet" \
  --item-metadata "$OUT_DIR/normalized/item_metadata.parquet" \
  --interactions "$OUT_DIR/normalized/interactions.parquet" \
  --output-dir "$OUT_DIR/metrics"

echo "[AUDIT-SID] DONE: $OUT_DIR"
find "$OUT_DIR" -maxdepth 3 -type f | sort
