# CIKM Resource Paper Plan

Timestamp: 2026-05-20 02:17:10 CST

Working title:

> SIDInspector: A Mapping-First Diagnostic Resource for Semantic-ID Tokenizers

Naming decision: `SIDInspector` is the paper-facing name. `AUDIT-SID` remains the
internal repository/project history name and should not be globally renamed
before submission.

## Framing Decision

Current decision: SIDInspector / AUDIT-SID CIKM v0 is a **diagnostic / interface resource**,
not a RecBole/BARS-style coverage resource. The paper should be judged by
whether a new SID method can plug into the mapping-first adapter contract and
receive useful D1-D5 diagnostic probes, not by the number of named tokenizers already
covered.

2026-05-20 17-day lift update: the paper plan now targets a more ambitious
8/10 attempt rather than a minimal closure path. The main finding should be
the D3 category-prefix inversion: a deterministic category-prefix row has
higher D3 co-occurrence prefix alignment than the current learned/exported
rows in the Musical worked example. The evidence package should aggressively
defend this finding through matched-capacity GRID, vertical replication
preflight, and bounded D3-vs-ranking context where feasible. See
`docs/CIKM_17_DAY_8PT_LIFT_PLAN.md`.

Consequences:

- GRID and ReSID are worked examples / public export paths.
- controlled mechanism probes are first-class diagnostic evidence, not degraded
  substitutes for missing methods.
- Table 1 should read as evidence-role and adapter-status coverage, not as a
  leaderboard coverage table.
- Type 1 coverage-resource ambitions are a future platform route after more
  faithful adapters or author-provided mappings exist.

Source of truth: `docs/RESOURCE_FRAMING_DECISION.md`.

## Claim-Evidence Matrix

| Claim | Evidence | Status | Paper section |
|---|---|---|---|
| SID tokenizers need artifact-level diagnostics beyond Recall@K/NDCG | Project spec, literature survey, method cluster audit | framing supported; cite verification still needed | §1 |
| SIDInspector provides a reusable mapping-first interface and D1-D5 artifact diagnostic probes | `src/audit_sid/interface.py`, `src/audit_sid/metrics.py`, adapter docs | supported by code and local tests | §2 |
| The toolkit can ingest public SID export paths through a reusable adapter contract | GRID All_Beauty exports; ReSID Musical GAOQ export; GRID Musical controlled feature-text row | supported as worked examples, not coverage-resource breadth | §2/§3 |
| D3 now measures semantic-collaborative mismatch using co-occurrence, not only metadata purity | `docs/D3_COLLABORATIVE_ALIGNMENT.md`, `tests/test_metrics.py` | supported | §2/§3 |
| Worked example and controlled mechanism probes show diagnostics expose distinct failure modes: collision collapse, prefix-depth neighborhood mismatch, and head/tail capacity | `docs/GRID_MUSICAL_SAME_DATASET_CPU.md`, `docs/CASE_STUDY_RESID_VS_SANITY.md`, `docs/QUALIFIED_COLLISION_PROBE.md`, `docs/CAPACITY_BUDGET_SWEEP.md`, `docs/VARIABLE_DEPTH_COST_PROBE.md` | supported diagnostically; probes validate mechanism sensitivity but are not named-method coverage | §3 |
| Optional D6 can inspect continual-tokenizer churn | `docs/DACT_DRIFT_SMOKE.md`, `tools/autodl_audit_sid/compute_sid_churn.py` | optional appendix/short note only; not main evidence | §4 or omit |
| The current artifact is a resource-demo, not a same-dataset leaderboard | `docs/GATE0A_EVIDENCE_MATRIX.md`, `docs/GRID_MUSICAL_SAME_DATASET_CPU.md` | must be stated explicitly | §4 |

## Strong-Accept Lift Plan

The current draft is externally reviewed at 8.0--8.1/10 under a conservative
Resource Track framing. After the 2026-05-20 framing decision, the first lift is
not more method-count coverage; it is making the adapter/interface resource
shape unmistakable. Only after that should we consider extra reference
implementations or named-method adapters.

| Lift item | Why it helps | Minimum evidence | PDF impact |
|---|---|---|---|
| Adapter specification | makes the Type 4 resource shape explicit | required adapter outputs, validator gates, extension workflow | add/strengthen §2 paragraph or compact table |
| Mechanism-probe reframing | upgrades stressors from fallback evidence to diagnostic validation | qualified collision, capacity budget, variable depth probes | rename Table 3 and rewrite §3 narrative |
| Worked-example wording | prevents two-method leaderboard reading | GRID/ReSID framed as public export paths, not central contribution | abstract and §3 title/opening |
| Optional reference implementation | useful only after reframing | minimal RQ reference implementation with `IMPL_NOTES.md`, not named reproduction | repository artifact; optional paper mention |
| Third true named tokenizer facet | future Type 1/platform bridge | one faithful B2/B3 method with joinable SID export | Table 1 update only if real |

