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

## Current Thesis

AUDIT-SID is the current public-first methodology candidate. It should be framed as representation-to-deployment diagnostics for semantic-ID tokenizers/codebooks, not as another SID generation algorithm or a simple leaderboard.

## Current Gate

Gate 0 is code/artifact feasibility:

> verify whether at least two public SID/tokenizer implementations can export item-to-SID mappings and generator outputs on one small public dataset.

Do not launch full experiments before Gate 0 and dataset support audit pass.

## Venue Target

Short-term target: CIKM 2026 Resource Track.

Key dates:

- Abstract: 2026-05-30 AoE
- Paper: 2026-06-06 AoE

Gate 0 must pass by 2026-05-24. If not, do not force a weak CIKM submission. Longer-term backups are SIGIR 2027 Resource/Reproducibility-style track, RecSys 2027 Resource/Reproducibility, and CIKM 2027 Resource.

## Boundary

This branch is public-stage only. Do not commit Huawei internal data, business logs, or proprietary implementation details.
