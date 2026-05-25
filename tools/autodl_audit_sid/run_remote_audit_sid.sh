#!/usr/bin/env bash
set -uo pipefail

WORKSPACE="${WORKSPACE:-/root/autodl-tmp/Sec_phrase}"
QUEUE_MODE="${QUEUE_MODE:-robust}"
DEVICE="${DEVICE:-cuda:0}"
NUM_WORKERS="${NUM_WORKERS:-8}"
GAOQ_NUM_THREADS="${GAOQ_NUM_THREADS:-$NUM_WORKERS}"
GAOQ_KMEANS_N_JOBS="${GAOQ_KMEANS_N_JOBS:-$GAOQ_NUM_THREADS}"
GAOQ_USE_BALANCED_KMEANS="${GAOQ_USE_BALANCED_KMEANS:-true}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
RUN_ID="${RUN_ID:-audit_sid_${QUEUE_MODE}_$(date +%Y%m%d_%H%M%S)}"
LOG_DIR="${WORKSPACE}/_gate0_artifacts/autodl_runs/logs"
LOG_FILE="${LOG_DIR}/${RUN_ID}.log"
ARCHIVE_DIR="${ARCHIVE_DIR:-/root/autodl-fs/audit_sid/${RUN_ID}}"

if [ ! -d "$WORKSPACE" ]; then
  echo "Missing workspace: $WORKSPACE" >&2
  echo "Unpack the AutoDL bundle under /root/autodl-tmp/Sec_phrase before launching." >&2
  exit 2
fi

if [ ! -f "$WORKSPACE/tools/autodl_audit_sid/run_autodl_gate0_queue.sh" ]; then
  echo "Missing queue runner under workspace: $WORKSPACE/tools/autodl_audit_sid/run_autodl_gate0_queue.sh" >&2
  exit 2
fi

mkdir -p "$LOG_DIR"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "=== SIDInspector REMOTE RUNNER ==="
echo "Run ID: $RUN_ID"
echo "Workspace: $WORKSPACE"
echo "Queue mode: $QUEUE_MODE"
echo "Device: $DEVICE"
echo "Num workers: $NUM_WORKERS"
echo "GAOQ num threads: $GAOQ_NUM_THREADS"
echo "GAOQ KMeans n_jobs: $GAOQ_KMEANS_N_JOBS"
echo "GAOQ balanced KMeans: $GAOQ_USE_BALANCED_KMEANS"
echo "Python: $PYTHON_BIN"
date

cd "$WORKSPACE" || exit 2

COMMIT="$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")"
MESSAGE="$(git log -1 --format='%s' 2>/dev/null || echo "N/A")"

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
if [ -f AUTODL_BUNDLE_PROVENANCE.txt ]; then
  echo "Bundle Provenance:"
  cat AUTODL_BUNDLE_PROVENANCE.txt
elif [ -f docs/AUTODL_BUNDLE_PROVENANCE.md ]; then
  echo "Bundle Provenance:"
  cat docs/AUTODL_BUNDLE_PROVENANCE.md
fi
echo "==================="

echo "=== INITIAL RESOURCE CHECK ==="
nvidia-smi --query-gpu=index,utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null || true
nvidia-smi pmon -c 1 2>/dev/null || true
free -h 2>/dev/null || true
ps aux | grep python | grep -v grep | head -20 || true
echo "=============================="

set +e
QUEUE_MODE="$QUEUE_MODE" DEVICE="$DEVICE" NUM_WORKERS="$NUM_WORKERS" GAOQ_NUM_THREADS="$GAOQ_NUM_THREADS" GAOQ_KMEANS_N_JOBS="$GAOQ_KMEANS_N_JOBS" GAOQ_USE_BALANCED_KMEANS="$GAOQ_USE_BALANCED_KMEANS" PYTHON_BIN="$PYTHON_BIN" \
  bash tools/autodl_audit_sid/run_autodl_gate0_queue.sh
EXIT_CODE=$?

echo "=== FINAL SUMMARY ==="
PYTHONPATH=src "$PYTHON_BIN" tools/autodl_audit_sid/summarize_gate0_runs.py \
  --run-root _gate0_artifacts/autodl_runs \
  --output _gate0_artifacts/autodl_runs/gate0_summary.csv \
  --strict
SUMMARY_EXIT_CODE=$?
set -e
echo "Queue exit code: $EXIT_CODE"
echo "Summary exit code: $SUMMARY_EXIT_CODE"
date

echo "=== ARCHIVE TO AUTODL-FS ==="
ARCHIVE_OK=1
mkdir -p "$ARCHIVE_DIR" || ARCHIVE_OK=0
cp -r "$WORKSPACE/_gate0_artifacts/autodl_runs" "$ARCHIVE_DIR/" || ARCHIVE_OK=0
cp -r "$WORKSPACE/docs" "$ARCHIVE_DIR/docs_snapshot" || ARCHIVE_OK=0
cp "$LOG_FILE" "$ARCHIVE_DIR/" || ARCHIVE_OK=0
echo "Archive dir: $ARCHIVE_DIR"
find "$ARCHIVE_DIR" -maxdepth 3 -type f | sort | tail -80 || true
echo "============================"

if [ "$ARCHIVE_OK" != "1" ] || [ ! -f "$ARCHIVE_DIR/$(basename "$LOG_FILE")" ]; then
  echo "Archive verification failed. NOT shutting down; preserve /root/autodl-tmp for manual retrieval." >&2
  exit 30
fi

if [ "$EXIT_CODE" != "0" ] || [ "$SUMMARY_EXIT_CODE" != "0" ]; then
  echo "Queue or summary failed. Results were archived, but NOT shutting down for inspection." >&2
  if [ "$EXIT_CODE" != "0" ]; then
    exit "$EXIT_CODE"
  fi
  exit "$SUMMARY_EXIT_CODE"
fi

echo "=========================================="
echo "SIDInspector runner finished. Auto shutdown in 300 seconds."
echo "To keep the instance, disable AutoDL console auto-shutdown or interrupt this runner now."
echo "=========================================="
sleep 300
shutdown -h now

exit "$EXIT_CODE"
