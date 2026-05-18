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

## Active Decision

Proceed with caution to feasibility only. Novelty is about `7/10` if the work is a diagnostic methodology paper; pure public leaderboard is abandoned.

## Next Concrete Task

Run Gate 0:

1. identify open public SID/tokenizer implementations;
2. verify whether at least two can export item-to-SID mappings;
3. verify whether generator outputs or candidate lists can be captured;
4. stop and report if artifact extraction is not feasible.

No full training should start before Gate 0 passes.
