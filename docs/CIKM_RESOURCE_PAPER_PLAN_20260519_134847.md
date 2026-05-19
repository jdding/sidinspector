# CIKM Resource Paper Plan

Timestamp: 2026-05-19 12:41:13 CST

Working title:

> AUDIT-SID: Artifact-Level Diagnostics for Semantic-ID Tokenizers in
> Generative Recommendation

## Claim-Evidence Matrix

| Claim | Evidence | Status | Paper section |
|---|---|---|---|
| SID tokenizers need artifact-level diagnostics beyond Recall@K/NDCG | Project spec, literature survey, method cluster audit | framing supported; cite verification still needed | §1 |
| AUDIT-SID provides a reusable mapping-first interface and D1-D5a artifact diagnostics | `src/audit_sid/interface.py`, `src/audit_sid/metrics.py`, adapter docs | supported by code and local tests | §2 |
| The toolkit can ingest real public SID artifacts from both a canonical RQ-style exporter and a recent tokenizer/codebook method | GRID All_Beauty exports; ReSID Musical GAOQ export; GRID Musical controlled feature-text row | supported; same-item-universe diagnostic row added, but not faithful raw-text TIGER/GRID reproduction | §3 |
| D3 now measures semantic-collaborative mismatch using co-occurrence, not only metadata purity | `docs/D3_COLLABORATIVE_ALIGNMENT.md`, `tests/test_metrics.py` | supported | §2/§3 |
| Case study shows diagnostics expose distinct failure modes: collision collapse, prefix-depth neighborhood mismatch, and head/tail capacity | `docs/GRID_MUSICAL_SAME_DATASET_CPU.md`, `docs/CASE_STUDY_RESID_VS_SANITY.md` | supported diagnostically; main table is same-item Musical, ReSID/sanity controls are secondary | §3 |
| Optional D6 can inspect continual-tokenizer churn | `docs/DACT_DRIFT_SMOKE.md`, `tools/autodl_audit_sid/compute_sid_churn.py` | optional appendix/short note only; not main evidence | §4 or omit |
| The current artifact is a resource-demo, not a same-dataset leaderboard | `docs/GATE0A_EVIDENCE_MATRIX.md`, `docs/GRID_MUSICAL_SAME_DATASET_CPU.md` | must be stated explicitly | §4 |

## Abstract Draft

Semantic-ID tokenizers have become a central component of generative
recommendation, where items are mapped into discrete code sequences and
retrieved through sequence generation. Existing evaluations mostly report final
ranking metrics, leaving tokenizer artifacts themselves under-diagnosed: a
method can have acceptable aggregate Recall@K while hiding codebook collapse,
harmful collisions, poor collaborative neighborhood alignment, or inefficient
prefix structure. We present AUDIT-SID, a mapping-first diagnostic toolkit for
semantic-ID tokenizer artifacts. AUDIT-SID standardizes item-to-SID mappings, metadata,
and interaction histories, and computes five diagnostics: codebook utilization,
collision profile, semantic-collaborative alignment, head-tail capacity
allocation, and lightweight trie/deployment-cost proxies. In public Amazon
resource demos, AUDIT-SID ingests a GRID/RQ-KMeans-style export and a ReSID/GAOQ
export, and provides controlled sanity tokenizers for interpretation. A
same-item-universe Musical diagnostic row shows that the toolkit can compare
an official GRID residual-k-means export over processed feature text with
ReSID/GAOQ on the same items, exposing sharply different collision, prefix, and
head-tail capacity profiles. These results illustrate AUDIT-SID's value as a
reproducible resource for inspecting SID tokenizer artifacts, while also
clarifying the limits of current evidence: the paper is a toolkit and
diagnostic case study, not a new tokenizer, a faithful TIGER reproduction, or a
same-dataset leaderboard.

## Scope Sentence

Use this in §2 or §4:

> AUDIT-SID covers six artifact-level failure dimensions: capacity utilization,
> collision profile, semantic-collaborative alignment, head-tail allocation,
> deployment-cost proxy, and drift stability. These diagnostics target
> tokenizer artifacts before or alongside downstream model evaluation.

