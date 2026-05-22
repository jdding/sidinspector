# D3 Prefix-Ranking Context Probe

Timestamp: 2026-05-20 17:28:00 CST

## Verdict

This is a useful W3 context probe, but it is **not** downstream Recall/NDCG
validation.

The probe uses the SID prefix neighborhoods themselves as a simple
popularity-tiebroken retrieval rule: for each user, collect prefixes from train
items, retrieve non-train items sharing those prefixes, rank by prefix-match
count and item popularity, and test whether the validation item appears in the
top 20. It runs on the same Musical item universe and first 5,000 evaluable
validation users.

Safe claim:

> In a no-training prefix-neighborhood retrieval probe, D3-L1 is positively
> associated with depth-1 prefix retrieval recall across the six Musical rows,
> while deeper-prefix behavior remains non-monotonic. This supports treating D3
> as a diagnostic context signal, not as a replacement for generator evaluation.

Unsafe claim:

> D3 predicts trained-generator Recall@K/NDCG.

## Inputs

- GRID feature-text SID:
  `_gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/grid_export/normalized/sid_assignments.parquet`
- GRID ft-cap SID:
  `_gate0_artifacts/grid_same_dataset_runs/matched_capacity_grid_32_1280_1280_seed42_20260520/grid_export/normalized/sid_assignments.parquet`
- ReSID + sanity SIDs:
  `_gate0_artifacts/resid_real_runs/combined_resid_sanity/sid_assignments.parquet`
- Interactions:
  `_gate0_artifacts/resid_musical_normalized/interactions.parquet`

## Outputs

- `_gate0_artifacts/prefix_ranking_probe/musical_valid_depth1_k20_5000users_20260520/`
- `_gate0_artifacts/prefix_ranking_probe/musical_valid_depth2_k20_5000users_20260520/`
- `_gate0_artifacts/prefix_ranking_probe/musical_test_depth1_k20_5000users_20260520/`

## Results

### Depth 1 Prefix Retrieval

| Method | D3-L1 weighted | Recall@20 proxy | Mean candidates |
|---|---:|---:|---:|
| sanity_mod_collision_hash | 0.0038 | 0.0056 | 501 |
| GRID feature-text | 0.0552 | 0.0240 | 2,369 |
| GRID ft-cap | 0.0796 | 0.0192 | 4,115 |
| ReSID GAOQ | 0.1527 | 0.0424 | 2,848 |
| sanity_popularity_balanced | 0.3137 | 0.0480 | 11,733 |
| sanity_category_prefix | 0.4488 | 0.0512 | 11,775 |

Correlation across six rows:

- Spearman: 0.943, p=0.0048
- Pearson: 0.892, p=0.0168

### Depth 1 Test Split Check

| Method | Recall@20 proxy | Mean candidates |
|---|---:|---:|
| sanity_mod_collision_hash | 0.0054 | 501 |
| GRID feature-text | 0.0220 | 2,370 |
| GRID ft-cap | 0.0240 | 4,117 |
| ReSID GAOQ | 0.0374 | 2,849 |
| sanity_popularity_balanced | 0.0388 | 11,735 |
| sanity_category_prefix | 0.0494 | 11,772 |

Correlation across six rows using the same D3-L1 values:

- Spearman: 1.000, p=0.0000
- Pearson: 0.906, p=0.0129

### Depth 2 Prefix Retrieval

| Method | D3-L1 weighted | Recall@20 proxy | Mean candidates |
|---|---:|---:|---:|
| sanity_mod_collision_hash | 0.0038 | 0.0056 | 501 |
| GRID feature-text | 0.0552 | 0.0114 | 67 |
| GRID ft-cap | 0.0796 | 0.0104 | 28 |
| ReSID GAOQ | 0.1527 | 0.0358 | 92 |
| sanity_popularity_balanced | 0.3137 | 0.0036 | 123 |
| sanity_category_prefix | 0.4488 | 0.0558 | 6,437 |

Correlation across six rows:

- Spearman: 0.371, p=0.468
- Pearson: 0.647, p=0.165

## Interpretation

The depth-1 result gives D3 a limited behavioral retrieval context: rows with
higher D3-L1 generally recover held-out validation and test items better under
the same simple prefix-neighborhood rule. This directly addresses part of W3's
concern without pretending to run a generator.

The depth-2 result is more mixed. Popularity-balanced has relatively high D3-L1
but poor depth-2 prefix retrieval, and category-prefix has very large candidate
sets. This is useful because it supports the paper's current position: D3 is a
warning/context signal that must be read together with D2, D4, and D5.

## Paper Use

Recommended use for CIKM v0:

- artifact repository or reviewer-response note;
- at most one short sentence if page budget allows.

Do not add it as a main paper claim unless the wording says "prefix-neighborhood
retrieval proxy" and avoids "Recall@K/NDCG".
