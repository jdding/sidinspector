# SIDInspector 17-Day 8/10 Lift Plan

Timestamp: 2026-05-20 16:14:52 CST

## Position

The project is no longer in a conservative-only closure mode. Given the real
deadline window to the 2026-06-06 paper deadline, SIDInspector should pursue an
aggressive but gated 8/10 Resource Track lift.

The core adjustment is:

> make a sharp diagnostic finding first-class, then add targeted experiments to
> defend it against the most likely reviewer attacks.

This plan supersedes the earlier "no new experiments unless a gap is selected"
stance. The selected evidence gaps are now explicit: D3 inversion strength,
capacity-mismatch defense, downstream grounding, and optional method breadth.

## Aggressive Acceptance Upgrade

User calibration on 2026-05-20 evening: the target is not to avoid a weak
reject or gamble at the borderline; the target is an 8/10 acceptance attempt.
Therefore the plan should not stop after the first set of defensive probes.

The upgraded rule is:

> keep the conservative claim boundary, but make the evidence package more
> aggressive than the minimum plan.

That means the next stage is not "more tables"; it is a harder closure package:

1. **Turn B3 from context into grounding if feasible.** The completed
   prefix-neighborhood runs are useful, but they are still not Recall/NDCG
   validation. The next attempt should add a small, fixed ranking evaluator over
   SID-induced candidate sets and report Recall@K/NDCG@K or explicitly document
   why the resulting protocol is still proxy-only.
2. **Add a third vertical with a real learned/export row if feasible.** Musical
   plus All_Beauty is good, but Sports/MovieLens are currently supplement or
   sanity-only. The next vertical should prefer Books/Beauty/Sports only if it
   has joinable metadata, interactions, and a real learned/export SID row.
3. **Promote Finding B as a real backup axis.** Qualified aliasing is not a
   replacement for Hu et al.'s claim; it should be framed as mapping-level
   early warning before generator training. If D3 grounding stays proxy-only,
   this becomes the second memorable finding.
4. **Treat B5 as reference-adapter breadth, not named-method breadth.** The
   release gate still blocks fake named evidence. A minimal RQ/RQ-VAE reference
   adapter can still be valuable if it is labeled as a SIDInspector reference
   implementation with implementation notes and no reproduction claim.
5. **Move external read-through earlier.** A fresh reviewer pass should happen
   after the next hard-evidence update, not only after final polish.

## Sixth-Round Review Decision

The 2026-05-20 simulated review v2 is treated as the current decision input.
It scores the active clarity draft around 7/10: the paper now has a memorable
D3 finding and three defensive lifts, but it still needs a small set of
targeted closures before an 8/10 attempt is credible.

Accepted next actions:

1. **W2: make the All_Beauty coarse-category interpretation explicit.**
   The 0.968 D3 value should be written as dataset-level taxonomy--behavior
   alignment exposed by D3, not as evidence that category identifiers are
   universally better tokenizers.
2. **W3: repeat B6-style fixed-reranker ranking context on All_Beauty if
   feasible.** The goal is to reduce the small-n weakness in the Musical-only
   D3/Recall correlation. If blocked, freeze the gap rather than inventing a
   proxy claim.
3. **W4: redesign Fig. 1 as a finding preview.** The bottom panels should show
   D3 inversion, matched-capacity GRID, fixed-reranker grounding, and
   portability/qualified-aliasing support.
4. **W1/Lift 5: implement only a gated reference adapter.**
   `rqvae_minimal_reference` is allowed as a third independent code path for
   the adapter contract. It is not a third named-method reproduction and does
   not fully remove the published-method coverage weakness.

See `docs/SIMULATED_REVIEW_V2_DECISION.md` for the detailed action boundary.

## Target Claims

| Claim | Role | Minimum convincing evidence | Decision rule |
|---|---|---|---|
| C1: D3 exposes a behavioral-prefix blind spot | primary finding | Category-prefix D3 is higher than learned/exported SID rows on Musical; rewrite paper around this as a diagnostic warning, not a tokenizer-quality claim | always execute writing lift |
| C2: The D3 inversion is not a one-off table artifact | strengthening evidence | Repeat D3 sanity/learned-row comparison on at least one additional feasible vertical, or document why available artifacts block faithful comparison | run preflight first; admit only real joinable rows |
| C3: Capacity mismatch does not invalidate the worked example | defense | Matched-capacity GRID Musical row with widths `32,1280,1280`, or a documented GPU/implementation stop-loss result | run one bounded GPU-worthy attempt |
| C4: D3 has downstream context | defense / stretch | Small D3-vs-ranking correlation or explicitly negative/orthogonal result on Musical | run only after C1/C3 are stable |
| C5: Method breadth is improving without fake reproduction | stretch / gated | One minimal reference implementation or true author/release artifact with implementation notes; clearly not a named-method reproduction | run only after local smoke and validator pass; cut if it risks paper quality |
| C6: A second memorable finding survives scrutiny | backup finding | Qualified aliasing risk is shown as mapping-level early warning, not as a rediscovery of collision inequality | promote if D3 grounding remains proxy-only |

