# Case Study: ReSID vs Sanity SID Baselines

**生成时间**：2026-05-19 03:18:36 CST
**状态**：D1-D5a/D3v2 case-study table generated

## Scope

This case study compares the first real ReSID/GAOQ mapping against three
deterministic sanity SID baselines on ReSID processed Amazon-2023
`Musical_Instruments`.

This is the clean same-dataset diagnostic case study for the conditional Gate
0A resource-demo route. It is not a GRID-vs-ReSID method leaderboard.

Inputs:

- real mapping: `_gate0_artifacts/resid_real_runs/normalized_resid_gaoq_1epoch/sid_assignments.parquet`;
- sanity mappings: `_gate0_artifacts/sanity_musical/sid_assignments.parquet`;
- combined mapping: `_gate0_artifacts/resid_real_runs/combined_resid_sanity/sid_assignments.parquet`;
- item metadata/interactions: `_gate0_artifacts/resid_real_runs/normalized_resid_gaoq_1epoch/`.

Metric output:

- `_gate0_artifacts/resid_real_runs/combined_resid_sanity/metrics_d3v2/`.

Generated summary:

```bash
python3 tools/autodl_audit_sid/summarize_case_study.py \
  --metrics-dir _gate0_artifacts/resid_real_runs/combined_resid_sanity/metrics_d3v2 \
  --output-csv _gate0_artifacts/case_study/resid_sanity_d3v2_summary.csv \
  --output-md _gate0_artifacts/case_study/resid_sanity_d3v2_summary.md
```

## Methods

| Method | Type | SID depth | Items |
|---|---|---:|---:|
| `resid_gaoq` | real ReSID/GAOQ tokenizer mapping | 3 | 23,742 |
| `sanity_category_prefix` | category-derived sanity baseline | 4 | 23,742 |
| `sanity_mod_collision_hash` | intentional high-collision negative control | 4 | 23,742 |
| `sanity_popularity_balanced` | popularity-bucket sanity baseline | 4 | 23,742 |

## Compact Diagnostic Table

| Method | D2 full collision | D3 depth-1 collab recall | D3 depth-2 collab recall | D3 category purity | D4 head unique | D4 tail unique | D5 duplicate SID |
|---|---:|---:|---:|---:|---:|---:|---:|
| `resid_gaoq` | 0.0000 | 0.1535 | 0.0175 | 0.5669 | 1.0000 | 1.0000 | 0.0000 |
| `sanity_category_prefix` | 0.0000 | 0.4470 | 0.3095 | 0.6569 | 1.0000 | 1.0000 | 0.0000 |
| `sanity_mod_collision_hash` | 1.0000 | 0.0037 | 0.0037 | 0.0892 | 0.0324 | 0.0322 | 0.9892 |
| `sanity_popularity_balanced` | 0.0860 | 0.3026 | 0.0011 | 0.0840 | 0.9639 | 0.9619 | 0.0436 |

## Diagnostic Reading

This case study gives a non-D1-only story:

- D2 and D5a catch the intentionally bad collision baseline: only 256 unique
  full SIDs for 23,742 items and duplicate SID rate 0.9892.
- D3v2 separates collaborative neighborhood alignment from category purity.
  Category-prefix has the strongest depth-1 co-occurrence alignment because it
  hard-codes taxonomy, but that is a sanity upper-control rather than learned
  tokenizer evidence.
- ReSID GAOQ has zero full collisions and perfect head/mid/tail unique-SID
  ratios, but weaker collaborative-prefix recall than category-prefix. That is
  a capacity-vs-neighborhood tradeoff, not a simple win/loss.
- Popularity-balanced IDs have moderate collision and high depth-1 collaborative
  recall, but depth-2 recall collapses. This shows why prefix-depth diagnostics
  matter for deployment-cost and beam/search behavior.

## Paper Boundary

Safe wording:

> AUDIT-SID exposes different artifact failure modes: collision collapse,
> capacity allocation, metadata/collaborative grouping, and prefix-depth cost.

Unsafe wording:

- ReSID is better/worse than GRID on recommendation quality;
- category-prefix is a tokenizer method;
- D2 is causal downstream collision harm;
- this bounded 1-epoch ReSID export is final ReSID quality.
