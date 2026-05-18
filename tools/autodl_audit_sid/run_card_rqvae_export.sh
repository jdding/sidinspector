#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
CARD_DIR="${CARD_DIR:-$ROOT_DIR/_gate0_repos/CARD}"
ITEM_METADATA="${ITEM_METADATA:-$ROOT_DIR/_gate0_artifacts/resid_musical_normalized/item_metadata.parquet}"
INTERACTIONS="${INTERACTIONS:-$ROOT_DIR/_gate0_artifacts/resid_musical_normalized/interactions.parquet}"
RUN_ROOT="${RUN_ROOT:-$ROOT_DIR/_gate0_artifacts/autodl_runs}"
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

mkdir -p "$OUT_DIR" "$CKPT_DIR"

echo "[AUDIT-SID CARD] root=$ROOT_DIR"
echo "[AUDIT-SID CARD] exp_id=$EXP_ID"
echo "[AUDIT-SID CARD] card_dir=$CARD_DIR"
echo "[AUDIT-SID CARD] item_metadata=$ITEM_METADATA"
echo "[AUDIT-SID CARD] device=$DEVICE"

if [ ! -d "$CARD_DIR" ]; then
  echo "Missing CARD repo: $CARD_DIR" >&2
  exit 2
fi
if [ ! -f "$ITEM_METADATA" ]; then
  echo "Missing item metadata: $ITEM_METADATA" >&2
  exit 2
fi

"$PYTHON_BIN" -m pip install -q pandas pyarrow numpy==1.26.4 tqdm transformers scikit-learn

ITEM_METADATA="$ITEM_METADATA" INPUT_PARQUET="$INPUT_PARQUET" "$PYTHON_BIN" - <<'PY'
import os
import numpy as np
import pandas as pd

src = os.environ["ITEM_METADATA"]
dst = os.environ["INPUT_PARQUET"]
frame = pd.read_parquet(src)
feature_cols = [c for c in ("store_id", "category_l1", "category_l2", "category_l3") if c in frame.columns]
if not feature_cols:
    raise SystemExit("No categorical feature columns found for CARD feature-proxy item_emb.parquet")

encoded = pd.get_dummies(frame[feature_cols].astype(str), dtype=np.float32)
values = encoded.to_numpy(dtype=np.float32)
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
echo "[AUDIT-SID CARD] checkpoint: $BEST_CKPT"

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
  --dataset-name Musical_Instruments \
  --method card_rqvae_feature_proxy

PYTHONPATH="$ROOT_DIR/src" PYTHONPYCACHEPREFIX=/tmp/audit_sid_pycache \
  "$PYTHON_BIN" -m audit_sid.metrics \
  --sid-assignments "$OUT_DIR/normalized/sid_assignments.parquet" \
  --item-metadata "$ITEM_METADATA" \
  --interactions "$INTERACTIONS" \
  --output-dir "$OUT_DIR/metrics"

echo "[AUDIT-SID CARD] DONE: $OUT_DIR"
find "$OUT_DIR" -maxdepth 3 -type f | sort
