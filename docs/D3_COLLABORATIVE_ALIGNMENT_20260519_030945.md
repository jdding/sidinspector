# D3 Collaborative Alignment Upgrade

Timestamp: 2026-05-19 03:09:45 CST

## Decision

`d3_alignment.csv` is no longer a category-purity-only proxy. The metric now
uses item-item co-occurrence from the interaction table as the required
collaborative reference and reports SID-prefix recall of collaborative
neighbors.

Category purity is retained as an auxiliary semantic metadata column:

- `level0_category_purity_mean`
- `level0_non_singleton_buckets`

## Metric Definition

For each dataset/method artifact:

1. build item-item co-occurrence counts from training interactions;
2. if the table has a `split` column but no `train` rows, fall back to all
   rows instead of treating interactions as empty;
3. keep each item's top-k co-occurrence neighbors;
4. for each SID prefix depth, report how often those collaborative neighbors
   share the same SID prefix.

Default controls:

- `--d3-top-k 20`
- `--d3-max-pair-events 2000000`
- `--d3-max-user-items 200`

This avoids using SASRec as a single oracle and directly addresses the
external-review concern that D3 must not only measure category taxonomy
alignment.

## Local Smoke Evidence

Unit smoke:

```bash
python3 -m unittest tests/test_metrics.py
```

Result: pass, 2 tests.

Real-artifact smoke:

```bash
PYTHONPATH=src python3 -m audit_sid.metrics \
  --sid-assignments _gate0_artifacts/resid_real_runs/normalized_resid_gaoq_1epoch/sid_assignments.parquet \
  --item-metadata _gate0_artifacts/resid_real_runs/normalized_resid_gaoq_1epoch/item_metadata.parquet \
  --interactions _gate0_artifacts/resid_real_runs/normalized_resid_gaoq_1epoch/interactions.parquet \
  --output-dir _gate0_artifacts/resid_real_runs/normalized_resid_gaoq_1epoch/metrics_d3v2 \
  --d3-top-k 20 \
  --d3-max-pair-events 2000000
```

```bash
PYTHONPATH=src python3 -m audit_sid.metrics \
  --sid-assignments _gate0_artifacts/grid_cluster_a_runs/grid_official_rqkmeans_All_Beauty_text_smoke5000_local/grid_export/normalized/sid_assignments.parquet \
  --item-metadata _gate0_artifacts/grid_cluster_a_runs/grid_official_rqkmeans_All_Beauty_text_smoke5000_local/input/item_metadata.parquet \
  --interactions _gate0_artifacts/grid_cluster_a_runs/grid_official_rqkmeans_All_Beauty_text_smoke5000_local/input/interactions.parquet \
  --output-dir _gate0_artifacts/grid_cluster_a_runs/grid_official_rqkmeans_All_Beauty_text_smoke5000_local/grid_export/metrics_d3v2 \
  --d3-top-k 20 \
  --d3-max-pair-events 2000000 \
  --allow-partial-coverage
```

## Initial D3v2 Results

| Dataset | Method | Depth | Users used | Pair events | Collab items | Mean collab-prefix recall | Weighted recall | Category purity |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Musical_Instruments | ReSID GAOQ | 1 | 55,785 | 1,603,318 | 23,691 | 0.1535 | 0.1527 | 0.5669 |
| Musical_Instruments | ReSID GAOQ | 2 | 55,785 | 1,603,318 | 23,691 | 0.0175 | 0.0175 | 0.5669 |
| Musical_Instruments | ReSID GAOQ | 3 | 55,785 | 1,603,318 | 23,691 | 0.0000 | 0.0000 | 0.5669 |
| All_Beauty | GRID RQ-KMeans 5k | 1 | 291 | 605 | 423 | 0.1044 | 0.0727 | 0.9947 |
| All_Beauty | GRID RQ-KMeans 5k | 2 | 291 | 605 | 423 | 0.0260 | 0.0104 | 0.9947 |
| All_Beauty | GRID RQ-KMeans 5k | 3 | 291 | 605 | 423 | 0.0118 | 0.0052 | 0.9947 |

## Interpretation

The metric now separates semantic/category organization from collaborative
organization. The All_Beauty GRID 5k artifact has very high level-0 category
purity but low collaborative-prefix recall, which is exactly the kind of
semantic-collaborative mismatch D3 is supposed to expose. ReSID Musical has
moderate category purity and stronger level-0 collaborative recall, but recall
collapses at deeper prefixes because the final SID is unique.

This is still not a same-dataset method comparison, so it does not close Gate
0A by itself. It does remove the earlier D3 proxy blocker for local artifacts.
