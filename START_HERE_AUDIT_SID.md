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

1. `docs/DOCUMENT_INDEX.md`
2. `docs/ARCHIVE_INDEX.md`
3. `docs/ARTIFACTS_INDEX.md`
4. `docs/PROJECT_SPEC.md`
5. `docs/GATE0_DECISION.md`
6. `refine-logs/EXPERIMENT_TRACKER.md`
7. `docs/AUTODL_GATE0A_STAGING.md`
8. `docs/GRID_CLUSTER_A_EXPORT_PREP.md`
9. `docs/RESID_REAL_MAPPING_SMOKE.md`
10. `docs/METHOD_REPRESENTATIVENESS_AUDIT.md`
11. `refine-logs/EXPERIMENT_PLAN.md`
12. `RESEARCH_BRIEF.md`
13. `idea-stage/LITERATURE_REVIEW.md`
14. `idea-stage/IDEA_REPORT.md`

## Active Decision

Gate 0 artifact feasibility has passed. Gate 0A remains open.

The current evidence is enough to say public artifacts can export joinable SID
mappings, but not enough to say the CIKM case study is ready. Novelty remains
about `7/10` if the work is a diagnostic methodology paper; pure public
leaderboard is abandoned.

## Next Concrete Task

Continue Gate 0A:

1. use `docs/AUTODL_GATE0A_STAGING.md` as the current AutoDL runbook;
2. run a larger real GRID/RQ-KMeans Cluster A job when GPU is available;
3. decide whether A/B must be aligned on one dataset or can remain artifact-feasibility cross-dataset;
4. replace or clearly caveat category-purity D3 before paper use;
5. keep CARD and Sports proxy rows out of primary method evidence.

No proxy strengthening should start before Gate 0A priorities are resolved.

## Frozen CIKM v0 Scope

Read `docs/AUDIT_SID_CIKM_EXECUTION_SPEC.md` before changing scope.
Read `docs/PROJECT_SPEC.md` as the unified execution contract.
Read `docs/SID_METHOD_CLUSTER_AUDIT.md` before deciding methods.
Read `docs/METHOD_REPRESENTATIVENESS_AUDIT.md` before launching any artifact extraction or training.

- `Musical_Instruments` is quick-smoke only.
- Paper-facing Gate 0A evidence should include at least one canonical vertical: `Sports_and_Outdoors` is preferred, and `Beauty_and_Personal_Care` is the second Amazon-2023 option.
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
