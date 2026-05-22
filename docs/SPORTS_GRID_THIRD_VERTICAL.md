# SIDInspector B7 Sports GRID Third-Vertical Export

Timestamp: 2026-05-20 19:05:25 CST

## Verdict

B7 now has a real third-vertical learned/export row: GRID/RQ-KMeans-style
feature-text export on `Sports_and_Outdoors`. This is not a proxy/control row.
It uses ReSID public processed item features/interactions for the Sports
vertical, encodes item-feature text, exports residual MiniBatchKMeans SIDs, and
runs D1-D5 metrics with zero SID coverage gaps.

The 20,000-item run is the current evidence row. The 5,000-item run is retained
as a bounded smoke/provenance artifact.

## Artifacts

- Normalized Sports input:
  `_gate0_artifacts/resid_Sports_and_Outdoors_normalized/`
- 5,000-item GRID export:
  `_gate0_artifacts/grid_sports_feature_text_runs/grid_official_rqkmeans_Sports_and_Outdoors_resid_feature_text_5000_cpu_seed42_20260520/`
- 20,000-item GRID export:
  `_gate0_artifacts/grid_sports_feature_text_runs/grid_official_rqkmeans_Sports_and_Outdoors_resid_feature_text_20000_cpu_seed42_20260520/`
- Preparation script:
  `tools/autodl_audit_sid/prepare_resid_feature_grid_inputs.py`
- Export script:
  `tools/autodl_audit_sid/run_grid_rqkmeans_direct_export.py`

## Commands

Normalize ReSID Sports schema:

```bash
PYTHONPATH=/Users/timber/Documents/Sec_phrase/src \
python3 -m audit_sid.adapters.resid \
  --dataset-root _gate0_repos/ReSID-dataset/Sports_and_Outdoors/leave_one_out/dataset \
  --output-dir _gate0_artifacts/resid_Sports_and_Outdoors_normalized \
  --dataset-name Sports_and_Outdoors
```

Prepare 20,000 item-feature embeddings:

```bash
python3 tools/autodl_audit_sid/prepare_resid_feature_grid_inputs.py \
  --item-metadata _gate0_artifacts/resid_Sports_and_Outdoors_normalized/item_metadata.parquet \
  --interactions _gate0_artifacts/resid_Sports_and_Outdoors_normalized/interactions.parquet \
  --output-dir _gate0_artifacts/grid_sports_feature_text_runs/grid_official_rqkmeans_Sports_and_Outdoors_resid_feature_text_20000_cpu_seed42_20260520/input \
  --dataset-name Sports_and_Outdoors \
  --max-items 20000 \
  --device cpu \
  --batch-size 256
```

Run GRID/RQ-KMeans export:

```bash
python3 tools/autodl_audit_sid/run_grid_rqkmeans_direct_export.py \
  --embeddings _gate0_artifacts/grid_sports_feature_text_runs/grid_official_rqkmeans_Sports_and_Outdoors_resid_feature_text_20000_cpu_seed42_20260520/input/item_embeddings.pt \
  --item-ids _gate0_artifacts/grid_sports_feature_text_runs/grid_official_rqkmeans_Sports_and_Outdoors_resid_feature_text_20000_cpu_seed42_20260520/input/item_ids.npy \
  --item-metadata _gate0_artifacts/grid_sports_feature_text_runs/grid_official_rqkmeans_Sports_and_Outdoors_resid_feature_text_20000_cpu_seed42_20260520/input/item_metadata.parquet \
  --interactions _gate0_artifacts/grid_sports_feature_text_runs/grid_official_rqkmeans_Sports_and_Outdoors_resid_feature_text_20000_cpu_seed42_20260520/input/interactions.parquet \
  --output-dir _gate0_artifacts/grid_sports_feature_text_runs/grid_official_rqkmeans_Sports_and_Outdoors_resid_feature_text_20000_cpu_seed42_20260520/grid_export \
  --dataset-name Sports_and_Outdoors \
  --method grid_official_rqkmeans_sports_resid_feature_text \
  --codebook-width 128 \
  --num-hierarchies 3 \
  --batch-size 4096 \
  --steps-per-layer 80 \
  --device cpu \
  --seed 42
```

## Key Results

| Run | Items | Interaction items | Metadata gap | Interaction gap | Unique full SID | Duplicate SID rate | D3 L1 weighted | D4 tail unique ratio | Prefix counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Sports GRID 5k | 5,000 | 4,981 | 0 | 0 | 3,127 | 0.3746 | 0.0764 | 0.8235 | 128;3105;3127 |
| Sports GRID 20k | 20,000 | 19,961 | 0 | 0 | 8,165 | 0.5918 | 0.0550 | 0.6528 | 128;7986;8165 |

## Interpretation

- This closes the immediate B7 preflight gap for a third vertical with a real
  learned/export SID row.
- It does not add a third named tokenizer; it adds a third vertical for the GRID
  export path. That is useful for portability and robustness, not method
  coverage.
- The Sports 20k D3 score is low and close to the Musical/All_Beauty GRID range,
  which supports the cross-vertical observation that this GRID feature-text
  export does not automatically yield high collaborative prefix alignment.
- This row should be paper-supporting evidence or artifact-table evidence, not
  a leaderboard claim.
