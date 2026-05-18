# Dataset Schema Audit: ReSID Musical Instruments

**生成时间**：2026-05-18 17:10:11 CST
**状态**：primary dataset schema pass；ready for adapter/export smoke
**数据源**：`PIIR/ReSID-dataset` on Hugging Face, revision `b508d21`

## Scope

只拉取 `Musical_Instruments/leave_one_out/dataset/**` 的 LFS 文件，不下载全量 924MB 数据集。实际下载约 12.4MB parquet 数据，用于列名、行数、join key、interaction coverage 检查。

Local path:

`_gate0_repos/ReSID-dataset/Musical_Instruments/leave_one_out/dataset`

## File Layout

| Subpath | Files | Columns | Rows |
|---|---:|---|---:|
| `item_feature/` | 1 parquet | `item_id`, `store_id`, `cate1_id`, `cate2_id`, `cate3_id` | 23,742 |
| `train/` | 2 parquet | `user_id`, `history`, `target`, `timestamp` | 318,612 |
| `valid/` | 2 parquet | `user_id`, `history`, `target`, `timestamp` | 57,296 |
| `test/` | 2 parquet | `user_id`, `history`, `target`, `timestamp` | 57,256 |
| `item_feature_explain.json` | 1 json | feature metadata | 5 feature definitions |

## Feature Dictionary

From `item_feature_explain.json`:

| Feature | id_num | Observed unique count |
|---|---:|---:|
| `item_id` | 23,743 | 23,742 |
| `store_id` | 4,095 | 4,094 |
| `cate1_id` | 31 | 30 |
| `cate2_id` | 82 | 81 |
| `cate3_id` | 289 | 288 |

The `id_num` values include zero/padding conventions. Actual item IDs are contiguous from 1 to 23,742.

## Interaction Coverage

| Split | Rows | Users | Unique targets | History length min / median / max | Unique item coverage | Missing from `item_feature` |
|---|---:|---:|---:|---|---:|---:|
| train | 318,612 | 57,359 | 23,693 | 1 / 4 / 34 | 23,742 | 0 |
| valid | 57,296 | 57,296 | 16,431 | 2 / 5 / 34 | 23,711 | 0 |
| test | 57,256 | 57,256 | 16,111 | 3 / 6 / 35 | 23,739 | 0 |

## AUDIT-SID Interface Mapping

| AUDIT-SID table | Source | Status |
|---|---|---|
| `item_metadata` | `item_feature` parquet | PASS |
| `interactions` | expand `history` plus `target` from train/valid/test | PASS |
| popularity buckets | count item occurrences in `history` and `target` | PASS |
| category metadata | `cate1_id`, `cate2_id`, `cate3_id` | PASS |
| `sid_assignments` | ReSID GAOQ output `item_code_mapping.parquet`; GRID `cluster_ids`; sanity generator | PENDING export smoke |
| `generator_outputs` | not required for v0; D5b optional | DEFER |

## Diagnostic Support

| Diagnostic | Dataset support | Notes |
|---|---|---|
| D1 utilization | yes | needs `sid_assignments` only |
| D2 collision harm | yes | history/target interactions and category controls available |
| D3 semantic-collaborative alignment | yes | co-occurrence reference + category purity available; no SASRec required |
| D4 head-tail capacity | yes | popularity buckets computable from interactions |
| D5a deployment-cost proxy | yes | SID trie statistics from mapping |
| D5b generator cost | deferred | needs generated candidates |
| D6 drift | no for v0 | static leave-one-out dataset |

## Decision

`Musical_Instruments` passes Gate 1 schema requirements for CIKM v0.

This dataset is small enough for fast adapter development, has complete join coverage between interactions and item features, and exposes categorical side information sufficient for D2/D3/D4 controls.

## Next Step

Implement normalized adapters:

- `src/audit_sid/adapters/resid.py` for ReSID dataset and GAOQ mapping;
- `src/audit_sid/adapters/grid.py` for GRID merged prediction outputs;
- sanity baseline generator after interaction popularity is loaded.

Then run bounded export smoke:

1. convert ReSID dataset to normalized `item_metadata` and `interactions`;
2. either export one real ReSID/GAOQ SID mapping or record missing checkpoint/training blocker;
3. generate sanity `sid_assignments` from `item_id` / popularity / category as the first fully normalized artifact.
