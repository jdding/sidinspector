#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
DATASET_NAME="${DATASET_NAME:-Musical_Instruments}"
CARD_DIR="${CARD_DIR:-$ROOT_DIR/_gate0_repos/CARD}"
ITEM_METADATA="${ITEM_METADATA:-$ROOT_DIR/_gate0_artifacts/resid_${DATASET_NAME}_normalized/item_metadata.parquet}"
INTERACTIONS="${INTERACTIONS:-$ROOT_DIR/_gate0_artifacts/resid_${DATASET_NAME}_normalized/interactions.parquet}"
RUN_ROOT="${RUN_ROOT:-$ROOT_DIR/_gate0_artifacts/autodl_runs}"
case "$RUN_ROOT" in
  /*) ;;
  *) RUN_ROOT="$ROOT_DIR/$RUN_ROOT" ;;
esac
EXP_ID="${EXP_ID:-card_rqvae_e${CARD_EPOCHS:-20}_seed${SEED:-42}_$(date +%Y%m%d_%H%M%S)}"
OUT_DIR="$RUN_ROOT/$EXP_ID"
INPUT_PARQUET="$OUT_DIR/item_emb.parquet"
CKPT_DIR="$OUT_DIR/ckpt"
CODE_PATH="$OUT_DIR/card_rqvae_codes.npy"
CARD_EPOCHS="${CARD_EPOCHS:-20}"
SEED="${SEED:-42}"
DEVICE="${DEVICE:-cuda:0}"
NUM_WORKERS="${NUM_WORKERS:-8}"
BATCH_SIZE="${BATCH_SIZE:-1024}"
CODEBOOK_WIDTHS="${CODEBOOK_WIDTHS:-32 40 19}"
LAYERS="${LAYERS:-128 64}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
SKIP_PIP_INSTALL="${SKIP_PIP_INSTALL:-0}"
CARD_FEATURE_MODE="${CARD_FEATURE_MODE:-onehot}"

mkdir -p "$OUT_DIR" "$CKPT_DIR"

if [ ! -f "$ITEM_METADATA" ] && [ "$DATASET_NAME" = "Musical_Instruments" ]; then
  LEGACY_DIR="$ROOT_DIR/_gate0_artifacts/resid_musical_normalized"
  if [ -f "$LEGACY_DIR/item_metadata.parquet" ]; then
    ITEM_METADATA="$LEGACY_DIR/item_metadata.parquet"
    INTERACTIONS="$LEGACY_DIR/interactions.parquet"
  fi
fi

echo "[SIDInspector CARD] root=$ROOT_DIR"
echo "[SIDInspector CARD] exp_id=$EXP_ID"
echo "[SIDInspector CARD] card_dir=$CARD_DIR"
echo "[SIDInspector CARD] dataset=$DATASET_NAME"
echo "[SIDInspector CARD] item_metadata=$ITEM_METADATA"
echo "[SIDInspector CARD] device=$DEVICE"
echo "[SIDInspector CARD] feature_mode=$CARD_FEATURE_MODE"

if [ ! -d "$CARD_DIR" ]; then
  echo "Missing CARD repo: $CARD_DIR" >&2
  exit 2
fi
if [ ! -f "$ITEM_METADATA" ]; then
  echo "Missing item metadata: $ITEM_METADATA" >&2
  exit 2
fi

if [ "$SKIP_PIP_INSTALL" != "1" ]; then
  "$PYTHON_BIN" -m pip install -q pandas pyarrow numpy==1.26.4 tqdm transformers scikit-learn
else
  echo "[SIDInspector CARD] SKIP_PIP_INSTALL=1; using existing Python environment"
fi

ITEM_METADATA="$ITEM_METADATA" INPUT_PARQUET="$INPUT_PARQUET" CARD_FEATURE_MODE="$CARD_FEATURE_MODE" "$PYTHON_BIN" - <<'PY'
import os
import numpy as np
import pandas as pd

src = os.environ["ITEM_METADATA"]
dst = os.environ["INPUT_PARQUET"]
mode = os.environ.get("CARD_FEATURE_MODE", "onehot")
frame = pd.read_parquet(src)
feature_cols = [c for c in ("store_id", "category_l1", "category_l2", "category_l3") if c in frame.columns]
if not feature_cols:
    raise SystemExit("No categorical feature columns found for CARD feature-proxy item_emb.parquet")

if mode == "onehot":
    encoded = pd.get_dummies(frame[feature_cols].astype(str), dtype=np.float32)
    values = encoded.to_numpy(dtype=np.float32)
elif mode == "compact":
    values_list = []
    for col in feature_cols:
        codes = pd.Categorical(frame[col].astype(str)).codes.astype(np.float32)
        denom = max(float(codes.max()), 1.0)
        scaled = codes / denom
        values_list.extend([scaled, np.sin(np.pi * scaled), np.cos(np.pi * scaled)])
    item_scaled = frame["item_id"].astype(np.float32).to_numpy()
    item_scaled = item_scaled / max(float(item_scaled.max()), 1.0)
    values_list.append(item_scaled)
    values = np.stack(values_list, axis=1).astype(np.float32)
else:
    raise SystemExit(f"Unknown CARD_FEATURE_MODE={mode}; use onehot or compact")

norm = np.linalg.norm(values, axis=1, keepdims=True)
values = values / np.maximum(norm, 1e-12)

out = pd.DataFrame({
    "ItemID": frame["item_id"].astype(int).to_numpy(),
    "embedding": [row for row in values],
})
out.to_parquet(dst, index=False)
print(f"wrote {len(out)} rows to {dst}; dim={values.shape[1]}")
PY

pushd "$CARD_DIR/rqvae4" >/dev/null
PYTHONPATH="$CARD_DIR" PYTHONPYCACHEPREFIX=/tmp/audit_sid_pycache \
  "$PYTHON_BIN" main.py \
  --data_path "$INPUT_PARQUET" \
  --epochs "$CARD_EPOCHS" \
  --batch_size "$BATCH_SIZE" \
  --num_workers "$NUM_WORKERS" \
  --eval_step 1 \
  --warmup_epochs 1 \
  --device "$DEVICE" \
  --num_emb_list $CODEBOOK_WIDTHS \
  --layers $LAYERS \
  --ckpt_dir "$CKPT_DIR" \
  2>&1 | tee "$OUT_DIR/card_train_stdout.log"
popd >/dev/null

BEST_CKPT="$(find "$CKPT_DIR" -name best_collision_model.pth -print | sort | tail -1)"
if [ -z "$BEST_CKPT" ]; then
  echo "CARD best_collision_model.pth not found under $CKPT_DIR" >&2
  exit 3
fi
echo "[SIDInspector CARD] checkpoint: $BEST_CKPT"

pushd "$CARD_DIR/rqvae4" >/dev/null
PYTHONPATH="$CARD_DIR" PYTHONPYCACHEPREFIX=/tmp/audit_sid_pycache \
  "$PYTHON_BIN" generate_code.py \
  --ckpt_path "$BEST_CKPT" \
  --data_path "$INPUT_PARQUET" \
  --out_path "$CODE_PATH" \
  --device "$DEVICE" \
  --batch_size "$BATCH_SIZE" \
  2>&1 | tee "$OUT_DIR/card_generate_code_stdout.log"
popd >/dev/null

PYTHONPATH="$ROOT_DIR/src" PYTHONPYCACHEPREFIX=/tmp/audit_sid_pycache \
  "$PYTHON_BIN" -m audit_sid.adapters.card \
  --codes-path "$CODE_PATH" \
  --output-dir "$OUT_DIR/normalized" \
  --dataset-name "$DATASET_NAME" \
  --method card_rqvae_feature_proxy

PYTHONPATH="$ROOT_DIR/src" PYTHONPYCACHEPREFIX=/tmp/audit_sid_pycache \
  "$PYTHON_BIN" -m audit_sid.metrics \
  --sid-assignments "$OUT_DIR/normalized/sid_assignments.parquet" \
  --item-metadata "$ITEM_METADATA" \
  --interactions "$INTERACTIONS" \
  --output-dir "$OUT_DIR/metrics"

echo "[SIDInspector CARD] DONE: $OUT_DIR"
find "$OUT_DIR" -maxdepth 3 -type f | sort
