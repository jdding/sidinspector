# AUDIT-SID Strict Claim Audit

Timestamp: 2026-05-19 20:22:55 CST

Scope: current CIKM Resource draft in `paper/main.tex` and
`paper/sections/{1_introduction,2_toolkit,3_resource_demo,4_availability_limits}.tex`
after the table-structure polish pass.

## Verdict

PASS with conservative wording retained.

The current draft remains scoped to a CIKM 2026 Resource Track artifact-audit
claim. It does not present AUDIT-SID as a new tokenizer, a downstream
Recall/NDCG leaderboard, a faithful end-to-end TIGER/GRID/ReSID reproduction,
or an industrial serving-latency study.

## Quantitative Claims Checked

| Claim location | Paper claim | Evidence | Status |
|---|---:|---:|---|
| Abstract / Table 2 caption | Musical same-item case uses 23,742 items | `paper_assets/tables/table2_musical_diagnostic.csv`: both rows `items=23742.0` | exact/rounding ok |
| Abstract / Table 2 | GRID feature-text has 3,749 unique full SIDs | same CSV: `unique_sid=3749.0` | exact |
| Abstract / Table 2 | GRID feature-text full-collision rate is 0.9769 | same CSV: `full_collision_rate=0.9769` | exact |
| Table 2 | GRID feature-text D3 recovery is 0.0552 | same CSV: `D3 L1 collab=0.0552` | exact |
| Table 2 | GRID feature-text D4 tail is 0.3695 | same CSV: `D4 tail=0.3695` | exact |
| Table 2 | GRID feature-text D5a prefix counts are `64/3440/3749` | same CSV: `prefix_counts=64;3440;3749` | exact formatting conversion |
| Table 2 | ReSID bounded has 23,742 unique full SIDs | same CSV: `unique_sid=23742.0` | exact |
| Abstract / Table 2 | ReSID bounded full-collision rate is 0.0000 | same CSV: `full_collision_rate=0.0` | exact/format ok |
| Table 2 | ReSID bounded D3 recovery is 0.1535 | same CSV: `D3 L1 collab=0.1535` | exact |
| Table 2 | ReSID bounded D4 tail is 1.0000 | same CSV: `D4 tail=1.0` | exact/format ok |
| Table 2 | ReSID bounded D5a prefix counts are `32/1280/23742` | same CSV: `prefix_counts=32;1280;23742` | exact formatting conversion |
| Table 3 / Section 3 | GRID collided pairs have 3.86x co-occurrence lift | `paper_assets/tables/table8_qualified_collision_probe.csv`: `3.8631578947368426` | rounded ok |
| Table 3 / Section 3 | collision-heavy hash control has 1.19x co-occurrence lift | same CSV: `1.1851851851851851` | rounded ok |
| Table 3 / Section 3 | width-24 head-reserved controller has tail unique ratio 0.028 | `paper_assets/tables/table9_capacity_budget_sweep.csv`: `0.0281902844198338` | rounded ok |

## Scope Claims Checked

| Claim | Current wording | Audit status |
|---|---|---|
| Not a leaderboard | Abstract, Table 2 caption, and Section 3 explicitly say the work is not a downstream leaderboard | ok |
| Not faithful TIGER/GRID reproduction | Table 1, Table 2 caption, Section 3, and Section 4 state GRID Musical is controlled feature-text, not raw-text TIGER/GRID | ok |
| ReSID bounded export | Abstract and Table 2 label ReSID as bounded/exported mapping evidence | ok |
| CARD not claimed | Table 1 and Section 4 say no faithful CARD result is reported | ok |
| Controller boundary | Abstract, Introduction, Section 3, and Section 4 frame controller rows as method-inspired stressors, not named-tokenizer coverage | ok |
| D2 limit | Section 2 and Section 4 say D2 has a bounded interaction-qualified controller, but not causal harm | ok |
| D3 limit | Section 2 and Section 4 say D3 is a collaborative diagnostic proxy, not proven monotonic with Recall/NDCG | ok |
| D5a limit | Section 2, Section 3, and Section 4 say D5a is structural prefix/cost evidence, not real serving latency | ok |
| D7 limit | Fig. 1, Section 2, and Table 1 say D7 needs generator outputs or beam traces and is not current evidence | ok |
| Online / industrial impact | Table 1 and Section 4 explicitly say no production serving or online-impact claim | ok |

## Remaining Submission Risks

1. The local ACM draft is still anonymous. If CIKM 2026 Resource submission is
   single-blind, final author and affiliation metadata must be inserted before
   submission.
2. The artifact should be frozen through the `audit-sid-cikm-resource-v0.1` tag
   and verified from a clean checkout before final submission.
3. The evidence still supports a resource-demo claim, not a full system-quality
   claim. Do not rewrite the abstract toward benchmark language.
4. Controller rows should stay out of Table 1 method coverage unless they are
   explicitly labeled as controlled stressors in repository tables.

## Page / Figure / Table State

The current compile produces a 5-page PDF: body text fills through page 4,
while references and the GenAI Usage Disclosure are outside the four-page body.
Fig. 1 is a generated vector PDF. Table 1 is a facet-by-diagnostic coverage matrix,
Table 2 is the same-item Musical artifact-profile table with D5a prefix counts,
Table 3 is the controlled-stressor signal table, and Table 4 is a reviewer
artifact checklist tied to clean-checkout verification.
