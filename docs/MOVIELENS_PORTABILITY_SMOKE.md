# MovieLens Portability Smoke

Timestamp: 2026-05-19 11:53:10 CST

## Verdict

`LOCAL_SMOKE_PASSED_NON_AMAZON_SCHEMA`

The AUDIT-SID mapping-first interface and D1-D5a/D3v2 metrics run on a
non-Amazon dataset schema using only local CPU. This is a toolkit portability
smoke, not a main empirical result and not a new tokenizer experiment.

## Dataset And Bound

- Source: local `/Volumes/TU280Pro/Research/DataSet/MovieLens-25M/archive.zip`
- Dataset member files used: `ml-25m/movies.csv`, `ml-25m/ratings.csv`
- Bound: first 1,000,000 ratings rows, first 10,000 observed movie items
- Metadata: movie title plus primary genre
- SID systems: sanity baselines only
- Output: `_gate0_artifacts/movielens_portability_smoke/ml25m_1mratings_10kitems/`

Runner:

```bash
PYTHONPATH=src python3 tools/autodl_audit_sid/run_movielens_portability_smoke.py \
  --zip-path /Volumes/TU280Pro/Research/DataSet/MovieLens-25M/archive.zip \
  --output-dir _gate0_artifacts/movielens_portability_smoke/ml25m_1mratings_10kitems \
  --max-ratings 1000000 \
  --max-items 10000
```

## Coverage

| Method | SID items | Metadata items | Interaction items | Missing metadata SID | Missing interaction SID |
|---|---:|---:|---:|---:|---:|
| `sanity_category_prefix` | 10,000 | 10,000 | 10,000 | 0 | 0 |
| `sanity_mod_collision_hash` | 10,000 | 10,000 | 10,000 | 0 | 0 |
| `sanity_popularity_balanced` | 10,000 | 10,000 | 10,000 | 0 | 0 |

## Diagnostic Range

| Method | Unique SID | Duplicate SID rate | Full collision rate | D3 L1 weighted recall | D4 head/mid/tail unique ratio | Prefix counts |
|---|---:|---:|---:|---:|---|---|
| `sanity_category_prefix` | 10,000 | 0.0000 | 0.0000 | 0.278778 | 1.0000 / 1.0000 / 1.0000 | `19;19;19;10000` |
| `sanity_mod_collision_hash` | 256 | 0.9744 | 1.0000 | 0.003766 | 0.0768 / 0.0768 / 0.0768 | `256;256;256;256` |
| `sanity_popularity_balanced` | 9,824 | 0.0176 | 0.0350 | 0.769779 | 0.9853 / 0.9865 / 0.9889 | `4;1024;9824;9824` |

## Interpretation

This closes the optional portability smoke in the current plan:

- `item_metadata`, `interactions`, and `sid_assignments` can be produced from a
  non-Amazon movie schema.
- D1-D5a and D3v2 all run without Amazon-specific assumptions.
- The sanity baselines still produce a meaningful diagnostic range on
  collision, prefix alignment, and head-tail capacity.

Safe paper wording:

> As a portability check, AUDIT-SID also runs unchanged on a bounded
> MovieLens-25M smoke slice using movie genres and ratings interactions. We use
> this only to validate the toolkit input contract beyond Amazon schemas.

Do not claim:

- MovieLens is part of the main SID tokenizer benchmark.
- These sanity SID rows evaluate a real SID tokenizer.
- The bounded first-1M-ratings slice supports dataset-level recommender claims.

## Local Validation

- `PYTHONPYCACHEPREFIX=/private/tmp/sec_phrase_pycache python3 -m py_compile tools/autodl_audit_sid/run_movielens_portability_smoke.py`
- `python3 -m unittest tests/test_metrics.py tests/test_sid_churn.py`
- Tiny smoke: 100k ratings / 2k items passed before the 1M / 10k run.