## Spec-to-Experiment Translation Gate

| Spec / reviewer pressure | Experiment block | Same dataset? | Same split? | Same metric? | Same method variant? | Status |
|---|---|---:|---:|---:|---:|---|
| "A resource needs a memorable finding" | B1 D3 inversion rewrite | yes, Musical | yes | yes, D3 | current rows | pass |
| "Sanity row should not be hidden as a control" | B1 D3 inversion rewrite + Fig/Table update | yes | yes | yes | current rows | pass |
| "GRID vs ReSID is capacity-biased" | B2 matched-capacity GRID | yes, Musical | yes | D1-D5 | GRID feature-text, prefix-matched | done; Table 2 row integrated |
| "D3 may be a proxy disconnected from ranking" | B3 D3-vs-ranking context | yes, Musical | bounded split | D3 + retrieval proxy | current rows + simple evaluator | completed as 1k + 5k bounded prefix-retrieval context; not fixed-reranker or generator validation |
| "Single dataset core" | B4 vertical replication preflight | All_Beauty feasible | verified | D3 + D1-D5 subset | GRID feature-text plus controls | done as All_Beauty 20k 3-seed artifact evidence; coarse-category caveat |
| "Only two named methods" | B5 release recheck + B9 reference adapter | any joinable dataset | verify | D1-D5 | labeled reference/probe, not named reproduction | release recheck no-go for third named method; `rqvae_minimal_reference` reopened as gated adapter only |
| "8/10 needs harder grounding" | B6 small ranking validation | yes, Musical first; All_Beauty if feasible | bounded split | D3 + fixed-reranker Recall/NDCG context | fixed evaluator, same candidate/rerank protocol | Musical done locally; All_Beauty replication delegated |
| "Need three datasets, not two" | B7 third vertical learned/export row | Sports | verified | D1-D5/D3 | real GRID learned/export row | done locally at 20k; not third named tokenizer |
| "Need second memorable finding" | B8 qualified-aliasing finding lift | Musical mechanism plus real-row context | n/a | D2/D3 risk lift | controlled mechanism probe | read-only review done; usable as early-warning backup only |

## Experiment Blocks

### B1: D3 Inversion As Main Finding

- Claim tested: learned/exported SID rows do not automatically produce
  behaviorally meaningful prefixes.
- Dataset: ReSID processed `Musical_Instruments`.
- Systems: GRID feature-text, bounded ReSID/GAOQ, category-prefix,
  mod-collision hash, popularity-balanced.
- Metric: D3 L1 co-occurrence prefix recall, with D2/D4/D5 context.
- Current evidence: category-prefix D3 = 0.447, ReSID = 0.154, GRID = 0.055.
- Success criterion: paper explicitly makes this a diagnostic finding, while
  saying it is not a claim that category-prefix is a better recommender
  tokenizer.
- Output: abstract sentence, §1 contribution, §4 subsection, Fig. 1 D3 panel,
  claim-audit row.

### B2: Matched-Capacity GRID Defense

- Claim tested: whether the GRID row's high aliasing is only an artifact of a
  much smaller prefix-capacity budget.
- Dataset: Musical same item universe.
- System: GRID/RQ-KMeans feature-text with per-level widths `32,1280,1280`.
- Metrics: D1-D5; primary columns are full-code aliasing, unique full codes,
  D3 L1, D4 tail, D5 prefix counts.
- Execution: one GPU-worthy AutoDL run per `docs/AUTODL_MATCHED_CAPACITY_GRID_PLAN.md`.
- Stop-loss: if GPU path is CPU-bound or produces no artifact, record the
  blocker honestly and keep the caveat.
- Paper decision:
  - clean and informative: Table 2 now includes `GRID ft-cap`;
  - do not describe it as a faithful TIGER/GRID or ReSID-matched reproduction.

