# AUDIT-SID Document Index

Timestamp: 2026-05-19 01:01:03 CST

## Current Status

- Gate 0: **passed for artifact feasibility**.
- Gate 0A: **open**.
- Paper case study: **not yet ready**.
- Current compute state: AutoDL Gate 0A staging is transfer-verified; next GPU
  use should run a real GRID/RQ-KMeans 20k/50k strengthening job, not proxy rows.
- Dataset stance: `Musical_Instruments` is quick-smoke only; paper-facing Gate
  0A should use at least one canonical vertical, preferably
  `Sports_and_Outdoors`, with `Beauty_and_Personal_Care` as the next Amazon-2023
  option.

## Read This First

| Purpose | Current file | Notes |
|---|---|---|
| Project contract | `docs/PROJECT_SPEC.md` | Unified thesis, gates, method coverage, diagnostics |
| Current gate verdict | `docs/GATE0_DECISION.md` | Gate 0 artifact-feasibility pass; Gate 0A still open |
| Live tracker | `refine-logs/EXPERIMENT_TRACKER.md` | Operational source of truth for tasks and status |
| Latest remote runbook | `docs/AUTODL_GATE0A_STAGING.md` | AutoDL paths, transferred files, next GPU command |
| Cluster A evidence | `docs/GRID_CLUSTER_A_EXPORT_PREP.md` | GRID official-module RQ-KMeans local 5k export |
| Cluster B evidence | `docs/RESID_REAL_MAPPING_SMOKE.md` | ReSID balanced GAOQ local real mapping |

## Gate Evidence

### Gate 0

Use these files:

- `docs/GATE0_DECISION.md`
- `docs/GRID_CLUSTER_A_EXPORT_PREP.md`
- `docs/RESID_REAL_MAPPING_SMOKE.md`
- `docs/AUTODL_GATE0A_STAGING.md`

Do **not** use these as current verdicts:

- `docs/GATE0_RESULTS_20260518_233331.md`
- `docs/GATE0_RESULTS_20260518_234958.md`
- `docs/GATE0_RESULTS.md`

Those files are retained because they document the proxy-matrix correction. The
current verdict is `docs/GATE0_DECISION.md`.

### Gate 0A

Gate 0A is still open. Before treating the work as paper-ready, resolve:

- dataset alignment between GRID and ReSID;
- D3 semantic-collaborative alignment versus current category-purity proxy;
- GRID direct official-module wrapper versus full GRID Hydra/TFRecord path;
- seed/stability reporting;
- reviewer-facing case-study dataset choice.

## Method Evidence

| Method line | Current status | File |
|---|---|---|
| GRID / RQ-KMeans Cluster A | real artifact-feasibility path, 5k All_Beauty | `docs/GRID_CLUSTER_A_EXPORT_PREP.md` |
| ReSID / GAOQ Cluster B | real bounded 1-epoch export, Musical_Instruments | `docs/RESID_REAL_MAPPING_SMOKE.md` |
| Sanity baselines | available for metric sensitivity | `docs/METRIC_SMOKE.md`, `docs/CASE_STUDY_RESID_VS_SANITY.md` |
| CARD | repaired fallback only; do not count as primary evidence | `docs/CARD_SOURCE_REPAIR.md` |
| Sports proxy matrix | pipeline evidence only | `docs/GATE0_RESULTS.md` |

## AutoDL State

Use `docs/AUTODL_GATE0A_STAGING.md` as the current remote runbook.

Older AutoDL docs are historical:

- `docs/AUTODL_READY_HANDOFF.md`
- `docs/AUTODL_READINESS_REPORT.md`
- `docs/AUTODL_REMOTE_STAGING.md`
- `docs/AUTODL_GAOQ_STOPLOSS.md`

They are still useful for provenance, but they should not override the latest
Gate 0A staging file.

## Historical Planning

Use these for context, not for current status:

- `docs/AUDIT_SID_VENUE_PLAN.md`
- `docs/AUDIT_SID_CIKM_EXECUTION_SPEC.md`
- `docs/EXTERNAL_REVIEW_ABSORPTION.md`
- `docs/SID_METHOD_CLUSTER_AUDIT.md`
- `docs/METHOD_REPRESENTATIVENESS_AUDIT.md`
- `docs/TOKENIZER_DATASET_CATEGORY_AUDIT.md`

## Artifact Policy

- Fixed-name docs are the latest readable entry points.
- Timestamped docs are immutable history.
- Do not delete old timestamped files.
- Do not count proxy rows as named-method evidence in future paper tables.
