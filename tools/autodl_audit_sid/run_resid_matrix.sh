#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
MATRIX_MODE="${MATRIX_MODE:-gate0}"
SMOKE_DATASET="${SMOKE_DATASET:-Musical_Instruments}"
CANONICAL_DATASET="${CANONICAL_DATASET:-Sports_and_Outdoors}"

run_one() {
  local dataset_name="$1"
  local exp_id="$2"
  local epochs="$3"
  local seed="$4"
  local b1="${5:-}"
  local b2="${6:-}"
  local g2="${7:-}"
  echo "[SIDInspector matrix] starting $exp_id dataset=$dataset_name epochs=$epochs seed=$seed"
  DATASET_NAME="$dataset_name" EXP_ID="$exp_id" FAMAE_EPOCHS="$epochs" SEED="$seed" \
    B1="$b1" B2="$b2" G2="$g2" \
    GAOQ_NUM_THREADS="${GAOQ_NUM_THREADS:-$NUM_WORKERS}" \
    GAOQ_KMEANS_N_JOBS="${GAOQ_KMEANS_N_JOBS:-${GAOQ_NUM_THREADS:-$NUM_WORKERS}}" \
    GAOQ_USE_BALANCED_KMEANS="${GAOQ_USE_BALANCED_KMEANS:-true}" \
    bash "$ROOT_DIR/tools/autodl_audit_sid/run_resid_gate0_export.sh"
  echo "[SIDInspector matrix] finished $exp_id"
}

case "$MATRIX_MODE" in
  gate0)
    run_one "$SMOKE_DATASET" "g0_smoke_${SMOKE_DATASET}_resid_famae1_seed42" 1 42
    ;;
  canonical)
    run_one "$CANONICAL_DATASET" "g0_canonical_${CANONICAL_DATASET}_resid_famae1_seed42" 1 42
    ;;
  robust)
    run_one "$CANONICAL_DATASET" "g0_canonical_${CANONICAL_DATASET}_resid_famae1_seed42" 1 42
    run_one "$CANONICAL_DATASET" "g0_canonical_${CANONICAL_DATASET}_resid_famae5_seed42" 5 42
    run_one "$CANONICAL_DATASET" "g0_canonical_${CANONICAL_DATASET}_resid_famae5_seed43" 5 43
    ;;
  sweep)
    run_one "$CANONICAL_DATASET" "g0_canonical_${CANONICAL_DATASET}_resid_famae1_seed42" 1 42
    run_one "$CANONICAL_DATASET" "g0_canonical_${CANONICAL_DATASET}_resid_famae5_seed42" 5 42
    run_one "$CANONICAL_DATASET" "g0_canonical_${CANONICAL_DATASET}_resid_famae5_seed43" 5 43
    run_one "$CANONICAL_DATASET" "g0_canonical_${CANONICAL_DATASET}_resid_famae5_seed42_cap_small" 5 42 64 96 96
    run_one "$CANONICAL_DATASET" "g0_canonical_${CANONICAL_DATASET}_resid_famae5_seed42_cap_large" 5 42 192 192 192
    ;;
  quality)
    run_one "$CANONICAL_DATASET" "g0_canonical_${CANONICAL_DATASET}_resid_famae5_seed42" 5 42
    run_one "$CANONICAL_DATASET" "g0_canonical_${CANONICAL_DATASET}_resid_famae5_seed43" 5 43
    run_one "$CANONICAL_DATASET" "g0_canonical_${CANONICAL_DATASET}_resid_famae20_seed42" 20 42
    ;;
  *)
    echo "Unknown MATRIX_MODE=$MATRIX_MODE. Use gate0, canonical, robust, sweep, or quality." >&2
    exit 2
    ;;
esac
