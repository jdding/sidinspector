# AUDIT-SID / SIDInspector Document Index

Timestamp: 2026-05-22 12:39:49 CST

## Current Status

- Paper-facing name: **SIDInspector**. AUDIT-SID remains the repository and
  historical provenance name.
- Gate 0: **passed for artifact feasibility**.
- Gate 0A: **conditional pass for conservative resource-demo framing**.
- Paper case study: **ready at diagnostic-resource level**, not as a SID
  leaderboard.
- Experiment plan: **reopened only for targeted 8/10 lift evidence**; B3
  robustness, All_Beauty 3-seed D3, MovieLens sanity portability, and B5 release
  recheck are now recorded. Remaining work is paper integration and final
  writing/review hygiene, not broad method expansion.
- CIKM format stance: **no usable appendix**; Resource 4-page limit includes
  appendices and acknowledgments.
- Current compute state: run locally first. AutoDL/no-GPU is staging and
  verification only unless a specific GPU-only blocker is documented.
- Dataset stance: main paper can use the same-item-universe Musical diagnostic
  row; `Sports_and_Outdoors` remains future canonical-vertical strengthening,
  not a current blocker.
- Paper-writing stance: the submitted first-draft line uses a five-section Resource Track
  structure, expands cited references to 28 entries, preserves the same
  artifact-only claim boundary, and uses three main tables rather than the
  older Table 4 artifact-checklist layout. Sections 4 and 5 now absorb B6/B7 as
  ranking-context and third-vertical portability evidence without changing the
  non-leaderboard boundary.
- Resource framing stance: CIKM v0 is a diagnostic/interface resource, not a
  RecBole/BARS-style coverage resource. The current source of truth is
  `docs/RESOURCE_FRAMING_DECISION.md`.
- Title/abstract stance: current PDF title is `SIDInspector: A Mapping-First
  Diagnostic Resource for Semantic-ID Tokenizers`; abstract starts from the
  missing artifact-inspection interface and keeps the key Musical numeric
  anchors.
- Active lift stance: `docs/CIKM_17_DAY_8PT_LIFT_PLAN.md` is the current
  optimistic 8/10 plan through the full paper deadline. It reopens explicit
  evidence gaps around the D3 inversion finding, matched-capacity GRID defense,
  vertical replication evidence, D3 ranking validation, third-vertical
  feasibility, and qualified-aliasing backup finding. B6 fixed-reranker
  validation and B7 Sports GRID third-vertical evidence are now locally done.

## Read This First

