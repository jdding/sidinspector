# SIDInspector Strict Claim Audit

Timestamp: 2026-05-20 19:40:00 CST

Scope: the CIKM Resource manuscript submitted outside this reviewer artifact,
cross-checked against the frozen evidence tables shipped here after integrating
the AutoDL matched-capacity GRID row (`GRID ft-cap`), B6 fixed-reranker
validation, B7 Sports GRID third-vertical evidence, and the R3-delta wording
fixes.

## Verdict

PASS with two caveats retained.

The current draft truthfully reports the matched-capacity result, B6
fixed-reranker validation, and B7 Sports GRID third-vertical row while keeping
their interpretation at artifact-profile scope. It does not present
SIDInspector as a tokenizer, a benchmark/leaderboard, a faithful end-to-end
TIGER/GRID/ReSID reproduction, or a trained-generator Recall/NDCG predictor.
The `GRID ft-cap` row reduces the R3 W2 capacity-confound risk, and B6 reduces
the W3 concern by adding fixed-reranker ranking context without claiming
downstream generator validation.

Post-R3-delta update: the paper now explicitly states that `GRID ft-cap` is not
a full item-unique leaf match and that additional capacity may reduce aliasing
further. It also states that the current demonstration uses two controlled
public export paths rather than broad tokenizer coverage. These edits are
claim-safe and align with the external R3-delta review's remaining W1/W2
caveats.

The remaining caveats are still material for review:

1. Named-method coverage remains thin: GRID/RQ-KMeans feature-text and bounded
   ReSID/GAOQ are worked examples, not broad method coverage.
2. D3 now has bounded fixed-reranker context, but remains a diagnostic
   neighborhood-alignment signal rather than a validated monotonic proxy for
   trained-generator Recall@K or NDCG.

## Quantitative Claims Checked

| Claim location | Paper claim | Evidence | Status |
|---|---:|---:|---|
| Abstract / Table 2 | Musical worked example uses 23,742 items | `paper_assets/tables/table2_musical_diagnostic.csv`: all main rows `items=23742.0` | exact/rounding ok |
| Abstract / Table 2 | GRID feature-text has 3,749 unique full codes | same CSV: `unique_sid=3749.0` | exact |
| Abstract / Table 2 | GRID feature-text full-code aliasing rate is 0.9769 | same CSV: `full_collision_rate=0.9769` | exact |
| Abstract / Table 2 | GRID feature-text full-code aliasing is stable at 0.9751--0.9769 across three seeds | `paper_assets/tables/table7_grid_musical_3seed.csv`: seeds 42/43/44 are 0.9769/0.9751/0.9756 | exact range |
| Table 2 | GRID feature-text mean unique is 3,857±112 | table7 seeds 3749/3972/3849, mean 3856.7, sample stdev 111.5 | rounded ok |
| Table 2 | GRID feature-text D3 is .0519±.0037 | table7 seeds 0.0552/0.0479/0.0526, mean 0.0519, sample stdev 0.0037 | rounded ok |
| Table 2 | GRID feature-text D4 tail is .377±.008 | table7 seeds 0.3695/0.3852/0.3773, mean 0.3773, sample stdev 0.0079 | rounded ok |
| Abstract / Table 2 | GRID ft-cap reduces aliasing to 0.7785 | `table2_musical_diagnostic.csv`: `full_collision_rate=0.7785`; raw D2 `0.778452` | rounded ok |
| Table 2 | GRID ft-cap has 9,874 unique full SIDs | same CSV and D5 raw file: `unique_sid=9874` | exact |
| Table 2 | GRID ft-cap D3 L1 is .0796 | same CSV: `D3 L1 collab=0.0796`; raw weighted D3 `0.07959536124184992` | rounded ok |
| Table 2 | GRID ft-cap D4 tail is .6391 | same CSV: `D4 tail=0.6391`; raw D4 `0.639064` | rounded ok |
| Table 2 | GRID ft-cap D5 prefixes are `32/9300/9874` | same CSV: `prefix_counts=32;9300;9874` | formatting conversion ok |
| Table 2 | ReSID bounded has 23,742 unique full SIDs | same CSV: `unique_sid=23742.0` | exact |
| Abstract / Table 2 | ReSID bounded is aliasing-free in its exported mapping | same CSV: `full_collision_rate=0.0` | exact/format ok |
| Table 2 | ReSID bounded D3 recovery is 0.1535 | same CSV: `D3 L1 collab=0.1535` | exact |
| Table 2 | ReSID bounded D4 tail is 1.0000 | same CSV: `D4 tail=1.0` | exact/format ok |
| Table 2 | ReSID bounded D5 prefix counts are `32/1280/23742` | same CSV: `prefix_counts=32;1280;23742` | exact formatting conversion |
| Table 3 / Section 4 | qualified aliases have 3.86x co-occurrence lift | `paper_assets/tables/table8_qualified_collision_probe.csv`: `3.8631578947368426` | rounded ok |
| Table 3 / Section 4 | hash aliases have 1.19x co-occurrence lift | same CSV: `1.1851851851851851` | rounded ok |
| Table 3 / Section 4 | capacity probe head unique is 1.000 and tail unique is 0.028 | `paper_assets/tables/table9_capacity_budget_sweep.csv`: head `1.0`, tail `0.0281902844198338` | rounded ok |
| Table 3 / Section 4 | variable-depth max vs active prefixes are 12,010 and 7,914 | `paper_assets/tables/table10_variable_depth_cost_probe.csv`: `standard_prefix_counts=64;4096;12010;19924`, `effective_prefix_counts=64;4096;7914;7914` | exact extracted values |
| Section 4 | All_Beauty 20k panel repeats the D3 inversion: category-prefix 0.968 vs GRID 0.081 | `paper_assets/tables/table13_all_beauty_vertical_d3.csv`: seed42 `sanity_category_prefix=0.968438`, `grid_official_rqkmeans_all_beauty_20k_seed42=0.081147`; seeds 43/44 GRID are `0.087240/0.089778`; metadata marked coarse fallback | rounded ok |
| Section 4 / B6 | D3 has Spearman 0.943 with candidate recall and 0.886 with fixed-reranker Recall@20 across six rows | `_gate0_artifacts/d3_ranking_validation/musical_fixed_rerank_5000_20260520/d3_ranking_validation_correlations.csv`: `0.942857142857143` and `0.8857142857142858`, `rows=6`; frozen in `paper_assets/tables/table11_d3_ranking_validation.csv` | rounded ok |
| Section 4 / B6 | B6 uses a 5,000-user Musical fixed-reranker check | `paper_assets/tables/table11_d3_ranking_validation.csv`: all depth-1 co-occurrence rows have `targets_evaluated=9986` under the 5,000-user bound | scope ok |
| Section 4 / B7 | Sports 20k GRID export has complete joins, D3-L1 0.055, duplicate-SID rate 0.592 | `paper_assets/tables/table12_sports_grid_vertical.csv`: 20k row has `metadata_without_sid=0`, `interaction_without_sid=0`, `D3 L1 collab=0.054982`, `duplicate_sid_rate=0.59175` | rounded ok |
| Section 4 / B7 | Sports 20k GRID row has 8,165 unique full SIDs and D5 prefixes `128/7986/8165` | same CSV: `unique_sid=8165`, `prefix_counts=128;7986;8165` | exact/formatting ok |

