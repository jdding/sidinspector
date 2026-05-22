# SIDInspector B3 D3 Ranking-Context Probe: Musical

Timestamp: 2026-05-20 17:30:00 CST

## Verdict

The B3 bounded ranking-context probe is complete as a CPU local smoke. It uses a
prefix-neighborhood retrieval proxy over existing Musical SID artifacts. This
is **not** downstream Recall/NDCG validation and should not be written as a
trained recommender result.

A 5,000-user robustness rerun completed on 2026-05-20 and preserves the same
interpretation: D3 remains broadly aligned with prefix-candidate coverage, while
Hit@20 stays low for every row. This strengthens the diagnostic-context claim
without turning D3 into a Recall@K surrogate.

Safe claim:

> D3 has ranking-context signal under a lightweight prefix-retrieval proxy, but
> the very low Hit@20 values show that it is a diagnostic artifact measure, not
> a replacement for downstream recommendation evaluation.

## Artifact

- Script:
  `tools/autodl_audit_sid/run_d3_ranking_context.py`
- Test:
  `tests/test_d3_ranking_context.py`
- Local output:
  `_gate0_artifacts/d3_ranking_context/musical_prefix_retrieval_1000_20260520/`
- Summary CSV:
  `_gate0_artifacts/d3_ranking_context/musical_prefix_retrieval_1000_20260520/d3_ranking_context_summary.csv`
- Manifest:
  `_gate0_artifacts/d3_ranking_context/musical_prefix_retrieval_1000_20260520/manifest.json`

## Command

```bash
python3 tools/autodl_audit_sid/run_d3_ranking_context.py \
  --output-dir _gate0_artifacts/d3_ranking_context/musical_prefix_retrieval_1000_20260520 \
  --max-users 1000 \
  --top-k 20 \
  --prefix-depths 1,2 \
  --d3-max-pair-events 250000 \
  --max-candidates-per-prefix 5000
```

Robustness rerun:

```bash
python3 tools/autodl_audit_sid/run_d3_ranking_context.py \
  --output-dir _gate0_artifacts/d3_ranking_context/musical_prefix_retrieval_5000_20260520 \
  --max-users 5000 \
  --top-k 20 \
  --prefix-depths 1,2 \
  --d3-max-pair-events 500000 \
  --max-candidates-per-prefix 5000
```

## Key Depth-1 Results

| Method | D3 L1 weighted | Candidate coverage | Hit@20 | MRR@20 | Mean candidates |
|---|---:|---:|---:|---:|---:|
| category-prefix | 0.4393 | 0.6047 | 0.0471 | 0.0149 | 6,640 |
| popularity-balanced | 0.3887 | 0.7134 | 0.0461 | 0.0134 | 9,792 |
| ReSID GAOQ | 0.1308 | 0.3647 | 0.0421 | 0.0137 | 2,836 |
| GRID ft-cap | 0.0761 | 0.2590 | 0.0311 | 0.0097 | 4,085 |
| GRID feature-text | 0.0525 | 0.1964 | 0.0235 | 0.0076 | 2,356 |
| mod-collision hash | 0.0038 | 0.0195 | 0.0055 | 0.0022 | 500 |

## Robustness: 5,000 Users

| Method | D3 L1 weighted | Candidate coverage | Hit@20 | MRR@20 | Mean candidates |
|---|---:|---:|---:|---:|---:|
| category-prefix | 0.4383 | 0.6126 | 0.0496 | 0.0139 | 6,585 |
| popularity-balanced | 0.3442 | 0.7141 | 0.0445 | 0.0125 | 9,885 |
| ReSID GAOQ | 0.1353 | 0.3601 | 0.0444 | 0.0131 | 2,848 |
| GRID ft-cap | 0.0760 | 0.2487 | 0.0266 | 0.0089 | 4,114 |
| GRID feature-text | 0.0523 | 0.1859 | 0.0263 | 0.0093 | 2,369 |
| mod-collision hash | 0.0039 | 0.0195 | 0.0062 | 0.0025 | 501 |

## Interpretation

- D3 and candidate coverage are broadly aligned in both the 1,000-user and
  5,000-user runs: rows with high D3 tend to retrieve more held-out targets
  somewhere in the prefix-neighborhood candidate set.
- Hit@20 is low for every row, including category-prefix and popularity-balanced
  controls. This blocks any claim that D3 is validated as a downstream ranking
  metric.
- The GRID ft-cap row improves over the smaller GRID feature-text row on both
  D3 and prefix-retrieval context, but remains below ReSID and the category
  control. This is consistent with the matched-capacity interpretation:
  capacity matters, but it does not erase the D3 gap.
- Popularity-balanced has high candidate coverage but severe aliasing and weak
  Hit@20, reinforcing that D1/D2/D3/D4/D5 must be read together.

## Paper Use

This is suitable for artifact-repository evidence and a cautious sentence in
the limits/future-work discussion. It should not become a main result table
unless the paper expands beyond the current 4-page Resource Track budget.

Unsafe wording:

- D3 predicts Recall@K.
- Category-prefix is a better recommender tokenizer.
- Prefix retrieval is equivalent to generator training.
