# Vertical D3 Replication Note

Timestamp: 2026-05-20 17:10:00 CST

## Verdict

The B4 vertical-replication preflight is already locally closed for one feasible
additional vertical: `All_Beauty`.

This evidence strengthens the D3-inversion story as a diagnostic finding, but it
uses coarse `category` fallback metadata on All_Beauty and does not solve the
separate W3 downstream-validation concern. The safe claim is:

> On Musical and All_Beauty, category-derived controls recover more
> co-occurrence prefix neighbors than the learned GRID feature-text exports,
> showing that D3 surfaces a behavioral-prefix diagnostic that should be read
> with D2/D4/D5 rather than as a tokenizer-quality score.

Unsafe claim:

> D3 predicts Recall@K/NDCG or category-prefix is a better recommender
> tokenizer.

## Evidence

### All_Beauty 20k

Source:

- `_gate0_artifacts/vertical_replication/all_beauty_20k_grid_sanity_20260520/vertical_d3_summary.csv`
- `_gate0_artifacts/vertical_replication/all_beauty_20k_grid_sanity_20260520/metrics/`
- Detailed result note:
  `docs/VERTICAL_D3_REPLICATION_ALL_BEAUTY.md`

Key rows:

| Row | Unique SIDs | D2 full-code aliasing | D3 L1 weighted | D4 tail | Prefix counts |
|---|---:|---:|---:|---:|---|
| GRID/RQ-KMeans feature-text | 16,718 | 0.25555 | 0.08115 | 0.92307 | 128/7126/16718 |
| Category-prefix control | 20,000 | 0.00000 | 0.96844 | 1.00000 | 2/2/2/20000 |
| Mod-collision hash | 256 | 1.00000 | 0.00457 | 0.03839 | 256/256/256/256 |
| Popularity-balanced | 1,024 | 1.00000 | 0.25004 | 0.15297 | 4/1024/1024/1024 |

### All_Beauty 5k

Source:

- `_gate0_artifacts/vertical_replication/all_beauty_5k_smoke_20260520/vertical_d3_summary.csv`
- `_gate0_artifacts/vertical_replication/all_beauty_5k_smoke_20260520/metrics/`

Key rows:

| Row | Unique SIDs | D2 full-code aliasing | D3 L1 weighted | D4 tail | Prefix counts |
|---|---:|---:|---:|---:|---|
| GRID/RQ-KMeans feature-text | 4,281 | 0.23080 | 0.07463 | 0.92917 | 64/1895/4281 |
| Category-prefix control | 5,000 | 0.00000 | 0.94527 | 1.00000 | 2/2/2/5000 |
| Mod-collision hash | 256 | 1.00000 | 0.00249 | 0.15366 | 256/256/256/256 |
| Popularity-balanced | 1,024 | 1.00000 | 0.21393 | 0.52341 | 4/1024/1024/1024 |

## Interpretation For The Paper

This should be used as artifact-repository evidence or a one-sentence support
line, not as another main table unless page budget is reopened.

Possible safe sentence:

> The D3 inversion is not unique to the Musical table: on a 20k All_Beauty
> vertical replication, category-prefix reaches 0.968 D3-L1 while a GRID
> feature-text export reaches 0.081, reinforcing that D3 detects
> behaviorally coherent prefixes rather than method quality by itself.

Keep both qualifications immediately nearby:

> This is a diagnostic-context result, not a downstream ranking validation.

> The All_Beauty category-prefix control uses coarse `category` fallback
> metadata, so it is not evidence that a rich category hierarchy dominates
> learned SID tokenizers.

## Status

- B4 vertical replication preflight: `LOCAL_DONE_FOR_ALL_BEAUTY`.
- Paper admission: optional; likely artifact-repo or single-sentence support.
- Remaining W3: partly contextualized by `docs/D3_RANKING_CONTEXT_MUSICAL.md`,
  but still open as downstream validation because the B3 proxy is not a trained
  Recall/NDCG evaluation.
