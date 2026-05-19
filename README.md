# AUDIT-SID Idea Discovery

This branch runs a public-first idea-discovery pass for AUDIT-SID: diagnostic evaluation of semantic-ID tokenizers and codebooks in generative recommendation/retrieval.

## Start Here

1. `START_HERE_AUDIT_SID.md`
2. `docs/CURRENT_STATE.md`
3. `docs/CIKM_EXPERIMENT_DESIGN.md`
4. `docs/DOCUMENT_INDEX.md`
5. `docs/ARCHIVE_INDEX.md`
6. `docs/ARTIFACTS_INDEX.md`
7. `docs/PROJECT_SPEC.md`
8. `docs/GATE0_DECISION.md`
9. `docs/GATE0A_EVIDENCE_MATRIX.md`
10. `docs/GRID_MUSICAL_SAME_DATASET_CPU.md`
11. `docs/CIKM_RESOURCE_PAPER_PLAN.md`
12. `refine-logs/EXPERIMENT_TRACKER.md`
13. `refine-logs/EXPERIMENT_PLAN.md`

## Current Thesis

AUDIT-SID is the current public-first methodology candidate. It should be framed as representation-to-deployment diagnostics for semantic-ID tokenizers/codebooks, not as another SID generation algorithm or a simple leaderboard.

## Current Gate

Gate 0 artifact feasibility is **passed**:

- Cluster A: GRID official-module RQ-KMeans exports 5,000 joinable `All_Beauty` SIDs with D1-D5a metrics.
- Cluster B: ReSID balanced GAOQ exports 23,742 joinable `Musical_Instruments` SIDs with D1-D5a metrics.
- Sanity baselines exist for metric sensitivity.

Gate 0A core is **conditionally passed for a conservative resource-demo framing**:

- It is enough for a toolkit/resource demo with method coverage and a
  same-item-universe GRID Musical feature-text vs ReSID Musical diagnostic
  table.
- It is not enough for a same-dataset GRID-vs-ReSID leaderboard or a claim that ReSID Sports balanced GAOQ completed.
- D3 is no longer category-purity-only; `d3_alignment.csv` now includes co-occurrence collaborative top-k prefix recall.

## Frozen CIKM v0 Scope

- Dataset: `Musical_Instruments` now supports the main same-item-universe
  diagnostic row. `Sports_and_Outdoors` remains preferred for future
  canonical-vertical strengthening, but exact balanced ReSID GAOQ is not
  currently tractable enough to block Gate 0A.
- Methods: canonical RQ-VAE/TIGER-style SID, one representative recent tokenizer innovation such as ReSID if artifact export is meaningful, and random/popularity/category sanity ID baseline.
- Diagnostics: D1-D5a artifact diagnostics over `item -> SID` mappings:
  utilization, collision profile, semantic-collaborative alignment, head-tail
  capacity allocation, and lightweight SID-trie deployment-cost proxy.
- Optional only: D6 drift/churn and future generator-output D5b/D7.
- Paper stance: resource-first. Strong empirical finding is a stretch goal, not the core CIKM claim.

## Venue Target

Short-term target: CIKM 2026 Resource Track.

Key dates:

- Abstract: 2026-05-30 AoE
- Paper: 2026-06-06 AoE

Gate 0 has passed, and Gate 0A has a conditional resource-demo pass. If the paper needs a stronger same-dataset method comparison, do not force a weak CIKM submission. Longer-term backups are SIGIR 2027 Resource/Reproducibility-style track, RecSys 2027 Resource/Reproducibility, and CIKM 2027 Resource.

Method representativeness is part of Gate 0. A shallow RQ-VAE + ReSID comparison is not enough for submission.

The must-run method coverage is cluster-based: canonical SID baseline + representative recent tokenizer/codebook innovation from Cluster B + sanity lower bound.

Current public-code priority: convert the conditional Gate 0A result into paper-ready tables and wording. CARD compact feature proxy is controlled stressor/backlog only and should not be counted as faithful named-method evidence.

## Boundary

This branch is public-stage only. Do not commit Huawei internal data, business logs, or proprietary implementation details.
