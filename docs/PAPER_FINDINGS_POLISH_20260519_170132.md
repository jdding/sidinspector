# Paper Findings Polish

Timestamp: 2026-05-19 17:01:32 CST

Purpose: record the results-based paper polish after the v0 experiment package
was closed.

## Changes

- Abstract now includes the GRID Musical three-seed stability range:
  full-collision rate stays within `0.9751--0.9769`.
- Introduction now states that the case study supports diagnostic findings,
  not model-quality claims.
- Section 3 now has an explicit `Diagnostic findings` paragraph:
  1. collision pressure is stable in the controlled GRID Musical row;
  2. collision-free full codes and collaborative-prefix alignment are separate
     objectives;
  3. D4/D5a separate tail capacity from prefix/fan-out structure.
- Section 4 now restates why the case study is resource-worthy without
  ranking GRID against ReSID.

## Claim Boundary

The polish does not add new experimental claims. It only rephrases existing
evidence from:

- `paper_assets/tables/table2_musical_diagnostic.csv`;
- `paper_assets/tables/table3_sanity_controls.csv`;
- `paper_assets/tables/table7_grid_musical_3seed.csv`;
- `docs/GRID_MUSICAL_3SEED_LOCAL.md`.

The draft still avoids downstream superiority, faithful TIGER/GRID
reproduction, faithful CARD reproduction, real serving latency, and D7
generator-output claims.

## Verification

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` succeeds.
- The compiled PDF remains 5 pages total, with the paper body through page 4
  and references/GenAI disclosure on page 5.
