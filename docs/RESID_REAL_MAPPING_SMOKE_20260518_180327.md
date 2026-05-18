# ReSID Real Mapping Smoke

**生成时间**：2026-05-18 18:03:27 CST
**状态**：first real ReSID/GAOQ item-to-SID mapping exported and scored locally

## What Ran

Local CPU bounded export:

1. FAMAE 1 epoch on ReSID `Musical_Instruments`;
2. GAOQ with `b1=32`, `b2=40`, `g2=40`, `use_balancedkmeans=true`;
3. ReSID adapter normalization;
4. D1-D5a metric runner.

This run used the local ignored clone under `_gate0_repos/ReSID` and wrote outputs only under `_gate0_artifacts/`.

## Local Patches

The local ReSID clone was patched for execution only:

- `utils.py` now reads `num_workers` from config;
- `pin_memory` is disabled when CUDA is unavailable.

This avoids macOS/PyTorch shared-memory failure from multi-worker DataLoader during local CPU smoke. The patch is not part of the public toolkit source.

## Timing

FAMAE 1 epoch on local CPU:

- train: 156 batches;
- validation: 28 batches;
- test: 28 batches;
- total training duration reported by ReSID: 2 minutes 54.38 seconds.

GAOQ CPU export completed and wrote the item mapping.

## Artifacts

| Artifact | Path | Notes |
|---|---|---|
| FAMAE checkpoint | `_gate0_artifacts/resid_real_runs/logs/famae/Musical_Instruments/gate0_famae_cpu_1epoch/seed_42/2026-05-18_17-52-53/best_model.pth` | 15 MB |
| GAOQ raw mapping | `_gate0_artifacts/resid_real_runs/logs/gaoq/Musical_Instruments/gate0_gaoq_cpu_from_1epoch/seed_42/2026-05-18_17-56-42/item_feature/item_code_mapping.parquet` | 23,742 rows |
| Normalized SID table | `_gate0_artifacts/resid_real_runs/normalized_resid_gaoq_1epoch/sid_assignments.parquet` | 23,742 rows |
| Metrics | `_gate0_artifacts/resid_real_runs/normalized_resid_gaoq_1epoch/metrics/` | coverage + D1-D5a CSVs |

## Metric Summary

Coverage:

| Dataset | Method | SID items | Metadata items | Interaction items | Metadata without SID | Interaction without SID |
|---|---|---:|---:|---:|---:|---:|
| `Musical_Instruments` | `resid_gaoq` | 23,742 | 23,742 | 23,736 | 0 | 0 |

D1 utilization:

| Level | Unique codes | Entropy | Gini |
|---|---:|---:|---:|
| `sid_level_0` | 32 | 5.0000 | 0.0001 |
| `sid_level_1` | 40 | 5.3219 | 0.0027 |
| `sid_level_2` | 19 | 4.2479 | 0.0042 |

Other diagnostics:

- full-SID duplicate rate: `0.0`;
- level-0 category purity proxy: `0.5669`;
- head/mid/tail SID unique ratio: `1.0 / 1.0 / 1.0`;
- SID length: `3`;
- prefix counts: `32;1280;23742`.

## Gate Interpretation

This satisfies the first real Cluster B mapping requirement for AUDIT-SID. It does not complete Gate 0 because the sprint still needs either:

- a Cluster A canonical SID mapping, preferably GRID/RQ-VAE or RKMeans/TIGER-style; or
- an explicit decision that CARD or another public artifact is the fastest representative fallback.

The local result is strong enough to move AutoDL from "debug dependency/path" to "run a small matrix for robustness and quality."
