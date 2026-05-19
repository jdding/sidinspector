# SID Cluster And Diagnostic Refresh

Timestamp: 2026-05-19 13:06:06 CST

Scope: update AUDIT-SID's method-cluster taxonomy after the 2026-05-19
reference refresh, with explicit implications for D1-D7 diagnostic coverage.
This supersedes the early broad taxonomy in `docs/SID_METHOD_CLUSTER_AUDIT.md`
where it conflicts.

## Bottom Line

The new literature does not create a need to abandon the current CIKM v0 method
set. It does change how we should describe the method space.

The old taxonomy over-compressed recent work into one large "Cluster B recent
tokenizer/codebook innovation" bucket. That was acceptable for Gate 0A, but it
is too coarse for the paper and for D1-D7 coverage planning.

The updated view:

- **Cluster A** remains canonical SID generation: RQ-VAE/RQ-KMeans/RVQ,
  TIGER-style, GRID-style.
- **Cluster B** should stay the main recent-tokenizer bucket, but it must be
  split into facets B1-B4 because different papers stress different diagnostic
  axes.
- **Cluster C** is temporal/drift/staleness.
- **Cluster D** is deployment/search/industrial use, mostly a diagnostic target
  rather than a CIKM v0 runnable method.
- **Reference-only layers** are needed for evaluation-tool and identifier
  foundations; they are not SID methods and should not be scored as such.

## Updated Taxonomy

### Reference Layer R0: Evaluation And Identifier Foundations

These papers justify the problem framing but are not method clusters for AUDIT-SID.

| Role | Papers | Use |
|---|---|---|
| Identifier/indexing foundation | How to Index Item IDs; Better Generalization with Semantic IDs | motivate learned IDs and ranking/deployment relevance |
| Diagnostic/toolkit precedent | RecList, Elliot | justify resource/toolkit evaluation beyond aggregate NDCG |
| Broad survey/context | generative search/recommendation surveys | optional related-work compression |

Do not include R0 papers in the Method Coverage Table as "methods to run".

### Cluster A: Canonical SID Generators

Role: baseline SID generation based on residual/vector quantization or similar
hierarchical discrete identifiers.

Representative methods:

- TIGER / RQ-VAE-style semantic IDs;
- GRID RQ-KMeans/RQ-VAE/RVQ paths;
- GenRec-style SID implementations;
- raw RQ-VAE/RQ-KMeans baselines.

Moved out or marked as bridge:

- LC-Rec is not a pure Cluster A baseline for AUDIT-SID taxonomy. It uses
  vector-quantized IDs, but its key motivation is collaborative semantics, so it
  should be cited under B1 or as an A-to-B bridge.

CIKM v0 role: must have at least one runnable A artifact. Current evidence uses
GRID official-module RQ-KMeans.

### Cluster B: Recent Tokenizer / Codebook Innovation

Cluster B remains the main "recent method" bucket, but paper-facing coverage
must expose its facets.

| Facet | Meaning | Representative papers | Primary diagnostics |
|---|---|---|---|
| B1 collaborative / predictability aligned | tokenizer should encode collaborative or sequence-predictive structure | ReSID, LC-Rec, CoST, LETTER, DiscRec | D3, D1, D4 |
| B2 collision / utilization / capacity aware | collision and codebook usage are explicit design targets | QuaSID, AdaSID, CARD, CapsID, HiD-VAE-style collision work | D1, D2, D4 |
| B3 ranking / differentiable / retrieval aligned | SID learning is tied to ranking/retrieval objectives or differentiability | DIGER, joint search-rec SID, CQ-SID-inspired work | D3, D5, D7 |
| B4 architecture / bottleneck aware | method changes SID length, routing, or input/output interface to reduce bottlenecks | AsymRec, CapsID, Long SID / ACERec-style work | D4, D5, D7 |

Important implication:

ReSID is a valid runnable B method because it covers B1 and some B2. But it does
not cover all B facets. Therefore the paper should not imply that "ReSID
represents all recent tokenizer innovation." It is the runnable B anchor, while
CARD/QuaSID/AdaSID/CapsID/AsymRec/DIGER explain why AUDIT-SID's diagnostics need
to cover more than ReSID's own claims.

### Cluster C: Temporal / Continual / Staleness

Role: SID mappings change as catalogs, interactions, or model updates evolve.

Representative papers:

- DACT;
- collaborative semantic ID staleness papers;
- controlled tokenizer refresh simulations.

Primary diagnostics:

- D6 churn/stability;
- D1/D2/D3 under before-after mappings;
- D4 churn by popularity bucket.

CIKM v0 role: optional. Current DACT smoke is useful evidence for the interface,
not a replacement for Cluster B.

### Cluster D: Deployment, Search, And Industrial SID Surfaces

Role: production and search/retrieval settings where SID artifacts interact with
latency, beam search, indexing, candidate generation, and multi-task surfaces.

Representative papers:

- Snapchat SID use cases;
- Better Generalization with Semantic IDs;
- joint search and recommendation SID;
- CQ-SID/search-oriented SID papers.

Primary diagnostics:

