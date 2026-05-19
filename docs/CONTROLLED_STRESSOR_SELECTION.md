# Controlled Stressor Selection

Timestamp: 2026-05-19 18:24:00 CST

Status: **controller plan selected; no new method evidence claimed**.

Purpose: choose controlled SID/tokenizer stressors that can strengthen
diagnostic interpretation without being confused with named tokenizer method
coverage.

## Decision

Controlled stressors should stay in a separate artifact-repo table. They are
useful for double-checking whether D1-D5a respond to known failure modes, but
they do not solve the reviewer concern that only a small number of named
tokenizer artifacts are currently in the main evidence.

This separation is important because self-implemented or synthetic stressors
introduce implementation choices that are not attributable to the original
paper authors. Therefore:

1. official named-tokenizer artifacts and controlled stressors must appear in
   different tables;
2. stressor names must not use paper method names;
3. stressors can support metric-sensitivity or finding-interpretation claims,
   not method-superiority claims;
4. a stressor is admitted only if it maps to D1-D5a and corresponds to either
   an existing AUDIT-SID finding or a public related-work failure mode;
5. D7/generator behavior remains out of scope unless real `generator_outputs`
   or candidate traces are available.

## Current Controllers

| Controller | Existing implementation | Diagnostic target | Current role | v0 action |
|---|---|---|---|---|
| `collision_collapse` | `sanity_mod_collision_hash` | D1/D2/D5a | Lower-bound collision calibration; confirms D2/D5a catch full collapse | Use existing Table 3 artifact rows; no new run |
| `semantic_only_grouping` | `sanity_category_prefix` | D2/D3/D5a | Category-derived upper-control; shows metadata purity is not the same as learned tokenization | Use existing Table 3 artifact rows; no new run |
| `popularity_capacity_skew` | `sanity_popularity_balanced` | D3/D4/D5a | Popularity/capacity calibration; helps interpret head-tail and prefix fan-out | Use existing Table 3 artifact rows; no new run |
| `qualified_collision_probe` | not implemented as a separate controller | D2b/D3 | QuaSID-motivated interaction-qualified collision check using co-occurrence and popularity-matched non-collision pairs | Candidate local addition only if it can reuse current Musical artifacts without new GPU |
| `capacity_budget_sweep` | not implemented | D1/D2/D4/D5a | AdaSID/CARD-motivated synthetic capacity-pressure sweep over fixed-depth code widths | Defer unless the paper needs one more artifact-table row |
| `variable_depth_cost_probe` | not implemented | D4/D5a/D7-boundary | CapsID/long-SID-motivated prefix-depth and trie-cost stress test | Defer; do not add unless variable/EOS depth is handled cleanly |
| `drift_churn_probe` | DACT Tools 0.6 -> 0.7 smoke | D6 | Continual-tokenization churn example | Optional artifact evidence only, not main v0 controller |

## Recommended v0 Set

Use the three existing controllers:

- `collision_collapse`;
- `semantic_only_grouping`;
- `popularity_capacity_skew`.

These already support the paper's current findings without adding new code or
new interpretability risk. They should be described as controlled sanity
stressors in the artifact repository, not as extra methods.

One extra controller is worth considering if time permits:

- `qualified_collision_probe`: compute whether full-SID collision groups
  contain interaction-neighbor items more often than matched non-collision
  pairs after controlling for popularity bucket. This would strengthen D2 from
  "collision profile" toward "interaction-qualified collision harm" while
  staying honest that it is not causal downstream harm.

Do not implement `capacity_budget_sweep` or `variable_depth_cost_probe` for v0
unless the paper needs a specific extra claim. They would add more synthetic
degrees of freedom than the current four-page CIKM Resource paper can explain.

## Paper Placement

Main paper:

- keep named evidence in Table 1/Table 2;
- mention controllers only as artifact-repo calibration rows;
- do not use controller rows to claim broader method coverage.

Artifact repository:

- keep a dedicated controlled-stressor table;
- include the method-name boundary in the table caption;
- link each controller to D1-D5a and the related finding it validates.

## If Official Releases Arrive

If authors provide official mappings/checkpoints later, compare them only
against named-method rows under the admission rule in
`docs/THIRD_METHOD_EVIDENCE_GATE.md`. Controlled stressors remain calibration
rows. They should not be used as a substitute for, or direct approximation of,
official QuaSID/AdaSID/CapsID/DIGER evidence.
