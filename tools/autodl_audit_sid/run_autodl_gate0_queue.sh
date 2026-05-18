#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
QUEUE_MODE="${QUEUE_MODE:-quick}"
DEVICE="${DEVICE:-cuda:0}"
NUM_WORKERS="${NUM_WORKERS:-8}"
SUMMARY_PATH="${SUMMARY_PATH:-$ROOT_DIR/_gate0_artifacts/autodl_runs/gate0_summary.csv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

bash "$ROOT_DIR/tools/autodl_audit_sid/preflight_autodl.sh"

run_card() {
  local exp_id="$1"
  local epochs="$2"
  local seed="$3"
  local widths="$4"
  local layers="$5"
  CARD_EPOCHS="$epochs" SEED="$seed" DEVICE="$DEVICE" NUM_WORKERS="$NUM_WORKERS" \
    PYTHON_BIN="$PYTHON_BIN" EXP_ID="$exp_id" CODEBOOK_WIDTHS="$widths" LAYERS="$layers" \
    bash "$ROOT_DIR/tools/autodl_audit_sid/run_card_rqvae_export.sh"
}

case "$QUEUE_MODE" in
  quick)
    MATRIX_MODE=gate0 DEVICE="$DEVICE" NUM_WORKERS="$NUM_WORKERS" PYTHON_BIN="$PYTHON_BIN" \
      bash "$ROOT_DIR/tools/autodl_audit_sid/run_resid_matrix.sh"
    run_card "card_rqvae_feature_proxy_e5_seed42" 5 42 "32 40 19" "128 64"
    ;;
  robust)
    MATRIX_MODE=robust DEVICE="$DEVICE" NUM_WORKERS="$NUM_WORKERS" PYTHON_BIN="$PYTHON_BIN" \
      bash "$ROOT_DIR/tools/autodl_audit_sid/run_resid_matrix.sh"
    run_card "card_rqvae_feature_proxy_e20_seed42" 20 42 "32 40 19" "128 64"
    ;;
  sweep)
    MATRIX_MODE=sweep DEVICE="$DEVICE" NUM_WORKERS="$NUM_WORKERS" PYTHON_BIN="$PYTHON_BIN" \
      bash "$ROOT_DIR/tools/autodl_audit_sid/run_resid_matrix.sh"
    run_card "card_rqvae_feature_proxy_e5_seed42" 5 42 "32 40 19" "128 64"
    run_card "card_rqvae_feature_proxy_e20_seed42" 20 42 "32 40 19" "128 64"
    run_card "card_rqvae_feature_proxy_e20_seed43" 20 43 "32 40 19" "128 64"
    run_card "card_rqvae_feature_proxy_e20_seed42_cap_small" 20 42 "16 32 16" "128 64"
    run_card "card_rqvae_feature_proxy_e20_seed42_cap_large" 20 42 "64 64 32" "256 128"
    ;;
  quality)
    MATRIX_MODE=quality DEVICE="$DEVICE" NUM_WORKERS="$NUM_WORKERS" PYTHON_BIN="$PYTHON_BIN" \
      bash "$ROOT_DIR/tools/autodl_audit_sid/run_resid_matrix.sh"
    run_card "card_rqvae_feature_proxy_e20_seed42" 20 42 "32 40 19" "128 64"
    run_card "card_rqvae_feature_proxy_e50_seed42" 50 42 "32 40 19" "256 128"
    ;;
  *)
    echo "Unknown QUEUE_MODE=$QUEUE_MODE. Use quick, robust, sweep, or quality." >&2
    exit 2
    ;;
esac

PYTHONPATH="$ROOT_DIR/src" "$PYTHON_BIN" "$ROOT_DIR/tools/autodl_audit_sid/summarize_gate0_runs.py" \
  --run-root "$ROOT_DIR/_gate0_artifacts/autodl_runs" \
  --output "$SUMMARY_PATH"

echo "[AUDIT-SID queue] summary=$SUMMARY_PATH"