### B3: D3-Vs-Ranking Context

- Claim tested: whether D3 is monotonic with a bounded downstream proxy, or
  instead measures an orthogonal artifact property.
- Dataset: Musical first; no cross-dataset expansion until Musical is stable.
- Candidate low-cost evaluators:
  - prefix-neighborhood retrieval using SID prefixes;
  - small SASRec/generator run only if existing scripts can be bounded and
    deterministic enough for a one-day result.
- Systems: category-prefix, ReSID, GRID feature-text, popularity-balanced.
- Success criterion: any result is useful if reported honestly:
  - positive correlation: D3 is a plausible early signal;
  - weak/no correlation: D3 exposes a distinct artifact property;
  - negative correlation: a stronger diagnostic finding, but only if verified.
- Cut rule: if setup takes more than one day or introduces ambiguous training
  confounders, cut from CIKM and leave for WSDM.
- Current status: completed as bounded prefix-neighborhood retrieval proxies in
  `docs/D3_RANKING_CONTEXT_MUSICAL.md`. The original 1,000-user run and the
  5,000-user robustness run both give D3 ranking-context signal through
  candidate coverage, but low Hit@20 across all rows means this is not
  downstream Recall/NDCG validation.

### B4: Vertical Replication Preflight

- Claim tested: whether D3 inversion is dataset-dependent or robust across
  feasible public verticals.
- Candidate verticals: `Beauty_and_Personal_Care`, `Sports_and_Outdoors`,
  `All_Beauty`.
- First action: preflight available joinable artifacts, not training.
- Admit only rows that have:
  - `sid_assignments`;
  - metadata and interaction joins;
  - D3 co-occurrence computation;
  - clear evidence role.
- Paper decision:
  - if at least one additional vertical repeats the inversion, strengthen C1;
  - if not, report dataset dependence as a diagnostic observation;
  - if no faithful learned row exists, keep this out of main paper and document
    the gap.

Current status: `All_Beauty` is done as a 20k three-seed vertical panel. Across
GRID seeds 42/43/44, D3-L1 is `0.0811/0.0872/0.0898` while category-prefix
remains `0.9684`. See `docs/VERTICAL_D3_REPLICATION_ALL_BEAUTY.md`. This
supports the cross-vertical diagnostic inversion story, but the category-prefix
control uses coarse `category` fallback metadata and is still not downstream
Recall/NDCG validation. `Sports` is retained only as a proxy/control supplement,
and MovieLens is retained only as non-Amazon sanity/probe portability.

### B5: Reference Implementation / True Artifact Stretch

- Goal: reduce method-breadth anxiety without returning to a coverage-resource
  claim.
- Acceptable forms:
  - minimal RQ reference implementation with `IMPL_NOTES.md`;
  - official/author-provided artifact that exports item-level SIDs;
  - repaired method only if all deviations are documented and it is not named
    as a faithful reproduction.
- Cut rule: if it competes with B1/B2/B3 writing and claim audit, cut.

Current status: cut for the CIKM sprint after release recheck. DIGER still has
no ready public mapping/checkpoint package, and QuaSID/AdaSID/CapsID/CARD still
lack official artifacts that pass `docs/THIRD_METHOD_EVIDENCE_GATE.md`. Do not
start a local paper-inspired third named tokenizer implementation unless a new
official or author-provided artifact appears.

Aggressive revision: B5 is cut as **named-method evidence**, but a labeled
reference adapter remains allowed if it is cheap, tested, and clearly named as
`SIDInspector reference RQ/RQ-VAE`, not TIGER/CARD/ReSID/QuaSID/etc. This can
help Resource readers see how to attach new tokenizers without pretending to
increase reproduced-method coverage.

Current sixth-round decision: reopen only the reference-adapter path under the
label `rqvae_minimal_reference`. Required gates are `IMPL_NOTES.md`, local
512/2k smoke, validator pass, D1-D5 metrics, and explicit paper wording that
the row demonstrates an independent adapter/code path rather than a published
method reproduction. If the run collapses, it can be reported only after
implementation sanity checks rule out a coding bug.

### B6: Small Ranking Validation

- Claim tested: whether D3 has any measurable relationship to held-out
  recommendation retrieval/ranking under a fixed, mapping-dependent protocol.
- Dataset: Musical first.
- Systems: category-prefix, popularity-balanced, hash, ReSID, GRID feature-text,
  GRID ft-cap.
