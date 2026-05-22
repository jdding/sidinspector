# Final Submission Check

Timestamp: 2026-05-22 00:33:38 CST

Target: CIKM 2026 Resource Track

## Verdict

PASS for local PDF/package submission readiness, with one non-blocking external
artifact note: command-line access to the Anonymous GitHub URL is intercepted by
Cloudflare, which is already documented in the artifact quickstart. A manual
browser check of the anonymous URL remains recommended immediately before upload.

## Official Track Constraints Checked

- Resource papers: 4 pages including appendices and acknowledgments, plus
  unlimited pages for GenAI Usage Disclosure and references.
- Review mode: single-blind; author names and affiliations should appear.
- Template: ACM two-column `sigconf`.
- Resource abstract deadline: 2026-05-30.
- Resource paper deadline: 2026-06-06.
- GenAI Usage Disclosure must appear before references and does not count toward
  the page limit.

Official pages checked:

- `https://cikm2026.diag.uniroma1.it/resource-papers/`
- `https://cikm2026.diag.uniroma1.it/submission-policies-and-information/`

## Paper / PDF Checks

| Check | Result |
|---|---|
| PDF path | `paper/main.pdf` |
| PDF title | `SIDInspector: A Mapping-First Diagnostic Resource for Semantic-ID Tokenizers` |
| PDF pages | 5 total |
| Page-budget interpretation | Main content ends on page 4; references start on page 5 |
| GenAI disclosure placement | Page 4, immediately before references |
| Author mode | Single-blind author metadata present |
| Author block | One visual name line plus shared Huawei email suffix |
| Stale author scan | No stale Fudan email or anonymous paper topmatter in active paper |
| Figure accessibility | Figure 1 has `\Description{...}` |

Post-check section-title polish was applied and recompiled successfully:

- §2 `Artifact Interface and Validation`
- §3 `Diagnostic Probes and Evidence Roles`
- §4 `Worked Examples and Probe Evidence`
- §5 `Artifact Availability and Limits`

Current author block in the active PDF:

- Jiandong Ding, Heng Chang, Huijie Qin, and Tianying Liu
- `{dingjiandong2,heng.chang,qinhuijie,liutianying2}@huawei.com`
- Huawei Technologies; Shanghai, China

## Build / Verification

| Command | Result |
|---|---|
| `latexmk -pdf -interaction=nonstopmode -halt-on-error -cd paper/main.tex` | PASS after section-title polish |
| `python3 tools/verify_paper_artifact.py` | PASS |
| `python3 -m pytest tests -q` | PASS: 26 passed |
| `git diff --check` | PASS |
| Active-paper stale marker scan | PASS for active paper; expected anonymous-artifact wording remains in artifact docs |
| BibTeX warning scan | PASS: `warning$ -- 0` in `paper/main.blg` |

Remaining LaTeX warnings:

- `Unused global option(s): [natbib=true]` from the local `acmart` class.
- `Package balance Warning: You have called \balance in second column`.

Both are non-blocking; there are no undefined citations/references or overfull
box warnings in the final log scan.

## Test Scope Note

`python3 -m pytest -q` at repository root is not a valid final signal because it
recurses into vendored/upstream directories:

- `_gate0_artifacts/python_deps/{numpy,pandas,scipy}` require `hypothesis`.
- `_gate0_repos/DACT/LC-Rec-backbone/test_qwen*.py` requires `peft`.

The valid project test command is `python3 -m pytest tests -q`, which passed.

## Artifact / Availability

- Reviewer tag recorded in paper and docs: `audit-sid-cikm-resource-v0.1`.
- Anonymous artifact URL recorded in paper and docs:
  `https://anonymous.4open.science/r/sidinspector-9BB2`.
- License recorded: MIT.
- Reviewer verifier passed locally.
- `curl -I -L` to the anonymous URL returns HTTP 403 with Cloudflare challenge
  headers (`cf-mitigated: challenge`). This matches the existing quickstart
  caveat that non-browser clients may be blocked; manual browser verification is
  still recommended before final upload.

## Claim / Scope Check

The active paper maintains the intended claim boundary:

- It says SIDInspector is not a leaderboard, not a new tokenizer, and not a
  benchmark suite.
- It distinguishes named-method rows, reference adapters, controls, and
  controlled mechanism probes.
- It states that D2 is not causal collision harm, D3 is not trained-generator
  ranking, D5 is structural cost rather than measured latency, D6 is optional,
  and D7 requires generator traces not present in the current rows.
- It explicitly states that RQ-min is not third named-method coverage and that
  CARD is not faithful CARD evidence.

## Final Upload Checklist

Before uploading to EasyChair:

1. Use `paper/main.pdf` as the submission PDF.
2. Confirm the EasyChair track is `CIKM 2026 Resource`.
3. Nominate at least one author as reviewer, per Resource Track instructions.
4. Open the anonymous artifact URL in a normal browser once from outside the
   repo workflow and confirm the reviewer page renders.
5. Do not run root-level `pytest`; use `python3 -m pytest tests -q` for project
   tests.
