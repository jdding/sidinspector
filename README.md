# AUDIT-SID Idea Discovery

This branch runs a public-first idea-discovery pass for AUDIT-SID: diagnostic evaluation of semantic-ID tokenizers and codebooks in generative recommendation/retrieval.

## Start Here

1. `START_HERE_AUDIT_SID.md`
2. `RESEARCH_BRIEF.md`
3. `idea-stage/LITERATURE_REVIEW.md`
4. `idea-stage/IDEA_REPORT.md`
5. `refine-logs/NOVELTY_CHECK.md`
6. `refine-logs/REVIEW_SUMMARY.md`
7. `refine-logs/FINAL_PROPOSAL.md`
8. `refine-logs/EXPERIMENT_PLAN.md`
9. `refine-logs/PIPELINE_SUMMARY.md`
10. `refine-logs/EXPERIMENT_TRACKER.md`
11. `docs/AUDIT_SID_VENUE_PLAN.md`
12. `docs/PROJECT_SPEC.md`
13. `docs/AUDIT_SID_CIKM_EXECUTION_SPEC.md`
14. `docs/SID_METHOD_CLUSTER_AUDIT.md`
15. `docs/METHOD_REPRESENTATIVENESS_AUDIT.md`
16. `docs/EXTERNAL_REVIEW_ABSORPTION.md`
17. `docs/GATE0_REPO_AUDIT.md`
18. `docs/DATASET_SCHEMA_AUDIT.md`
19. `docs/ADAPTER_SMOKE.md`
20. `docs/METRIC_SMOKE.md`
21. `docs/GRID_ADAPTER_SMOKE.md`
22. `docs/REAL_MAPPING_PREFLIGHT.md`
23. `docs/RESID_RUN_PREFLIGHT.md`
24. `docs/CODE_REVIEW_FIXES.md`
25. `docs/RESID_REAL_MAPPING_SMOKE.md`
26. `docs/AUTODL_GPU_EXPERIMENT_PLAN.md`
27. `docs/CASE_STUDY_RESID_VS_SANITY.md`
28. `docs/CODE_REVIEW_FIXES_ROUND2.md`
29. `docs/LOCAL_RQKMEANS_PROXY.md`

## Current Thesis

AUDIT-SID is the current public-first methodology candidate. It should be framed as representation-to-deployment diagnostics for semantic-ID tokenizers/codebooks, not as another SID generation algorithm or a simple leaderboard.

## Current Gate

Gate 0 is code/artifact feasibility:

> verify whether GRID/RQ-VAE and ReSID, or CARD fallback, can export joinable item-to-SID mappings into `src/audit_sid/interface.py`.

Do not launch full experiments before Gate 0 and dataset support audit pass.

## Frozen CIKM v0 Scope

- Dataset: ReSID processed Amazon-2023 `Musical_Instruments`; Amazon 2014 Beauty/Sports as backup.
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

Current public-code priority: GRID/RQ-VAE for Cluster A, ReSID for Cluster B, CARD fallback if GRID is too heavy. DIGER is backup only; CapsID/AdaSID/AsymRec stay future support unless runnable code appears. Repo-level artifact-path audit, ReSID `Musical_Instruments` schema probe, sanity SID adapter smoke, D1-D5a metric smoke, and GRID output-format adapter smoke are done. Local ReSID FAMAE -> GAOQ produced the first real Cluster B SID mapping and D1-D5a metrics. A local RQ-KMeans feature-proxy baseline is available for toolkit development, but Gate 0 remains open because Cluster A public implementation coverage is still missing.

## Boundary

This branch is public-stage only. Do not commit Huawei internal data, business logs, or proprietary implementation details.
