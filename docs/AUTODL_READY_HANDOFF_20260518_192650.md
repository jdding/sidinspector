# AutoDL Ready Handoff

**生成时间**：2026-05-18 19:18:15 CST
**状态**：TRANSFER_READY / RUNNER_READY / FULL_REPRO_BLOCKED_NO_GPU
**AutoDL skill**：aligned with `autodl-cloud-deploy` after correction

## Bundle

Local bundle:

```text
_gate0_artifacts/autodl_bundle/audit_sid_autodl_20260518_191815.tar.gz
```

Size: `30M`

SHA256:

```text
51a47e0505f9dc540522ca574b3e494fdec2ec6f5093a8a1a32d8b989596cd0b
```

The bundle includes:

- AUDIT-SID docs, tracker, manifest, and toolkit source;
- ReSID public repo and ReSID `Musical_Instruments` dataset shard;
- CARD public repo;
- normalized ReSID `item_metadata.parquet` and `interactions.parquet`;
- AutoDL runners and result summarizer.

Do not put AutoDL credentials into this repo. Use the local/private `autodl_config.md` or user-provided SSH details outside the public artifact if needed. No AutoDL connection file was found in this repo.

## AutoDL Target

Fixed target resource:

- CPU: 25 cores;
- RAM: 90 GB;
- GPU: 1 x RTX 5090.

## Remote Setup

After uploading the bundle to AutoDL:

```bash
mkdir -p /root/autodl-tmp/Sec_phrase
tar -xzf audit_sid_autodl_20260518_191815.tar.gz -C /root/autodl-tmp/Sec_phrase
cd /root/autodl-tmp/Sec_phrase
```

Resolve Python:

```bash
for p in python3 python /root/miniconda3/bin/python; do
  command -v "$p" >/dev/null 2>&1 && { command -v "$p"; break; }
done
```

Run preflight:

```bash
PYTHON_BIN=python3 bash tools/autodl_audit_sid/preflight_autodl.sh
```

Expected terminal state:

```text
ASSETS_READY RUNNER_READY
```

The remote workspace must stay under `/root/autodl-tmp/Sec_phrase`. Do not run active training from `/root/autodl-fs`; it is only for archiving completed outputs.

## Preferred Remote Runner

The AutoDL-specific runner is:

```text
tools/autodl_audit_sid/run_remote_audit_sid.sh
```

It records hardware specs and git commit, runs one queue, summarizes results, archives outputs to `/root/autodl-fs/audit_sid/<RUN_ID>/`, then performs script-owned automatic shutdown after a 300-second grace period. I must not execute shutdown manually.

Robust queue:

```bash
cd /root/autodl-tmp/Sec_phrase
QUEUE_MODE=robust DEVICE=cuda:0 NUM_WORKERS=8 PYTHON_BIN=python3 \
bash tools/autodl_audit_sid/run_remote_audit_sid.sh
```

Detached screen:

```bash
screen -S audit_sid_robust -dm bash -lc 'cd /root/autodl-tmp/Sec_phrase && QUEUE_MODE=robust DEVICE=cuda:0 NUM_WORKERS=8 PYTHON_BIN=python3 bash tools/autodl_audit_sid/run_remote_audit_sid.sh'
```

Monitor:

```bash
screen -r audit_sid_robust
tail -f /root/autodl-tmp/Sec_phrase/_gate0_artifacts/autodl_runs/logs/audit_sid_robust_*.log
```

## Direct Queue Commands

Use these only if intentionally bypassing the remote runner wrapper.

### Queue 1: Quick Smoke

Purpose: verify remote dependency/runtime path before spending the full GPU window.

```bash
QUEUE_MODE=quick DEVICE=cuda:0 NUM_WORKERS=8 PYTHON_BIN=python3 \
bash tools/autodl_audit_sid/run_autodl_gate0_queue.sh \
  2>&1 | tee _gate0_artifacts/autodl_runs/queue_quick.log
```

Runs:

