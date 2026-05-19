# AUDIT-SID Experiment Plan Full Audit

Timestamp: 2026-05-19 23:08:54 CST

Auditor: Codex local plan-to-evidence audit, using the current worktree. This is
not an independent external simulated review.

Target: CIKM 2026 Resource Track, conservative resource-demo framing.

## Verdict

The current experiment plan is **closed for the CIKM 2026 Resource v0 evidence
package**.

This means all experiments that are required by the active plan have either:

1. produced usable evidence for the v0 paper and artifact package;
2. been explicitly closed negative with documented evidence; or
3. been reclassified as future/supplementary work outside the current claim.

It does **not** mean AUDIT-SID is a full SID benchmark, a downstream
recommender-quality evaluation, or a complete survey of all named tokenizers.
The safe claim is a resource/toolkit claim: AUDIT-SID provides a mapping-first
SID artifact interface, D1-D5a diagnostics, optional D6 support, and a
conservative public case study that demonstrates diagnostic value without
leaderboard claims.

## Closure Summary

| Area | Status | Audit judgment |
|---|---|---|
| Gate 0 artifact feasibility | closed / pass | Real Cluster A and Cluster B item-to-SID export paths exist. |
| Gate 0A representativeness | conditionally closed | Sufficient only for resource-demo framing, not for same-dataset method benchmark claims. |
| Gate 1 dataset support | closed for v0 | Musical supports same-item case study; All_Beauty supports Cluster A scale/stability; MovieLens is portability smoke only. |
| Gate 2 diagnostics | closed for D1-D5a | D1-D5a implemented, tested, and used in tables; D6 optional; D7 future hook. |
| Gate 3 empirical check | reframed for resource v0 | Original downstream-metric contrast is not complete; scoped resource evidence supports diagnostic separability. |
| Gate 4 paper viability | closed for current route | Current route is viable as CIKM Resource v0 if claim limits are retained. |
| Strong-accept lift package | executed as far as current evidence allows | Same-dataset panel, GRID 3-seed stability, Fig. 1, and finding polish closed; third named tokenizer closed negative. |
| Method-inspired controllers | closed | All three selected controllers ran locally and are separated from named-method coverage. |
| Public artifact verification | closed | Verifier and unit tests pass in the current worktree. |
| Paper compile / format | closed for current draft | PDF compiles to 5 pages total, with body through page 4 and no ACM review-mode line numbers. |

## Gate-by-Gate Audit

### Gate 0: Artifact Feasibility

Status: **PASS**

Evidence:

- `docs/GATE0_DECISION.md`
- `docs/GRID_CLUSTER_A_EXPORT_PREP.md`
- `docs/RESID_REAL_MAPPING_SMOKE.md`

Current supported exports:

| Cluster | Evidence artifact | Dataset | Items | Supported diagnostics |
|---|---|---:|---:|---|
| A canonical SID | GRID/RQ-KMeans official-module export | Amazon-2023 All_Beauty bounded smoke | 5,000 | D1-D5a |
| B recent tokenizer/codebook | ReSID/GAOQ bounded export | ReSID processed Musical_Instruments | 23,742 | D1-D5a |
| Sanity/control | category/hash/popularity baselines | Musical_Instruments | 23,742 | D1-D5a |

Audit note: the old Sports proxy matrix is correctly reclassified as pipeline
evidence, not Gate 0 evidence. CARD proxy is not faithful CARD.

### Gate 0A: Method Representativeness

Status: **CONDITIONAL PASS FOR RESOURCE DEMO**

Evidence:

- `docs/GATE0A_EVIDENCE_MATRIX.md`
- `docs/METHOD_REPRESENTATIVENESS_AUDIT.md`
- `docs/METHOD_DIAGNOSTIC_SELECTION_MATRIX.md`

Accepted interpretation:

> AUDIT-SID demonstrates a resource interface and diagnostic suite on one
> canonical RQ semantic-ID exporter, one bounded ReSID/GAOQ named artifact, and
> controlled/sanity tokenizers.

Rejected interpretations:

- same-dataset leaderboard;
- faithful TIGER/GRID reproduction;
- faithful CARD evidence;
- ReSID Sports completion;
- D7/generator-output diagnostic coverage.

### Gate 1: Dataset Support

Status: **CLOSED FOR V0**

Evidence:

- `docs/DATASET_SCHEMA_AUDIT.md`
- `docs/CANONICAL_VERTICAL_SCHEMA_AUDIT.md`
- `docs/GRID_MUSICAL_SAME_DATASET_CPU.md`
- `docs/GRID_MUSICAL_3SEED_LOCAL.md`
- `docs/MOVIELENS_PORTABILITY_SMOKE.md`

Audited role split:

