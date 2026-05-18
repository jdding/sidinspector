# AUDIT-SID Idea Discovery

This branch runs a public-first idea-discovery pass for AUDIT-SID: diagnostic evaluation of semantic-ID tokenizers and codebooks in generative recommendation/retrieval.

## Start Here

1. `START_HERE_AUDIT_SID.md`
2. `docs/DOCUMENT_INDEX.md`
3. `docs/PROJECT_SPEC.md`
4. `docs/GATE0_DECISION.md`
5. `refine-logs/EXPERIMENT_TRACKER.md`
6. `docs/AUTODL_GATE0A_STAGING.md`
7. `docs/GRID_CLUSTER_A_EXPORT_PREP.md`
8. `docs/RESID_REAL_MAPPING_SMOKE.md`
9. `docs/METHOD_REPRESENTATIVENESS_AUDIT.md`
10. `refine-logs/EXPERIMENT_PLAN.md`

## Current Thesis

AUDIT-SID is the current public-first methodology candidate. It should be framed as representation-to-deployment diagnostics for semantic-ID tokenizers/codebooks, not as another SID generation algorithm or a simple leaderboard.

## Current Gate

Gate 0 artifact feasibility is **passed**:

- Cluster A: GRID official-module RQ-KMeans exports 5,000 joinable `All_Beauty` SIDs with D1-D5a metrics.
- Cluster B: ReSID balanced GAOQ exports 23,742 joinable `Musical_Instruments` SIDs with D1-D5a metrics.
- Sanity baselines exist for metric sensitivity.

Gate 0A is still **open**. Do not treat the current evidence as paper-ready until method representativeness, dataset alignment, D3, and stability are resolved.

## Frozen CIKM v0 Scope

- Dataset: `Musical_Instruments` is quick-smoke only. Gate 0A / paper-facing evidence should use at least one canonical vertical, with `Sports_and_Outdoors` preferred and `Beauty_and_Personal_Care` as the second Amazon-2023 option.
- Methods: canonical RQ-VAE/TIGER-style SID, one representative recent tokenizer innovation such as ReSID if artifact export is meaningful, and random/popularity/category sanity ID baseline.
- Diagnostics: codebook utilization, collision harm, semantic-collaborative alignment, head-tail capacity allocation, and lightweight SID-trie deployment-cost proxy.
- Optional only if cheap: generator-output cost proxy and DACT/drift stability.
- Paper stance: resource-first. Strong empirical finding is a stretch goal, not the core CIKM claim.

## Venue Target

Short-term target: CIKM 2026 Resource Track.

Key dates:

- Abstract: 2026-05-30 AoE
- Paper: 2026-06-06 AoE

Gate 0 must pass by 2026-05-24. If not, do not force a weak CIKM submission. Longer-term backups are SIGIR 2027 Resource/Reproducibility-style track, RecSys 2027 Resource/Reproducibility, and CIKM 2027 Resource.

Method representativeness is part of Gate 0. A shallow RQ-VAE + ReSID comparison is not enough for submission.

The must-run method coverage is cluster-based: canonical SID baseline + representative recent tokenizer/codebook innovation from Cluster B + sanity lower bound.

Current public-code priority: strengthen real GRID/RQ-KMeans Cluster A evidence and align it with real ReSID Cluster B evidence. CARD is fallback/provenance only and should not be counted as primary method evidence. AutoDL Gate 0A staging is transfer-verified; next GPU use should run a larger real GRID run, not proxy strengthening.

## Boundary

This branch is public-stage only. Do not commit Huawei internal data, business logs, or proprietary implementation details.