| Purpose | Current file | Notes |
|---|---|---|
| Post-submission workspace map | `docs/WORKSPACE_ORGANIZATION.md` | Active files after redundant timestamp snapshots were removed |
| Current state entrypoint | `docs/CURRENT_STATE.md` | Start here for live verdict, evidence snapshot, and open gaps |
| Resource framing decision | `docs/RESOURCE_FRAMING_DECISION.md` | Freezes Type 4 diagnostic/interface framing for CIKM v0 and leaves Type 1 coverage as future platform route |
| CIKM experiment design | `docs/CIKM_EXPERIMENT_DESIGN.md` | Paper table plan and D1-D5 main / D6-D7 extension scope |
| 17-day 8/10 lift plan | `docs/CIKM_17_DAY_8PT_LIFT_PLAN.md` | Active aggressive plan: D3 inversion main finding, matched-capacity GRID, vertical replication, B6 ranking validation, B7 third vertical, B8 qualified-aliasing backup |
| Matched-capacity GRID result | `docs/MATCHED_CAPACITY_GRID_AUTODL_RESULT.md` | AutoDL port 21551 B2 result: GRID ft-cap, 9,874 unique SIDs, D2 aliasing 0.778452, D3 L1 0.079595 |
| All_Beauty vertical D3 replication | `docs/VERTICAL_D3_REPLICATION_ALL_BEAUTY.md` | AutoDL port 21551 B4 result with coarse-category caveat: GRID All_Beauty 20k 3-seed D3 range 0.0811--0.0898 vs category-prefix 0.9684 |
| Musical D3 ranking-context probe | `docs/D3_RANKING_CONTEXT_MUSICAL.md` | B3 prefix-retrieval proxy: 5,000-user robustness keeps D3 aligned with candidate coverage, but low Hit@20 blocks downstream-validation claims |
| Musical D3 fixed-reranker validation | `docs/D3_RANKING_VALIDATION_MUSICAL.md` | B6 local validation: SID prefixes define candidates, shared train-only reranker reports candidate recall, Recall@20, NDCG@20, MRR@20, and D3 correlations |
| Sports GRID third vertical | `docs/SPORTS_GRID_THIRD_VERTICAL.md` | B7 local evidence: real Sports_and_Outdoors GRID/RQ-KMeans feature-text export, 20k items, zero coverage gaps, D1-D5 metrics |
| MovieLens D3 sanity summary | `docs/MOVIELENS_D3_SANITY_SUMMARY.md` | Non-Amazon schema/probe portability only: category, popularity, and hash sanity rows with zero coverage gaps |
| Sports proxy/control D3v2 supplement | `docs/SPORTS_PROXY_D3V2_SUPPLEMENT.md` | Artifact supplement only: Sports proxy rows show directional D3 gap, but do not count as named-method evidence |
| B5 release recheck | `docs/B5_RELEASE_RECHECK.md` | No new official third named-method artifact is ready; keep B5 as release-watch/backlog |
| Diagnostic probe taxonomy | `docs/DIAGNOSTIC_PROBE_TAXONOMY.md` | Current naming source: D1-D5 main probes, D6 temporal churn, D7 generation traces, mechanism-probe terminology |
| SID problem coverage audit | `docs/SID_PROBLEM_COVERAGE_AUDIT.md` | Current answer to whether D1-D6 cover literature SID problems: artifact-level main modes yes, full system quality no |
| Strong-accept experiment plan | `refine-logs/EXPERIMENT_PLAN.md` | Optional 8.5 lift package: third named tokenizer, same-dataset panel, stability, Fig. 1 redesign |
| CIKM format audit | `docs/CIKM_RESOURCE_FORMAT_AUDIT.md` | Official Resource page constraint; no-appendix paper strategy |
| Citation audit | `docs/CITATION_AUDIT.md` | Refreshed 2026-05-21: 28 active cited entries, ICML 2026 SID/tokenizer scan, and metadata fixes |
| Reference refresh | `docs/SID_REFERENCE_REFRESH.md` | Literature gap scan and recommended compact reference set |
| Cluster/diagnostic refresh | `docs/SID_CLUSTER_DIAGNOSTIC_REFRESH.md` | Updated method taxonomy and D1-D7 coverage plan |
| Method x diagnostic matrix | `docs/METHOD_DIAGNOSTIC_SELECTION_MATRIX.md` | Working table for choosing new methods by D1-D7 coverage and finding material |
| B2/B3 method screen | `docs/B2_B3_METHOD_SCREEN.md` | Latest third-method screen; no new named tokenizer enters main evidence |
| Third-method evidence gate | `docs/THIRD_METHOD_EVIDENCE_GATE.md` | Admission rule: no self-implemented paper-inspired method as named evidence |
| Method release scout | `docs/METHOD_RELEASE_SCOUT.md` | Official-release screen for QuaSID/AdaSID/CapsID/DIGER |
| CARD original evidence gate | `docs/CARD_ORIGINAL_NURQVAE_EVIDENCE_GATE.md` | CARD failed for v0 main evidence because official quantizer modules are missing |
| Controlled mechanism probes | `docs/CONTROLLED_STRESSOR_SELECTION.md` | Historical execution note for method-inspired probes; separate from named-method coverage |
| Qualified collision probe | `docs/QUALIFIED_COLLISION_PROBE.md` | D2/D3 mechanism-probe result for interaction-qualified collision risk |
| Capacity budget sweep | `docs/CAPACITY_BUDGET_SWEEP.md` | D1/D2/D4/D5 mechanism-probe result for capacity pressure |
| Variable depth cost probe | `docs/VARIABLE_DEPTH_COST_PROBE.md` | D5 structural-cost mechanism-probe result |
| Author artifact emails | `docs/AUTHOR_ARTIFACT_EMAIL_DRAFTS.md` | Sent DIGER/QuaSID/CapsID artifact-request messages and DIGER author reply; optional future-adapter information |
| GRID Musical 3-seed local run | `docs/GRID_MUSICAL_3SEED_LOCAL.md` | Local same-dataset stability support for the GRID feature-text row |
| Experiment closure audit | `docs/EXPERIMENT_PLAN_CLOSURE_AUDIT.md` | Current closure check: no additional v0 experiment required before writing/review |
| Full experiment-plan audit | `docs/EXPERIMENT_PLAN_FULL_AUDIT.md` | Current complete plan-to-evidence audit: v0 experiments closed, residual work classified |
| Paper findings polish | `docs/PAPER_FINDINGS_POLISH.md` | Latest results-based paper polish: Section 3 diagnostic findings and claim boundary |
| Paper mechanism-probe integration | `docs/PAPER_CONTROLLER_INTEGRATION.md` | Latest writing pass absorbing qualified-collision, capacity-budget, and variable-depth probe findings |
| Paper structure/reference update | `docs/PAPER_STRUCTURE_REFERENCE_UPDATE.md` | Five-section Resource Track structure and pre-ICML-refresh 27-entry citation coverage |
| Additional experiment preflight code | `docs/ADDITIONAL_EXPERIMENT_PREFLIGHT_CODE.md` | Local CPU input-contract gate for future method/artifact additions |
| Figure/table strategy | `docs/PAPER_FIGURE_TABLE_STRATEGY.md` | One-vector-figure/three-table body plan and artifact-repo table boundary |
| Strict claim audit | `docs/PAPER_STRICT_CLAIM_AUDIT.md` | Current paper wording and numeric-claim audit, including mechanism-probe numbers |
| Internal review round 1 | `docs/INTERNAL_REVIEW_ROUND1.md` | First local CIKM Resource review, 7.1/10, with required fixes |
| Internal review round 2 | `docs/INTERNAL_REVIEW_ROUND2.md` | Second local CIKM Resource review, 8.0/10, external-review gate |
| External simulated review plan | `docs/EXTERNAL_SIM_REVIEW_PLAN.md` | External review target fixed at CIKM 2026 Resource Track and 8.0/10 |
| External simulated review round 1 | `docs/EXTERNAL_SIM_REVIEW_ROUND1.md` | External scores 7.2/7.4 -> 7.7 after packaging fixes; release gate for 8.0 |
| External simulated review round 2 | `docs/EXTERNAL_SIM_REVIEW_ROUND2.md` | External 8.0/8.1 after pushed tag and clean-checkout verification |
| External R3 delta result | `review-stage/EXTERNAL_REVIEW_R3_DELTA_RESULT.md` | Stricter post-matched-capacity review: 6/10; W2 moderate, W1/W3 remain score ceiling |
| Public artifact manifest | `ARTIFACT_MANIFEST.md` | Reviewer-facing clean-checkout manifest and local-cache boundary |
| Artifact quickstart | `ARTIFACT_QUICKSTART.md` | Pinned-tag clean-checkout verifier commands |
| BibTeX audit | `docs/BIBTEX_AUDIT.md` | Paper-ready BibTeX generated from verified pages |
| BibTeX file | `paper_assets/references/audit_sid_references.bib` | Current paper reference file |
| CIKM paper draft | `paper/main.tex` | SIDInspector ACM draft using CIKM literal `sigconf,natbib=true,anonymous=true`; `paper/main.pdf` compiles to 5 pages total, no review-mode line numbers, GenAI precedes References |
| Latest writing integration | `paper/sections/4_demonstration.tex` | B3/B4/Sports evidence is written as diagnostic context/support, not downstream validation or named-method coverage |
| Paper-facing tables | `paper_assets/tables/` | Generated CSV/MD/TeX tables; Table 1 and Table 2 are PDF candidates |
| Project contract | `docs/PROJECT_SPEC.md` | Unified thesis, gates, method coverage, diagnostics |
| Current gate verdict | `docs/GATE0_DECISION.md` | Gate 0 artifact-feasibility pass; Gate 0A conservative resource-demo pass |
| Live tracker | `refine-logs/EXPERIMENT_TRACKER.md` | Operational source of truth for tasks and status |
| Archive map | `docs/ARCHIVE_INDEX.md` | Historical docs grouped without moving or deleting provenance |
| Round 4 physical archive | `docs/archive/2026-05-20-round4-cleanup/` | Timestamped snapshots moved out of active directories after explicit cleanup request |
| Local artifact map | `docs/ARTIFACTS_INDEX.md` | `_gate0_artifacts/` size, evidence boundary, cleanup candidates |
| Latest remote runbook | `docs/AUTODL_NO_GPU_POST_COMMIT_SYNC.md` | AutoDL is staging/verification only in current local-first policy |
| Latest remote result | `docs/AUTODL_GATE0A_GRID_RESULTS.md` | AutoDL GRID 20k/50k clean batch completed |
| Main case study | `docs/GRID_MUSICAL_SAME_DATASET_CPU.md` | Same-item-universe GRID feature-text vs ReSID Musical diagnostic row |
| Cluster A evidence | `docs/GRID_CLUSTER_A_EXPORT_PREP.md` | GRID official-module RQ-KMeans local 5k export |
| Cluster B evidence | `docs/RESID_REAL_MAPPING_SMOKE.md` | ReSID balanced GAOQ local real mapping |
| Next-method selection | `docs/METHOD_DIAGNOSTIC_SELECTION_MATRIX.md` | Prioritize B2/B3/B4 candidates before running new methods |

