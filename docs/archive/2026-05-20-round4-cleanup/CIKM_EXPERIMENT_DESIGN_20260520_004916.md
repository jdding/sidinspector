# CIKM Experiment Design For AUDIT-SID

Timestamp: 2026-05-19 12:29:57 CST

Strong-accept planning update: 2026-05-19 15:36:33 CST

Execution update: 2026-05-19 15:58:57 CST. The B2/B3 third-method screen
found no low-risk new main-evidence tokenizer; local work therefore shifted to
same-dataset stability, adding GRID Musical feature-text seeds 43/44 to seed
42.

Closure update: 2026-05-19 16:26:26 CST. The current v0 experiment package is
closed. No additional local or GPU run is required before the next paper
writing/review iteration; remaining work is citation drift, real single-blind
metadata, final copy-editing, and claim audit after text changes.

Round 4 paper-sync update: 2026-05-20 00:49:16 CST. Current paper source uses
Fig. 1 as a pipeline plus diagnostic preview, Table 1 as evidence-only
facet/status coverage, Table 2 as the same-item Musical diagnostic table with
sanity rows and GRID three-seed mean/variance, and Table 3 as a controlled
stressor signal table. The older reviewer-artifact Table 4 has been deleted;
clean-checkout verification is summarized in Section 5. Gate 3 wording remains
resource-scoped diagnostic separability, not the original downstream-metric
Gate 3 pass.

## Target Claim

AUDIT-SID should be submitted as a Resource Track paper about a reusable SID artifact audit toolkit.

Primary claim:

> A mapping-first diagnostic toolkit can standardize SID tokenizer artifacts and expose collision, collaborative-alignment, head-tail capacity, and deployment-cost failure modes that final Recall/NDCG alone do not reveal.

Anti-claims:

- not a new tokenizer;
- not a leaderboard;
- not a faithful TIGER reproduction;
- not a downstream superiority claim.

## Must-Run Experiment Blocks

Scope rule:

- Main paper diagnostics are D1-D5a over `item -> SID` artifacts.
- D6 drift/churn is optional.
- D7 generator/retrieval behavior is a future/interface diagnostic that requires
  `generator_outputs`.
- D2 is reported as collision profile in v0; the bounded qualified-collision
  controller adds D2b calibration evidence but does not prove causal downstream
  harm.
- Generator predictability, invalid generated paths, and candidate duplication
  require `generator_outputs`; treat old D5b wording as future D7.

### B1: Artifact Interface Coverage

- Purpose: show the toolkit can ingest real public SID artifacts.
- Systems: GRID/RQ-KMeans, ReSID/GAOQ, sanity baselines.
- Metrics: coverage report plus supported diagnostics.
- Table target: Method Coverage Table.
- Success: every main method has `sid_assignments`, `item_metadata`, and `interactions` joinable with zero missing SID joins.

### B2: Same-Item-Universe Diagnostic Case Study

- Purpose: answer the strongest audit concern: A/B evidence must share a dataset.
- Dataset: ReSID processed Amazon-2023 `Musical_Instruments`.
- Systems: GRID official MiniBatchKMeans over processed feature-text embeddings; ReSID balanced GAOQ; sanity controls if space allows.
- Metrics: D1, D2, D3v2, D4, D5a.
- Table target: Main paper Table 2.
- Success: the table shows non-redundant differences across collision, collaborative alignment, and head-tail capacity.
- Caveat: GRID Musical is a controlled diagnostic row, not raw-text TIGER/GRID reproduction.
- Stability update: GRID Musical feature-text now has seeds 42/43/44 with
  complete joins and stable high collision pressure. Use
  `docs/GRID_MUSICAL_3SEED_LOCAL.md` as the source if the paper needs a compact
  variance statement.

### B3: Metric Non-Redundancy And Sanity Controls

- Purpose: show D1-D5a are not one repeated statistic.
- Dataset: Musical.
- Systems: ReSID plus category-prefix, mod-collision hash, popularity-balanced controls.
- Metrics: D2 collision, D3v2, D4, D5a.
- Table target: appendix or compressed main table.
- Success: collision-heavy, category-heavy, and popularity-balanced controls are separated by different diagnostics.

Required readings in the table narrative:

- D2 catches collision collapse but does not by itself prove causal downstream harm.
- D3 separates semantic grouping from collaborative co-occurrence alignment.
- D4 must appear in the main table because head/tail capacity is central to
  recommender SID quality.
- D5a is a structural trie/prefix cost proxy without generator outputs.

### B4: Scale/Stability Evidence

- Purpose: show the canonical exporter works beyond toy size.
- Dataset: All_Beauty.
- Systems: GRID/RQ-KMeans 20k seeds 42/43/44; 50k seed42 optional.
- Metrics: D1-D5a summary, duplicate SID rate, D3v2.
- Table target: appendix or one compact robustness row.
- Success: 20k seed range is reported; 50k is marked preliminary unless more seeds are added.

