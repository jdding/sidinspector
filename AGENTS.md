# AGENTS.md

## Pipeline Status

language: zh
active_skill: /idea-discovery
active_branch: codex/audit-sid-idea-discovery
remote: git@github.com:jdding/lifecycle-ope-preflight.git

## Project Contract

This repository must follow the ARIS skill protocols from:

- `/Users/timber/aris-source/skills/skills-codex/idea-discovery/SKILL.md`
- `/Users/timber/aris-source/skills/skills-codex/research-refine/SKILL.md`
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
<!-- ARIS-CODEX:BEGIN -->
## ARIS Codex Skill Scope
ARIS Codex packages installed in this project: skills-codex
Managed entries: 90
Manifest: `.aris/installed-skills-codex.txt`
ARIS repo root: `/Users/timber/aris-source`
Project skill path: `.agents/skills/<skill-name>`
For ARIS Codex workflows, prefer the project-local skills under `.agents/skills/`.
When a skill needs ARIS helper scripts, resolve the repo root from the manifest or set it explicitly:
`ARIS_REPO=$(awk -F'	' '$1=="repo_root"{print $2; exit}' "/Users/timber/Documents/Sec_phrase/.aris/installed-skills-codex.txt")`
For commands/tests that should feed the AxiomDesk quality loop, run them through:
`python3 /Users/timber/aris-source/tools/axiomdesk_run.py --project "/Users/timber/Documents/Sec_phrase" -- <command ...>`
This records tool calls, failed commands, inferred test runs, and git file changes in `.aris/meta/events.jsonl`.
Do not edit or delete symlinked skills in place; update upstream or rerun:
`bash /Users/timber/aris-source/tools/install_aris_codex.sh "/Users/timber/Documents/Sec_phrase" --reconcile`
For copied Codex installs, use:
`bash /Users/timber/aris-source/tools/smart_update_codex.sh --project "/Users/timber/Documents/Sec_phrase"`
<!-- ARIS-CODEX:END -->