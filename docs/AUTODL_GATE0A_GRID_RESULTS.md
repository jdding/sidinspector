# AutoDL Gate 0A GRID Results

Timestamp: 2026-05-19 01:33:00 CST

## Status

`GRID_GATE0A_BATCH_PASSED`

AutoDL host:

```bash
ssh -p 10197 root@connect.westc.seetacloud.com
```

Remote run:

- screen: `audit_sid_gate0a_grid_20260519_0133`
- local commit recorded in runner: `3905b34`
- runner: `tools/autodl_audit_sid/run_remote_gate0a_grid_batch.sh`
- remote log:
  `/root/autodl-tmp/Sec_phrase/_gate0_artifacts/grid_cluster_a_runs/logs/audit_sid_gate0a_grid_20260519_0133.log`
- remote archive:
  `/root/autodl-fs/audit_sid/audit_sid_gate0a_grid_20260519_0133/`
- local pulled evidence:
  `_gate0_artifacts/grid_cluster_a_runs/`

The completed runner entered its 300-second automatic shutdown window, then the
private screen was interrupted to keep the instance available for follow-up
analysis. No other process was stopped.

## Hardware And Runtime

The runner recorded:

- GPU: NVIDIA GeForce RTX 5090, 32607 MiB
- CPU cores reported by container: 208
- RAM total reported by container: 754 GiB

The user-facing AutoDL instance contract remains the user's fixed allocation:
30 CPU cores, 90 GB RAM, 1 x RTX 5090. The higher container-visible CPU/RAM
numbers are recorded as observed environment details, not as the purchased
instance spec.

Initial post-launch monitoring showed active GPU work:

- embedding stage pmon: Python process with about 48-55% SM utilization;
- no sustained idle-GPU/CPU-bound failure after dependency repair.

## Batch Outcome

| Run | Items | Seed | Exit | Start | Finish |
|---|---:|---:|---:|---|---|
| `grid_official_rqkmeans_All_Beauty_text_20000_cuda_seed42` | 20,000 | 42 | 0 | 2026-05-19T01:29:41+08:00 | 2026-05-19T01:30:18+08:00 |
| `grid_official_rqkmeans_All_Beauty_text_20000_cuda_seed43` | 20,000 | 43 | 0 | 2026-05-19T01:30:18+08:00 | 2026-05-19T01:30:56+08:00 |
| `grid_official_rqkmeans_All_Beauty_text_20000_cuda_seed44` | 20,000 | 44 | 0 | 2026-05-19T01:30:56+08:00 | 2026-05-19T01:31:32+08:00 |
| `grid_official_rqkmeans_All_Beauty_text_50000_cuda_seed42` | 50,000 | 42 | 0 | 2026-05-19T01:31:32+08:00 | 2026-05-19T01:32:24+08:00 |

All runs produced:

- `grid_export/grid_export_manifest.json`
- `grid_export/normalized/sid_assignments.parquet`
- D1-D5a metric CSVs

## Metric Snapshot

| Run | Coverage | Unique SID | Duplicate SID rate | Prefix counts | Full collision rate | L0 category purity |
|---|---:|---:|---:|---|---:|---:|
| 20k seed42 | 20,000/20,000 metadata; 0 interaction gaps | 16,718 | 0.1641 | `128;7126;16718` | 0.2556 | 0.9957 |
| 20k seed43 | 20,000/20,000 metadata; 0 interaction gaps | 16,951 | 0.1524 | `128;7104;16951` | 0.2379 | 0.9962 |
| 20k seed44 | 20,000/20,000 metadata; 0 interaction gaps | 16,503 | 0.1748 | `128;6891;16503` | 0.2661 | 0.9962 |
| 50k seed42 | 50,000/50,000 metadata; 0 interaction gaps | 37,146 | 0.2571 | `128;10021;37146` | 0.3731 | 0.9964 |

The 50k run also reports full per-level codebook usage:

- level 0: 128/128 codes, entropy 6.6920, Gini 0.3465
- level 1: 128/128 codes, entropy 6.9136, Gini 0.1910
- level 2: 128/128 codes, entropy 6.9419, Gini 0.1534

## Interpretation

This closes a major Gate 0A risk for Cluster A scale and seed stability:

- the real GRID official-module RQ-KMeans path scales from local 5k to remote
  20k/50k;
- all four runs are joinable and complete D1-D5a;
- 20k seed variance is visible but not pathological:
  duplicate SID rate ranges from 0.1524 to 0.1748.

It does **not** close all of Gate 0A:

- A and B are still not aligned on the same canonical vertical;
- D3 is still category-purity proxy, not semantic-collaborative alignment;
- GRID remains a direct official-module wrapper, not the full Hydra/TFRecord
  GRID pipeline;
- ReSID canonical vertical evidence still needs a clean decision after the
  previous GAOQ CPU stop-loss.

## Notes

The logs contain two non-fatal warnings:

- `libgomp: Invalid value for environment variable OMP_NUM_THREADS`
- `fatal: detected dubious ownership in repository ... _gate0_repos/GRID`

Neither blocked the exports. The manifest records GRID commit
`2fe3475b2d369580234093f35d52b1a2f54d0472` through the fallback path.
