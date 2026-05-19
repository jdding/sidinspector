# Third External Audit Response

Timestamp: 2026-05-19 11:09:20 CST

## Accepted Finding

The audit's main critique is correct: before this response, real Cluster A evidence and real Cluster B evidence did not share a dataset. That made any A/B mechanism comparison vulnerable to dataset confounding.

## Immediate Action Taken

Because the AutoDL instance is currently no-GPU, the response was run locally on CPU rather than waiting for GPU.

Added a same-item-universe Musical diagnostic row:

- Input: ReSID `Musical_Instruments` normalized item metadata and interactions.
- Embedding source: local MiniLM over processed feature text built from `store_id` and category levels.
- Method: official GRID `MiniBatchKMeans` residual k-means exporter.
- Runner: `tools/autodl_audit_sid/run_grid_musical_cpu_smoke.sh`
- Output: `_gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/`

## Result

| System | Dataset | Unique SID | Duplicate SID rate | Full collision rate | D3 L1 weighted recall | D4 head/mid/tail unique ratio |
|---|---|---:|---:|---:|---:|---|
| GRID feature-text | Musical_Instruments | 3749 | 0.842094 | 0.976876 | 0.055176 | 0.353001 / 0.358952 / 0.369494 |
| ReSID GAOQ | Musical_Instruments | 23742 | 0.000000 | 0.000000 | 0.153544 | 1.000000 / 1.000000 / 1.000000 |

## What This Fixes

- Adds an A/B diagnostic row on the same item universe.
- Makes D1/D2/D3v2/D4 differences interpretable as a controlled diagnostic contrast, not purely cross-dataset comparison.
- Makes D4 visible in the evidence snapshot.

## What It Does Not Fix

- It is not a faithful raw-text TIGER/GRID reproduction.
- It does not validate D3v2 against downstream Recall/NDCG.
- It does not add 50k multi-seed GRID evidence.
- It does not remove the need for citation verification.

## Paper Wording Update

The paper plan now treats this as a same-item-universe diagnostic row and keeps the caveat explicit:

> official GRID residual-k-means export over processed feature text, compared with ReSID/GAOQ on the same ReSID Musical item universe.

This should replace any broad "GRID vs ReSID" language.
