#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
RESID_DIR="${RESID_DIR:-$ROOT_DIR/_gate0_repos/ReSID}"
DATASET_DIR="${DATASET_DIR:-$ROOT_DIR/_gate0_repos/ReSID-dataset/Musical_Instruments/leave_one_out/dataset}"
RUN_ROOT="${RUN_ROOT:-$ROOT_DIR/_gate0_artifacts/autodl_runs}"
EXP_ID="${EXP_ID:-resid_gate0_e${FAMAE_EPOCHS:-3}_seed${SEED:-42}_$(date +%Y%m%d_%H%M%S)}"
OUT_DIR="$RUN_ROOT/$EXP_ID"
CONFIG_DIR="$OUT_DIR/configs"
LOG_DIR="$OUT_DIR/logs"
FAMAE_EPOCHS="${FAMAE_EPOCHS:-3}"
SEED="${SEED:-42}"
DEVICE="${DEVICE:-cuda:0}"
GAOQ_DEVICE="${GAOQ_DEVICE:-cpu}"
NUM_WORKERS="${NUM_WORKERS:-4}"
BATCH_SIZE="${BATCH_SIZE:-2048}"
B1="${B1:-32}"
B2="${B2:-40}"
G2="${G2:-40}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

mkdir -p "$CONFIG_DIR" "$LOG_DIR"

echo "[AUDIT-SID] root=$ROOT_DIR"
echo "[AUDIT-SID] exp_id=$EXP_ID"
echo "[AUDIT-SID] resid_dir=$RESID_DIR"
echo "[AUDIT-SID] dataset_dir=$DATASET_DIR"
echo "[AUDIT-SID] device=$DEVICE gaoq_device=$GAOQ_DEVICE"

if [ ! -d "$RESID_DIR" ]; then
  echo "Missing ReSID repo: $RESID_DIR" >&2
  exit 2
fi
if [ ! -d "$DATASET_DIR" ]; then
  echo "Missing ReSID dataset: $DATASET_DIR" >&2
  exit 2
fi

"$PYTHON_BIN" -m pip install -q \
  pyyaml tqdm pandas pyarrow transformers scikit-learn scipy \
  numpy==1.26.4 k-means-constrained==0.7.3

"$PYTHON_BIN" - <<'PY'
from pathlib import Path
import os

path = Path(os.environ["RESID_DIR"]) / "utils.py"
text = path.read_text()
text = text.replace("num_workers=4,", "num_workers=getattr(args, \"num_workers\", 4),")
text = text.replace("pin_memory=True,", "pin_memory=torch.cuda.is_available(),")
path.write_text(text)
PY

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
use_balancedkmeans: true
version: ${EXP_ID}_gaoq
YAML

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
  --dataset-name Musical_Instruments \
  --gaoq-mapping "$GAOQ_MAPPING"

PYTHONPATH="$ROOT_DIR/src" PYTHONPYCACHEPREFIX=/tmp/audit_sid_pycache \
  "$PYTHON_BIN" -m audit_sid.metrics \
  --sid-assignments "$OUT_DIR/normalized/sid_assignments.parquet" \
  --item-metadata "$OUT_DIR/normalized/item_metadata.parquet" \
  --interactions "$OUT_DIR/normalized/interactions.parquet" \
  --output-dir "$OUT_DIR/metrics"

echo "[AUDIT-SID] DONE: $OUT_DIR"
find "$OUT_DIR" -maxdepth 3 -type f | sort