### B5: Portability/Optional Extensions

- DACT D6 churn: optional drift/churn note.
- MovieLens portability: optional schema smoke only.
- AutoDL sync/provenance: artifact reproducibility note, not an experiment result.

## Strong-Accept Lift Package

Current external simulated review is 8.0--8.1/10. The limiting factor is not
claim discipline or artifact packaging; it is method/evidence breadth. The
following tasks are not required for the current external-8 gate, but they are
the most plausible path toward an 8.5-style strong Resource Track review.

Closure status: executed for v0 as far as current public/local evidence allows.
L1 closed negative; L2/L3/L5 closed with the current same-item panel,
three-seed GRID Musical stability, and redesigned Fig. 1. L4 is now a writing
and claim-discipline task, not an experiment blocker.

### L1: Third Real Named Tokenizer Facet

- Goal: add one additional true named tokenizer/codebook method beyond
  GRID/RQ-KMeans and ReSID.
- Screening table: `docs/METHOD_DIAGNOSTIC_SELECTION_MATRIX.md`.
- Preferred facets: B2 collision/capacity or B3 ranking/retrieval alignment.
- Candidate order:
  1. QuaSID/AdaSID/CapsID/CARD if a faithful item-to-SID export is practical;
  2. DIGER or joint search-rec SID if a mapping export exists without training
     a full generator;
  3. CARD only if it can be presented as a faithful named-method artifact, not
     as the current compact feature proxy.
- Success criterion: joinable `sid_assignments`, `item_metadata`, and
  `interactions` plus at least D1/D2/D3v2/D4/D5a or a clearly justified subset.
- Failure interpretation: keep the method in Table 1 as literature/backlog; do
  not force a proxy into main evidence.
- Current screen result: `docs/B2_B3_METHOD_SCREEN.md` closes the current
  screen with no new main-evidence method. QuaSID/AdaSID/CapsID are
  paper/motivation only in this pass, DIGER is incomplete for artifact export,
  and CARD remains proxy/control unless the original `nu-rq-vae` path is
  repaired and reviewed.

### L2: Same-Dataset A/B Panel

- Goal: strengthen the current same-item Musical comparison into a compact A/B
  panel rather than a two-row anecdote.
- Minimum content:
  - GRID feature-text Musical;
  - ReSID GAOQ Musical;
  - sanity controls as calibration rows in artifact tables;
  - optional third named method if L1 succeeds.
- Metrics: D2 full collision, D3 L1 collaborative prefix recall, D4 head/tail
  unique capacity, D5a prefix counts.
- Main-paper target: either an upgraded Table 2 or a small two-panel Fig. 2 if
  page budget allows.
- Safe claim: diagnostics expose capacity/collision/alignment tradeoffs on the
  same item universe.
- Unsafe claim: downstream recommendation superiority or faithful TIGER
  reproduction.

### L3: Stability And Vertical Breadth

- Existing evidence:
  - GRID All_Beauty 20k has three seeds: duplicate SID rate 0.1524--0.1748.
  - GRID Musical feature-text now has three local CPU seeds: duplicate SID rate
    0.8327--0.8421 and full-collision rate 0.9751--0.9769.
  - GRID All_Beauty 50k seed42 is available as scale evidence.
  - MovieLens-25M bounded smoke supports schema portability, not tokenizer
    quality.
  - DACT Tools smoke supports optional D6 churn.
- Stronger target:
  - pull the GRID 20k three-seed summary into the reviewer resource directory
    and cite it explicitly in §4;
  - add one compact variance statement if the body can absorb it;
  - run ReSID additional seeds only if GAOQ mapping can be completed without
    re-opening the Sports CPU bottleneck.
- Do not treat FAMAE-only checkpoints as seed-stability evidence until GAOQ
  item-to-SID mappings exist.

### L4: Finding Sharpening

Candidate findings to write as diagnostic findings, not model-quality claims:

1. Collision-free capacity and collaborative prefix alignment are different
   objectives: ReSID Musical has zero full collisions but weaker D3 L1
   co-occurrence prefix recall than category-prefix sanity.
2. Same-item GRID feature-text vs ReSID exposes severe capacity/collision
   contrast: 3,749 vs 23,742 unique SIDs on 23,742 items.
3. Prefix depth matters: popularity-balanced sanity can look reasonable at
   depth 1 while collapsing at deeper prefix recall.

Each finding needs a direct table/figure hook and an explicit limitation
sentence.

## Fig. 1 Redesign Brief

Current Fig. 1 is serviceable but too linear. Redesign it only if it can make a
stronger 10-second argument:

