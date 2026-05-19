# GRID Musical Same-Dataset CPU Run

Timestamp: 2026-05-19 11:09:20 CST

## Why This Run Exists

The third external audit correctly identified the strongest remaining evidence gap: real Cluster A and real Cluster B evidence were on different datasets. This run adds a same-item-universe Musical row using the official GRID MiniBatchKMeans module on ReSID `Musical_Instruments` processed item features.

This is a controlled diagnostic row, not a faithful TIGER/GRID raw-text reproduction:

- same dataset and same item IDs as the ReSID Musical GAOQ row;
- official GRID residual k-means implementation is used;
- input embeddings are generated from ReSID processed feature text (`store_id`, category levels), because local and staged assets do not include Amazon-2023 raw `Musical_Instruments` title/review JSONL.

## Run

- Runner: `tools/autodl_audit_sid/run_grid_musical_cpu_smoke.sh`
- Input prep: `tools/autodl_audit_sid/prepare_resid_feature_grid_inputs.py`
- Exporter: `tools/autodl_audit_sid/run_grid_rqkmeans_direct_export.py`
- Device: local CPU
- Dataset: `Musical_Instruments`
- Items: 23742
- Interactions: ReSID normalized target-only interactions
- GRID codebook: width 64, depth 3
- Steps per layer: 40
- Output:
  - `_gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/`
  - `_gate0_artifacts/grid_same_dataset_runs/musical_same_dataset_grid_vs_resid_summary_20260519_110722.csv`

## Same-Dataset Summary

| System | Method | Items | Missing metadata SID | Missing interaction SID | Unique SID | Duplicate SID rate | Full collision rate | D3 L1 weighted recall | D3 L2 weighted recall | D3 L3 weighted recall | D4 head/mid/tail unique ratio | Prefix counts |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| GRID feature-text | `grid_official_rqkmeans_resid_feature_text` | 23742 | 0 | 0 | 3749 | 0.842094 | 0.976876 | 0.055176 | 0.004177 | 0.003997 | 0.353001 / 0.358952 / 0.369494 | `64;3440;3749` |
| ReSID GAOQ | `resid_gaoq` | 23742 | 0 | 0 | 23742 | 0.000000 | 0.000000 | 0.153544 | 0.017159 | 0.000000 | 1.000000 / 1.000000 / 1.000000 | `32;1280;23742` |

## Interpretation

This run materially improves the evidence matrix because it gives the toolkit a same-dataset A/B diagnostic row. It should be used to answer the audit question "why not compare on one dataset?" at the diagnostic level.

The safe claim is:

> On the same ReSID Musical item universe, AUDIT-SID can expose sharply different SID capacity/collision/alignment profiles between an official GRID residual-k-means export over processed feature text and ReSID GAOQ.

Do not write:

- GRID is worse than ReSID as a recommender;
- this is a faithful TIGER or raw-text GRID reproduction;
- D3v2 proves downstream Recall/NDCG;
- the feature-text controlled row replaces the existing All_Beauty GRID evidence.

## Remaining Caveat

The input representation is not the original Amazon raw title/review text used by the earlier All_Beauty GRID runs. If raw `Musical_Instruments` Amazon-2023 JSONL becomes available, rerun GRID Musical with raw text and keep this feature-text row as a controlled fallback.
