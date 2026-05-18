#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
QUEUE_MODE="${QUEUE_MODE:-quick}"
DEVICE="${DEVICE:-cuda:0}"
NUM_WORKERS="${NUM_WORKERS:-8}"
SUMMARY_PATH="${SUMMARY_PATH:-$ROOT_DIR/_gate0_artifacts/autodl_runs/gate0_summary.csv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
CARD_SOURCE_FAIL="${CARD_SOURCE_FAIL:-skip}"
SKIP_QUEUE_PIP_INSTALL="${SKIP_QUEUE_PIP_INSTALL:-0}"
ALLOW_RESID_ONLY="${ALLOW_RESID_ONLY:-0}"

mkdir -p "$ROOT_DIR/_gate0_artifacts/autodl_runs"

REQUIRE_CUDA=1 bash "$ROOT_DIR/tools/autodl_audit_sid/preflight_autodl.sh"

CARD_READY=1
if ! "$PYTHON_BIN" "$ROOT_DIR/tools/autodl_audit_sid/check_card_source.py" \
    --card-dir "$ROOT_DIR/_gate0_repos/CARD"; then
  CARD_READY=0
fi

if [ "$CARD_READY" != "1" ] && [ "$QUEUE_MODE" != "quick" ] && [ "$ALLOW_RESID_ONLY" != "1" ]; then
  echo "[AUDIT-SID queue] CARD/Cluster-A source is incomplete; refusing QUEUE_MODE=$QUEUE_MODE." >&2
  echo "[AUDIT-SID queue] Run QUEUE_MODE=quick for bounded smoke, or set ALLOW_RESID_ONLY=1 explicitly." >&2
  exit 21
fi

if [ "$SKIP_QUEUE_PIP_INSTALL" != "1" ]; then
  "$PYTHON_BIN" -m pip install -q \
    pyyaml tqdm pandas pyarrow transformers scikit-learn scipy \
    numpy==1.26.4 k-means-constrained==0.7.3
else
  echo "[AUDIT-SID queue] SKIP_QUEUE_PIP_INSTALL=1; using existing Python environment"
fi

export SKIP_PIP_INSTALL=1

run_card() {
  local exp_id="$1"
  local epochs="$2"
  local seed="$3"
  local widths="$4"
  local layers="$5"
  if [ "$CARD_READY" != "1" ]; then
    echo "[AUDIT-SID queue] CARD source incomplete for $exp_id"
    if [ "$CARD_SOURCE_FAIL" = "skip" ]; then
      mkdir -p "$ROOT_DIR/_gate0_artifacts/autodl_runs/$exp_id"
      {
        echo "status=SKIPPED_CARD_SOURCE_INCOMPLETE"
        echo "exp_id=$exp_id"
        date
      } > "$ROOT_DIR/_gate0_artifacts/autodl_runs/$exp_id/SKIPPED.txt"
      return 0
    fi
    return 20
  fi
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
  --output "$SUMMARY_PATH" \
  --strict

echo "[AUDIT-SID queue] summary=$SUMMARY_PATH"