| Dataset line | Role | Caveat |
|---|---|---|
| Musical_Instruments | main same-item case study | small category; paper must state bounded public case study |
| All_Beauty | Cluster A scale/stability support | cross-dataset relative to ReSID main row |
| Sports_and_Outdoors / Beauty_and_Personal_Care | staged/audited but not current evidence | ReSID Sports exact GAOQ bottleneck remains unresolved |
| MovieLens | schema portability smoke | sanity SID only, not method evidence |

### Gate 2: Diagnostics

Status: **CLOSED FOR D1-D5a**

Evidence:

- `src/audit_sid/metrics.py`
- `tests/test_metrics.py`
- `tests/test_preflight_metric_inputs.py`
- `paper_assets/tables/table2_musical_diagnostic.csv`
- `paper_assets/tables/table8_qualified_collision_probe.csv`
- `paper_assets/tables/table9_capacity_budget_sweep.csv`
- `paper_assets/tables/table10_variable_depth_cost_probe.csv`

Coverage:

| Diagnostic | Current v0 status | Scope boundary |
|---|---|---|
| D1 utilization | implemented and used | artifact-level capacity profile |
| D2 collision profile | implemented and used | not strict causal harm |
| D2b interaction-qualified collision | bounded controller evidence | controller/stressor, not named-method coverage |
| D3 collaborative alignment | upgraded to co-occurrence D3v2 | proxy, not proven monotonic with Recall/NDCG |
| D4 head-tail capacity | implemented and used | item-to-SID artifact profile |
| D5a prefix/deployment-cost proxy | implemented and used | structural cost proxy, not serving latency |
| D6 drift/churn | optional smoke available | not main paper requirement |
| D7 generator/retrieval behavior | interface hook only | requires generator outputs or beam traces |

### Gate 3: Empirical Check

Status: **REFRAMED BY RESOURCE-SCOPED EVIDENCE, NOT PASSED UNDER THE ORIGINAL DOWNSTREAM-METRIC FORM**

The original broad form of Gate 3 mentioned downstream Recall/NDCG, tail Recall,
invalid generation, and beam/candidate cost. Those are not completed and should
not be claimed. The current v0 closure is instead based on non-redundant
artifact-level evidence:

- same-item Musical table shows GRID feature-text and ReSID GAOQ have sharply
  different D2/D3/D4/D5a profiles on the same 23,742-item universe;
- GRID Musical seeds 42/43/44 show the high collision pressure is stable for
  that controlled row;
- method-inspired controllers show that raw collision, qualified collision,
  capacity allocation, and prefix-cost structure are separable diagnostic
  surfaces.

The paper should not say that the original Gate 3 criterion is passed. The safe
wording is that scoped resource evidence supports diagnostic separability.

### Gate 4: Paper Viability

Status: **PASS FOR RESOURCE TRACK ROUTE**

Evidence:

- `paper/main.tex`
- `paper/main.pdf`
- `docs/PAPER_STRICT_CLAIM_AUDIT.md`
- `docs/PAPER_STRUCTURE_REFERENCE_UPDATE.md`

Paper viability depends on retaining the current claim boundary. The paper is
not viable if rewritten as a broad SID benchmark or method-comparison paper.

## Strong-Accept Lift Package Audit

| Lift item | Status | Evidence | Audit judgment |
|---|---|---|---|
| Third named tokenizer | closed negative | `docs/B2_B3_METHOD_SCREEN.md`, `docs/METHOD_RELEASE_SCOUT.md`, `docs/CARD_ORIGINAL_NURQVAE_EVIDENCE_GATE.md` | No safe third named method enters v0. |
| Same-dataset A/B panel | closed | `docs/GRID_MUSICAL_SAME_DATASET_CPU.md`, `paper_assets/tables/table2_musical_diagnostic.csv` | Usable as diagnostic panel with feature-text caveat. |
| Stability evidence | closed | `docs/GRID_MUSICAL_3SEED_LOCAL.md`, `paper_assets/tables/table7_grid_musical_3seed.csv` | GRID Musical collision pressure is stable across seeds 42/43/44. |
| Finding sharpening | closed | `docs/PAPER_FINDINGS_POLISH.md`, `docs/PAPER_CONTROLLER_INTEGRATION.md` | Findings are artifact-level, not downstream-ranking claims. |
| Fig. 1 redesign | closed | `tools/paper_figures/generate_audit_sid_pipeline.py`, `paper/figures/fig1_audit_sid_pipeline.pdf` | Current figure supports resource-interface narrative. |

## Controller Suite Audit

Status: **CLOSED**

| Controller | Evidence | Supports | Paper role |
|---|---|---|---|
| `qualified_collision_probe` | `docs/QUALIFIED_COLLISION_PROBE.md`, `table8_qualified_collision_probe.csv` | D2b/D3; raw collision vs interaction-qualified risk | compact stressor evidence |
| `capacity_budget_sweep` | `docs/CAPACITY_BUDGET_SWEEP.md`, `table9_capacity_budget_sweep.csv` | D1/D2/D4/D5a capacity pressure | compact stressor evidence |
| `variable_depth_cost_probe` | `docs/VARIABLE_DEPTH_COST_PROBE.md`, `table10_variable_depth_cost_probe.csv` | D4/D5a and D7 boundary | optional/artifact evidence |