## Gate Evidence

### Gate 0

Use these files:

- `docs/GATE0_DECISION.md`
- `docs/GRID_CLUSTER_A_EXPORT_PREP.md`
- `docs/RESID_REAL_MAPPING_SMOKE.md`
- `docs/AUTODL_GATE0A_STAGING.md`

Do **not** use these as current verdicts:

- `docs/GATE0_RESULTS_20260518_233331.md`
- `docs/GATE0_RESULTS_20260518_234958.md`
- `docs/GATE0_RESULTS.md`

Those files are retained because they document the proxy-matrix correction. The
current verdict is `docs/GATE0_DECISION.md`.

### Gate 0A

Gate 0A has a conditional pass for a conservative resource-demo framing. The
main paper should use:

- method coverage table with explicit artifact caveats;
- same-item-universe Musical diagnostic row;
- D1-D5 as main mapping-level diagnostic probes;
- D6 only as optional temporal-churn evidence;
- D7 only as a generator-trace hook until real outputs exist.

Do not treat this as a same-dataset leaderboard or full SID system-quality
benchmark. The first submission draft has passed local compile, verifier,
and citation-drift checks; remaining work is response-time polish or
post-submission revision, not new v0 evidence generation.

Paper-facing generated tables:

- `paper_assets/tables/table1_method_coverage.*`
- `paper_assets/tables/table2_musical_diagnostic.*`
- `paper_assets/tables/table3_sanity_controls.*`
- `paper_assets/tables/table4_grid_scale.*`
- `paper_assets/tables/table5_dact_d6_churn.*`
- `paper_assets/tables/table6_movielens_portability.*`

