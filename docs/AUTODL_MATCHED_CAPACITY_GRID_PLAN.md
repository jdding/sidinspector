# AutoDL Matched-Capacity GRID Plan

Time: 2026-05-20 16:03 CST

## Purpose

Run exactly one GPU-worthy follow-up for the R3 simulated CIKM Resource review:
the matched-capacity GRID/RQ-KMeans ablation requested under W2.

This is not a broad sweep. The goal is to answer one reviewer attack surface:
does the GRID same-item row still show substantial aliasing when the RQ-KMeans
export is given a ReSID-like prefix-capacity budget?

## Why AutoDL Is Justified

Local CPU attempt:

- Config: Musical feature-text embeddings, per-level widths `32,1280,1280`,
  seed 42.
- Status: stopped under `BLOCKED_LOCAL_CPU_STOPLOSS`.
- Evidence: no output artifacts were produced before stop-loss.

The exporter uses the public GRID `MiniBatchKMeans` implementation and supports
CUDA through the `--device cuda` path. The expensive portion is centroid
initialization/update and assignment over 23,742 items with 1,280-code layers,
so the RTX 5090 is plausibly useful. The run remains bounded to one dataset,
one seed, and one capacity setting.

## Launch Target

- Host: `ssh -p 10197 root@connect.westc.seetacloud.com`
- Expected instance: 30 vCPU, 90GB RAM, 1x RTX 5090.
- Remote work root: `/root/autodl-tmp/audit-sid-matched-grid-20260520`
- Do not kill or reuse unrelated sessions.
- Do not manually shut down the host from Codex; shutdown remains human/platform
  managed unless a pre-approved runner owns it.

## Command Class

The full run should execute the existing exporter with:

```bash
PYTHONPATH=src python3 tools/autodl_audit_sid/run_grid_rqkmeans_direct_export.py \
  --grid-dir _gate0_repos/GRID \
  --embeddings _gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/input/item_embeddings.pt \
  --item-ids _gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/input/item_ids.npy \
  --item-metadata _gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/input/item_metadata.parquet \
  --interactions _gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/input/interactions.parquet \
  --output-dir _gate0_artifacts/grid_same_dataset_runs/matched_capacity_grid_32_1280_1280_seed42_20260520/grid_export \
  --dataset-name Musical_Instruments \
  --method grid_official_rqkmeans_resid_feature_text_prefix_matched \
  --per-level-widths 32,1280,1280 \
  --batch-size 4096 \
  --steps-per-layer 40 \
  --init-buffer-size 4096 \
  --device cuda \
  --seed 42
```

After export, run the existing metric/table path and retrieve:

- `sid_assignments.parquet`
- `metrics_summary.json`
- D1-D5 CSVs
- run log
- environment/Git hash note

## Stop-Loss

Within 2--5 minutes of launch:

- check `nvidia-smi`;
- check the private screen log;
- stop only this private run if GPU memory is allocated but SM utilization stays
  near zero and CPU/Python is clearly the bottleneck.

If the run completes:

- compare D2 full aliasing and D4 tail capacity against the existing GRID and
  ReSID rows;
- only admit into the paper if it directly clarifies the capacity-mismatch
  caveat;
- otherwise document it as an audit note, not main evidence.

## Current Status

`COMPLETED_AUTODL_GPU` on port 21551.

- Private screen: `audit_sid_matched_grid_1600`.
- Exit: `RUN_EXIT=0`.
- Result report: `docs/MATCHED_CAPACITY_GRID_AUTODL_RESULT.md`.
- Local result root:
  `_gate0_artifacts/grid_same_dataset_runs/matched_capacity_grid_32_1280_1280_seed42_20260520/`.
- Key metrics: 9,874 unique full SIDs, D2 full-code aliasing 0.778452,
  D3 L1 weighted co-occurrence recall 0.079595, D4 tail unique-SID ratio
  0.639064, D5 prefixes `32;9300;9874`.
- Stop-loss: passed, with 97--99% SM utilization and about 20.8GB GPU memory
  allocated during the check.
- Result root:
  `_gate0_artifacts/grid_same_dataset_runs/matched_capacity_grid_32_1280_1280_seed42_20260520/grid_export/`
- Main result: 9,874 unique full SIDs, D2 aliasing 0.778452, D3 L1 0.079539,
  D4 tail unique-SID ratio 0.639064, D5 prefixes `32/9300/9874`.
