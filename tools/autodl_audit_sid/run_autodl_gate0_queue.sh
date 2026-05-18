#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
QUEUE_MODE="${QUEUE_MODE:-quick}"
DEVICE="${DEVICE:-cuda:0}"
NUM_WORKERS="${NUM_WORKERS:-8}"
SUMMARY_PATH="${SUMMARY_PATH:-$ROOT_DIR/_gate0_artifacts/autodl_runs/gate0_summary.csv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

bash "$ROOT_DIR/tools/autodl_audit_sid/preflight_autodl.sh"

case "$QUEUE_MODE" in
  quick)
    MATRIX_MODE=gate0 DEVICE="$DEVICE" NUM_WORKERS="$NUM_WORKERS" PYTHON_BIN="$PYTHON_BIN" \
      bash "$ROOT_DIR/tools/autodl_audit_sid/run_resid_matrix.sh"
    CARD_EPOCHS=5 DEVICE="$DEVICE" NUM_WORKERS="$NUM_WORKERS" PYTHON_BIN="$PYTHON_BIN" \
      EXP_ID=card_rqvae_feature_proxy_e5_seed42 \
      bash "$ROOT_DIR/tools/autodl_audit_sid/run_card_rqvae_export.sh"
    ;;
  robust)
    MATRIX_MODE=robust DEVICE="$DEVICE" NUM_WORKERS="$NUM_WORKERS" PYTHON_BIN="$PYTHON_BIN" \
      bash "$ROOT_DIR/tools/autodl_audit_sid/run_resid_matrix.sh"
    CARD_EPOCHS=20 DEVICE="$DEVICE" NUM_WORKERS="$NUM_WORKERS" PYTHON_BIN="$PYTHON_BIN" \
      EXP_ID=card_rqvae_feature_proxy_e20_seed42 \
      bash "$ROOT_DIR/tools/autodl_audit_sid/run_card_rqvae_export.sh"
    ;;
  quality)
    MATRIX_MODE=quality DEVICE="$DEVICE" NUM_WORKERS="$NUM_WORKERS" PYTHON_BIN="$PYTHON_BIN" \
      bash "$ROOT_DIR/tools/autodl_audit_sid/run_resid_matrix.sh"
    CARD_EPOCHS=20 DEVICE="$DEVICE" NUM_WORKERS="$NUM_WORKERS" PYTHON_BIN="$PYTHON_BIN" \
      EXP_ID=card_rqvae_feature_proxy_e20_seed42 \
      bash "$ROOT_DIR/tools/autodl_audit_sid/run_card_rqvae_export.sh"
    CARD_EPOCHS=50 DEVICE="$DEVICE" NUM_WORKERS="$NUM_WORKERS" PYTHON_BIN="$PYTHON_BIN" \
      EXP_ID=card_rqvae_feature_proxy_e50_seed42 \
      bash "$ROOT_DIR/tools/autodl_audit_sid/run_card_rqvae_export.sh"
    ;;
  *)
    echo "Unknown QUEUE_MODE=$QUEUE_MODE. Use quick, robust, or quality." >&2
    exit 2
    ;;
esac

PYTHONPATH="$ROOT_DIR/src" "$PYTHON_BIN" "$ROOT_DIR/tools/autodl_audit_sid/summarize_gate0_runs.py" \
  --run-root "$ROOT_DIR/_gate0_artifacts/autodl_runs" \
  --output "$SUMMARY_PATH"

echo "[AUDIT-SID queue] summary=$SUMMARY_PATH"
