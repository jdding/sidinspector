#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
PYTHON_BIN="${PYTHON_BIN:-}"

if [ -z "$PYTHON_BIN" ]; then
  for candidate in python3 python /root/miniconda3/bin/python; do
    if command -v "$candidate" >/dev/null 2>&1; then
      PYTHON_BIN="$(command -v "$candidate")"
      break
    fi
  done
fi

if [ -z "$PYTHON_BIN" ]; then
  echo "[AUDIT-SID preflight] no python interpreter found" >&2
  exit 2
fi

echo "[AUDIT-SID preflight] root=$ROOT_DIR"
echo "[AUDIT-SID preflight] python=$PYTHON_BIN"
date
uname -a

if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi --query-gpu=index,name,memory.used,memory.total,driver_version --format=csv,noheader
else
  echo "[AUDIT-SID preflight] nvidia-smi not found"
fi

if command -v screen >/dev/null 2>&1; then
  screen -ls || true
else
  echo "[AUDIT-SID preflight] screen not found"
fi

required_paths=(
  "$ROOT_DIR/src/audit_sid"
  "$ROOT_DIR/tools/autodl_audit_sid/run_resid_gate0_export.sh"
  "$ROOT_DIR/tools/autodl_audit_sid/run_resid_matrix.sh"
  "$ROOT_DIR/tools/autodl_audit_sid/run_card_rqvae_export.sh"
  "$ROOT_DIR/_gate0_repos/ReSID/main.py"
  "$ROOT_DIR/_gate0_repos/CARD/rqvae4/main.py"
  "$ROOT_DIR/_gate0_repos/ReSID-dataset/Musical_Instruments/leave_one_out/dataset/item_feature"
  "$ROOT_DIR/_gate0_artifacts/resid_musical_normalized/item_metadata.parquet"
  "$ROOT_DIR/_gate0_artifacts/resid_musical_normalized/interactions.parquet"
)

for path in "${required_paths[@]}"; do
  if [ -e "$path" ]; then
    echo "[AUDIT-SID preflight] OK $path"
  else
    echo "[AUDIT-SID preflight] MISSING $path" >&2
    exit 3
  fi
done

"$PYTHON_BIN" - <<'PY'
import importlib

mods = ["numpy", "pandas", "pyarrow", "torch"]
for mod in mods:
    try:
        m = importlib.import_module(mod)
        version = getattr(m, "__version__", "unknown")
        print(f"[AUDIT-SID preflight] import {mod}: OK {version}")
    except Exception as exc:
        print(f"[AUDIT-SID preflight] import {mod}: MISSING {type(exc).__name__}: {exc}")

try:
    import torch
    print(f"[AUDIT-SID preflight] torch.cuda.is_available={torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"[AUDIT-SID preflight] cuda_device={torch.cuda.get_device_name(0)}")
except Exception as exc:
    print(f"[AUDIT-SID preflight] torch cuda check failed: {exc}")
PY

if "$PYTHON_BIN" "$ROOT_DIR/tools/autodl_audit_sid/check_card_source.py" --card-dir "$ROOT_DIR/_gate0_repos/CARD"; then
  echo "[AUDIT-SID preflight] CARD_SOURCE_READY"
else
  echo "[AUDIT-SID preflight] CARD_SOURCE_INCOMPLETE; CARD queue entries will be skipped unless CARD_SOURCE_FAIL=error"
fi

ROOT_DIR="$ROOT_DIR" "$PYTHON_BIN" - <<'PY'
import os
from pathlib import Path
import pandas as pd

root = Path(os.environ["ROOT_DIR"])
item_metadata = root / "_gate0_artifacts/resid_musical_normalized/item_metadata.parquet"
interactions = root / "_gate0_artifacts/resid_musical_normalized/interactions.parquet"

meta = pd.read_parquet(item_metadata)
inter = pd.read_parquet(interactions)
print(f"[AUDIT-SID preflight] item_metadata rows={len(meta)} unique_items={meta['item_id'].nunique()}")
print(f"[AUDIT-SID preflight] interactions rows={len(inter)} unique_items={inter['item_id'].nunique()}")
splits = {str(k): int(v) for k, v in inter["split"].value_counts().sort_index().items()}
print(f"[AUDIT-SID preflight] interaction splits={splits}")
PY

if command -v sha256sum >/dev/null 2>&1; then
  sha256sum \
    "$ROOT_DIR/_gate0_artifacts/resid_musical_normalized/item_metadata.parquet" \
    "$ROOT_DIR/_gate0_artifacts/resid_musical_normalized/interactions.parquet"
elif command -v shasum >/dev/null 2>&1; then
  shasum -a 256 \
    "$ROOT_DIR/_gate0_artifacts/resid_musical_normalized/item_metadata.parquet" \
    "$ROOT_DIR/_gate0_artifacts/resid_musical_normalized/interactions.parquet"
fi

echo "[AUDIT-SID preflight] ASSETS_READY RUNNER_READY"