Do not reopen the Sports ReSID GAOQ bottleneck unless a bounded CPU/GPU path is
first proven. FAMAE-only checkpoints are useful assets but are not item-to-SID
seed evidence.

Execution update: `docs/B2_B3_METHOD_SCREEN.md` did not find a safe third
named tokenizer for current main evidence. QuaSID/AdaSID/CapsID remain
coverage/motivation, DIGER is incomplete for artifact export, and CARD remains
proxy/control unless the original `nu-rq-vae` path is repaired. The current
evidence lift should therefore use `docs/GRID_MUSICAL_3SEED_LOCAL.md` for
same-dataset stability rather than forcing a proxy method into Table 2.

## Abstract Draft

Current abstract logic: start from the missing inspection interface for
exported item-to-code artifacts, then introduce SIDInspector as the reusable
adapter/validator/probe resource, then use the Musical worked example and
controlled mechanism probes as evidence. This avoids inviting a downstream
Recall/NDCG-correlation burden while retaining numeric evidence anchors.

Key abstract anchors now in `paper/main.tex`:

- 23,742-item Musical worked example;
- GRID/RQ-KMeans-style feature-text row: 3,749 unique full codes and 0.9769
  full-code aliasing rate;
- GRID three-seed full-code aliasing stability: 0.9751--0.9769;
- bounded ReSID/GAOQ export: aliasing-free in its exported mapping and higher
  collaborative-prefix recovery;
- mechanism probes separate raw aliasing volume, interaction-qualified
  aliasing risk, head-to-tail capacity, and active-prefix cost.

## Scope Sentence

Use this in §2 or §4:

> AUDIT-SID implements five mapping-level diagnostic probes: D1 utilization,
> D2 aliasing, D3 neighborhood alignment, D4 popularity allocation, and D5
> structural cost. D6 temporal churn is available when paired tokenizer
> snapshots exist, and D7 generation traces are reserved for artifacts that
> expose generated candidates or beam logs.

Do not write that D1-D7 are all implemented or that they cover complete SID
system quality.

## Four-Page Structure

Format constraint:

- CIKM Resource paper is a strict 4-page PDF including appendices and
  acknowledgments.
- References and GenAI Usage Disclosure do not count toward the 4-page limit.
- Design the paper as if no appendix is available. Core evidence must appear in
  the 4-page body; full CSVs, logs, commands, and extra examples belong in the
  GitHub artifact.

### §1 Introduction

Length target: 0.8 pages.

Content:

- SID tokenizers/codebooks are now a real bottleneck in generative
  recommendation.
- Final ranking metrics do not reveal why a tokenizer fails on collisions,
  neighborhoods, tail capacity, or decoding cost.
- Contribution list:
  1. a public mapping-first SID artifact interface;
  2. D1-D5 diagnostic-probe suite;
  3. public resource-demo evidence on GRID/ReSID/sanity artifacts, including
     one same-item-universe Musical diagnostic row;
  4. honest limitations and method-coverage table.

Required citations to verify:

- TIGER / generative retrieval with semantic IDs [VERIFY].
- ReSID [VERIFY].
- GRID or RQ/RVQ semantic-ID exporter [VERIFY].
- CARD/DIGER/CapsID-style recent tokenizer innovations [VERIFY].

### §2 Toolkit and Diagnostics

Length target: 1.1 pages.

Content:

- Input schema: `sid_assignments`, `item_metadata`, `interactions`, optional
  `generator_outputs`.
- Adapter pattern: ReSID, GRID, CARD/control, sanity.
- D1-D5 definitions:
  - D1 utilization: entropy/Gini/dead-code style summaries;
  - D2 aliasing: full SID and prefix collisions, plus bounded interaction-qualified calibration;
  - D3 neighborhood alignment: co-occurrence top-k prefix recall plus category purity auxiliary column;
  - D4 popularity allocation: head/mid/tail capacity and prefix allocation;
  - D5 structural cost: SID length, prefix fan-out, duplicate SID rate.
- Optional D6 temporal churn: SID churn/drift across tokenizer refreshes.
- Future D7 generation traces when `generator_outputs` are available:
  next-token entropy, SID likelihood, invalid path rate, and generated
  candidate duplication.
- Adapter specification:
  - minimum adapter output is normalized `sid_assignments`;
  - optional enrichments are `item_metadata`, `interactions`, refresh pairs, and
    `generator_outputs`;
  - validator gates check stable keys, missing mappings, duplicate keys,
    consistent depth, and evidence-role provenance;
  - a new method enters Table 1 as an adapter row only after the validator
    passes and its evidence role is declared.

Figure/table:

- Figure 1: generated vector dataflow from tokenizer artifacts to D1-D5 probes,
  optional D6 churn, and future D7 traces
  boundary.

