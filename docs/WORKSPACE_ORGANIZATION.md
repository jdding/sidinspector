# SIDInspector Workspace Organization

Timestamp: 2026-05-22 12:39:49 CST

## Current Active Surface

The active post-submission workspace should be read from fixed-name latest
files, not timestamp snapshots:

| Area | Active path |
|---|---|
| Paper PDF | `paper/main.pdf` |
| Paper source | `paper/main.tex`, `paper/sections/*.tex`, `paper/references.bib` |
| Reviewer quickstart | `README.md`, `ARTIFACT_QUICKSTART.md`, `ARTIFACT_MANIFEST.md` |
| Project state | `docs/CURRENT_STATE.md`, `docs/FINAL_SUBMISSION_CHECK.md` |
| Citation state | `docs/CITATION_AUDIT.md`, `paper_assets/references/audit_sid_references.bib` |
| Experiment state | `refine-logs/EXPERIMENT_PLAN.md`, `refine-logs/EXPERIMENT_TRACKER.md` |
| Paper evidence | `paper_assets/tables/`, `docs/PAPER_STRICT_CLAIM_AUDIT.md` |
| Code and tests | `src/`, `tools/`, `tests/` |
| External review state | `review-stage/` |

## Cleanup Applied

Large timestamp-snapshot sets from the 2026-05-18 to 2026-05-22 submission
sprint were removed after user approval. They were redundant historical
snapshots of fixed-name latest files, old manuscript builds, old generated
tables, old review prompts, and timestamped script copies.

## What Was Removed

- Root-level timestamp snapshots such as `MANIFEST_*.md`, `README_*.md`,
  `ARTIFACT_MANIFEST_*.md`, and `RESEARCH_BRIEF_*.md`.
- Timestamped docs under `docs/`.
- Timestamped experiment trackers/plans under `refine-logs/`.
- Old manuscript snapshots under `paper/`.
- Timestamped table/bib snapshots under `paper_assets/`.
- Timestamped review-stage and script snapshots.

## What Was Intentionally Kept

- Current fixed-name latest files.
- Current `paper/main.*` build outputs needed for local paper work.
- `_gate0_artifacts/` evidence bundles and run artifacts.
- Existing earlier archive directories such as `paper/archive/` and
  `refine-logs/archive/`.

## Operating Rule Going Forward

Use fixed-name latest files for active work. Older timestamp histories are now
recoverable from git history rather than from duplicate working-tree files.
