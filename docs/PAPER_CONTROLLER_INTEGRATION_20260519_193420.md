# Paper Controller Integration

Timestamp: 2026-05-19 19:34:20 CST

## Purpose

This note records the writing pass that absorbed the completed
method-inspired controller suite into the CIKM 2026 Resource draft. The
controllers remain outside named-tokenizer method coverage. Their role is to
stress-test whether AUDIT-SID diagnostics react to known artifact failure
modes that are discussed in the SID literature.

## Integrated Evidence

| Controller | Paper role | Main evidence | Boundary |
|---|---|---|---|
| `qualified_collision_probe` | D2b support for interaction-qualified collision risk | GRID collided pairs show 3.86x train co-occurrence lift over popularity-matched non-collision pairs; collision-heavy hash control shows 1.19x | Bounded controller, not causal collision harm |
| `capacity_budget_sweep` | D1/D2/D4/D5a support for capacity pressure and head-tail allocation | Width-24 head-reserved policy keeps head unique ratio at 1.0 while tail unique ratio is 0.028190 | Controlled allocation stressor, not an adaptive-codebook method |
| `variable_depth_cost_probe` | D5a boundary support for active-prefix cost | Active prefix structure can differ from a fixed maximum-depth schema | Interface/cost stressor, not generator-output D7 evidence |

## Paper Edits

- `paper/sections/3_resource_demo.tex` now states the three controller-backed
  findings in the diagnostic-findings paragraph.
- `paper/sections/4_availability_limits.tex` now records that D2 has a bounded
  interaction-qualified controller but is still not strict causal harm.
- `paper/main.tex` and `paper/sections/1_introduction.tex` now frame the
  controllers as method-inspired artifact checks rather than method coverage.

## Compile Status

`paper/main.pdf` compiles to 5 pages total. The body fills through page 4, and
references plus the GenAI disclosure occupy page 5. The timestamped snapshot is
`paper/main_20260519_193420.pdf`.

## Claim Boundary

This pass does not change the main evidence boundary:

- named-method evidence remains GRID feature-text and bounded ReSID on the
  same Musical item universe, plus separate GRID scale and ReSID smoke assets;
- controllers are stressors for D2/D4/D5a interpretation, not third-method
  coverage;
- no downstream Recall@K/NDCG, serving-latency, faithful CARD, or generator
  predictability claim is introduced.