- Candidate protocol:
  - generate candidate sets from SID prefixes as in B3;
  - apply the same fixed reranker for every mapping, such as popularity,
    co-occurrence score, or a small deterministic item-item scorer;
  - report candidate recall, fixed-reranker Recall@20, fixed-reranker NDCG@20,
    fixed-reranker MRR@20, and D3 correlation.
- Success criterion:
  - if D3 correlates with candidate recall but not final Recall, write that D3
    is an early candidate-generation signal;
  - if D3 does not correlate, write that D3 diagnoses a distinct artifact
    property and keep the stronger boundary;
  - if protocol depends on arbitrary reranker choices, keep it out of the main
    paper and document it as a supplement.
- Stop rule: do not train a heavy generator or introduce an evaluator that
  changes several variables at once.

Current status: done locally. `tools/autodl_audit_sid/run_d3_ranking_validation.py`
uses SID prefixes only to define candidate sets and applies the same train-only
co-occurrence/popularity reranker to every row. In the 5,000-user depth-1 run,
D3 has Spearman `0.9429` with candidate recall, `0.8857` with fixed-reranker
Recall@20, and `0.9429` with fixed-reranker NDCG@20/MRR@20 across six
artifact/control rows. See
`docs/D3_RANKING_VALIDATION_MUSICAL.md`. This is usable as early
candidate/ranking-context validation, not as trained generator Recall/NDCG.

Sixth-round extension status: completed as a bounded All_Beauty temporal-LOO
panel. The local All_Beauty interaction file is splitless, so a strict
train/valid split was constructed by dropping singleton users and using each
remaining user's last event as validation. On 1,000 targets and four
artifact/control rows, D3 has Spearman `1.0000` with candidate recall and
`0.8000` with fixed-reranker Recall@20/NDCG@20/MRR@20. See
`docs/D3_RANKING_VALIDATION_ALL_BEAUTY.md` and
`paper_assets/tables/table14_all_beauty_d3_ranking_validation.csv`. This is
usable only as supplementary ranking-context replication, not as trained
generator validation.

### B9: `rqvae_minimal_reference` Adapter Gate

- Claim tested: \tool can attach a third independent SID-generation code path
  through the same mapping contract.
- Evidence role: reference adapter / contract demonstration, not named-method
  coverage and not TIGER/GRID/ReSID reproduction.
- Required files:
  - `methods/rqvae_minimal_reference/IMPL_NOTES.md`;
  - local exporter/smoke script;
  - validator output;
  - D1-D5 table if the smoke/full run passes.
- Admission criterion for paper:
  - local 512/2k smoke passes;
  - the mapping is well formed and joinable;
  - D1-D5 metrics are computed from exported mappings;
  - the table/prose label is `RQ-VAE-min` or `rqvae_minimal_reference` with a
    reproduction caveat.
- Cut rule: if implementation sanity is unclear, do not put it in the paper.

### B10: Figure 1 Finding Preview

- Goal: make the first figure match the current paper argument.
- Panels:
  - D3 inversion on Musical;
  - matched-capacity GRID capacity/aliasing shift;
  - fixed-reranker D3 grounding;
  - All_Beauty/Sports portability plus qualified aliasing support.
- Success criterion: the figure can be read as the paper's diagnostic argument
  in miniature, while the caption still states that D6/D7 are extension hooks.

### B7: Third Vertical Learned/Export Row

- Claim tested: whether the D3 inversion/dataset-dependence story survives
  beyond Musical and All_Beauty.
- Preferred datasets: Books, Beauty_and_Personal_Care, or Sports_and_Outdoors.
- Admission criteria:
  - real learned/export SID row, not only proxy/control;
  - complete metadata and interaction joins;
  - D1-D5/D3 metrics;
  - clear caveat if category metadata is coarse or taxonomy-driven.
- Success criterion:
  - consistent with Musical/All_Beauty: stronger cross-vertical diagnostic
    inversion;
  - inconsistent: valuable dataset-dependence finding;
  - blocked by artifacts: document the gap and do not overstate Sports/MovieLens.

Current status: done locally for `Sports_and_Outdoors` with a real GRID/RQ-KMeans
feature-text export. The 20,000-item run has zero coverage gaps, 8,165 unique
full SIDs, duplicate SID rate `0.59175`, D3 L1 weighted `0.054982`, D4 tail
unique ratio `0.652840`, and D5 prefixes `128;7986;8165`. See
`docs/SPORTS_GRID_THIRD_VERTICAL.md`. This closes the third-vertical GRID
portability gap, but it does not add a third named tokenizer.

