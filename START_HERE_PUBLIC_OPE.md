# Start Here: Public OPE Preflight

## Current Branch

`codex/public-ope-preflight`

## Required Skill Protocol

Use the ARIS skill implementation strictly:

`/Users/timber/aris-source/skills/skills-codex/idea-discovery/SKILL.md`

Before writing or refreshing artifacts, follow:

- `shared-references/output-versioning.md`
- `shared-references/output-manifest.md`
- `shared-references/output-language.md`

Do not create advisory-only notes that bypass the skill's staged workflow, timestamped output convention, manifest schema, or tracker updates.

## Remote

Private GitHub repository:

`git@github.com:jdding/lifecycle-ope-preflight.git`

Tracked branch:

`origin/codex/public-ope-preflight`

## Current Goal

Run the public-data phase of a two-stage OPE research program:

1. Public preflight: build lifecycle-stratified OPE diagnostics on public datasets.
2. Production validation: later map the stable protocol to internal business logs and compare against deployment or A/B outcomes.

## Read Order

1. `RESEARCH_BRIEF.md`
2. `idea-stage/IDEA_REPORT.md`
3. `docs/PUBLIC_DATASETS.md`
4. `refine-logs/EXPERIMENT_PLAN.md`
5. `refine-logs/EXPERIMENT_TRACKER.md`

## Active Decision

The first public research target is:

> Lifecycle-stratified OPE reliability protocol under sparse support.

The first execution gate is dataset feasibility, not model training.

## Next Concrete Task

Start with Open Bandit Dataset / OBP and KuaiRand schema inspection:

- Confirm whether OBP can run a small estimator smoke without large downloads.
- Confirm whether KuaiRand random-exposure rows provide enough fields for lifecycle-like cohort construction and direct/near-direct propensity handling.
- Update `refine-logs/EXPERIMENT_TRACKER.md` before launching any larger data processing.
