# Qualified Collision Probe

Timestamp: 2026-05-19 19:01:39 CST

Status: **LOCAL_CONTROLLER_DONE**.

Role: first method-inspired controller in `docs/CONTROLLED_STRESSOR_SELECTION.md`.
It strengthens D2 from a raw collision profile toward an
interaction-qualified collision-risk diagnostic, without claiming causal
downstream harm or reproducing QuaSID.

## Command

```bash
python3 tools/autodl_audit_sid/run_qualified_collision_probe.py \
  --sid-assignments _gate0_artifacts/resid_real_runs/normalized_resid_gaoq_1epoch/sid_assignments.parquet \
  --sid-assignments _gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/grid_export/normalized/sid_assignments.parquet \
  --sid-assignments _gate0_artifacts/sanity_musical/sid_assignments.parquet \
  --item-metadata _gate0_artifacts/resid_musical_normalized/item_metadata.parquet \
  --interactions _gate0_artifacts/resid_musical_normalized/interactions.parquet \
  --output-dir _gate0_artifacts/controllers/qualified_collision_probe_20260519_1901 \
  --max-collision-pairs 30000 \
  --max-pair-events 800000 \
  --max-user-items 80 \
  --popularity-bins 10 \
  --seed 42
```

Tracked public summary:

- `paper_assets/tables/table8_qualified_collision_probe.csv`;
- `paper_assets/tables/table8_qualified_collision_probe.md`.

Ignored local details:

- `_gate0_artifacts/controllers/qualified_collision_probe_20260519_1901/qualified_collision_pairs.csv`;
- `_gate0_artifacts/controllers/qualified_collision_probe_20260519_1901/qualified_collision_summary.csv`;
- `_gate0_artifacts/controllers/qualified_collision_probe_20260519_1901/qualified_collision_manifest.json`.

## Summary

| Method | Full collision groups | Collision pairs possible | Collision pair sample | Matched sample | Collision share-user rate | Matched share-user rate | Lift |
|---|---:|---:|---:|---:|---:|---:|---:|
| GRID feature-text | 3,200 | 135,528 | 30,000 | 30,000 | 0.012233 | 0.003167 | 3.863 |
| ReSID GAOQ | 0 | 0 | 0 | 0 | 0.000000 | 0.000000 | n/a |
| category-prefix sanity | 0 | 0 | 0 | 0 | 0.000000 | 0.000000 | n/a |
| mod-collision hash sanity | 256 | 1,089,096 | 30,000 | 30,000 | 0.003200 | 0.002700 | 1.185 |
| popularity-balanced sanity | 1,006 | 1,066 | 1,066 | 1,066 | 0.009381 | 0.004690 | 2.000 |

## Interpretation

The controller produces a useful D2b signal.

- The controlled GRID feature-text row has many full-SID collisions, but the
  more important result is that collided pairs are about `3.86x` more likely
  to appear as train co-occurrence pairs than popularity-matched non-collision
  pairs. This supports the claim that D2 can move beyond raw collision counts
  toward interaction-qualified collision risk.
- The mod-collision hash sanity row has far more possible collision pairs, but
  its interaction-qualified lift is only `1.19x`. This is the key sanity check:
  collision volume alone is not the same as interaction-qualified collision
  risk.
- ReSID GAOQ and category-prefix sanity have no full-SID collisions in this
  artifact, so D2b is not applicable for them. This should be reported as
  `no_full_sid_collisions`, not as superiority.

Safe paper claim:

> A method-inspired collision controller separates raw collision volume from
> interaction-qualified collision risk: the GRID feature-text row shows higher
> co-occurrence lift among collided pairs than a collision-heavy hash control.

Do not claim:

- causal downstream harm;
- QuaSID reproduction;
- that zero full collision implies better recommendation quality.

## Next Step

Proceed to `capacity_budget_sweep`, the second method-inspired controller. It
should reuse the same Musical item universe and run D1/D2/D4/D5a over
controlled fixed-depth codebook budgets.
