# AUDIT-SID Archive Index

Timestamp: 2026-05-22 12:39:49 CST

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
| Post-submission workspace map | `docs/WORKSPACE_ORGANIZATION.md` |
| Project contract | `docs/PROJECT_SPEC.md` |
| Current gate verdict | `docs/GATE0_DECISION.md` |
| Live tracker | `refine-logs/EXPERIMENT_TRACKER.md` |
| Active AutoDL runbook | `docs/AUTODL_GATE0A_STAGING.md` |
| Cluster A evidence | `docs/GRID_CLUSTER_A_EXPORT_PREP.md` |
| Cluster B evidence | `docs/RESID_REAL_MAPPING_SMOKE.md` |

## Physical Archive Migrations

### 2026-05-22 Post-Submission Snapshot Deletion

After the first paper submission draft, the user explicitly requested a
systematic local cleanup because timestamped sprint files made navigation
confusing. The first pass moved these files into a temporary local archive;
after review, the user authorized deletion because the files were redundant
historical snapshots and recoverable from git history if needed.

Removed scope: timestamp snapshots across root docs, `docs/`, `refine-logs/`,
`paper/`, `paper_assets/`, `review-stage/`, `src/`, and `tools/`. Current
fixed-name latest files, current paper sources, current paper PDF, tests,
verifier, and `_gate0_artifacts/` evidence bundles remain in place.

The active map for post-submission work is:

- `docs/WORKSPACE_ORGANIZATION.md`

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

### 2026-05-20 D3 Dedup Cleanup

The user explicitly requested archiving duplicate local notes to avoid confusing
future evidence reads. The following scratch notes were moved out of the active
docs directory:

- `docs/archive/2026-05-20-dedup/VERTICAL_D3_REPLICATION_NOTE.md`
- `docs/archive/2026-05-20-dedup/D3_PREFIX_RANKING_CONTEXT.md`

The earlier lightweight ranking-probe runner and its obsolete outputs were also
archived because the canonical implementation is now
`tools/autodl_audit_sid/run_d3_ranking_context.py`:

- `tools/archive/2026-05-20-dedup/run_prefix_ranking_probe.py`
- `_gate0_artifacts/archive/2026-05-20-dedup/prefix_ranking_probe/`

Current active entry points are:

- `docs/VERTICAL_D3_REPLICATION_ALL_BEAUTY.md`
- `docs/D3_RANKING_CONTEXT_MUSICAL.md`

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

The 2026-05-22 snapshot deletion removed the main navigation blocker. Future
cleanup should be limited to obvious generated caches or a reviewer-package
refresh, and should keep fixed-name latest files in place.