### §3 Worked Example and Mechanism Probes

Length target: 1.25 pages.

Content:

- Method coverage table:
  - GRID official-module RQ-KMeans on All_Beauty;
  - ReSID GAOQ on Musical_Instruments;
  - GRID official-module RQ-KMeans on the same Musical item universe using
    processed feature text;
  - sanity lower bounds;
  - CARD/DIGER listed as controlled/backlog/future support, not main evidence.
- Main case-study table from `docs/GRID_MUSICAL_SAME_DATASET_CPU.md`.
- Stability support from `docs/GRID_MUSICAL_3SEED_LOCAL.md` if there is room
  for one compact variance sentence.
- ReSID/sanity non-redundancy controls from
  `docs/CASE_STUDY_RESID_VS_SANITY.md`.
- Main reading: the worked example shows how an adapter emits comparable audit
  artifacts, and the mechanism probes show that diagnostics respond to
  controlled collision/capacity/depth changes.

Tables:

- Table 1: adapter/evidence-role coverage and supported diagnostics.
- Table 2: GRID Musical feature-text row vs ReSID Musical worked example.
- Table 3: controlled mechanism probes.
- ReSID/sanity non-redundancy controls stay in the artifact repo.

### §4 Resource Availability, Limitations, and Conclusion

Length target: 1.2 pages.

Content:

- GitHub/artifact package contents.
- Clean-checkout verifier paragraph and reviewer workflow: inspect manifest,
  rerun metric command, inspect failure
  slices.
- Claim discipline: separate mapping statements, diagnostic statements, and
  system-quality statements.
- Reproducibility notes: scripts, metrics, ignored large artifacts, public data.
- Limitations:
  - GRID Musical same-item-universe row uses ReSID processed feature text, not
    raw Amazon title/review text;
  - ReSID Sports exact balanced GAOQ stopped due CPU-bound constrained k-means;
  - D2 remains a collision profile, not strict causal harm;
  - D3v2 is a diagnostic proxy and is not yet validated as monotonic with
    Recall/NDCG;
  - no downstream generator-output D7 in v0;
  - D6 is optional continual-tokenization evidence;
  - online impact, full generator training dynamics, multi-task search-rec
    quality, and industrial policy/fairness are out of scope.
- Conclusion: resource-first contribution; future work extends same-dataset
  method coverage, generator outputs, and drift diagnostics.

## Figure and Table Plan

| ID | Type | Description | Source | Priority |
|---|---|---|---|---|
| Fig. 1 | generated vector pipeline | Normalized SID artifacts flow into validation, D1-D5 diagnostic probes, optional D6, and future D7 | `paper/figures/fig1_audit_sid_pipeline.pdf` | high |
| Table 1 | method/facet coverage | Facet, representative anchors, v0 evidence role, diagnostics, and claim boundary | `paper/sections/2_toolkit.tex` | high |
| Table 2 | diagnostic case study | GRID Musical feature-text row vs bounded ReSID Musical diagnostic profile | `paper_assets/tables/table2_musical_diagnostic.*` | high |
| Table 3 | controlled mechanism probes | Qualified collision, capacity budget, and variable-depth signals | `paper/sections/4_demonstration.tex`, `paper_assets/tables/table8_qualified_collision_probe.*`, `paper_assets/tables/table9_capacity_budget_sweep.*`, `paper_assets/tables/table10_variable_depth_cost_probe.*` | high |
| Supplement table | ReSID/sanity controls | ReSID vs sanity D2/D3/D4/D5 compact table | `paper_assets/tables/table3_sanity_controls.*` | artifact repo |
| Supplement table | GRID scale/stability | All_Beauty 20k seeds and 50k seed summary | `paper_assets/tables/table4_grid_scale.*` | artifact repo |
| Supplement table | D6 churn | DACT Tools 0.6 -> 0.7 common-item SID churn and rare full collisions | `paper_assets/tables/table5_dact_d6_churn.*` | artifact repo |
| Supplement table | MovieLens portability | non-Amazon schema smoke | `paper_assets/tables/table6_movielens_portability.*` | artifact repo |

Do not plan a conventional appendix. If space remains, include only a compact
verifier/resource-availability paragraph in §5. The current paper has no Table
4.

## Red Lines

Do not write:

- "we reproduce ReSID on Sports";
- "CARD results" for the compact feature proxy;
- "D2 proves downstream harm";
- "D3v2 is validated as monotonic with Recall/NDCG";
- "D1-D7 cover complete SID system quality";
- "D5 measures real generator serving latency";
- "GRID feature-text row is a faithful raw-text TIGER/GRID reproduction";
- "seed-stable superiority" for ReSID Musical.
- "DACT replaces the Cluster B main line".

Safe title/abstract stance:

- open diagnostic toolkit;
- artifact-level inspection;
- resource-demo case study;
- method coverage table with explicit caveats.
