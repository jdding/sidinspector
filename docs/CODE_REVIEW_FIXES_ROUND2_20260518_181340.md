# Code Review Fixes Round 2

**生成时间**：2026-05-18 18:13:40 CST
**状态**：second sub-agent review findings fixed and smoke-tested

## Review Verdict

Second read-only review found no P0 issue that contaminates the current ReSID + sanity case study. It flagged two P1 risks:

- D2 popularity column could be misread because full-SID collision and prefix collision were mixed in one row;
- coverage validation reported partial SID coverage but did not fail by default.

It also flagged two P2 issues:

- multi-dataset combined runs need dataset-aware metadata/interactions;
- `sanity_category_prefix` had a pandas `.get()` default-argument edge case.

## Fixes Applied

| Finding | Fix |
|---|---|
| D2 popularity could be misread | Replaced the old popularity column with `mean_popularity_full_collision_items` and `mean_popularity_prefix_collision_items` |
| Partial coverage did not fail | Metrics now fail by default when a method misses metadata or interaction items; use `--allow-partial-coverage` only explicitly |
| Multi-dataset combined runs unsafe | Multi-dataset SID inputs now require `dataset` columns in `item_metadata` and `interactions`; otherwise the runner fails |
| `sanity_category_prefix` metadata fallback edge case | Added explicit candidate-column resolver for `category_l1/l2/l3` or `category` |

## Verification

Passed:

```bash
PYTHONPATH=src PYTHONPYCACHEPREFIX=/private/tmp/audit_sid_pycache \
python3 -m py_compile src/audit_sid/adapters/sanity.py src/audit_sid/metrics.py

PYTHONPATH=src PYTHONPYCACHEPREFIX=/private/tmp/audit_sid_pycache \
python3 -m audit_sid.metrics \
  --sid-assignments _gate0_artifacts/resid_real_runs/combined_resid_sanity/sid_assignments.parquet \
  --item-metadata _gate0_artifacts/resid_real_runs/normalized_resid_gaoq_1epoch/item_metadata.parquet \
  --interactions _gate0_artifacts/resid_real_runs/normalized_resid_gaoq_1epoch/interactions.parquet \
  --output-dir _gate0_artifacts/resid_real_runs/combined_resid_sanity/metrics

PYTHONPATH=src PYTHONPYCACHEPREFIX=/private/tmp/audit_sid_pycache \
python3 -m audit_sid.metrics \
  --sid-assignments _gate0_artifacts/sanity_musical/sid_assignments.parquet \
  --item-metadata _gate0_artifacts/resid_musical_normalized/item_metadata.parquet \
  --interactions _gate0_artifacts/resid_musical_normalized/interactions.parquet \
  --output-dir _gate0_artifacts/sanity_musical/metrics
```

Updated D2 output now includes:

- `mean_popularity_full_collision_items`;
- `mean_popularity_prefix_collision_items`.

## AutoDL Bundle

Latest local bundle:

```text
_gate0_artifacts/autodl_bundle/audit_sid_autodl_20260518_181327.tar.gz
```

Size: 25 MB.

## Remaining Boundary

D2 is still a collision profile, not matched counterfactual harm. D4 is still a head/mid/tail capacity profile, not downstream tail-user or tail-item harm.
