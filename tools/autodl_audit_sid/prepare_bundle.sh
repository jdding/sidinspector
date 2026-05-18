#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-$(pwd)}"
OUT_DIR="${OUT_DIR:-$ROOT_DIR/_gate0_artifacts/autodl_bundle}"
STAMP="$(date +%Y%m%d_%H%M%S)"
BUNDLE="$OUT_DIR/audit_sid_autodl_$STAMP.tar.gz"

mkdir -p "$OUT_DIR"

tar -czf "$BUNDLE" \
  --exclude='*/.git' \
  --exclude='*/__pycache__' \
  --exclude='._*' \
  README.md START_HERE_AUDIT_SID.md MANIFEST.md findings.md AGENTS.md \
  RESEARCH_BRIEF.md idea-stage refine-logs docs src tools \
  _gate0_repos/ReSID _gate0_repos/ReSID-dataset _gate0_repos/CARD \
  _gate0_artifacts/resid_musical_normalized \
  _gate0_artifacts/resid_real_runs/logs/famae/Musical_Instruments/gate0_famae_cpu_1epoch/seed_42/2026-05-18_17-52-53/best_model.pth

echo "$BUNDLE"
ls -lh "$BUNDLE"
tar -tzf "$BUNDLE" | head -40