Current compiled paper draft:

- `paper/main.pdf` compiles to 5 pages total with generated vector Fig. 1,
  redesigned Table 1, D5-aware compact Table 2, and controlled mechanism-probe
  Table 3.
  The body fills through page 4; references and GenAI disclosure extend to
  page 5.
- `paper/sections/2_toolkit.tex` contains the artifact pipeline figure and
  facet-aware coverage table.
- `paper/sections/4_demonstration.tex` contains the same-item Musical
  diagnostic table and the controlled mechanism-probe table.
- `paper/sections/5_availability_limits.tex` contains the availability,
  reviewer workflow, clean-checkout verifier, and claim-discipline text. The
  current paper has no Table 4.
- `docs/INTERNAL_REVIEW_ROUND1.md` and `docs/INTERNAL_REVIEW_ROUND2.md`
  record the two internal reviews requested before external simulated review.
- `docs/EXTERNAL_SIM_REVIEW_PLAN.md` fixes the external simulated review target
  at 8.0/10 for CIKM 2026 Resource Track.
- `docs/EXTERNAL_SIM_REVIEW_ROUND1.md` records the first external review cycle
  and the packaging fixes required to make external 8.0 plausible.
- `docs/EXTERNAL_SIM_REVIEW_ROUND2.md` records the pushed-tag clean checkout
  evidence and closes the external simulated-review target at 8.0/8.1.
