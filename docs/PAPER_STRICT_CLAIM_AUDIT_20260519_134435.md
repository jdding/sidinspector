# AUDIT-SID Strict Claim Audit

Timestamp: 2026-05-19 13:44:35 CST

Scope: current CIKM Resource draft in `paper/main.tex` and
`paper/sections/{1_introduction,2_toolkit,3_resource_demo,4_availability_limits}.tex`.

## Verdict

PASS with conservative wording retained.

The current draft no longer reads as a SID leaderboard or as a faithful
end-to-end reproduction of TIGER, ReSID, CARD, or downstream generative
recommendation. The main paper claims are scoped to an artifact-audit resource:
mapping contract, D1-D5a diagnostics, optional D6 churn, and future D7 only when
generator outputs are available.

## Quantitative Claims Checked

| Claim location | Paper claim | Evidence | Status |
|---|---:|---:|---|
| Abstract / Table 2 | Musical same-item case uses 23,742 items | `paper_assets/tables/table2_musical_diagnostic.csv`: both rows `items=23742.0` | exact/rounding ok |
| Abstract / Table 2 | GRID feature-text has 3,749 unique full SIDs | same CSV: `unique_sid=3749.0` | exact |
| Abstract / Table 2 | GRID feature-text full-collision rate is 0.9769 | same CSV: `full_collision_rate=0.9769` | exact |
| Table 2 | GRID feature-text D3 L1 is 0.0552 | same CSV: `D3 L1 collab=0.0552` | exact |
| Table 2 | GRID feature-text D4 tail is 0.3695 | same CSV: `D4 tail=0.3695` | exact |
| Table 2 | ReSID bounded has 23,742 unique full SIDs | same CSV: `unique_sid=23742.0` | exact |
| Abstract / Table 2 | ReSID bounded full-collision rate is 0.0000 | same CSV: `full_collision_rate=0.0` | exact/format ok |
| Table 2 | ReSID bounded D3 L1 is 0.1535 | same CSV: `D3 L1 collab=0.1535` | exact |
| Table 2 | ReSID bounded D4 tail is 1.0000 | same CSV: `D4 tail=1.0` | exact/format ok |

## Scope Claims Checked

| Claim | Current wording | Audit status |
|---|---|---|
| Not a leaderboard | Abstract, Table 2 caption, and §3 explicitly say the work is not a downstream leaderboard | ok |
| Not faithful TIGER reproduction | Table 1, Table 2 caption, §3, and §4 state GRID Musical is controlled feature-text, not raw-text TIGER | ok |
| ReSID bounded export | Abstract and Table 2 label ReSID as bounded/exported mapping evidence | ok |
| CARD not claimed | Table 1 and §4 say no faithful CARD result is reported | ok |
| D2 limit | §2 and §4 say D2 is collision profile, not causal harm | ok |
| D3 limit | §2 and §4 say D3 is a collaborative diagnostic proxy, not proven monotonic with Recall/NDCG | ok |
| D5a limit | §2 and §4 say D5a is structural cost, not real serving latency | ok |
| D7 limit | Fig. 1, §2, and Table 1 say D7 needs generator outputs or beam traces and is not current evidence | ok |
| Online / industrial impact | Table 1 and §4 explicitly say no production serving or online-impact claim | ok |

## Remaining Wording Risks

1. `public Amazon resource demos` in the abstract is acceptable but should stay
   tied to `resource demos`; do not rewrite it as public benchmark evidence.
2. `collision-free under its exported mapping` is numerically correct, but it
   should remain tied to the bounded exported mapping rather than ReSID as a
   full system.
3. Table 1 is now literature-aware. Do not treat B2/B3/B4 rows as reproduced
   methods in any future abstract or introduction edit.

## Page / Figure / Table State

The current compile produces a 5-page PDF: body text fills through page 4, while
references and the GenAI Usage Disclosure extend onto page 5. This matches the
current writing goal of using the four-page body budget while keeping
references/disclosure outside the core body. Fig. 1 is now a generated vector
PDF from `tools/paper_figures/generate_audit_sid_pipeline.py`, not a temporary
LaTeX text box.