## Scope Claims Checked

| Claim | Current wording | Audit status |
|---|---|---|
| Not a leaderboard | Abstract and Section 5 say the resource is not a tokenizer or leaderboard and the Musical case study is not a method ranking | ok |
| Not faithful TIGER/GRID reproduction | Table 1, Section 4, and Section 5 label GRID as controlled feature-text / not raw-text TIGER | ok |
| Matched-capacity row scope | Section 4 labels `GRID ft-cap` as capacity-matched / same feature-text path; no faithful reproduction claim | ok |
| ReSID bounded export | Table 1 and Section 5 label the main ReSID evidence as bounded Musical export | ok |
| Structural floor | Table 2 caption and Section 4 state item-unique rows force D2=0 and D4 tail=1.0 | ok |
| D2 limit | Section 3 and Section 5 say D2 is a profile plus interaction-qualified mechanism probe, not causal harm | ok |
| D3 limit | Section 4 and Section 5 say D3 is a diagnostic warning/triage signal; B6 is explicitly fixed-reranker context, not trained-generator validation | ok |
| D5 limit | Table 2 caption, Section 3, and Section 5 say D5 is structural cost, not measured latency | ok |
| D6/D7 limit | Fig. 1, Section 2, Section 3, and Section 5 scope D6 as optional refresh-pair evidence and D7 as generator-trace hook only | ok |
| Controlled probes | Table 1/3 and Section 4 keep probes outside named-method coverage | ok |

## Issues Fixed During This Audit

1. `GRID ft-cap` D3 was displayed as `.0795` in the manuscript Table 2, while the paper-facing CSV and raw weighted D3 value round to `.0796`. Fixed to `.0796` in Table 2 and the D3 range sentence.
2. The abstract previously did not mention the matched-capacity ablation. It now states that the GRID capacity-matched row reduces aliasing to 0.7785 but does not eliminate it.
3. Active naming was rechecked after the earlier working-name drift. Active paper/artifact files now use `SIDInspector`; older timestamped snapshots are not active submission inputs.
4. R3-delta wording fixes added the All_Beauty D3 replication sentence and the
   two-controlled-export limitation. Both have direct evidence and avoid
   downstream ranking claims.
5. B6/B7 code-review hardening added frozen Table 11/Table 12 CSVs and expanded
   the verifier so the paper cannot pass clean-checkout verification if these
   new numbers drift or disappear.
6. B6 wording was tightened from generic `Recall@20/NDCG@20` to
   `fixed-reranker Recall@20/NDCG@20` where the scope could otherwise be read as
   trained-generator evaluation.

## Verification

- The submitted manuscript PDF compiled successfully during the final paper pass.
- PDF title: `SIDInspector: A Mapping-First Diagnostic Resource for Semantic-ID Tokenizers`.
- `tools/verify_paper_artifact.py` passes and checks the `GRID ft-cap`,
  B4 All_Beauty D3, B6 fixed-reranker, and B7 Sports GRID rows.
- `python3 -m unittest discover -s tests`: 24 passed.
- `git diff --check`: pass.
- Log scan finds no undefined references/citations, no invalid math-mode warnings, and no overfull boxes.

## Remaining Review Risks

1. W1 remains: two named worked-example paths plus controls/probes are still closer to a resource demo than a broad coverage resource.
2. W3 is reduced but not eliminated: D3 now has fixed-reranker context, but the
   paper still does not validate it against trained-generator Recall/NDCG.
3. The artifact tag/package must be refreshed if `GRID ft-cap`, B6, and B7
   should be public-review reproducible rather than local provenance only.
4. Final single-blind author metadata still needs insertion before Resource submission if the track requires author information.