Do not write that D1-D6 cover complete SID system quality.

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
  2. D1-D5a diagnostic suite;
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
- D1-D5a definitions:
  - D1 utilization: entropy/Gini/dead-code style summaries;
  - D2a collision profile: full SID and prefix collisions;
  - D2b interaction-qualified collision harm: future extension unless bounded
    implementation is added;
  - D3 semantic-collaborative alignment: co-occurrence top-k prefix recall plus
    category purity auxiliary column;
  - D4 head/mid/tail capacity;
  - D5a SID length, prefix fan-out, duplicate SID rate.
- Optional D6: SID churn/drift across tokenizer refreshes.
- Future D5b/D7 when `generator_outputs` are available: next-token entropy,
  SID likelihood, invalid path rate, and generated candidate duplication.

Figure/table:

- Figure 1: generated vector dataflow from tokenizer artifacts to D1-D5a/D6/D7
  boundary.

### §3 Resource Demo and Case Study

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
- ReSID/sanity non-redundancy controls from
  `docs/CASE_STUDY_RESID_VS_SANITY.md`.
- Main reading: diagnostics distinguish collision collapse, metadata grouping,
  collaborative prefix alignment, and head/tail capacity.

Tables:

- Table 1: method coverage and artifact availability.
- Table 2: GRID Musical feature-text row vs ReSID Musical diagnostic table.
- Table 3: reviewer-facing artifact package checklist.
- ReSID/sanity non-redundancy controls stay in the artifact repo.

### §4 Resource Availability, Limitations, and Conclusion

Length target: 1.2 pages.

Content:

- GitHub/artifact package contents.
- Table 3 reviewer-facing package checklist.
- Reviewer workflow: inspect manifest, rerun metric command, inspect failure
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
  - no downstream generator-output D5b/D7 in v0;
  - D6 is optional continual-tokenization evidence;
  - online impact, full generator training dynamics, multi-task search-rec
    quality, and industrial policy/fairness are out of scope.
- Conclusion: resource-first contribution; future work extends same-dataset
  method coverage, generator outputs, and drift diagnostics.

## Figure and Table Plan

| ID | Type | Description | Source | Priority |
|---|---|---|---|---|
| Fig. 1 | generated vector pipeline | Normalized SID artifacts flow into validation, D1-D5a diagnostics, optional D6, and future D7 | `paper/figures/fig1_audit_sid_pipeline.pdf` | high |
| Table 1 | method/facet coverage | Facet, representative anchors, v0 evidence role, diagnostics, and claim boundary | `paper/sections/2_toolkit.tex` | high |
| Table 2 | diagnostic case study | GRID Musical feature-text row vs bounded ReSID Musical diagnostic profile | `paper_assets/tables/table2_musical_diagnostic.*` | high |
| Table 3 | artifact package | Reviewer-facing artifact package and provenance surface | `paper/sections/4_availability_limits.tex` | high |
| Supplement table | ReSID/sanity controls | ReSID vs sanity D2/D3v2/D4/D5a compact table | `paper_assets/tables/table3_sanity_controls.*` | artifact repo |
| Supplement table | GRID scale/stability | All_Beauty 20k seeds and 50k seed summary | `paper_assets/tables/table4_grid_scale.*` | artifact repo |
| Supplement table | D6 churn | DACT Tools 0.6 -> 0.7 common-item SID churn and rare full collisions | `paper_assets/tables/table5_dact_d6_churn.*` | artifact repo |
| Supplement table | MovieLens portability | non-Amazon schema smoke | `paper_assets/tables/table6_movielens_portability.*` | artifact repo |

Do not plan a conventional appendix. If space remains, include only a compact
artifact checklist in §4.

## Red Lines

Do not write:

- "we reproduce ReSID on Sports";
- "CARD results" for the compact feature proxy;
- "D2 proves downstream harm";
- "D3v2 is validated as monotonic with Recall/NDCG";
- "D1-D6 cover complete SID system quality";
- "D5a measures real generator serving cost";
- "GRID feature-text row is a faithful raw-text TIGER/GRID reproduction";
- "seed-stable superiority" for ReSID Musical.
- "DACT replaces the Cluster B main line".

Safe title/abstract stance:

- open diagnostic toolkit;
- artifact-level inspection;
- resource-demo case study;
- method coverage table with explicit caveats.
