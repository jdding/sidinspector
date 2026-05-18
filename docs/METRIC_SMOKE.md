# Metric Smoke: D1-D5a on Sanity SID Baselines

**生成时间**：2026-05-18 17:30:38 CST
**状态**：D1-D5a mapping-first metric runner completed on sanity baselines

## Command

```bash
PYTHONPATH=src PYTHONPYCACHEPREFIX=/private/tmp/audit_sid_pycache \
python3 -m audit_sid.metrics \
  --sid-assignments _gate0_artifacts/sanity_musical/sid_assignments.parquet \
  --item-metadata _gate0_artifacts/resid_musical_normalized/item_metadata.parquet \
  --interactions _gate0_artifacts/resid_musical_normalized/interactions.parquet \
  --output-dir _gate0_artifacts/sanity_musical/metrics
```

## Outputs

Generated outputs are under ignored `_gate0_artifacts/` and are not committed.

| Diagnostic | Output | Smoke result |
|---|---|---|
| D1 utilization | `d1_utilization.csv` | per-level entropy, Gini, unique-code count emitted for all sanity methods |
| Coverage | `coverage_report.csv` | item-id coverage and uniqueness checks emitted before metrics |
| D2 collision | `d2_collision.csv` | full-SID and prefix-depth collision summaries emitted |
| D3 semantic alignment | `d3_alignment.csv` | level-0 category-purity proxy emitted |
| D4 head-tail capacity | `d4_head_tail.csv` | popularity bucket capacity and entropy summaries emitted |
| D5a deployment cost | `d5a_deployment_cost.csv` | SID length, unique SID count, duplicate rate, and prefix trie counts emitted |

## Sanity Checks

The smoke run distinguishes the three sanity baselines in expected directions:

| Method | D2 full collision rate | D3 level-0 category purity | D5a duplicate SID rate | D5a prefix counts |
|---|---:|---:|---:|---|
| `sanity_category_prefix` | 0.0000 | 0.6569 | 0.0000 | `30;83;313;23742` |
| `sanity_popularity_balanced` | 0.0840 | 0.0840 | 0.0426 | `4;1024;22730;22730` |
| `sanity_mod_collision_hash` | 1.0000 | 0.0892 | 0.9892 | `256;256;256;256` |

This is enough to validate the metric plumbing and basic diagnostic sensitivity before running on a real tokenizer mapping.

Update: after code review, metrics now group by `dataset, method`, validate item-id coverage before scoring, use train target events for popularity, and emit collision profiles for every prefix depth.

## Interpretation Boundary

This is not yet a Gate 0 pass. The runner has only been validated on deterministic sanity baselines. The unresolved Gate 0 blocker remains a real ReSID/GAOQ or GRID/RQ-VAE item-to-SID export that can be normalized into `src/audit_sid/interface.py`.

## Notes

PyArrow emitted harmless sandbox-related `sysctlbyname` warnings while reading parquet files. The metric command completed successfully and all five output tables were generated.
