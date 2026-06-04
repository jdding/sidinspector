# SIDInspector Project State

Last updated: 2026-06-04

## Project Layout

This repository is the formal SIDInspector project. It should contain the
maintained toolkit code, reviewer-facing documentation, V0 paper source, and
future V1 work.

- `src/sidinspector/`: released toolkit code and future D7 extensions.
- `docs/`: resource documentation, reproducibility matrix, adapter notes, and
  project state.
- `papers/cikm2026-resource-v0/`: CIKM 2026 Resource V0 paper source and final
  PDF snapshot.
- `experiments/`: future experiment work. Create `experiments/d7_generator_traces/`
  before starting SIDInspector V1 experiments.

## V0 Boundary

V0 is a CIKM 2026 Resource-track artifact/interface claim. It supports
mapping-first inspection of Semantic-ID tokenizer artifacts through adapter
contracts, validation, D1-D5 mapping probes, optional D6 churn, reviewer
quickstart, official adapter rows, and a reproducibility matrix.

Do not upgrade V0 into a tokenizer leaderboard, third named-method coverage
claim, trained-generator validation, causal collision-harm claim, or measured
serving-latency claim without new evidence.

## V1 Direction

The intended V1 line is D7 generator-trace diagnostics. The first gate should
define a trace schema, SID-to-item reverse lookup, invalid/stale/out-of-catalog
failure taxonomy, and a small Musical/Beauty smoke that tests whether D1-D5
mapping signals predict D7 generator failures.

Keep V1 small until D7 shows non-redundant signal. Do not start a broad adapter
sweep or leaderboard framing before the D7 gate is passed.

## Incubator Boundary

The previous incubator workspace remains at:

`/Users/timber/Documents/Sec_phrase`

Large historical SID artifacts and cloned upstream repositories remain there:

- `/Users/timber/Documents/Sec_phrase/_gate0_artifacts`
- `/Users/timber/Documents/Sec_phrase/_gate0_repos`

Those directories are not part of the formal SIDInspector repository. Reference
them only as local provenance or historical evidence paths.
