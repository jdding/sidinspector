# AutoDL GPU Experiment Plan: AUDIT-SID Gate 0

**生成时间**：2026-05-18 18:00:00 CST
**状态**：GPU staging plan prepared; local CPU FAMAE smoke has produced a checkpoint

## Current Local Evidence

- ReSID `Musical_Instruments` data schema passes.
- Adapter and D1-D5a metrics pass sanity smoke after code review fixes.
- Local CPU FAMAE 1 epoch completed and produced `best_model.pth`.
- Local GAOQ finished and produced the first real ReSID/GAOQ mapping; AutoDL should now run robustness/quality variants, not dependency debugging.

## Recommended AutoDL Instance

Use a single-GPU instance first:

| Requirement | Recommendation |
|---|---|
| GPU | Fixed user instance: 1 x RTX 5090 |
| VRAM | RTX 5090 capacity is sufficient for the planned ReSID FAMAE matrix |
| CPU/RAM | Fixed user instance: 25 CPU cores, 90 GB RAM |
| Disk | 50 GB free |
| Image | PyTorch image with CUDA, Python 3.9-3.11 preferred |

Avoid spending on multi-GPU for Gate 0. The immediate bottleneck is export feasibility, not final model quality.

## Prepared Script

Use:

```bash
tools/autodl_audit_sid/run_resid_gate0_export.sh
```

It runs:

1. install minimal ReSID runtime deps, using `k-means-constrained==0.7.3` because the repo pin `0.7.6` is not available from PyPI;
2. patch the local ReSID clone so `num_workers` is config-controlled;
3. train FAMAE for a bounded epoch count;
4. run GAOQ and export `item_feature/item_code_mapping.parquet`;
5. normalize the mapping with `src/audit_sid/adapters/resid.py`;
6. run D1-D5a metrics and write CSVs.

## Experiment Matrix

| ID | Purpose | Command |
|---|---|---|
| G0-E1 | Fast real mapping gate | `FAMAE_EPOCHS=1 DEVICE=cuda:0 NUM_WORKERS=4 bash tools/autodl_audit_sid/run_resid_gate0_export.sh` |
| G0-E2 | More stable mapping for paper smoke | `FAMAE_EPOCHS=5 DEVICE=cuda:0 NUM_WORKERS=4 bash tools/autodl_audit_sid/run_resid_gate0_export.sh` |
| G0-E3 | Seed robustness if E1/E2 pass | `FAMAE_EPOCHS=5 SEED=43 DEVICE=cuda:0 NUM_WORKERS=4 bash tools/autodl_audit_sid/run_resid_gate0_export.sh` |
| G0-E4 | Higher-quality case-study candidate | `FAMAE_EPOCHS=20 DEVICE=cuda:0 NUM_WORKERS=4 bash tools/autodl_audit_sid/run_resid_gate0_export.sh` |

Stop after G0-E1 if it fails before GAOQ mapping export. Run G0-E2 only after `normalized/sid_assignments.parquet` and `metrics/coverage_report.csv` exist.

## Bundle

Create a transfer bundle:

```bash
bash tools/autodl_audit_sid/prepare_bundle.sh
```

On AutoDL:

```bash
mkdir -p Sec_phrase
tar -xzf audit_sid_autodl_*.tar.gz -C Sec_phrase
cd Sec_phrase
python3 -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
FAMAE_EPOCHS=1 DEVICE=cuda:0 NUM_WORKERS=4 bash tools/autodl_audit_sid/run_resid_gate0_export.sh
```

For a sequential matrix:

```bash
MATRIX_MODE=robust DEVICE=cuda:0 NUM_WORKERS=8 bash tools/autodl_audit_sid/run_resid_matrix.sh
```

## Expected Success Artifact

The run is successful only if these files exist:

- `_gate0_artifacts/autodl_runs/<exp>/normalized/sid_assignments.parquet`
- `_gate0_artifacts/autodl_runs/<exp>/metrics/coverage_report.csv`
- `_gate0_artifacts/autodl_runs/<exp>/metrics/d1_utilization.csv`
- `_gate0_artifacts/autodl_runs/<exp>/metrics/d2_collision.csv`
- `_gate0_artifacts/autodl_runs/<exp>/metrics/d3_alignment.csv`
- `_gate0_artifacts/autodl_runs/<exp>/metrics/d4_head_tail.csv`
- `_gate0_artifacts/autodl_runs/<exp>/metrics/d5a_deployment_cost.csv`

## Decision Rule

If G0-E1 produces a real ReSID SID mapping, Gate 0 has at least one real Cluster B mapping. The next required step is Cluster A, likely GRID only if an embedding/checkpoint path can be made cheap; otherwise CIKM 2026 should be treated as high risk and CARD fallback should be evaluated.