- Claim supported: AUDIT-SID is an artifact-audit contract with diagnostics and
  evidence maturity levels, not just a data-processing pipeline.
- Reader takeaway: what inputs are required, what D1-D5a can be computed now,
  what D6/D7 require, and which evidence levels are main/control/backlog.
- Visual grammar: three-band schema:
  1. artifact contract inputs (`sid_assignments`, `item_metadata`,
     `interactions`, optional `generator_outputs`);
  2. diagnostic facets D1-D5a / optional D6 / future D7;
  3. evidence maturity output (`main named exports`, `controls`,
     `resource-only tables`, `future/backlog`).
- Review risk: avoid a decorative architecture diagram; the figure must reduce
  reviewer confusion about D5a/D7 and named-method evidence boundaries.

## Paper Tables

| Table | Required | Content | Source |
|---|---|---|---|
| Fig. 1 | yes | Generated vector artifact pipeline and D1-D7 boundary | `paper/figures/fig1_audit_sid_pipeline.pdf` |
| Table 1 | yes | Facet-aware method coverage, evidence role, diagnostics, and claim boundary | `paper/sections/2_toolkit.tex` |
| Table 2 | yes | GRID Musical feature-text vs bounded ReSID Musical diagnostic profile plus sanity/calibration rows and GRID three-seed summary | `paper/sections/4_demonstration.tex`, `paper_assets/tables/table2_musical_diagnostic.*` |
| Table 3 | yes | Controlled stressor / diagnostic / baseline / under-stress signal table | `paper/sections/4_demonstration.tex`, `paper_assets/tables/table8_qualified_collision_probe.*`, `paper_assets/tables/table9_capacity_budget_sweep.*`, `paper_assets/tables/table10_variable_depth_cost_probe.*` |
| Artifact table | no | ReSID/sanity non-redundancy controls | `paper_assets/tables/table3_sanity_controls.*` |
| Artifact table | no | GRID All_Beauty scale/stability | `paper_assets/tables/table4_grid_scale.*` |
| Artifact table | no | DACT D6 churn | `paper_assets/tables/table5_dact_d6_churn.*` |

CIKM Resource Track counts appendices against the 4-page limit. Design the
submission with no required appendix. The current draft uses the four-page body
budget and moves references/GenAI disclosure after the body; optional result
tables live in the GitHub artifact. Section 5 carries the clean-checkout
verifier paragraph instead of a fourth table.

## Writing Plan

### Section 1: Introduction

Problem: SID tokenizers are evaluated mostly by final ranking metrics, while their artifact-level failure modes remain hidden.

Contributions:

1. standardized artifact interface;
2. D1-D5a diagnostics;
3. public method coverage and same-item-universe case study;
4. reproducible toolkit and explicit limitations.

### Section 2: Toolkit

Define:

- `sid_assignments`;
- `item_metadata`;
- `interactions`;
- optional `generator_outputs`;
- D1-D5a, optional D6, and future D7.

Use this exact scope sentence:

> AUDIT-SID covers a seven-axis artifact diagnostic plan: capacity utilization,
> collision profile, semantic-collaborative alignment, head-tail allocation,
> structural deployment-cost proxy, drift stability, and generator/retrieval
> behavior. The current v0 implements D1-D5a over item-to-SID mappings, includes
> optional D6 churn support, and reserves D7 for artifacts that expose generated
> candidates or beam traces.

Keep equations/tables short. The goal is reproducible resource clarity.

### Section 3: Experiments

Lead with Table 1 and Table 2.

Narrative:

- AUDIT-SID ingests both Cluster A and Cluster B artifacts.
- On the same Musical item universe, the diagnostics reveal sharply different capacity/collision/alignment profiles.
- Sanity baselines show why D2/D3/D4/D5a are non-redundant.

### Section 4: Limitations And Resource Release

State:

- GRID Musical uses processed feature text.
- TIGER is future support; GRID is used because it exposes a clean residual-quantization export path.
- D3v2 is a diagnostic proxy, not a downstream performance proof.
- D2 is a collision profile, not strict causal harm.
- D5a has no generator outputs and is therefore a structure-cost proxy.
- D6 is optional continual-tokenization evidence.
- D7 is not implemented in current evidence because no main artifact exposes
  per-user generated candidates or beam traces.
- Online impact, full generator training dynamics, multi-task search-rec, and
  industrial policy/fairness are out of scope.
- CARD proxy and DACT are not main evidence.

## Go / No-Go

Proceed to CIKM abstract if:

- citation metadata is verified;
- Table 1 and Table 2 are finalized;
- public artifact/reproduction instructions are clean enough for review.

Do not submit if:

- the paper drifts back into leaderboard claims;
- method caveats are hidden;
- the artifact package cannot reproduce at least the main diagnostic tables.
