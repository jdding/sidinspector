# Case Study: ReSID vs Sanity SID Baselines

**生成时间**：2026-05-18 18:09:38 CST
**状态**：first local diagnostic case-study table generated

## Scope

This case study compares the first real ReSID/GAOQ mapping against three deterministic sanity SID baselines on ReSID `Musical_Instruments`.

Inputs:

- real mapping: `_gate0_artifacts/resid_real_runs/normalized_resid_gaoq_1epoch/sid_assignments.parquet`;
- sanity mappings: `_gate0_artifacts/sanity_musical/sid_assignments.parquet`;
- item metadata / interactions: target-only normalized ReSID dataset.

Combined output:

- `_gate0_artifacts/resid_real_runs/combined_resid_sanity/sid_assignments.parquet`;
- `_gate0_artifacts/resid_real_runs/combined_resid_sanity/metrics/`.

## Methods

| Method | Type | SID depth | Items |
|---|---|---:|---:|
| `resid_gaoq` | real ReSID/GAOQ tokenizer mapping | 3 | 23,742 |
| `sanity_category_prefix` | category-derived sanity baseline | 4 | 23,742 |
| `sanity_mod_collision_hash` | intentional high-collision negative control | 4 | 23,742 |
| `sanity_popularity_balanced` | popularity-bucket sanity baseline | 4 | 23,742 |

The metric runner now supports mixed SID depths across methods.

## D5a Deployment/Trie Summary

| Method | SID length | Unique SID | Duplicate SID rate | Prefix counts |
|---|---:|---:|---:|---|
| `resid_gaoq` | 3 | 23,742 | 0.0000 | `32;1280;23742` |
| `sanity_category_prefix` | 4 | 23,742 | 0.0000 | `30;83;313;23742` |
| `sanity_mod_collision_hash` | 4 | 256 | 0.9892 | `256;256;256;256` |
| `sanity_popularity_balanced` | 4 | 22,707 | 0.0436 | `4;1024;22707;22707` |

## D3 Semantic Proxy

| Method | Level-0 category purity proxy | Non-singleton level-0 buckets |
|---|---:|---:|
| `resid_gaoq` | 0.5669 | 32 |
| `sanity_category_prefix` | 0.6569 | 25 |
| `sanity_mod_collision_hash` | 0.0892 | 256 |
| `sanity_popularity_balanced` | 0.0840 | 4 |

Interpretation: ReSID's top-level partition is materially more category-aligned than random/popularity controls, but less category-pure than the category-prefix sanity baseline. This is a useful demo result because it shows the diagnostic is not merely measuring category labels.

## D2 Collision Profile

| Method | Full collision rate | Prefix-depth behavior |
|---|---:|---|
| `resid_gaoq` | 0.0000 | full collision disappears at depth 3; depth 1/2 prefixes are shared by all items |
| `sanity_category_prefix` | 0.0000 | full collision disappears at depth 4; intermediate prefixes are heavily shared |
| `sanity_mod_collision_hash` | 1.0000 | only 256 full SIDs for 23,742 items |
| `sanity_popularity_balanced` | 0.0860 | full SID collisions remain after depth 4 |

## Interpretation Boundary

This is a mapping-level diagnostic case study, not a downstream recommendation result. D2 is still a collision profile, not a matched counterfactual harm estimate. The current evidence is sufficient for toolkit/demo value, but not sufficient for claims about Recall/NDCG degradation.

## Next Use

Use this table as the first paper demo only if paired with:

- a Cluster A canonical SID mapping;
- or a clear limitation statement that CIKM 2026 is being de-risked around ReSID + sanity only while Cluster A remains pending.
