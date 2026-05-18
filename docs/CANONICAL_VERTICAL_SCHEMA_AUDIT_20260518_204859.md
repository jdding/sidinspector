# Canonical Vertical Schema Audit

**Time**: 2026-05-18 20:48:59 CST
**Status**: `Sports_and_Outdoors` and `Beauty_and_Personal_Care` downloaded and schema-audited.
**Storage**: primary local storage moved to `/Volumes/TU280Pro/Research/DataSet/ReSID-dataset`; workspace path `_gate0_repos/ReSID-dataset` is a symlink.

## Decision

`Musical_Instruments` remains the quick-smoke dataset. Paper-facing Gate 0 must include at least `Sports_and_Outdoors`. `Beauty_and_Personal_Care` is now available as an optional second canonical vertical.

## Dataset Inventory

| Category | Source format | Local storage | Size |
|---|---|---|---:|
| `Musical_Instruments` | ReSID processed Amazon-2023 leave-one-out parquet | external ReSID dataset root via symlink | 12M |
| `Sports_and_Outdoors` | ReSID processed Amazon-2023 leave-one-out parquet | external ReSID dataset root via symlink | 87M |
| `Beauty_and_Personal_Care` | ReSID processed Amazon-2023 leave-one-out parquet | external ReSID dataset root via symlink | 149M |

The external raw Amazon-2023 folder `/Volumes/TU280Pro/Research/DataSet/amazon_2023` contains raw `.jsonl.gz` and `meta_*.jsonl.gz` files, including `All_Beauty` and `Video_Games`, but not the ReSID-processed parquet layout needed for immediate Gate 0.

## Schema Results

| Category | Items | `store_id` unique | `cate1_id` unique | `cate2_id` unique | `cate3_id` unique |
|---|---:|---:|---:|---:|---:|
| `Sports_and_Outdoors` | 151,411 | 33,948 | 200 | 269 | 664 |
| `Beauty_and_Personal_Care` | 193,383 | 40,058 | 53 | 110 | 351 |

## Interaction Coverage

| Category | Split | Rows | Users | Unique targets | History length min / median / max | Item coverage | Missing from item metadata |
|---|---|---:|---:|---:|---|---:|---:|
| `Sports_and_Outdoors` | train | 2,108,189 | 409,309 | 151,016 | 1 / 3 / 34 | 151,411 | 0 |
| `Sports_and_Outdoors` | valid | 408,489 | 408,489 | 104,847 | 2 / 4 / 33 | 150,997 | 0 |
| `Sports_and_Outdoors` | test | 407,783 | 407,783 | 99,408 | 3 / 5 / 34 | 151,354 | 0 |
| `Beauty_and_Personal_Care` | train | 3,650,871 | 712,259 | 192,868 | 1 / 3 / 37 | 193,383 | 0 |
| `Beauty_and_Personal_Care` | valid | 711,346 | 711,346 | 130,311 | 2 / 4 / 36 | 192,628 | 0 |
| `Beauty_and_Personal_Care` | test | 710,662 | 710,662 | 124,628 | 3 / 5 / 37 | 193,136 | 0 |

## Gate Implication

- `Sports_and_Outdoors` passes the dataset support gate and should be the first canonical vertical in AutoDL.
- `Beauty_and_Personal_Care` also passes schema/coverage checks, but is larger and should be used only after the Sports run is stable.
- Both categories have complete item-feature coverage and category metadata for D2/D3/D4.
- `prepare_bundle.sh` now dereferences the ReSID dataset symlink so AutoDL bundles include the actual parquet shards, not a local-only symlink.

## Next Execution Order

1. Keep `QUEUE_MODE=quick` as Musical-only remote smoke.
2. Run `QUEUE_MODE=canonical` for `Sports_and_Outdoors` after quick succeeds.
3. Do not run `robust`, `sweep`, or `quality` until canonical Sports passes and the CARD/Cluster-A blocker is resolved or explicitly scoped as ReSID-only debugging.
