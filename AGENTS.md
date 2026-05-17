# AGENTS.md

## Pipeline Status

language: zh
active_skill: /idea-discovery
active_branch: codex/public-ope-preflight
remote: git@github.com:jdding/lifecycle-ope-preflight.git

## Project Contract

This repository must follow the ARIS skill protocols from:

- `/Users/timber/aris-source/skills/skills-codex/idea-discovery/SKILL.md`
- `/Users/timber/aris-source/skills/skills-codex/shared-references/output-versioning.md`
- `/Users/timber/aris-source/skills/skills-codex/shared-references/output-manifest.md`
- `/Users/timber/aris-source/skills/skills-codex/shared-references/output-language.md`

## Operating Rules

- Before substantive research work, load the relevant ARIS skill file and follow its workflow rather than only borrowing the skill name.
- For overwriteable outputs, write a timestamped file with second-level precision first, then copy the same content to the fixed-name latest file.
- Keep `MANIFEST.md` in the ARIS table schema.
- Keep `findings.md` append-only once it exists.
- Keep all public-stage artifacts free of Huawei internal data, business logs, and proprietary implementation details.
- Update `refine-logs/EXPERIMENT_TRACKER.md` whenever a gate, run, or decision changes.