These controllers are useful for validating diagnostic behavior, but they do
not expand named-tokenizer coverage.

## Current Verification

Commands run in the current worktree:

```text
python3 tools/verify_paper_artifact.py
python3 -m unittest discover -s tests
pdfinfo paper/main.pdf
rg -n "Not using review mode|LaTeX Warning: Unused global option|Overfull|undefined|Error" paper/main.log
```

Results:

| Check | Result |
|---|---|
| Public artifact verifier | pass: `AUDIT-SID public artifact verification passed.` |
| Unit tests | pass: 16 tests OK |
| PDF page count | 5 pages total |
| CIKM class mode | log says `Not using review mode`; PDF has no line-number gutter |
| LaTeX warnings found by targeted grep | only local `acmart` unused key-value option warning for `natbib=true,anonymous=true` |

## Round 4 Absorption Addendum

Status: **ABSORBED INTO PAPER AND VERIFIER; NOT A NEW EXPERIMENT CLOSURE**

The latest Round 4 paper pass resolves the main wording/table mismatches that
were not reflected in the earlier closure audit:

| Item | Current state | Boundary |
|---|---|---|
| Gate 3 wording | Rewritten as resource-scoped diagnostic separability | Do not claim original downstream Gate 3 passed |
| Fig. 1 | Pipeline plus diagnostic preview with representative D1/D2/D3/D4/D5a signals | Figure is an audit-resource preview, not a leaderboard result |
| Table 1 | Evidence-only facet/status table | Only reports v0 evidence status, built-in stressors, and future backlog |
| Table 2 | Sanity rows, GRID three-seed mean/variance, ReSID/category-prefix structural-floor note | Same-capacity ablation remains future work |
| Table 3 | Controlled stressor / diagnostic / baseline / under-stress table | Variable-depth row uses max-depth 12,010 vs active 7,914 as D5a boundary evidence |
| Table 4 | Deleted from the main paper | Clean-checkout verifier is now summarized in one sentence in Section 5 |
| Verifier | Expanded beyond old Table 2/Table 7 checks | Covers sanity rows, collision probe, capacity sweep, and variable-depth probe |

This addendum supersedes the older tracker wording that described Table 4 as a
reviewer artifact checklist. The current paper has no Table 4. The remaining
evidence gap is the matched-capacity GRID ablation; the paper currently handles
it by caveat/future-work wording rather than by claiming that the ablation has
run.

## Remaining Work Classification

These are **not experiment blockers** for the current v0 package:

1. final citation drift check before submission;
2. real single-blind author and affiliation metadata;
3. final paper copy-editing and claim audit after text changes;
4. optional external simulated review rerun if the paper changes materially;
5. matched-capacity GRID ablation only if it is re-selected as an explicit
   evidence gap rather than treated as a v0 blocker;
6. sending author artifact-request emails after recipient addresses and email
   route are confirmed.

These are **future evidence gaps**, not current-plan blockers:

1. third true named B2/B3/B4 tokenizer artifact;
2. downstream Recall/NDCG or generator-output D7 validation;
3. ReSID Sports exact balanced GAOQ or another canonical vertical;
4. faithful CARD reproduction from complete author artifacts;
5. serving-latency or online-impact validation.

## Claim Impact

Supported:

- AUDIT-SID audits item-to-SID artifacts through a common interface.
- D1-D5a are implemented and used on public artifacts/controls.
- The same-item Musical case study exposes capacity/collision/alignment
  differences that aggregate downstream metrics would not localize by itself.
- Method-inspired controllers confirm that diagnostic axes can separate raw
  collision, interaction-qualified collision, capacity allocation, and prefix
  structure.

Needs qualifier:

- Gate 0A pass: only under conservative resource-demo framing.
- GRID Musical: controlled feature-text row, not faithful raw-text TIGER/GRID.
- ReSID: bounded 1-epoch FAMAE to balanced GAOQ mapping, not final-quality
  ReSID reproduction.
- D3v2: collaborative diagnostic proxy, not a proven downstream predictor.
- D5a: structural proxy, not measured serving cost.

Unsupported for v0:

- full SID system-quality benchmark;
- downstream recommender superiority;
- faithful CARD/DIGER/QuaSID/AdaSID/CapsID evidence;
- D7 generator/retrieval behavior coverage;
- production/online deployment impact.

## Final Audit Decision

The experiment plan is complete enough to stop running local/GPU experiments
for the current CIKM 2026 Resource v0 package. The next workstream should be
submission hygiene and paper-quality control, not more experiments, unless a
new evidence gap is explicitly selected and first passes the local preflight
gate.