- ReSID FAMAE 1 epoch -> GAOQ -> D1-D5a;
- CARD RQ-VAE feature-proxy 5 epochs -> code export -> D1-D5a.

### Queue 2: Robust

Purpose: preferred first serious batch on RTX 5090.

```bash
QUEUE_MODE=robust DEVICE=cuda:0 NUM_WORKERS=8 PYTHON_BIN=python3 \
bash tools/autodl_audit_sid/run_autodl_gate0_queue.sh \
  2>&1 | tee _gate0_artifacts/autodl_runs/queue_robust.log
```

Runs:

- ReSID `e1 seed42`;
- ReSID `e5 seed42`;
- ReSID `e5 seed43`;
- CARD RQ-VAE feature-proxy `e20 seed42`.

### Queue 2.5: Sweep

Purpose: accumulate enough Gate 0 evidence for seed/capacity sensitivity after robust succeeds.

```bash
QUEUE_MODE=sweep DEVICE=cuda:0 NUM_WORKERS=8 PYTHON_BIN=python3 \
bash tools/autodl_audit_sid/run_remote_audit_sid.sh
```

Runs:

- ReSID `e1 seed42`;
- ReSID `e5 seed42`;
- ReSID `e5 seed43`;
- ReSID capacity-small `B1=16,B2=32,G2=32`;
- ReSID capacity-large `B1=64,B2=40,G2=40`;
- CARD `e5 seed42`;
- CARD `e20 seed42`;
- CARD `e20 seed43`;
- CARD capacity-small `widths=16,32,16`;
- CARD capacity-large `widths=64,64,32`.

### Queue 3: Quality

Purpose: only if Queue 2 finishes cleanly and time remains.

```bash
QUEUE_MODE=quality DEVICE=cuda:0 NUM_WORKERS=8 PYTHON_BIN=python3 \
bash tools/autodl_audit_sid/run_autodl_gate0_queue.sh \
  2>&1 | tee _gate0_artifacts/autodl_runs/queue_quality.log
```

Runs:

- ReSID `e5 seed42`;
- ReSID `e5 seed43`;
- ReSID `e20 seed42`;
- CARD RQ-VAE feature-proxy `e20 seed42`;
- CARD RQ-VAE feature-proxy `e50 seed42`.

## Experiment Matrix

The explicit queue table is stored in:

```text
tools/autodl_audit_sid/gate0_experiment_matrix.tsv
```

## Result Summary

After a queue finishes:

```bash
PYTHONPATH=src python3 tools/autodl_audit_sid/summarize_gate0_runs.py \
  --run-root _gate0_artifacts/autodl_runs \
  --output _gate0_artifacts/autodl_runs/gate0_summary.csv
```

Important output paths:

```text
_gate0_artifacts/autodl_runs/*/normalized/sid_assignments.parquet
_gate0_artifacts/autodl_runs/*/metrics/coverage_report.csv
_gate0_artifacts/autodl_runs/*/metrics/d1_utilization.csv
_gate0_artifacts/autodl_runs/*/metrics/d2_collision.csv
_gate0_artifacts/autodl_runs/*/metrics/d3_alignment.csv
_gate0_artifacts/autodl_runs/*/metrics/d4_head_tail.csv
_gate0_artifacts/autodl_runs/*/metrics/d5a_deployment_cost.csv
_gate0_artifacts/autodl_runs/gate0_summary.csv
```

## Stop Conditions

Stop and report before running the next queue if:

- preflight does not show `torch.cuda.is_available=True`;
- ReSID fails before producing `item_code_mapping.parquet`;
- CARD fails before producing `card_rqvae_codes.npy`;
- coverage report has `metadata_without_sid > 0` or `interaction_without_sid > 0`;
- CARD feature-proxy has unusable coverage or pathological all-one-code collapse.

Gate 0 is not a full paper experiment. It is passed only when the exported mappings are joinable and D1-D5a metrics run cleanly for ReSID plus a Cluster A/CARD fallback mapping.
