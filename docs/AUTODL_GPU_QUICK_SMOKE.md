# AutoDL GPU Quick Smoke

Date: 2026-05-19 10:23 CST

## Run

- Remote: `ssh -p 10197 root@connect.westc.seetacloud.com`
- Workspace: `/root/autodl-tmp/Sec_phrase`
- Screen: `audit_sid_quick_20260519_101555`
- Mode: `QUEUE_MODE=quick`
- Launch policy: direct queue script, not `run_remote_audit_sid.sh`, so the instance was not auto-shutdown.
- Pulled local evidence:
  - `_gate0_artifacts/autodl_runs/gate0_summary_remote_quick_20260519_101555.csv`
  - `_gate0_artifacts/autodl_runs/logs/audit_sid_quick_20260519_101555.log`
  - `_gate0_artifacts/autodl_runs/g0_smoke_Musical_Instruments_resid_famae1_seed42/`
  - `_gate0_artifacts/autodl_runs/card_rqvae_feature_proxy_e5_seed42/`

## Preflight

`REQUIRE_CUDA=1` preflight passed on the RTX 5090 instance:

- `torch.cuda.is_available=True`
- device: `NVIDIA GeForce RTX 5090`
- `CARD_SOURCE_READY`
- `ASSETS_READY RUNNER_READY`

## New Quick Rows

| Run | Dataset | Method | Items | Missing metadata SID | Missing interaction SID | Unique SID | Duplicate SID rate | Full collision rate | Prefix counts | Level-0 category purity |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|---:|
| `g0_smoke_Musical_Instruments_resid_famae1_seed42` | `Musical_Instruments` | `resid_gaoq` | 23742 | 0 | 0 | 23742 | 0.000000 | 0.000000 | `32;1280;23742` | 0.548171 |
| `card_rqvae_feature_proxy_e5_seed42` | `Musical_Instruments` | `card_rqvae_feature_proxy` | 23742 | 0 | 0 | 4891 | 0.793994 | 0.919299 | `32;987;4891` | 0.426094 |

## Interpretation

This closes the GPU quick-smoke/provenance loop only. It does not change the paper's main evidence hierarchy:

- ReSID Musical balanced GAOQ remains valid smaller-dataset Cluster B evidence.
- CARD compact remains a controlled stressor/proxy/backlog row, not faithful CARD method evidence.
- Robust/sweep/quality remain out of scope unless a new explicit evidence gap is selected.

The remote summary still scans older unfinished Sports/Beauty checkpoint directories and prints missing-metric warnings for those historical partial runs. Those warnings are not direct failures of this quick screen.

## Final Remote State

After the screen exited:

- GPU: 0% utilization, 2 MiB / 32607 MiB
- Active experiment screens: none
- Old dead screens remain untouched.