- `ARTIFACT_MANIFEST.md`, `ARTIFACT_QUICKSTART.md`, `requirements.txt`, and
  `tools/verify_paper_artifact.py` are the public clean-checkout verification
  path.
- The optional strong-accept lift package is now recorded in
  `refine-logs/EXPERIMENT_PLAN.md`, `docs/CIKM_EXPERIMENT_DESIGN.md`,
  `docs/CIKM_RESOURCE_PAPER_PLAN.md`, and
  `docs/PAPER_FIGURE_TABLE_STRATEGY.md`.
- `docs/B2_B3_METHOD_SCREEN.md` records the 2026-05-19 B2/B3 screen:
  QuaSID/AdaSID/CapsID are coverage/motivation only, DIGER is incomplete for
  artifact export, and CARD remains proxy/control unless the original
  `nu-rq-vae` path is repaired.
- `docs/GRID_MUSICAL_3SEED_LOCAL.md` records the local CPU seeds 42/43/44 GRID
  Musical feature-text evidence and summary CSV paths.
- `docs/EXPERIMENT_PLAN_CLOSURE_AUDIT.md` closes the current experimental
  plan for v0 and keeps remaining citation/metadata/claim-audit work separate
  from new experiment work.
- `docs/EXPERIMENT_PLAN_FULL_AUDIT.md` is the latest complete closure report:
  Gate 0 is passed, Gate 0A is conditionally closed, D1-D5 and mechanism probes
  are closed, third named-tokenizer expansion is closed negative for v0, and
  the Round 4 addendum records the Table 4 deletion plus verifier expansion.
- `docs/PAPER_FINDINGS_POLISH.md` records the post-closure paper pass that
  turns the current evidence into explicit artifact-level findings.
- `docs/PAPER_CONTROLLER_INTEGRATION.md` records the follow-up writing pass
  that folds mechanism-probe results into Section 4 while keeping them outside
  named-method coverage.
- `docs/ADDITIONAL_EXPERIMENT_PREFLIGHT_CODE.md` records the subagent-prepared
  local preflight script for future method/artifact additions.
- `docs/THIRD_METHOD_EVIDENCE_GATE.md` records the no-self-implementation
  admission rule for any third named tokenizer.
- `docs/METHOD_RELEASE_SCOUT.md` records that QuaSID/AdaSID/CapsID/DIGER do
  not currently pass the official-artifact gate for v0 main evidence.
- `docs/CARD_ORIGINAL_NURQVAE_EVIDENCE_GATE.md` records the CARD original
  failure: source/import/export-contract smoke depends on local repair files,
  not a complete official CARD quantizer implementation.
- `docs/DIAGNOSTIC_PROBE_TAXONOMY.md` records the current D1-D7 naming policy.
- `docs/SID_PROBLEM_COVERAGE_AUDIT.md` records the current D1-D6 coverage
  boundary against SID method-paper problem claims.
- `docs/CONTROLLED_STRESSOR_SELECTION.md` records the historical execution note:
  `qualified_collision_probe`, `capacity_budget_sweep`, and
  `variable_depth_cost_probe` are locally executed as method-inspired
  controlled mechanism probes, not named-method coverage.
- `docs/AUTHOR_ARTIFACT_EMAIL_DRAFTS.md` records sent artifact-request
  messages for DIGER/QuaSID/CapsID and the DIGER author reply.
- `docs/R3_REVIEW_ABSORPTION.md` records the 5/10 simulated CIKM Resource
  review, the accepted action priorities, and the claim/write-up changes that
  are now folded into the paper.
- `review-stage/EXTERNAL_REVIEW_R3_DELTA_RESULT.md` records the follow-up
  review after `GRID ft-cap`: score 6/10, W2 partially resolved, W1 and W3 still
  cap the paper below the 8/10 target.
- `docs/MATCHED_CAPACITY_GRID_GATE.md` records the reopened GRID
  matched-capacity ablation gate. The current status is completed AutoDL GPU
  evidence and the result is integrated as the `GRID ft-cap` Table 2 row.
