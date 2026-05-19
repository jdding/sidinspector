# CIKM Resource Format Audit

Timestamp: 2026-05-19 12:41:13 CST

Source: `https://cikm2026.diag.uniroma1.it/resource-papers/`

## Verified Rules

- Resource papers are limited to 4 pages.
- The 4-page limit includes appendices and acknowledgments.
- References are unlimited.
- The GenAI Usage Disclosure section is unlimited.
- Online supplementary materials such as GitHub repositories, datasets, videos,
  and prototypes may be cited.
- Reviewers may decide whether to inspect supplementary material, so the paper
  must not depend on supplement-only evidence for its core claim.

## AUDIT-SID Consequence

Treat the paper as having no usable appendix. The 4-page main PDF must be
self-contained:

1. Problem and resource contribution.
2. Mapping-first artifact interface.
3. D1-D5a diagnostic definitions, with D6 optional.
4. Method coverage / evidence matrix.
5. One same-item-universe diagnostic case study.
6. Artifact/reproducibility entry point.
7. Boundaries and limitations.

Move the following to the GitHub artifact repository rather than the PDF:

- full per-run CSVs;
- seed-level logs and variance tables;
- full D1-D6 metric definitions;
- dataset schema details;
- exact commands and manifests;
- additional examples such as DACT D6 and MovieLens portability.

## Paper Layout Implication

Use only two mandatory tables in the 4-page PDF:

- Table 1: method coverage / evidence matrix.
- Table 2: same-item Musical diagnostic case study.

If space allows, include a very small artifact checklist. Do not add a long
appendix section.
