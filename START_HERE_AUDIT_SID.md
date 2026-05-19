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

1. `docs/CURRENT_STATE.md`
2. `docs/CIKM_EXPERIMENT_DESIGN.md`
3. `docs/DOCUMENT_INDEX.md`
4. `docs/ARCHIVE_INDEX.md`
5. `docs/ARTIFACTS_INDEX.md`
6. `docs/PROJECT_SPEC.md`
7. `docs/GATE0_DECISION.md`
8. `refine-logs/EXPERIMENT_TRACKER.md`
9. `docs/GRID_MUSICAL_SAME_DATASET_CPU.md`
10. `docs/CIKM_RESOURCE_PAPER_PLAN.md`
11. `refine-logs/EXPERIMENT_PLAN.md`

## Active Decision

Gate 0 artifact feasibility has passed. Gate 0A has a conditional pass for a
conservative CIKM Resource Track demo.

The current evidence is enough for a mapping-first artifact diagnostic toolkit
paper, centered on D1-D5a and the same-item-universe Musical diagnostic row.
It is not enough for a SID leaderboard, faithful TIGER reproduction, or full
generative recommender quality claim.

## Next Concrete Task

Continue paper-readiness tightening:

1. verify citation metadata from primary sources;
2. generate final method-coverage and diagnostic case-study tables;
3. keep D1-D5a as main artifact diagnostics and D6 as optional;
4. write strict limitations for D2/D3/D5a and generator-output gaps;
5. keep CARD and Sports proxy rows out of primary method evidence.

Run locally first. Use AutoDL only when a specific local blocker is documented.

## Frozen CIKM v0 Scope

Read `docs/AUDIT_SID_CIKM_EXECUTION_SPEC.md` before changing scope.
Read `docs/PROJECT_SPEC.md` as the unified execution contract.
Read `docs/SID_METHOD_CLUSTER_AUDIT.md` before deciding methods.
Read `docs/METHOD_REPRESENTATIVENESS_AUDIT.md` before launching any artifact extraction or training.

- `Musical_Instruments` is the current same-item-universe diagnostic case-study
  dataset.
- `Sports_and_Outdoors` remains future canonical-vertical strengthening, not a
  CIKM v0 blocker.
- Must-run method layers: canonical RQ-VAE/TIGER-style SID, one representative recent tokenizer innovation such as ReSID if artifact export is meaningful, and a sanity ID baseline.
- Must-have diagnostics: D1 utilization, D2 collision profile, D3
  semantic-collaborative alignment, D4 head-tail capacity allocation, D5a
  lightweight deployment-cost proxy.
- Optional only: D6 drift/churn and future D5b/D7 generator-output diagnostics.
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
