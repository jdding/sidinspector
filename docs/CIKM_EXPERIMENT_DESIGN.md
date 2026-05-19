# CIKM Experiment Design For AUDIT-SID

Timestamp: 2026-05-19 12:29:57 CST

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
- D2 is reported as collision profile in v0; interaction-qualified collision
  harm is future D2b unless a bounded implementation is added.
- Generator predictability, invalid generated paths, and candidate duplication
  require `generator_outputs` and belong to future D5b/D7.

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

## Paper Tables

| Table | Required | Content | Source |
|---|---|---|---|
| Table 1 | yes | Method coverage and artifact caveats | `docs/GATE0A_EVIDENCE_MATRIX.md` |
| Table 2 | yes | GRID Musical feature-text vs ReSID Musical D1-D5a | `docs/GRID_MUSICAL_SAME_DATASET_CPU.md` |
| Table 3 | yes or appendix | ReSID/sanity non-redundancy controls | `docs/CASE_STUDY_RESID_VS_SANITY.md` |
| Table 4 | appendix | GRID All_Beauty scale/stability | `docs/AUTODL_GATE0A_GRID_RESULTS.md` |
| Table 5 | optional appendix | DACT D6 churn | `docs/DACT_DRIFT_SMOKE.md` |

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
- D1-D5a and optional D6.

Use this exact scope sentence:

> AUDIT-SID covers six artifact-level failure dimensions: capacity utilization,
> collision profile, semantic-collaborative alignment, head-tail allocation,
> deployment-cost proxy, and drift stability. These diagnostics target
> tokenizer artifacts before or alongside downstream model evaluation.

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
