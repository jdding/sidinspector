# GRID Musical Three-Seed Local Run

Timestamp: 2026-05-19 15:58:57 CST

Purpose: strengthen the same-item-universe A/B panel without using GPU. This
reruns the GRID/RQ-KMeans feature-text export on the same ReSID processed
`Musical_Instruments` item universe with seeds 43 and 44, reusing the already
prepared local embeddings from the seed-42 run.

## Inputs

- Dataset: ReSID processed Amazon-2023 `Musical_Instruments`.
- Item universe: 23,742 items.
- Embeddings: existing local feature-text embeddings from
  `_gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/input/`.
- Method label:
  `grid_official_rqkmeans_resid_feature_text`.
- GRID config: codebook width 64, 3 hierarchies, 40 steps/layer, CPU device.

## Commands

Seed 43 and 44 were run with:

```bash
PYTHONPATH=/Users/timber/Documents/Sec_phrase/src \
python3 tools/autodl_audit_sid/run_grid_rqkmeans_direct_export.py \
  --grid-dir _gate0_repos/GRID \
  --embeddings _gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/input/item_embeddings.pt \
  --item-ids _gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/input/item_ids.npy \
  --item-metadata _gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/input/item_metadata.parquet \
  --interactions _gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/input/interactions.parquet \
  --output-dir <seed-output>/grid_export \
  --dataset-name Musical_Instruments \
  --method grid_official_rqkmeans_resid_feature_text \
  --codebook-width 64 \
  --num-hierarchies 3 \
  --batch-size 4096 \
  --steps-per-layer 40 \
  --init-buffer-size 4096 \
  --device cpu \
  --seed <43-or-44>
```

## Artifacts

| Seed | Output |
|---|---|
| 42 | `_gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/grid_export/` |
| 43 | `_gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_seed43_20260519_1600/grid_export/` |
| 44 | `_gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_seed44_20260519_1600/grid_export/` |

Summary CSVs:

- `_gate0_artifacts/grid_same_dataset_runs/musical_grid_feature_text_3seed_summary_20260519_1600.csv`
- `_gate0_artifacts/grid_same_dataset_runs/musical_grid_feature_text_3seed_stats_20260519_1600.csv`

## Results

| Seed | Unique SID | Duplicate SID Rate | Full Collision Rate | D3 L1 Weighted Recall | D3 L3 Weighted Recall | Head Unique Ratio | Tail Unique Ratio | Prefix Counts |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 42 | 3,749 | 0.8421 | 0.9769 | 0.0552 | 0.0040 | 0.3530 | 0.3695 | 64;3440;3749 |
| 43 | 3,972 | 0.8327 | 0.9751 | 0.0479 | 0.0034 | 0.3792 | 0.3852 | 64;3712;3972 |
| 44 | 3,849 | 0.8379 | 0.9756 | 0.0526 | 0.0041 | 0.3587 | 0.3773 | 64;3655;3849 |

Aggregate over seeds 42/43/44:

| Metric | Mean | Std | Min | Max |
|---|---:|---:|---:|---:|
| Unique SID | 3856.67 | 111.70 | 3749 | 3972 |
| Duplicate SID rate | 0.8376 | 0.0047 | 0.8327 | 0.8421 |
| Full collision rate | 0.9759 | 0.0009 | 0.9751 | 0.9769 |
| D3 L1 weighted recall | 0.0519 | 0.0037 | 0.0479 | 0.0552 |
| D3 L3 weighted recall | 0.0038 | 0.0004 | 0.0034 | 0.0041 |
| Head SID unique ratio | 0.3636 | 0.0138 | 0.3530 | 0.3792 |
| Tail SID unique ratio | 0.3773 | 0.0079 | 0.3695 | 0.3852 |

## Interpretation

The GRID Musical feature-text row is stable enough to use as artifact evidence:
complete joins persist across all three seeds, and the collision profile is
consistently high rather than a seed accident. This strengthens the
same-dataset A/B story against ReSID, but the caveat remains unchanged:
this row uses processed feature-text embeddings on the ReSID item universe and
is not a faithful raw-text TIGER/GRID reproduction.

Paper use:

- Safe: "On the same Musical item universe, AUDIT-SID shows that the
  feature-text GRID/RQ-KMeans export consistently has high collision pressure
  across three seeds, while ReSID/GAOQ is collision-free on its bounded export."
- Unsafe: "GRID is worse than ReSID" or "TIGER/GRID fails on Musical."
