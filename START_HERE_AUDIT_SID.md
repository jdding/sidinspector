# Start Here: AUDIT-SID

## Current Branch

`codex/audit-sid-idea-discovery`

## Required Skill Protocol

Use the ARIS skill implementation strictly:

- `/Users/timber/aris-source/skills/skills-codex/idea-discovery/SKILL.md`
- `/Users/timber/aris-source/skills/skills-codex/research-lit/SKILL.md`
- `/Users/timber/aris-source/skills/skills-codex/idea-creator/SKILL.md`
- `/Users/timber/aris-source/skills/skills-codex/novelty-check/SKILL.md`
- `/Users/timber/aris-source/skills/skills-codex/research-review/SKILL.md`
- `/Users/timber/aris-source/skills/skills-codex/research-refine-pipeline/SKILL.md`

Before writing or refreshing artifacts, follow:

- `shared-references/output-versioning.md`
- `shared-references/output-manifest.md`
- `shared-references/output-language.md`

## Current Goal

Evaluate whether AUDIT-SID can become a public-first methodology paper:

> representation-to-deployment diagnostics for semantic-ID tokenizers/codebooks in generative recommendation/retrieval.

## Read Order

1. `RESEARCH_BRIEF.md`
2. `idea-stage/LITERATURE_REVIEW.md`
3. `idea-stage/IDEA_REPORT.md`
4. `refine-logs/NOVELTY_CHECK.md`
5. `refine-logs/REVIEW_SUMMARY.md`
6. `refine-logs/FINAL_PROPOSAL.md`
7. `refine-logs/EXPERIMENT_PLAN.md`
8. `refine-logs/PIPELINE_SUMMARY.md`
9. `refine-logs/EXPERIMENT_TRACKER.md`
10. `docs/AUDIT_SID_VENUE_PLAN.md`
11. `docs/PROJECT_SPEC.md`
12. `docs/EXTERNAL_REVIEW_ABSORPTION.md`
13. `docs/GATE0_REPO_AUDIT.md`
14. `docs/DATASET_SCHEMA_AUDIT.md`
15. `docs/ADAPTER_SMOKE.md`
16. `docs/METRIC_SMOKE.md`
17. `docs/GRID_ADAPTER_SMOKE.md`
18. `docs/REAL_MAPPING_PREFLIGHT.md`
19. `docs/RESID_RUN_PREFLIGHT.md`
20. `docs/CODE_REVIEW_FIXES.md`
21. `docs/RESID_REAL_MAPPING_SMOKE.md`
22. `docs/AUTODL_GPU_EXPERIMENT_PLAN.md`
23. `docs/CASE_STUDY_RESID_VS_SANITY.md`
24. `docs/CODE_REVIEW_FIXES_ROUND2.md`
25. `docs/LOCAL_RQKMEANS_PROXY.md`
26. `docs/CLUSTER_A_PREFLIGHT.md`
27. `docs/AUTODL_READY_HANDOFF.md`

## Active Decision

Proceed with caution to feasibility only. Novelty is about `7/10` if the work is a diagnostic methodology paper; pure public leaderboard is abandoned.

## Next Concrete Task

Continue Gate 0:

1. prepare Cluster A canonical SID mapping path, preferably GRID/RQ-VAE or RKMeans/TIGER-style;
2. use `docs/AUTODL_READY_HANDOFF.md` and `tools/autodl_audit_sid/run_remote_audit_sid.sh` once the fixed RTX 5090 instance is ready;
3. run CARD RQ-VAE fallback export if GRID remains too heavy;
4. compare real ReSID against sanity baselines and the first Cluster A/CARD mapping;
5. stop with missing-asset list if Cluster A cannot export locally or on AutoDL by 2026-05-24.

No full training should start before Gate 0 passes.

## Frozen CIKM v0 Scope

Read `docs/AUDIT_SID_CIKM_EXECUTION_SPEC.md` before changing scope.
Read `docs/PROJECT_SPEC.md` as the unified execution contract.
Read `docs/SID_METHOD_CLUSTER_AUDIT.md` before deciding methods.
Read `docs/METHOD_REPRESENTATIVENESS_AUDIT.md` before launching any artifact extraction or training.

- Primary dataset: ReSID processed Amazon-2023 `Musical_Instruments`.
- Backup dataset: Amazon 2014 Beauty/Sports.
- Must-run method layers: canonical RQ-VAE/TIGER-style SID, one representative recent tokenizer innovation such as ReSID if artifact export is meaningful, and a sanity ID baseline.
- Must-have diagnostics: D1 utilization, D2 collision harm, D3 semantic-collaborative alignment, D4 head-tail capacity allocation, D5a lightweight deployment-cost proxy.
- Optional only: D5b generator-output cost and DACT/drift.
- Do not treat RQ-VAE + ReSID as automatically sufficient; Gate 0A must verify method representativeness.
- Must-run coverage is Cluster A canonical SID + Cluster B recent tokenizer/codebook innovation + sanity lower bound. Old B/C split is deprecated.
- Resource-first rule: strong empirical finding is a stretch goal; toolkit interface + coverage table + non-redundant case study are the CIKM core.
- Public code screen: DIGER is backup only; CapsID/AdaSID/AsymRec stay future-only unless runnable code appears; DRIL is not an independent candidate.

## Venue Plan

Read `docs/AUDIT_SID_VENUE_PLAN.md` before expanding experiments. Current recommendation:

- CIKM 2026 Resource Track is the immediate target;
- abstract deadline: 2026-05-30 AoE;
- paper deadline: 2026-06-06 AoE;
- Gate 0 must pass by 2026-05-24;
- if Gate 0 fails, do not force a weak CIKM submission;
- SIGIR 2027 / RecSys 2027 / CIKM 2027 are later backup or expansion targets.
