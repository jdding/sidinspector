#!/usr/bin/env bash
set -uo pipefail

WORKSPACE="${WORKSPACE:-/root/autodl-tmp/Sec_phrase}"
PYTHON_BIN="${PYTHON_BIN:-/root/miniconda3/bin/python}"
RUN_ID="${RUN_ID:-audit_sid_gate0a_grid_$(date +%Y%m%d_%H%M%S)}"
LOG_DIR="${WORKSPACE}/_gate0_artifacts/grid_cluster_a_runs/logs"
LOG_FILE="${LOG_DIR}/${RUN_ID}.log"
ARCHIVE_DIR="${ARCHIVE_DIR:-/root/autodl-fs/audit_sid/${RUN_ID}}"

if [ ! -d "$WORKSPACE" ]; then
  echo "Missing workspace: $WORKSPACE" >&2
  exit 2
fi

mkdir -p "$LOG_DIR"
exec > >(tee -a "$LOG_FILE") 2>&1

cd "$WORKSPACE" || exit 2

COMMIT="$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")"
MESSAGE="$(git log -1 --format='%s' 2>/dev/null || echo "N/A")"

echo "=== AUDIT-SID GATE0A GRID BATCH ==="
echo "Run ID: $RUN_ID"
echo "Workspace: $WORKSPACE"
echo "Python: $PYTHON_BIN"
date

echo "=== HARDWARE SPEC ==="
echo "Instance UUID: ${INSTANCE_UUID:-N/A}"
echo "CPU cores: $(nproc 2>/dev/null || echo 'N/A')"
echo "RAM total: $(free -h 2>/dev/null | awk '/^Mem:/{print $2}' || echo 'N/A')"
echo "GPU: $(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null | head -1 || echo 'N/A')"
echo "GPU utilization: $(nvidia-smi --query-gpu=index,utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null | head -1 || echo 'N/A')"
echo "====================="

echo "=== GIT VERSION ==="
echo "Git Commit: $COMMIT"
echo "Git Message: $MESSAGE"
echo "Git Diff:"
git diff --stat 2>/dev/null || true
echo "==================="

echo "=== INITIAL RESOURCE CHECK ==="
nvidia-smi --query-gpu=index,utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null || true
nvidia-smi pmon -c 1 2>/dev/null || true
free -h 2>/dev/null || true
ps aux | grep python | grep -v grep | head -20 || true
echo "=============================="

bash tools/autodl_audit_sid/preflight_gate0a_grid.sh

STATUS_FILE="${WORKSPACE}/_gate0_artifacts/grid_cluster_a_runs/${RUN_ID}_status.tsv"
mkdir -p "$(dirname "$STATUS_FILE")"
printf "exp_id\tmax_items\tseed\texit_code\tstarted_at\tfinished_at\n" > "$STATUS_FILE"

run_one() {
  local max_items="$1"
  local seed="$2"
  local exp_id="grid_official_rqkmeans_All_Beauty_text_${max_items}_cuda_seed${seed}"
  local start_ts
  local end_ts
  start_ts="$(date -Iseconds)"
  echo "=== RUN START $exp_id max_items=$max_items seed=$seed ==="
  SKIP_PIP_INSTALL=1 \
    PYTHON_BIN="$PYTHON_BIN" \
    MAX_ITEMS="$max_items" \
    CODEBOOK_WIDTH=128 \
    NUM_HIERARCHIES=3 \
    STEPS_PER_LAYER=40 \
    GRID_BATCH_SIZE=4096 \
    INIT_BUFFER_SIZE=8192 \
    DEVICE=cuda \
    EMBED_BATCH_SIZE=256 \
    SEED="$seed" \
    EXP_ID="$exp_id" \
    bash tools/autodl_audit_sid/run_gate0a_grid_batch.sh
  local exit_code=$?
  end_ts="$(date -Iseconds)"
  printf "%s\t%s\t%s\t%s\t%s\t%s\n" "$exp_id" "$max_items" "$seed" "$exit_code" "$start_ts" "$end_ts" >> "$STATUS_FILE"
  echo "=== RUN END $exp_id exit=$exit_code ==="
  return "$exit_code"
}

RUN_EXIT=0

run_one 20000 42 || RUN_EXIT=$?
if [ "$RUN_EXIT" = "0" ]; then run_one 20000 43 || RUN_EXIT=$?; fi
if [ "$RUN_EXIT" = "0" ]; then run_one 20000 44 || RUN_EXIT=$?; fi
if [ "$RUN_EXIT" = "0" ]; then run_one 50000 42 || RUN_EXIT=$?; fi

echo "=== FINAL RESOURCE CHECK ==="
nvidia-smi --query-gpu=index,utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null || true
nvidia-smi pmon -c 1 2>/dev/null || true
date
echo "============================"

echo "=== ARCHIVE TO AUTODL-FS ==="
ARCHIVE_OK=1
mkdir -p "$ARCHIVE_DIR" || ARCHIVE_OK=0
cp -r "$WORKSPACE/_gate0_artifacts/grid_cluster_a_runs" "$ARCHIVE_DIR/" || ARCHIVE_OK=0
cp -r "$WORKSPACE/docs" "$ARCHIVE_DIR/docs_snapshot" || ARCHIVE_OK=0
cp "$LOG_FILE" "$ARCHIVE_DIR/" || ARCHIVE_OK=0
echo "Archive dir: $ARCHIVE_DIR"
find "$ARCHIVE_DIR" -maxdepth 4 -type f | sort | tail -120 || true
echo "============================"

if [ "$ARCHIVE_OK" != "1" ] || [ ! -f "$ARCHIVE_DIR/$(basename "$LOG_FILE")" ]; then
  echo "Archive verification failed. NOT shutting down; preserve /root/autodl-tmp for manual retrieval." >&2
  exit 30
fi

if [ "$RUN_EXIT" != "0" ]; then
  echo "Gate 0A GRID batch failed with exit code $RUN_EXIT. Results were archived; NOT shutting down for inspection." >&2
  exit "$RUN_EXIT"
fi

echo "=========================================="
echo "Gate 0A GRID batch finished. Auto shutdown in 300 seconds."
echo "To keep the instance, interrupt this runner or disable AutoDL console auto-shutdown now."
echo "=========================================="
sleep 300
shutdown -h now
