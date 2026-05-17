# Public OPE Preflight Experiment Plan

**Generated**: 2026-05-17 22:53:33 CST
**Status**: GATED / METHOD-FIRST PREFLIGHT
**Primary method route**: Lifecycle-Adaptive Shrinkage DR for Sparse-Support Sequential Recommendation
**Diagnostic layer**: Lifecycle-State Credibility Protocol for OPE
**Novelty basis**: `refine-logs/NOVELTY_CHECK.md`
**Scope**: public-data phase only; no Huawei/internal data; no production OPE claim.

## Current Position

The project has now completed the required `/research-lit -> /idea-creator -> /novelty-check` chain.

The novelty gate rejects the first top-3 ideas as standalone "new OPE estimator" contributions. This should not force a resource-only paper. The updated direction is method-first: use lifecycle-state diagnostics to build and test a state-adaptive DR/switch/clipping estimator under sparse support.

Therefore this plan is still gated, but the gate now asks whether public datasets can support a method claim. A final claim-driven experiment plan should be written only after Gate A confirms that at least one public setting can compare global vs lifecycle-adaptive OPE estimators under measurable or oracle support sparsity.

## Claim Ladder Under Test

### C1: Public logs differ in lifecycle-OPE readiness

Some public datasets support strict OPE or oracle stress tests; others only support observational diagnostics. The output should be a D0/D1/D2 readiness card per dataset.

### C2: Global OPE shrinkage/switching is miscalibrated under lifecycle-structured support

If lifecycle states have sharply different support and variance, a single global clipping/switch threshold should either over-shrink well-supported states or under-shrink sparse states.

### C3: Lifecycle-adaptive OPE can improve worst-state reliability

The candidate method should improve worst-state RMSE, confidence coverage, policy-ranking stability, or credibility downgrade accuracy relative to global IPS/SNIPS/DR/switch baselines, while not materially damaging aggregate value accuracy.

## Gate A: Dataset Schema Feasibility

Do this before any full experiment.

| Dataset | Required Check | Pass Condition | Failure Action |
|---|---|---|---|
| OBP / Open Bandit Dataset | Estimator API, logged propensities, action/reward/context schema, ground-truth policy comparison examples | Can reproduce small IPW/SNIPW/DR/switch estimates and intervals | Keep only as estimator smoke baseline |
| KuaiRand | Random-exposure subset, timestamps, policy/scenario metadata, pre-exposure user history, item/user metadata | Can define lifecycle-like states without post-treatment leakage and isolate randomized or policy-known slices | Downgrade to D1 diagnostics only |
| KuaiRec | Fully observed user-item matrix and temporal/user metadata | Can construct oracle-style support thinning and aggregate-vs-state reversal stress tests | Use only as non-temporal oracle toy |
| MIND | Impression lists, timestamps, user histories, candidate/click labels | Can define temporal/lifecycle diagnostics while explicitly marking propensity missing | Keep as D0/D1 auxiliary; no strict IPS/DR claims |

For every dataset, add this method-specific audit question:

> Can this dataset compare global vs lifecycle-adaptive DR/switch/clipping under measurable or oracle support sparsity?

## Gate B: Minimal Protocol Pilot

Only run after Gate A passes for at least OBP plus one recommender dataset.

1. Implement dataset readiness cards: D0 observational, D1 estimated-propensity or partial-randomization, D2 logged-propensity/randomized or oracle.
2. Compute lifecycle states using only pre-exposure fields: onboarding/history length, active, pre-churn/inactivity trend, return-like gap where available.
3. Report support diagnostics by state: state size, action coverage, ESS, max/percentile importance weight, CI width, support violation rate.
4. Implement baseline global IPS/SNIPS/DR/switch/clipping estimators.
5. Implement a minimal lifecycle-adaptive shrinkage/switch rule.
6. Compare aggregate vs state-level OPE: value ranking, estimator disagreement, confidence interval inflation, and credibility downgrade cases.
7. Use KuaiRec-style oracle stress tests to check whether lifecycle-adaptive estimators improve sparse-state reliability.

## Gate C: Plan Freeze

Rewrite this file as a final experiment plan only after Gate A and a minimal Gate B smoke pass. The frozen plan must include:

- exact datasets and readiness labels;
- final lifecycle-state definitions;
- estimator list and clipping/switch rules;
- success/failure criteria for each claim;
- baseline subgroup definitions, including non-lifecycle activity/support bins;
- stop rules for downgrading the paper to a dataset-readiness tool;
- paper positioning: method-first if lifecycle-adaptive estimation passes; otherwise stop or pivot, not automatic resource-only submission.

## Explicit Non-Claims

- Do not claim a new OPE estimator until the lifecycle-adaptive mechanism beats global DR/switch/clipping and has a clean risk argument.
- Do not claim strict IPS/DR on MIND.
- Do not claim production validity without Huawei/internal logging-policy evidence.
- Do not use lifecycle labels unless they are pre-exposure and compared against generic subgroup/support baselines.

## Next Action

Run Gate A schema feasibility. Stop after producing a dataset-field audit, updated readiness labels, and a yes/no answer on whether public data can support the lifecycle-adaptive estimator comparison.
