# SIDInspector B6 D3 Fixed-Reranker Validation: Musical

Timestamp: 2026-05-20 19:05:25 CST

## Verdict

B6 is complete locally for Musical_Instruments as a bounded ranking validation.
This run is stronger than the earlier prefix-retrieval context probe because SID
mappings only define candidate sets; every row is ranked by the same train-only
co-occurrence/popularity reranker.
The run requires explicit split labels by default; splitless data can only be
used with an explicit proxy flag.

Safe claim:

> D3 neighborhood alignment is positively associated with prefix-candidate
> recall and with a fixed lightweight reranker on the Musical worked example.
> This supports D3 as an early candidate-generation and ranking-context signal,
> not as a trained generator Recall/NDCG substitute.

Unsafe claim:

> D3 is validated as downstream generator Recall@K/NDCG.

## Artifacts

- Script: `tools/autodl_audit_sid/run_d3_ranking_validation.py`
- Tests: `tests/test_d3_ranking_validation.py`
- 1,000-user output:
  `_gate0_artifacts/d3_ranking_validation/musical_fixed_rerank_1000_20260520/`
- 5,000-user output:
  `_gate0_artifacts/d3_ranking_validation/musical_fixed_rerank_5000_20260520/`

## Commands

```bash
python3 tools/autodl_audit_sid/run_d3_ranking_validation.py \
  --output-dir _gate0_artifacts/d3_ranking_validation/musical_fixed_rerank_1000_20260520 \
  --max-users 1000 \
  --top-k 20 \
  --prefix-depths 1,2 \
  --d3-max-pair-events 250000 \
  --max-candidates-per-prefix 5000
```

```bash
python3 tools/autodl_audit_sid/run_d3_ranking_validation.py \
  --output-dir _gate0_artifacts/d3_ranking_validation/musical_fixed_rerank_5000_20260520 \
  --max-users 5000 \
  --top-k 20 \
  --prefix-depths 1,2 \
  --d3-max-pair-events 500000 \
  --max-candidates-per-prefix 5000
```

## 5,000-User Depth-1 Results

Ranker: `cooccurrence_popularity`.

| Method | D3 L1 weighted | Candidate recall | Fixed-reranker Recall@20 | Fixed-reranker NDCG@20 | Fixed-reranker MRR@20 |
|---|---:|---:|---:|---:|---:|
| sanity_category_prefix | 0.4383 | 0.6126 | 0.0618 | 0.0292 | 0.0201 |
| sanity_popularity_balanced | 0.3442 | 0.7141 | 0.0620 | 0.0290 | 0.0198 |
| resid_gaoq | 0.1353 | 0.3601 | 0.0528 | 0.0252 | 0.0175 |
| grid ft-cap | 0.0760 | 0.2487 | 0.0321 | 0.0162 | 0.0118 |
| grid feature-text | 0.0523 | 0.1859 | 0.0340 | 0.0171 | 0.0124 |
| sanity_mod_collision_hash | 0.0039 | 0.0195 | 0.0070 | 0.0036 | 0.0026 |

## Correlation Summary

For the 5,000-user depth-1 `cooccurrence_popularity` reranker across six
artifact/control rows:

| Metric | Pearson with D3 | Spearman with D3 |
|---|---:|---:|
| candidate_recall | 0.9390 | 0.9429 |
| recall_at_k | 0.8583 | 0.8857 |
| ndcg_at_k | 0.8429 | 0.9429 |
| mrr_at_k | 0.8269 | 0.9429 |

The 1,000-user run is directionally consistent. Its depth-1
`cooccurrence_popularity` Spearman values are 0.9429 for candidate recall,
0.9429 for fixed-reranker Recall@20, and 1.0000 for fixed-reranker
NDCG@20/MRR@20.

## Interpretation

- The strongest supported point is early validation: D3 tracks whether prefix
  neighborhoods expose useful candidate sets and whether a shared lightweight
  reranker can exploit them.
- The category-prefix inversion remains visible under fixed reranking: the
  deterministic category row has the highest D3 and one of the strongest
  fixed-reranker Recall/NDCG rows.
- Popularity-balanced has the highest candidate recall but also severe aliasing,
  which reinforces the need to read D1-D5 together.
- These runs still do not train a generator, do not evaluate invalid generated
  SID paths, and do not replace downstream recommendation metrics.
