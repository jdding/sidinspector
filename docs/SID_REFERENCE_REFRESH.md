# SID Reference Refresh For AUDIT-SID

Timestamp: 2026-05-19 12:52:26 CST

Scope: literature refresh for the AUDIT-SID CIKM 2026 Resource Track paper.
This file is a paper-reference planning artifact, not a BibTeX file. Keep
`docs/CITATION_AUDIT.md` and `paper_assets/references/audit_sid_references.bib`
as the source of paper-ready citation metadata.

## Bottom Line

The current reference scaffold is directionally correct but too narrow for a
credible AUDIT-SID paper. It covers TIGER, GRID, ReSID, DIGER, DACT, QuaSID,
joint search-rec SID, and CARD, but it under-cites three important bodies of
work:

1. earlier identifier/tokenizer foundations before TIGER/ReSID;
2. 2024-2025 tokenizer methods that already argue for collaborative alignment
   and code-assignment diversity;
3. very recent 2026 industrial/tokenizer papers that map almost one-to-one to
   AUDIT-SID's D1-D6 diagnostics.

For a 4-page CIKM Resource paper, the reference strategy should be selective:
cite fewer papers in the PDF, but make the coverage table and artifact repo show
that the toolkit is aware of the wider method space.

## Must-Cite Core

These should appear in the main 4-page PDF unless severe page pressure forces a
cut.

| Paper | Primary source | Why it matters for AUDIT-SID | Citation role |
|---|---|---|---|
| TIGER / Recommender Systems with Generative Retrieval | `https://arxiv.org/abs/2305.05065` / NeurIPS 2023 page | Establishes semantic-ID generative recommendation with RQ-VAE-style item token sequences. | Intro baseline and Cluster A motivation |
| How to Index Item IDs for Recommendation Foundation Models | `https://arxiv.org/abs/2305.06569` | Shows item indexing itself is a first-order design variable for LLM/foundation-model recommendation. | Pre-TIGER identifier framing |
| Better Generalization with Semantic IDs | `https://arxiv.org/abs/2306.08121` | Industry-scale ranking use case; motivates head/tail and generalization diagnostics outside pure GenRec. | Deployment motivation for D4 and resource relevance |
| RecList / Beyond NDCG | `https://arxiv.org/abs/2111.09963` | Prior art for diagnostic/behavioral testing beyond aggregate ranking metrics. | Justifies toolkit/evaluation-paper framing |
| GRID handbook | `https://arxiv.org/abs/2507.22224`; `https://github.com/snap-research/GRID` | Open framework and current Cluster A artifact path. | Method coverage and artifact adapter |
| ReSID | `https://arxiv.org/abs/2602.02338`; `https://github.com/FuCongResearchSquad/ReSID` | Recommendation-native tokenizer/codebook evidence and current Cluster B artifact path. | Main Cluster B method |
| QuaSID | `https://arxiv.org/abs/2603.00632` | Explicitly argues collisions are heterogeneous, not uniformly harmful. | D2 caveat and future D2b motivation |
| CARD | `https://arxiv.org/abs/2604.26427`; `https://github.com/HAI-UESTC/CARD` | Non-uniform quantization and codebook-utilization pressure align with D1/D2. | Coverage/backlog, not experimental evidence |
| Snapchat SID use cases | `https://arxiv.org/abs/2604.03949` | Industrial paper explicitly discusses SID use cases, challenges, design choices, and online deployment. | Resource/industry relevance anchor |

## Strong Related Work, Use If Space Allows

| Paper | Primary source | AUDIT-SID dimension |
|---|---|---|
| LC-Rec | `https://arxiv.org/abs/2311.09049` | collaborative semantics, vector-quantized item indexing |
| CoST | `https://arxiv.org/abs/2404.14774` | contrastive quantization; item-neighborhood alignment, useful for D3 |
| LETTER | `https://arxiv.org/abs/2405.07314` | hierarchical semantics + collaborative regularization + diversity loss |
| DiscRec | `https://arxiv.org/abs/2506.15576` | semantic/collaborative disentanglement and token-item alignment |
| DIGER | `https://arxiv.org/abs/2601.19711` | differentiable SID, recommendation-loss alignment, codebook collapse |
| Text-as-Vision SID study | `https://arxiv.org/abs/2601.14697` | representation-source sensitivity for SID construction |
| Long SID / ACERec | `https://arxiv.org/abs/2602.13573` | expressiveness vs efficiency tradeoff, D5a/D5b motivation |
| DACT | `https://arxiv.org/abs/2603.29705`; `https://github.com/HomesAmaranta/DACT` | drift/churn, D6 optional |
| SID staleness | `https://arxiv.org/abs/2604.13273` | temporal drift and compatibility after SID refresh |
| AdaSID | `https://arxiv.org/abs/2604.23522` | adaptive collision handling and utilization |
| CapsID | `https://arxiv.org/abs/2605.05096` | soft routing and variable-length SID; tokenizer bottleneck claim |
| AsymRec | `https://arxiv.org/abs/2605.14512` | input/output bottleneck; continuous input plus discrete target |
| Survey of generative search and recommendation | `https://arxiv.org/abs/2404.16924` | broad context if one survey citation is needed |
| Elliot | `https://arxiv.org/abs/2103.02590` | reproducible recommender evaluation framework, optional toolkit precedent |

