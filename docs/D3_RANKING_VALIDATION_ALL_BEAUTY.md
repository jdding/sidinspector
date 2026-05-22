# SIDInspector B6 D3 Fixed-Reranker Validation: All_Beauty

Timestamp: 2026-05-20 21:25:56 CST

## Verdict

B6 is locally CPU-runnable for All_Beauty only after constructing an explicit
train/valid split. The available All_Beauty interaction parquet has
`split=all`, so the Musical command cannot be used as-is under the strict
fixed-reranker validation contract. I therefore froze a bounded temporal
leave-one-out split inside the allowed D3 artifact directory and ran the
existing fixed-reranker script without `--allow-splitless-proxy`.

Safe claim:

> On a 1,000-user bounded All_Beauty temporal-LOO panel, D3 remains positively
> associated with prefix-candidate recall and with a shared train-only
> co-occurrence/popularity reranker. This is a portability stressor for the D3
> ranking-context signal, not a downstream generator benchmark.

Unsafe claim:

> All_Beauty validates downstream generator Recall/NDCG, or the category-prefix
> control is a stronger learned SID tokenizer.

## Inputs And Split Gate

- Original interaction input:
  `_gate0_artifacts/grid_cluster_a_runs/grid_official_rqkmeans_All_Beauty_text_20000_cpu_seed45_d3v2_20260519_084529/input/interactions.parquet`
- Original split status: 148,315 rows, 142,596 users, `split={"all": 148315}`.
- Strict validation issue: no native `train`/`valid`/`test` labels exist locally.
- Constructed strict input:
  `_gate0_artifacts/d3_ranking_validation/all_beauty_fixed_rerank_1000_20260520/all_beauty_interactions_temporal_loo.parquet`
- Split policy: drop singleton users; for users with at least two events, earlier
  events are `train` and the last event is `valid`.
- Constructed split size: 10,109 rows, 4,390 users, `train=5,719`,
  `valid=4,390`.

## Artifacts

- Output root:
  `_gate0_artifacts/d3_ranking_validation/all_beauty_fixed_rerank_1000_20260520/`
- Summary:
  `_gate0_artifacts/d3_ranking_validation/all_beauty_fixed_rerank_1000_20260520/d3_ranking_validation_summary.csv`
- Correlations:
  `_gate0_artifacts/d3_ranking_validation/all_beauty_fixed_rerank_1000_20260520/d3_ranking_validation_correlations.csv`
- Split manifest:
  `_gate0_artifacts/d3_ranking_validation/all_beauty_fixed_rerank_1000_20260520/temporal_loo_split_manifest.json`
- Paper-facing table:
  `paper_assets/tables/table14_all_beauty_d3_ranking_validation.csv`

## Commands

Construct the bounded temporal split:

```bash
python3 - <<'PY'
import json
from pathlib import Path
import pandas as pd

src = Path('_gate0_artifacts/grid_cluster_a_runs/grid_official_rqkmeans_All_Beauty_text_20000_cpu_seed45_d3v2_20260519_084529/input/interactions.parquet')
out_dir = Path('_gate0_artifacts/d3_ranking_validation/all_beauty_fixed_rerank_1000_20260520')
out_dir.mkdir(parents=True, exist_ok=True)
out = out_dir / 'all_beauty_interactions_temporal_loo.parquet'
manifest = out_dir / 'temporal_loo_split_manifest.json'

df = pd.read_parquet(src).copy()
ordered = df.sort_values(['user_id', 'timestamp', 'item_id']).copy()
ordered['split'] = 'drop_singleton'
for user_id, idx in ordered.groupby('user_id', sort=True).groups.items():
    idx = list(idx)
    if len(idx) < 2:
        continue
    ordered.loc[idx[:-1], 'split'] = 'train'
    ordered.loc[idx[-1], 'split'] = 'valid'
keep = ordered[ordered['split'].isin(['train', 'valid'])].copy().reset_index(drop=True)
keep.to_parquet(out, index=False)
manifest.write_text(json.dumps({
    'source_interactions': str(src),
    'output_interactions': str(out),
    'policy': 'temporal leave-one-out over users with at least two interactions; all singleton users dropped; last event is valid, earlier events are train',
    'source_rows': int(len(df)),
    'source_users': int(df['user_id'].nunique()),
    'kept_rows': int(len(keep)),
    'kept_users': int(keep['user_id'].nunique()),
    'split_counts': {k:int(v) for k,v in keep['split'].value_counts().to_dict().items()},
}, indent=2, sort_keys=True) + '\n')
PY
```

Run fixed-reranker validation:

```bash
python3 /Users/timber/aris-source/tools/axiomdesk_run.py \
  --project /Users/timber/Documents/Sec_phrase -- \
  python3 tools/autodl_audit_sid/run_d3_ranking_validation.py \
  --sid-assignments _gate0_artifacts/vertical_replication/all_beauty_20k_grid_sanity_20260520/sid_assignments.parquet \
  --item-metadata _gate0_artifacts/grid_cluster_a_runs/grid_official_rqkmeans_All_Beauty_text_20000_cpu_seed45_d3v2_20260519_084529/input/item_metadata.parquet \
  --interactions _gate0_artifacts/d3_ranking_validation/all_beauty_fixed_rerank_1000_20260520/all_beauty_interactions_temporal_loo.parquet \
  --dataset-name All_Beauty \
  --output-dir _gate0_artifacts/d3_ranking_validation/all_beauty_fixed_rerank_1000_20260520 \
  --max-users 1000 \
  --top-k 20 \
  --prefix-depths 1,2 \
  --d3-max-pair-events 250000 \
  --max-candidates-per-prefix 5000 \
  --rankers cooccurrence_popularity
```

## Depth-1 Results

Ranker: `cooccurrence_popularity`; evaluated targets: 1,000.

| Method | D3 L1 weighted | Candidate recall | Fixed-reranker Recall@20 | Fixed-reranker NDCG@20 | Fixed-reranker MRR@20 |
|---|---:|---:|---:|---:|---:|
| category-prefix sanity | 0.9532 | 0.5140 | 0.0480 | 0.0223 | 0.0154 |
| popularity-balanced sanity | 0.2675 | 0.2360 | 0.0170 | 0.0072 | 0.0045 |
| GRID RQ-KMeans 20k seed42 | 0.0597 | 0.0850 | 0.0290 | 0.0162 | 0.0125 |
| mod-collision hash sanity | 0.0035 | 0.0060 | 0.0020 | 0.0015 | 0.0013 |

## Correlation Summary

For depth-1 `cooccurrence_popularity` across four rows:

| Metric | Pearson with D3 | Spearman with D3 |
|---|---:|---:|
| candidate_recall | 0.9832 | 1.0000 |
| recall_at_k | 0.8337 | 0.8000 |
| ndcg_at_k | 0.7433 | 0.8000 |
| mrr_at_k | 0.6720 | 0.8000 |

## Paper Use

This can enter the paper only as a bounded supplementary stressor for B6-style
ranking-context replication. The caveats must travel with it:

- the native All_Beauty local interaction file is splitless;
- the reported panel uses a constructed temporal leave-one-out split;
- All_Beauty metadata is coarse, so category-prefix is a diagnostic control, not
  a semantic hierarchy baseline;
- the result validates prefix candidate/reranker context, not a trained SID
  generator.