- `docs/AUTODL_MATCHED_CAPACITY_GRID_PLAN.md` is the AutoDL launch/completion
  plan for the single R3 W2 follow-up experiment.
- `docs/VERTICAL_D3_REPLICATION_ALL_BEAUTY.md` records that the D3 inversion
  repeats on All_Beauty GRID+controls panels, while still not validating D3
  against downstream Recall/NDCG. The duplicate scratch note was moved to
  `docs/archive/2026-05-20-dedup/`.

## Method Evidence

| Method line | Current status | File |
|---|---|---|
| GRID / RQ-KMeans Cluster A | real artifact-feasibility path plus same-item Musical controlled row and 3-seed stability | `docs/GRID_CLUSTER_A_EXPORT_PREP.md`, `docs/GRID_MUSICAL_SAME_DATASET_CPU.md`, `docs/GRID_MUSICAL_3SEED_LOCAL.md` |
| ReSID / GAOQ Cluster B | real bounded 1-epoch export, Musical_Instruments | `docs/RESID_REAL_MAPPING_SMOKE.md` |
| Sanity baselines | available for metric sensitivity | `docs/METRIC_SMOKE.md`, `docs/CASE_STUDY_RESID_VS_SANITY.md` |
| CARD | failed for v0 main evidence; original `nu-rq-vae` source/import/export-contract preflight depends on local quantizer repair | `docs/CARD_ORIGINAL_NURQVAE_EVIDENCE_GATE.md`, `docs/CARD_SOURCE_REPAIR.md`, `docs/THIRD_METHOD_EVIDENCE_GATE.md`, `tools/autodl_audit_sid/preflight_card_nurqvae.py` |
| DIGER / QuaSID / AdaSID / CapsID | official-release scout complete; not current main evidence | `docs/B2_B3_METHOD_SCREEN.md`, `docs/METHOD_DIAGNOSTIC_SELECTION_MATRIX.md`, `docs/METHOD_RELEASE_SCOUT.md` |
| Method-inspired probes | local done as separate controlled mechanism-probe evidence; not method evidence | `docs/CONTROLLED_STRESSOR_SELECTION.md`, `docs/QUALIFIED_COLLISION_PROBE.md`, `docs/CAPACITY_BUDGET_SWEEP.md`, `docs/VARIABLE_DEPTH_COST_PROBE.md`, `paper_assets/tables/table8_qualified_collision_probe.*`, `paper_assets/tables/table9_capacity_budget_sweep.*`, `paper_assets/tables/table10_variable_depth_cost_probe.*` |
| Sports proxy matrix | pipeline evidence only | `docs/GATE0_RESULTS.md` |

## AutoDL State

Use `docs/AUTODL_NO_GPU_POST_COMMIT_SYNC.md` as the current remote state. Use
`docs/AUTODL_GATE0A_STAGING.md` only if a new GPU-only blocker is selected.

Older AutoDL docs are historical:

- `docs/AUTODL_READY_HANDOFF.md`
- `docs/AUTODL_READINESS_REPORT.md`
- `docs/AUTODL_REMOTE_STAGING.md`
- `docs/AUTODL_GAOQ_STOPLOSS.md`

They are still useful for provenance, but they should not override the latest
Gate 0A staging file.

## Historical Planning

Use these for context, not for current status:

- `docs/AUDIT_SID_VENUE_PLAN.md`
- `docs/AUDIT_SID_CIKM_EXECUTION_SPEC.md`
- `docs/EXTERNAL_REVIEW_ABSORPTION.md`
- `docs/SID_METHOD_CLUSTER_AUDIT.md`
- `docs/METHOD_REPRESENTATIVENESS_AUDIT.md`
- `docs/TOKENIZER_DATASET_CATEGORY_AUDIT.md`

For timestamped-history navigation, use `docs/ARCHIVE_INDEX.md` instead of
opening old files one by one.

## Artifact Policy

- Fixed-name docs are the latest readable entry points.
- Timestamped docs are immutable history.
- Do not delete old timestamped files.
- Do not count proxy rows as named-method evidence in future paper tables.
- `_gate0_artifacts/` is git-ignored local state; use `docs/ARTIFACTS_INDEX.md`
  to decide what is evidence, debug provenance, or future cleanup candidate.
