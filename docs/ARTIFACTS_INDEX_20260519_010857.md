# AUDIT-SID Local Artifact Index

Timestamp: 2026-05-19 01:08:57 CST

## Policy

`_gate0_artifacts/` is local and git-ignored. Treat it as a working cache plus
evidence store. Do not delete or overwrite a run directory while Gate 0A is
active unless a current runbook says it is disposable.

Tracked documentation should reference artifacts through reports in `docs/` and
`refine-logs/`, not by assuming another machine has this exact local cache.

## Size Snapshot

| Path | Size | Current role |
|---|---:|---|
| `_gate0_artifacts/autodl_bundle` | 856M | old AutoDL bundles; large, locally useful, not primary evidence |
| `_gate0_artifacts/python_deps` | 256M | local dependency cache for constrained ReSID/Gate 0 runs |
| `_gate0_artifacts/resid_real_runs` | 40M | real ReSID balanced GAOQ evidence and combined metrics |
| `_gate0_artifacts/grid_cluster_a_runs` | 11M | real GRID/RQ-KMeans Cluster A local evidence |
| `_gate0_artifacts/resid_musical_normalized` | 6.1M | normalized ReSID Musical quick-smoke data |
| `_gate0_artifacts/sanity_musical` | 988K | sanity SID baseline outputs |
| `_gate0_artifacts/autodl_runs` | 412K | pulled remote proxy/debug summaries |
| `_gate0_artifacts/card_cpu_smoke` | 284K | CARD source-repair smoke artifacts |
| `_gate0_artifacts/local_rqkmeans_feature_proxy` | 240K | local proxy stressor, not named-method evidence |
| `_gate0_artifacts/grid_all_beauty_text_smoke32` | 144K | earliest GRID text smoke |
| `_gate0_artifacts/card_synthetic` | 16K | synthetic CARD adapter smoke |
| `_gate0_artifacts/grid_synthetic` | 12K | synthetic GRID adapter smoke |
| `_gate0_artifacts/resid_dataset_download_manifest.json` | 12K | local dataset download manifest |

## Keep During Gate 0A

These are active or near-active evidence:

- `_gate0_artifacts/grid_cluster_a_runs/`
- `_gate0_artifacts/resid_real_runs/`
- `_gate0_artifacts/resid_musical_normalized/`
- `_gate0_artifacts/sanity_musical/`
- `_gate0_artifacts/resid_dataset_download_manifest.json`

## Keep For Debug Provenance

These are useful for explaining why proxy rows were rejected or why fallback
paths are not primary evidence:

- `_gate0_artifacts/autodl_runs/`
- `_gate0_artifacts/card_cpu_smoke/`
- `_gate0_artifacts/card_synthetic/`
- `_gate0_artifacts/grid_synthetic/`
- `_gate0_artifacts/local_rqkmeans_feature_proxy/`
- `_gate0_artifacts/grid_all_beauty_text_smoke32/`

## Cleanup Candidates After Submission Decision

These are large and can be regenerated or replaced if storage pressure matters:

- `_gate0_artifacts/autodl_bundle/`
- `_gate0_artifacts/python_deps/`

Do not clean them mid-run unless storage becomes a blocker, because they may
still save setup time while AutoDL access is unstable.

## Evidence Boundary

Primary method evidence currently comes from:

- GRID / RQ-KMeans: `_gate0_artifacts/grid_cluster_a_runs/grid_official_rqkmeans_All_Beauty_text_smoke5000_local/`
- ReSID / GAOQ: `_gate0_artifacts/resid_real_runs/normalized_resid_gaoq_1epoch/`

Proxy/debug rows should not be promoted into paper method tables:

- `_gate0_artifacts/autodl_runs/card_rqvae_feature_proxy_Sports_and_Outdoors_compact_e5_seed42_gate0/`
- `_gate0_artifacts/autodl_runs/g0_canonical_Sports_and_Outdoors_resid_famae1_seed42_unbalanced_proxy/`
- `_gate0_artifacts/local_rqkmeans_feature_proxy/`
