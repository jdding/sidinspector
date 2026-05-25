# Controlled Mechanism Probe Selection

Timestamp: 2026-05-19 19:01:39 CST

Status: **method-inspired mechanism-probe suite executed locally; no named-method evidence claimed**.

Purpose: choose controlled SID/tokenizer mechanism probes that are inspired by
recurring method-family concerns in the SID literature, while keeping them
separate from named tokenizer method coverage.

## Decision

Controlled mechanism probes should stay in a separate artifact-repo table. They are
useful for double-checking whether D1-D5 respond to known method-family
failure modes, but they do not solve the reviewer concern that only a small
number of named tokenizer artifacts are currently in the main evidence.

This separation is important because self-implemented or synthetic probes
introduce implementation choices that are not attributable to the original
paper authors. Therefore:

1. official named-tokenizer artifacts and controlled mechanism probes must appear in
   different tables;
2. probe names must not use paper method names;
3. probes can support metric-sensitivity or finding-interpretation claims,
   not method-superiority claims;
4. a probe is admitted only if it maps to D1-D5 and corresponds to either
   an existing SIDInspector finding or a public related-work failure mode;
5. D7/generator behavior remains out of scope unless real `generator_outputs`
   or candidate traces are available.

## Planned Method-Inspired Probes

| Probe | Existing implementation | Diagnostic target | Current role | v0 action |
|---|---|---|---|---|
| `qualified_collision_probe` | `tools/autodl_audit_sid/run_qualified_collision_probe.py` | D2/D3 | QuaSID-inspired interaction-qualified collision check using co-occurrence and popularity-matched non-collision pairs | **Done**; see `docs/QUALIFIED_COLLISION_PROBE.md` |
| `capacity_budget_sweep` | `tools/autodl_audit_sid/run_capacity_budget_sweep.py` | D1/D2/D4/D5 | AdaSID/CARD-inspired capacity-pressure sweep over fixed-depth code widths | **Done**; see `docs/CAPACITY_BUDGET_SWEEP.md` |
| `variable_depth_cost_probe` | `tools/autodl_audit_sid/run_variable_depth_cost_probe.py` | D5/D7-boundary | CapsID/long-SID-inspired prefix-depth and trie-cost probe | **Done; D5 boundary evidence**; see `docs/VARIABLE_DEPTH_COST_PROBE.md` |

## Existing Generic Calibration Rows

These rows remain useful, but they are no longer the whole mechanism-probe
story. They are generic controls, not method-inspired mechanism-probe evidence.

| Generic row | Existing implementation | Diagnostic target | Current role |
|---|---|---|---|
| `collision_collapse` | `sanity_mod_collision_hash` | D1/D2/D5 | Lower-bound collision calibration; confirms D2/D5 catch full collapse |
| `semantic_only_grouping` | `sanity_category_prefix` | D2/D3/D5 | Category-derived upper-control; shows metadata purity is not the same as learned tokenization |
| `popularity_capacity_skew` | `sanity_popularity_balanced` | D3/D4/D5 | Popularity/capacity calibration; helps interpret popularity allocation and prefix fan-out |
| `drift_churn_probe` | DACT Tools 0.6 -> 0.7 smoke | D6 | Optional temporal-churn example, not part of the D1-D5 main evidence suite |

## Execution Results

1. `qualified_collision_probe`: **done**.
   - Reason: it directly addresses the weakest current D2 caveat: collision is
     currently a profile, not interaction-qualified harm.
   - Output: pair-level CSV plus `paper_assets/tables/table8_qualified_collision_probe.csv`.
   - Finding target: not all SID collisions are equally suspicious; D2 can
     separate raw collision count from interaction-qualified collision risk.

2. `capacity_budget_sweep`: **done**.
   - Reason: it tests whether D1/D2/D4 react coherently when the same item
     universe is compressed under controlled codebook budgets.
   - Output: synthetic fixed-depth SID assignments plus
     `paper_assets/tables/table9_capacity_budget_sweep.csv`.
   - Finding target: capacity pressure can surface as collision, tail-capacity
     loss, or prefix-cost changes; these are separable diagnostic dimensions.

3. `variable_depth_cost_probe`: **done; paper optional**.
   - Reason: it probes the D5 boundary for long/variable SIDs without
     claiming to reproduce CapsID, ACERec, or any unreleased method.
   - Output: variable-depth/EOS-like synthetic SID assignments plus
     `paper_assets/tables/table10_variable_depth_cost_probe.csv`.
   - Finding target: reducing collision or increasing capacity can shift cost
     into depth/path complexity. Include in the paper only if the result is
     clean and fits the four-page narrative.

## Paper Placement

Main paper:

- keep named evidence in Table 1/Table 2;
- if space allows, summarize method-inspired probes as one compact
  artifact/calibration table or one paragraph tied to repository tables;
- prioritize `qualified_collision_probe` and `capacity_budget_sweep` in the
  narrative; use `variable_depth_cost_probe` only if it produces a clean D5
  boundary result.

Artifact repository:

- keep a dedicated method-inspired mechanism-probe table;
- include the method-name boundary in the table caption;
- link each probe to D1-D5 and the related finding it validates;
- keep the older generic sanity rows as calibration rows, not probe
  substitutes.

## Claim Boundaries

Allowed:

- "SIDInspector includes method-inspired controlled mechanism probes for collision
  qualification, capacity pressure, and variable-depth cost."
- "These probes test whether D1-D5 respond to known SID tokenizer failure
  modes."

Not allowed:

- "SIDInspector reproduces QuaSID/AdaSID/CARD/CapsID/ACERec."
- "Probe results are evidence for named method quality."
- "Synthetic probes solve the method coverage breadth gap."

## If Official Releases Arrive

If authors provide official mappings/checkpoints later, compare them only
against named-method rows under the admission rule in
`docs/THIRD_METHOD_EVIDENCE_GATE.md`. Controlled mechanism probes remain calibration
rows. They should not be used as a substitute for, or direct approximation of,
official QuaSID/AdaSID/CapsID/DIGER evidence.
