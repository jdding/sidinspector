#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
RESID_DIR="${RESID_DIR:-$ROOT_DIR/_gate0_repos/ReSID}"
DATASET_NAME="${DATASET_NAME:-Sports_and_Outdoors}"
RESID_DATASET_ROOT="${RESID_DATASET_ROOT:-$ROOT_DIR/_gate0_repos/ReSID-dataset}"
DATASET_DIR="${DATASET_DIR:-$RESID_DATASET_ROOT/$DATASET_NAME/leave_one_out/dataset}"
RUN_ROOT="${RUN_ROOT:-$ROOT_DIR/_gate0_artifacts/autodl_runs}"
EXP_ID="${EXP_ID:-g0_canonical_${DATASET_NAME}_resid_famae1_seed42}"
SOURCE_EXP_ID="${SOURCE_EXP_ID:-$EXP_ID}"
OUT_DIR="$RUN_ROOT/$EXP_ID"
SOURCE_OUT_DIR="$RUN_ROOT/$SOURCE_EXP_ID"
CONFIG_DIR="$OUT_DIR/configs"
LOG_DIR="$OUT_DIR/logs"
GAOQ_DEVICE="${GAOQ_DEVICE:-cpu}"
NUM_WORKERS="${NUM_WORKERS:-8}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
GAOQ_NUM_THREADS="${GAOQ_NUM_THREADS:-8}"
GAOQ_KMEANS_N_JOBS="${GAOQ_KMEANS_N_JOBS:-$GAOQ_NUM_THREADS}"
GAOQ_USE_BALANCED_KMEANS_OVERRIDE="${GAOQ_USE_BALANCED_KMEANS_OVERRIDE:-}"
GAOQ_METHOD_NAME="${GAOQ_METHOD_NAME:-resid_gaoq}"

echo "[AUDIT-SID GAOQ-only] root=$ROOT_DIR"
echo "[AUDIT-SID GAOQ-only] exp_id=$EXP_ID"
echo "[AUDIT-SID GAOQ-only] source_exp_id=$SOURCE_EXP_ID"
echo "[AUDIT-SID GAOQ-only] dataset=$DATASET_NAME"
echo "[AUDIT-SID GAOQ-only] out_dir=$OUT_DIR"
echo "[AUDIT-SID GAOQ-only] device=$GAOQ_DEVICE threads=$GAOQ_NUM_THREADS n_jobs=$GAOQ_KMEANS_N_JOBS"
echo "[AUDIT-SID GAOQ-only] method=$GAOQ_METHOD_NAME balanced_override=${GAOQ_USE_BALANCED_KMEANS_OVERRIDE:-none}"

if [ ! -d "$SOURCE_OUT_DIR" ]; then
  echo "Missing source ReSID run dir: $SOURCE_OUT_DIR" >&2
  exit 2
fi
if [ ! -f "$SOURCE_OUT_DIR/configs/gaoq.yaml" ]; then
  echo "Missing source GAOQ config: $SOURCE_OUT_DIR/configs/gaoq.yaml" >&2
  exit 2
fi

mkdir -p "$CONFIG_DIR" "$LOG_DIR"
if [ "$SOURCE_OUT_DIR" != "$OUT_DIR" ]; then
  cp "$SOURCE_OUT_DIR/configs/gaoq.yaml" "$CONFIG_DIR/gaoq.yaml"
fi
if [ -n "$GAOQ_USE_BALANCED_KMEANS_OVERRIDE" ]; then
  case "$GAOQ_USE_BALANCED_KMEANS_OVERRIDE" in
    true|false) ;;
    *)
      echo "GAOQ_USE_BALANCED_KMEANS_OVERRIDE must be true or false, got: $GAOQ_USE_BALANCED_KMEANS_OVERRIDE" >&2
      exit 2
      ;;
  esac
  CONFIG_PATH="$CONFIG_DIR/gaoq.yaml" GAOQ_BALANCED="$GAOQ_USE_BALANCED_KMEANS_OVERRIDE" "$PYTHON_BIN" - <<'PY'
import os
from pathlib import Path

path = Path(os.environ["CONFIG_PATH"])
lines = path.read_text().splitlines()
updated = []
done = False
for line in lines:
    if line.startswith("use_balancedkmeans:"):
        updated.append(f"use_balancedkmeans: {os.environ['GAOQ_BALANCED']}")
        done = True
    else:
        updated.append(line)
if not done:
    updated.append(f"use_balancedkmeans: {os.environ['GAOQ_BALANCED']}")
path.write_text("\n".join(updated) + "\n")
PY
fi

"$PYTHON_BIN" "$ROOT_DIR/tools/autodl_audit_sid/patch_resid_runtime.py" \
  --resid-dir "$RESID_DIR"

export OMP_NUM_THREADS="$GAOQ_NUM_THREADS"
export MKL_NUM_THREADS="$GAOQ_NUM_THREADS"
export OPENBLAS_NUM_THREADS="$GAOQ_NUM_THREADS"
export NUMEXPR_NUM_THREADS="$GAOQ_NUM_THREADS"
export GAOQ_KMEANS_N_JOBS="$GAOQ_KMEANS_N_JOBS"

pushd "$RESID_DIR" >/dev/null
PYTHONPATH="$ROOT_DIR/src:$RESID_DIR" PYTHONPYCACHEPREFIX=/tmp/audit_sid_pycache \
  "$PYTHON_BIN" main.py --config "$CONFIG_DIR/gaoq.yaml" --device "$GAOQ_DEVICE" \
  2>&1 | tee "$OUT_DIR/gaoq_only_stdout.log"
popd >/dev/null

GAOQ_MAPPING="$(find "$LOG_DIR/gaoq" -path '*/item_feature/item_code_mapping.parquet' -print | sort | tail -1)"
if [ -z "$GAOQ_MAPPING" ]; then
  echo "GAOQ item_code_mapping.parquet not found under $LOG_DIR" >&2
  exit 4
fi
echo "[AUDIT-SID GAOQ-only] mapping=$GAOQ_MAPPING"

PYTHONPATH="$ROOT_DIR/src" PYTHONPYCACHEPREFIX=/tmp/audit_sid_pycache \
  "$PYTHON_BIN" -m audit_sid.adapters.resid \
  --dataset-root "$DATASET_DIR" \
  --output-dir "$OUT_DIR/normalized" \
  --dataset-name "$DATASET_NAME" \
  --gaoq-mapping "$GAOQ_MAPPING" \
  --method "$GAOQ_METHOD_NAME"

PYTHONPATH="$ROOT_DIR/src" PYTHONPYCACHEPREFIX=/tmp/audit_sid_pycache \
  "$PYTHON_BIN" -m audit_sid.metrics \
  --sid-assignments "$OUT_DIR/normalized/sid_assignments.parquet" \
  --item-metadata "$OUT_DIR/normalized/item_metadata.parquet" \
  --interactions "$OUT_DIR/normalized/interactions.parquet" \
  --output-dir "$OUT_DIR/metrics"

echo "[AUDIT-SID GAOQ-only] DONE: $OUT_DIR"
