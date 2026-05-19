# AUDIT-SID Archive Index

Timestamp: 2026-05-20 00:56:00 CST

## Policy

This repository keeps timestamped files as provenance. Do not delete them. A
physical archive migration is allowed only when the user explicitly asks for
local cleanup and fixed-name latest entry points remain in place.

For daily work, read `docs/DOCUMENT_INDEX.md` first. Use this file only when
you need to understand historical decisions, older proxy runs, or prior scope
changes.

## Current Entry Points

These files remain active and should stay in their current locations:

| Purpose | File |
|---|---|
| Repository overview | `README.md` |
| Recovery entrypoint | `START_HERE_AUDIT_SID.md` |
| Current document map | `docs/DOCUMENT_INDEX.md` |
| Project contract | `docs/PROJECT_SPEC.md` |
| Current gate verdict | `docs/GATE0_DECISION.md` |
| Live tracker | `refine-logs/EXPERIMENT_TRACKER.md` |
| Active AutoDL runbook | `docs/AUTODL_GATE0A_STAGING.md` |
| Cluster A evidence | `docs/GRID_CLUSTER_A_EXPORT_PREP.md` |
| Cluster B evidence | `docs/RESID_REAL_MAPPING_SMOKE.md` |

## Physical Archive Migrations

### 2026-05-20 Round 4 Cleanup

The user explicitly requested local file cleanup before committing to GitHub.
The following timestamped snapshots were moved out of active working
directories while keeping fixed-name latest files in place:

- `docs/archive/2026-05-20-round4-cleanup/`: Round 4 planning/state/audit
  timestamped snapshots.
- `paper/archive/2026-05-20-round4-cleanup/`: timestamped paper draft/PDF
  snapshots.
- `paper/archive/2026-05-20-round4-cleanup/sections/`: timestamped section
  snapshots.
- `refine-logs/archive/2026-05-20-round4-cleanup/`: timestamped experiment
  plan/tracker snapshots.
- `tools/archive/2026-05-20-round4-cleanup/`: timestamped figure-generator
  script snapshot.

This migration does not change the current paper source, fixed-name docs, or
evidence interpretation. `MANIFEST.md` records the archived paths.

## Historical Buckets

### Planning And Venue History

Use these to reconstruct how the project scope changed:

- `docs/AUDIT_SID_VENUE_PLAN*.md`
- `docs/AUDIT_SID_CIKM_EXECUTION_SPEC*.md`
- `docs/PROJECT_SPEC_*.md`
- `docs/EXTERNAL_REVIEW_ABSORPTION*.md`
- `docs/SID_METHOD_CLUSTER_AUDIT*.md`
- `docs/METHOD_REPRESENTATIVENESS_AUDIT*.md`
- `refine-logs/METHOD_DIRECTION_RETHINK*.md`
- `refine-logs/FINAL_PROPOSAL*.md`
- `refine-logs/PIPELINE_SUMMARY*.md`
- `refine-logs/REVIEW_SUMMARY*.md`
- `RESEARCH_BRIEF_*.md`

### Dataset And Method Audits

Use these for reviewer-facing provenance, not as the current runbook:

- `docs/GATE0_REPO_AUDIT*.md`
- `docs/DATASET_SCHEMA_AUDIT*.md`
- `docs/CANONICAL_VERTICAL_SCHEMA_AUDIT*.md`
- `docs/TOKENIZER_DATASET_CATEGORY_AUDIT*.md`
- `docs/REAL_MAPPING_PREFLIGHT*.md`
- `docs/RESID_RUN_PREFLIGHT*.md`
- `docs/CLUSTER_A_PREFLIGHT*.md`

### Pipeline And Metric Smokes

These validate plumbing and metric behavior. They are not named-method paper
evidence by themselves:

- `docs/ADAPTER_SMOKE*.md`
- `docs/METRIC_SMOKE*.md`
- `docs/GRID_ADAPTER_SMOKE*.md`
- `docs/CASE_STUDY_RESID_VS_SANITY*.md`
- `docs/LOCAL_RQKMEANS_PROXY*.md`

### Proxy Or Superseded Gate Verdicts

These are retained because they document mistakes and corrections. Do not cite
them as the current verdict:

- `docs/GATE0_RESULTS*.md`
- `docs/GATE0_DECISION_20260518_234958.md`

Current verdict: `docs/GATE0_DECISION.md`.

### AutoDL And Remote Execution History

Use the latest fixed-name runbook for action. Use timestamped versions for
remote provenance only:

- `docs/AUTODL_GPU_EXPERIMENT_PLAN*.md`
- `docs/AUTODL_READINESS_REPORT*.md`
- `docs/AUTODL_READY_HANDOFF*.md`
- `docs/AUTODL_REMOTE_STAGING*.md`
- `docs/AUTODL_CODE_REVIEW*.md`
- `docs/AUTODL_GAOQ_STOPLOSS*.md`
- `docs/AUTODL_GATE0A_STAGING_*.md`

Current action file: `docs/AUTODL_GATE0A_STAGING.md`.

### Source Repair And Fallbacks

These are useful if a fallback path is reopened. They should not be counted as
primary method evidence:

- `docs/CARD_SOURCE_REPAIR*.md`
- `tools/autodl_audit_sid/card_source_repair/`
- `tools/autodl_audit_sid/repair_card_source.py`
- `tools/autodl_audit_sid/check_card_source.py`

### Older Idea-Discovery Material

These are background for the original broader branch, not current AUDIT-SID
execution state:

- `START_HERE_PUBLIC_OPE.md`
- `docs/PUBLIC_DATASETS*.md`
- `docs/REA_REFRAME*.md`
- `docs/SEMANTIC_ID_TREND_TOP1*.md`
- `docs/EXPLORATION_CLOSEOUT*.md`
- `docs/FUTURE_DIRECTIONS*.md`
- `idea-stage/LITERATURE_REVIEW*.md`
- `idea-stage/IDEA_REPORT*.md`
- `refine-logs/NOVELTY_CHECK*.md`
- `refine-logs/DORMANT_TOPIC_REASSESSMENT*.md`

## Future Physical Cleanup

After the submission decision is settled, a safer physical cleanup would be:

1. create `docs/archive/2026-05-18-sprint/`;
2. move timestamped historical docs there with `git mv`;
3. update `MANIFEST.md` with migration rows;
4. keep all fixed-name latest docs in place.

Do not do this during active Gate 0A execution unless repository navigation
becomes a direct blocker.