### B8: Qualified Aliasing As Backup Finding

- Claim tested: mapping-level diagnostics can flag interaction-qualified
  aliasing risk before generator training.
- Existing evidence: controlled qualified-aliasing probe reports co-occurrence
  aliases at `3.86x` risk versus hash aliases at `1.19x`.
- Next writing task: make it explicit that SIDInspector is not rediscovering
  "collisions are unequal"; it provides an adapter-level way to measure
  collision qualification before downstream generator training.
- Paper role: backup memorable finding if D3 grounding remains proxy-only.

Current status: read-only B8 review passed with strict wording. The evidence can
support `interaction-qualified aliasing early warning`: GRID feature-text
collision pairs have `3.86x` train co-occurrence lift over popularity-matched
non-collision pairs, while hash has `1.19x`. It cannot support causal
collision-harm or QuaSID reproduction claims.

### MovieLens Sanity Portability

- Role: defensive portability support, not a core finding.
- Current status: completed from existing local artifacts in
  `docs/MOVIELENS_D3_SANITY_SUMMARY.md`.
- Key result: category-prefix D3 `0.2788`, popularity-balanced D3 `0.7698`,
  mod-collision hash D3 `0.0038`, with zero coverage gaps.
- Claim boundary: non-Amazon schema/probe portability only; not learned SID
  tokenizer evidence and not Recall/NDCG validation.

## 17-Day Schedule

| Date | Main work | Output | Decision |
|---|---|---|---|
| 2026-05-20 | Plan reset; fix SIDInspector naming; define lift package | this document; tracker update | aggressive path selected |
| 2026-05-21 | B1 paper rewrite | abstract/§1/§4/Fig. 1 emphasize D3 inversion | compile and claim audit |
| 2026-05-22 | B2 AutoDL matched-capacity launch; B4 preflight | matched GRID status; vertical asset table | completed early on 2026-05-20 |
| 2026-05-23 | B4 first feasible vertical D3 run or gap closure | D3 replication/gap note | completed early for All_Beauty; decide whether to add one sentence |
| 2026-05-24 | B3 Musical D3-vs-ranking setup | bounded evaluator smoke | go/cut correlation experiment |
| 2026-05-25 | B3 result or cut; B5 feasibility screen | correlation note; reference-impl decision | decide if B5 starts |
| 2026-05-26 | B5 implementation if still worthwhile; otherwise paper integration | adapter/probe artifact or cut note | no weak named-method claims |
| 2026-05-27 | B6 small ranking validation + B7 third-vertical preflight | ranking-grounding note; third-vertical go/no-go | decide whether evidence can enter main paper |
| 2026-05-28 | Sixth-round closure: W2 wording, All_Beauty B6 replication, RQ-VAE-min gate | updated paper/doc/code paths or gap notes | decide whether Lift 5 enters paper |
| 2026-05-29 | Figure/table redesign and response to review | Fig. 1/Table 2/Table 3 final candidates | strict claim audit |
| 2026-05-30 | CIKM abstract submission + abstract freeze | EasyChair abstract | freeze abstract wording |
| 2026-05-31 | Artifact cleanup / packaging | reviewer quickstart and manifest | clean checkout target |
| 2026-06-01 | External read-through | reviewer notes | patch only evidence-backed issues |
| 2026-06-02 | Final paper edits | submission PDF candidate | no new experiments unless P0 |
| 2026-06-03 | Citation and metadata audit | author metadata, BibTeX, GenAI disclosure | submission hygiene |
| 2026-06-04 | Clean checkout and zip/package verification | reproducibility report | release candidate |
| 2026-06-05 | Final simulated review and diff freeze | final issues list | only P0/P1 fixes |
| 2026-06-06 | Paper submission | final PDF + artifact link | submit |

## Risk Policy

This is an optimistic plan, not a promise that every result will support the
preferred story. The acceptable outcomes are:

- B1 succeeds alone: stronger 6.5--7 path.
- B1+B2 succeeds: credible 7--7.5 path.
- B1+B2+B3 or B4 succeeds: real 8/10 attempt. As of 2026-05-20 evening, B1,
  B2, B3-context, and B4 have completed under their scoped claim boundaries.
- B1 fails under review or evidence: do not force CIKM; pivot to a longer WSDM
  version.

The discipline is to run more, but only claim what survives.