## Diagnostic Coverage Mapping

| AUDIT-SID dimension | Best literature anchors | Notes |
|---|---|---|
| D1 utilization / capacity allocation | TIGER, GRID, ReSID, CARD, DIGER, AdaSID | Use this to argue codebook usage is a tokenizer artifact, not only a downstream metric side effect. |
| D2 collision profile / future D2b harm | TIGER, QuaSID, AdaSID, CapsID, HiD-VAE if included | QuaSID is the strongest reason to say collisions require qualification. |
| D3 semantic-collaborative alignment | LC-Rec, CoST, LETTER, ReSID, DiscRec | This is the area most under-cited in the current scaffold. |
| D4 head/tail capacity | Better Generalization with Semantic IDs, AsymRec, CapsID, Snapchat SID | Stronger if tied to long-tail/cold-start production concerns rather than generic fairness. |
| D5a deployment-cost proxy / D5b generator cost | TIGER, GRID, Long SID/ACERec, CapsID, AsymRec | D5a should stay structural unless generator outputs are available. |
| D6 drift/churn | DACT, SID staleness, Snapchat SID | D6 can be framed as optional but currently has enough literature support to be a real extension. |

## What Was Missing From The Current Scaffold

High-priority omissions:

- `How to Index Item IDs for Recommendation Foundation Models`: important
  pre-TIGER identifier/indexing framing.
- `Better Generalization with Semantic IDs`: important because it is an
  industry-scale ranking use case, not only a GenRec benchmark.
- `RecList`: a strong precedent for "beyond aggregate metrics" recommender
  diagnostic tooling.
- `CoST` and `LETTER`: representative 2024 tokenizer papers that directly
  motivate D3 and code-assignment diversity.
- `Snapchat SID use cases`: probably the single strongest 2026 industry anchor
  for why a resource/toolkit around SID artifacts matters.
- `AdaSID`, `CapsID`, `AsymRec`: newly visible 2026 papers after the original
  scaffold; they should at least appear in the method coverage discussion.

Lower-priority omissions:

- `DiscRec`, `Text-as-Vision`, `Long SID/ACERec`, `Elliot`, and the 2024
  generative search/recommendation survey. These are useful but probably not all
  viable in a 4-page PDF.

## Recommended 4-Page Reference Set

Main PDF should cite roughly 12-15 works:

1. TIGER.
2. How to Index Item IDs.
3. Better Generalization with Semantic IDs.
4. RecList.
5. GRID.
6. ReSID.
7. CoST or LETTER; prefer LETTER if discussing collaborative/diversity
   requirements, prefer CoST if discussing neighborhood alignment.
8. QuaSID.
9. CARD.
10. DACT or SID staleness; cite one in main text, put both in artifact docs if
    space is tight.
11. Snapchat SID use cases.
12. DIGER.
13. AdaSID.
14. CapsID or AsymRec; choose one depending on whether the paragraph stresses
    variable length or input/output bottlenecks.
15. CIKM Resource Track page only if the paper needs to cite artifact/supplement
    expectations; otherwise keep it in internal docs.

If the PDF is too tight, cut survey/Elliot/DiscRec/Text-as-Vision first, not the
industry or collision/collaborative-alignment anchors.

## Paper Writing Implications

The related-work story should not be "TIGER -> ReSID -> our toolkit." That is
too narrow and makes AUDIT-SID look like a two-method audit script.

Use this structure instead:

1. SID/tokenizers became central after learned item identifiers and TIGER-style
   generative retrieval.
2. New methods now optimize different artifact properties: collaborative
   alignment, utilization, collision qualification, variable length,
   differentiability, drift, and deployment.
3. The field lacks a small, mapping-first resource that audits these artifact
   properties in a common schema before full downstream reproduction.
4. AUDIT-SID fills that resource gap, with explicit boundaries around what
   artifact diagnostics can and cannot prove.

## Immediate Actions

- Update `docs/CITATION_AUDIT.md` in a later pass with the must-cite additions.
- Regenerate `paper_assets/references/audit_sid_references.bib` only after the
  final main-PDF reference set is chosen.
- Keep public-code status volatile: recheck CARD/DIGER/CapsID/AdaSID/AsymRec
  code availability near submission.
