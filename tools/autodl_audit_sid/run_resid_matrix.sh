#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
MATRIX_MODE="${MATRIX_MODE:-gate0}"

run_one() {
  local exp_id="$1"
  local epochs="$2"
  local seed="$3"
  echo "[AUDIT-SID matrix] starting $exp_id epochs=$epochs seed=$seed"
  EXP_ID="$exp_id" FAMAE_EPOCHS="$epochs" SEED="$seed" \
    bash "$ROOT_DIR/tools/autodl_audit_sid/run_resid_gate0_export.sh"
  echo "[AUDIT-SID matrix] finished $exp_id"
}

case "$MATRIX_MODE" in
  gate0)
    run_one "g0_e1_resid_famae1_seed42" 1 42
    ;;
  robust)
    run_one "g0_e1_resid_famae1_seed42" 1 42
    run_one "g0_e2_resid_famae5_seed42" 5 42
    run_one "g0_e3_resid_famae5_seed43" 5 43
    ;;
  quality)
    run_one "g0_e2_resid_famae5_seed42" 5 42
    run_one "g0_e3_resid_famae5_seed43" 5 43
    run_one "g0_e4_resid_famae20_seed42" 20 42
    ;;
  *)
    echo "Unknown MATRIX_MODE=$MATRIX_MODE. Use gate0, robust, or quality." >&2
    exit 2
    ;;
esac