- D5 structural deployment proxy;
- D7 generator/retrieval behavior when outputs are available;
- D6 drift/staleness if production refresh is discussed.

CIKM v0 role: literature and resource motivation. Do not claim AUDIT-SID
reproduces industrial deployment behavior.

## D1-D7 Diagnostic Coverage

The updated literature supports a seven-axis diagnostic plan, but not all seven
are main-paper runnable in v0.

| Diagnostic | What it tests | Literature pressure | Current status |
|---|---|---|---|
| D1 capacity/utilization | code usage, dead codes, prefix fan-out, entropy | TIGER, GRID, ReSID, CARD, AdaSID, DIGER | v0 implemented |
| D2 collision profile / harm | full/prefix collisions; future qualified harm | QuaSID, AdaSID, CapsID, TIGER | v0 profile implemented; D2b harm future |
| D3 semantic-collaborative alignment | SID neighborhood vs co-occurrence neighborhood | LC-Rec, CoST, LETTER, ReSID, DiscRec | D3v2 implemented as diagnostic proxy |
| D4 head-tail capacity | capacity allocation across popularity buckets | Better Generalization, AsymRec, CapsID, Snapchat SID | v0 implemented |
| D5 structural deployment proxy | SID length, trie fan-out, ambiguous prefixes | TIGER, GRID, Long SID, CapsID, AsymRec | v0 D5a implemented |
| D6 drift/staleness | churn under tokenizer refresh/catalog evolution | DACT, SID staleness, Snapchat SID | optional DACT smoke implemented |
| D7 generator/retrieval behavior | invalid generated SID paths, duplicate candidates, beam coverage, SID likelihood/entropy | TIGER generation, DIGER, AsymRec, search-rec SID, industrial SID | interface hook only; needs `generator_outputs` |

Terminology recommendation:

- Keep **D5a** as structural deployment proxy over `item -> SID` mappings.
- Rename the old "D5b generator-output cost" concept to **D7 generator/retrieval
  behavior** in planning docs. This avoids overloading D5 and makes clear why
  D7 is not currently covered by mapping-only artifacts.

## Method Reassignment Summary

| Method / paper | Old assignment | Updated assignment | Reason |
|---|---|---|---|
| TIGER | A | A | canonical semantic-ID generative retrieval |
| GRID | A | A | open canonical exporter / practitioner framework |
| RQ-VAE/RQ-KMeans | A | A | baseline SID generator family |
| LC-Rec | A or B | B1 / A-to-B bridge | collaborative semantics is the key distinguishing pressure |
| ReSID | B | B1 plus B2 | rec-native encoding and semantic quantization; runnable B anchor |
| CoST | not explicit | B1 | contrastive semantic tokenization for neighborhood alignment |
| LETTER | not explicit | B1 plus B2 | collaborative regularization and code-assignment diversity |
| DiscRec | not explicit | B1 | semantic/collaborative disentanglement |
| CARD | B | B2 | non-uniform quantization and utilization/collision pressure |
| QuaSID | not explicit | B2 | qualified collision harm motivates D2b |
| AdaSID | B | B2 | adaptive collision/capacity handling |
| CapsID | B | B2 plus B4 | soft-routed variable-length SID affects collisions and bottlenecks |
| DIGER | B/D | B3 | differentiable/ranking-aligned SID |
| AsymRec | B | B4 plus B3 | asymmetric input/output bottleneck and hierarchical quantization |
| DACT | C | C | drift-aware continual tokenization |
| SID staleness | C/future | C | temporal compatibility and refresh behavior |
| Snapchat SID | D | D | industrial SID use cases and design choices |
| Joint search-rec SID | D | D / B3 | multi-task search-rec retrieval surface |
| RecList/Elliot | absent | R0 evaluation precedent | toolkit/evaluation framing, not SID methods |
| How to Index Item IDs | absent | R0 identifier foundation | identifier design foundation, not a tokenizer artifact source |

## Implications For CIKM v0

The current v0 remains defensible if written narrowly:

- runnable A: GRID official-module RQ-KMeans;
- runnable B: ReSID balanced GAOQ;
- controls: sanity baselines;
- optional C: DACT D6 churn smoke;
- D target: literature/resource motivation only.

But the paper should not say it "covers the SID method space" empirically. It
should say the toolkit schema is designed around the method-space axes revealed
by recent work, and v0 demonstrates the schema on representative runnable
artifacts.

## Update Needed In Paper Wording

Use:

> Recent SID work now stresses distinct artifact-level concerns: collaborative
> alignment, collision qualification, capacity utilization, variable-length or
> asymmetric bottlenecks, temporal staleness, and deployment behavior. AUDIT-SID
> provides a common artifact interface and diagnostic suite for these concerns.

Avoid:

> AUDIT-SID fully covers all SID/tokenizer methods.

Avoid:

> ReSID is representative of all recent SID innovation.

Avoid:

> D1-D7 are all implemented in the current v0 evidence.

The accurate v0 statement is:

> AUDIT-SID implements D1-D5a over standardized item-to-SID artifacts, includes
> optional D6 churn support, and reserves D7 generator/retrieval behavior for
> artifacts that expose per-user generated candidates or beam traces.
