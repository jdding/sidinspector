# SID Problem Coverage Audit

Timestamp: 2026-05-20 14:25:04 CST

Scope: audit whether current SIDInspector diagnostics D1--D6 cover the SID
quality problems discussed by the current SID/tokenizer literature and by the
project's method taxonomy refresh.

## Verdict

D1--D6 cover the main **item-to-SID artifact** failure modes discussed by
current SID method papers, but they do **not** cover the full quality of a
generative recommendation system.

The safe paper claim is:

> SIDInspector covers six artifact-level failure dimensions: utilization,
> aliasing, neighborhood alignment, popularity allocation, structural cost, and
> temporal churn. These diagnostics inspect exported item-to-SID artifacts
> before or alongside downstream recommendation evaluation.

The unsafe paper claim is:

> D1--D6 fully cover SID/tokenizer quality or complete generative-recommender
> system quality.

## Coverage Matrix

| SID issue in current literature | Typical papers / facets | Covered by D1--D6? | Current diagnostic interpretation | Remaining gap |
|---|---|---|---|---|
| Mapping validity and joinability | all runnable tokenizers | Covered by validator, not D1--D6 | adapter contract checks item coverage, depth, and joins before metrics | not a diagnostic axis; keep as interface/validator claim |
| Codebook collapse, dead codes, underused codes, prefix imbalance | TIGER/RQ-style, GRID, ReSID, CARD/AdaSID-style capacity papers | Yes: D1 | D1 utilization reports per-level usage, prefix counts, imbalance, and dead/underused code signals | no downstream monotonicity claim |
| Full-SID and prefix aliasing | TIGER/RQ-style, QuaSID, AdaSID, CapsID | Mostly: D2 | D2 aliasing profiles duplicate full codes and duplicate prefixes; mechanism probes calibrate collision-heavy conditions | D2 is not strict causal collision harm |
| Qualified / harmful collision heterogeneity | QuaSID-style collision qualification | Partially: D2 plus mechanism probe | interaction-qualified probe shows that not all collisions carry equal co-occurrence risk | real method-level causal harm needs downstream or intervention evidence |
| Semantic grouping vs collaborative usefulness | LC-Rec, CoST, LETTER, ReSID, DiscRec | Mostly: D3 | D3 neighborhood alignment uses co-occurrence prefix recovery; metadata/category purity is auxiliary only | not proven monotonic with Recall@K/NDCG; reference neighborhood choice remains a design choice |
| RecSys-native predictability and prefix uncertainty | ReSID, DIGER, ranking-aligned tokenizers | Partially | D1/D3/D5 can expose capacity, alignment, and prefix structure related to predictability | actual next-token entropy, SID likelihood, invalid paths, and generated duplicate candidates require D7 generator traces |
| Head/mid/tail capacity allocation | Better-generalization, AsymRec/CapsID bottleneck discussions, industrial SID use | Yes: D4 | D4 splits capacity and uniqueness by popularity bucket | does not itself prove tail recommendation gain |
| Variable-length, asymmetric, or bottlenecked SID interfaces | CapsID, AsymRec, Long SID / ACERec-style work | Partially: D5 | D5 structural cost handles realized length, prefix fan-out, duplicate paths, and active-prefix burden over exported mappings | generator-side invalid-path and latency behavior require D7 or serving traces |
| Decoding, trie, beam, and serving cost | TIGER-style generation, DIGER, industrial/search-rec SID | Partially: D5 | D5 is a structural cost proxy over the mapping | real serving latency, beam coverage, and candidate-generation quality are outside D1--D6 |
| Temporal drift, catalog refresh, SID staleness | DACT, SID staleness papers, industrial refresh settings | Yes when paired snapshots exist: D6 | D6 temporal churn measures before/after SID changes and can be sliced by collision/popularity | online effect of churn or retraining cost is outside D6 |
| Unified search + recommendation SID behavior | joint search-rec SID, industrial/search surfaces | Not fully | D1--D6 can inspect the shared mapping if one exists | task-specific retrieval behavior and multi-task tradeoffs require D7 and task metrics |
| Full generator training dynamics and ranking quality | TIGER/ReSID/DIGER downstream experiments | No | D1--D6 are pre-training or alongside-training artifact diagnostics | Recall/NDCG, calibration, online impact, and generator learning curves remain system evaluation |

## Consequence For The Paper

The current draft should keep D1--D5 as the main mapping-level diagnostics,
D6 as optional refresh-pair evidence, and D7 as the explicit boundary for
generator-output behavior. This positioning is stronger than pretending that
D1--D6 are complete: it explains why SIDInspector is a resource for artifact
inspection rather than a replacement for downstream recommendation evaluation.

Recommended wording:

> D1--D6 cover the artifact-level pressures surfaced by recent SID work:
> utilization, aliasing and collision qualification, collaborative alignment,
> head-tail allocation, structural prefix cost, and churn under refresh. They
> do not cover generator-output behavior, measured serving latency, or
> downstream ranking impact unless additional D7/system artifacts are supplied.

## Paper-Claim Guardrails

- Say **artifact-level coverage**, not **full SID quality coverage**.
- Say **D2 aliasing profile plus bounded qualified-collision probe**, not
  **causal collision harm**.
- Say **D3 neighborhood-alignment diagnostic**, not **proven Recall/NDCG
  predictor**.
- Say **D5 structural cost proxy**, not **measured serving latency**.
- Say **D6 optional temporal churn**, not **main method result**.
- Say **D7 requires generator outputs or beam traces**, not **covered by D1--D6**.

## Next Action

No new experiment is required just to answer this coverage question. The
paper and strict claim audit should reference this boundary when future edits
touch abstract, introduction, diagnostics, or limitations.
