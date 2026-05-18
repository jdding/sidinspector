# AutoDL GAOQ Stop-Loss Report

Timestamp: 2026-05-18 22:52:22 CST

## Remote State Checked

- Host: `ssh -p 10197 root@connect.westc.seetacloud.com`
- Workspace: `/root/autodl-tmp/Sec_phrase`
- Run ID: `audit_sid_robust_20260518_2237`
- Private screen after check: no active AUDIT-SID screen
- GPU after check: RTX 5090, 0% utilization, no running GPU process

## Outcome

The queue did not finish successfully.

The Sports ReSID FAMAE 1-epoch stage completed and saved:

`_gate0_artifacts/autodl_runs/g0_canonical_Sports_and_Outdoors_resid_famae1_seed42/logs/famae/Sports_and_Outdoors/g0_canonical_Sports_and_Outdoors_resid_famae1_seed42_famae/seed_42/2026-05-18_22-32-35/best_model.pth`

The GAOQ stage did not produce:

- `item_code_mapping.parquet`
- normalized `sid_assignments.parquet`
- D1-D5a metrics
- a valid `gate0_summary.csv`

`gate0_summary.csv` on the remote workspace is 1 byte, and `/root/autodl-fs/audit_sid/` only contains the earlier failed archive `audit_sid_robust_20260518_2223`.

## Stop-Loss Reason

GAOQ is a CPU-only export stage in the current ReSID implementation:

- `run_resid_gate0_export.sh` launches GAOQ with `GAOQ_DEVICE=cpu` by default.
- `model/gaoq.py` materializes embeddings as NumPy via `.cpu().numpy()`.
- `use_balancedkmeans=true` routes clustering through `KMeansConstrained`.
- Remote API inspection shows `KMeansConstrained(..., n_jobs=1)` by default.

During the stopped run, GAOQ occupied roughly one CPU core while the RTX 5090 was idle. This triggered the AutoDL low-utilization stop-loss rule.

## Local Fix Prepared

Tracked runner changes now keep balanced GAOQ as the default but expose explicit CPU parallelism:

- `tools/autodl_audit_sid/patch_resid_runtime.py` patches the ignored ReSID checkout at runtime.
- `GAOQ_KMEANS_N_JOBS` is passed into `KMeansConstrained`.
- `GAOQ_NUM_THREADS` sets `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, and `NUMEXPR_NUM_THREADS`.
- `GAOQ_USE_BALANCED_KMEANS` defaults to `true`; setting it to `false` is only an explicit fast/proxy mode, not the formal ReSID result.

Recommended relaunch for the fixed instance:

```bash
screen -dmS audit_sid_robust_20260518_gjobs25 bash -lc 'export CUDA_VISIBLE_DEVICES=0; RUN_ID=audit_sid_robust_20260518_gjobs25 QUEUE_MODE=robust DEVICE=cuda:0 NUM_WORKERS=8 GAOQ_NUM_THREADS=25 GAOQ_KMEANS_N_JOBS=25 GAOQ_USE_BALANCED_KMEANS=true PYTHON_BIN=/root/autodl-tmp/Sec_phrase/.venv_audit_sid/bin/python SKIP_QUEUE_PIP_INSTALL=1 bash tools/autodl_audit_sid/run_remote_audit_sid.sh'
```

Monitor within 2-5 minutes after GAOQ starts. If balanced GAOQ still stays effectively single-core, stop and switch to a smaller canonical-only run or record `resid_gaoq_unbalanced_proxy` separately rather than mixing it with formal ReSID evidence.
