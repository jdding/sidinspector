# Paper Mechanism-Probe Integration

Timestamp: 2026-05-19 20:06:30 CST

## Purpose

This note records the writing pass that turns the completed method-inspired
mechanism-probe suite into a compact main-text table in the CIKM 2026 Resource
draft. The probes remain outside named-tokenizer method coverage. Their role
is to check whether AUDIT-SID diagnostics react to known artifact mechanisms
that are discussed in the SID literature.

## Integrated Evidence

| Probe | Paper role | Main evidence | Boundary |
|---|---|---|---|
| `qualified_collision_probe` | D2 support for interaction-qualified collision risk | GRID collided pairs show 3.86x train co-occurrence lift over popularity-matched non-collision pairs; collision-heavy hash control shows 1.19x | Bounded mechanism probe, not causal collision harm |
| `capacity_budget_sweep` | D1/D2/D4/D5 support for capacity pressure and popularity allocation | Width-24 head-reserved policy keeps head unique ratio at 1.0 while tail unique ratio is 0.028190 | Controlled allocation probe, not an adaptive-codebook method |
| `variable_depth_cost_probe` | D5 boundary support for active-prefix cost | Active prefix structure can differ from a fixed maximum-depth schema | Interface/cost probe, not generator-output D7 evidence |

## Paper Edits

- `paper/sections/4_demonstration.tex` now adds
  Table~\ref{tab:mechanism-probes} as a controlled mechanism-probe table and
  rewrites the diagnostic findings around Tables 2 and 3.
- `paper/main.tex`, `paper/sections/1_introduction.tex`, and
  `paper/sections/5_availability_limits.tex` were polished to reduce
  experiment-note wording and use a more compact resource-paper style.
- `paper/sections/5_availability_limits.tex` now records that D2 has a bounded
  interaction-qualified mechanism probe but is still not strict causal harm.

## Compile Status

`paper/main.pdf` compiles to 5 pages total. The body fills through page 4, and
references plus the GenAI disclosure occupy page 5. The timestamped snapshot is
`paper/main_20260519_200630.pdf`.

## Claim Boundary

This pass does not change the main evidence boundary:

- named-method evidence remains GRID feature-text and bounded ReSID on the
  same Musical item universe, plus separate GRID scale and ReSID smoke assets;
- probes are calibration rows for D2/D4/D5 interpretation, not third-method
  coverage;
- no downstream Recall@K/NDCG, serving-latency, faithful CARD, or generator
  predictability claim is introduced.
