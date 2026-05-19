# AUDIT-SID Current State

Timestamp: 2026-05-19 12:29:57 CST

## Read First

For current work, read these in order:

1. `docs/CURRENT_STATE.md`
2. `docs/CIKM_EXPERIMENT_DESIGN.md`
3. `docs/GATE0_DECISION.md`
4. `docs/GATE0A_EVIDENCE_MATRIX.md`
5. `docs/GRID_MUSICAL_SAME_DATASET_CPU.md`
6. `docs/CIKM_RESOURCE_PAPER_PLAN.md`
7. `refine-logs/EXPERIMENT_TRACKER.md`

Use `docs/DOCUMENT_INDEX.md` for navigation and `docs/ARCHIVE_INDEX.md` for historical provenance.

## Current Verdict

AUDIT-SID is a CIKM 2026 Resource Track candidate under a conservative resource/toolkit framing.

- Gate 0 artifact feasibility: passed.
- Gate 0A: conditional pass for a resource-demo framing.
- Main contribution: mapping-first SID artifact interface plus D1-D5a diagnostics,
  with D6 drift/churn as an optional extension.
- Main paper evidence: same-item-universe Musical diagnostic row plus method coverage table.
- Not claimed: new tokenizer, SID leaderboard, downstream recommender superiority, faithful TIGER reproduction.

## Evidence Snapshot

| Evidence block | Status | Current role | Main caveat |
|---|---|---|---|
| GRID All_Beauty | done | Cluster A scale/stability evidence, 20k x 3 seeds plus 50k seed42 | cross-dataset, 50k is single seed |
| ReSID Musical | done | Cluster B real named-method evidence | bounded 1-epoch FAMAE -> balanced GAOQ |
| GRID Musical CPU | done | same-item-universe diagnostic contrast against ReSID Musical | processed feature-text input, not raw-text TIGER/GRID reproduction |
| Sanity baselines | done | lower-bound controls for metric interpretation | not named methods |
| D3v2 | done | co-occurrence collaborative alignment | diagnostic proxy, not Recall/NDCG validation |
| DACT D6 | optional | churn/drift demonstration | optional only, not Cluster B replacement |
| MovieLens portability | optional done | non-Amazon schema smoke | sanity SIDs only, not main empirical evidence |

## Same-Item-Universe Musical Diagnostic Row

| System | Method | Items | Unique SID | Duplicate SID rate | Full collision rate | D3 L1 weighted recall | D4 head/mid/tail unique ratio |
|---|---|---:|---:|---:|---:|---:|---|
| GRID feature-text | `grid_official_rqkmeans_resid_feature_text` | 23742 | 3749 | 0.842094 | 0.976876 | 0.055176 | 0.353001 / 0.358952 / 0.369494 |
| ReSID GAOQ | `resid_gaoq` | 23742 | 23742 | 0.000000 | 0.000000 | 0.153544 | 1.000000 / 1.000000 / 1.000000 |

This is the main response to the third external audit's cross-dataset critique.

## Current Paper Shape

Main paper should contain:

1. artifact schema and adapter contract;
2. D1-D5a diagnostic definitions, explicitly scoped to item-to-SID artifacts;
3. method coverage table with caveats;
4. same-item-universe Musical diagnostic table;
5. reproducibility/resource checklist.

Appendix or optional:

- GRID All_Beauty scale/stability;
- DACT D6 churn;
- MovieLens portability;
- AutoDL staging/provenance.

## Current Compute Policy

Run locally first. AutoDL is currently no-GPU and should only be used for staging or verification until a specific GPU-only blocker is documented.

Do not launch robust/sweep/quality queues by default.

## Open Gaps

1. Citation metadata must be verified from source before LaTeX writing.
2. D3v2 is not yet validated against downstream Recall/NDCG.
3. TIGER is not reproduced; paper needs a short justification for GRID.
4. 50k GRID All_Beauty is single-seed and should be appendix/preliminary unless more seeds are added.
5. Paper tables still need to be generated into final LaTeX/CSV form.
6. D2 is currently a collision profile, not interaction-qualified causal harm.
7. Full generator behavior is out of scope unless optional `generator_outputs`
   are available for D5b/D7-style diagnostics.
