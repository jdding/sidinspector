# Public OPE Preflight Experiment Plan

## Objective

Build a public-data methodology preflight for lifecycle-stratified off-policy evaluation in recommendation. The public phase should determine which estimator and diagnostic claims are stable enough to justify later production validation.

## Claim Ladder

### Claim 1: Aggregate OPE can hide lifecycle-state unreliability.

Evidence required:

- Aggregate policy-value estimate is stable.
- At least one lifecycle-like state shows low effective sample size, heavy importance weights, high support violation, or inflated confidence intervals.
- The aggregate conclusion changes or weakens after per-state reliability gating.

### Claim 2: Lifecycle-stratified diagnostics can classify OPE estimates by credibility.

Evidence required:

- A fixed diagnostic rule assigns estimates to credible, weakly credible, or observational-only.
- The rule behaves consistently across at least two datasets.
- Failure cases are reported, not filtered out.

### Claim 3: Public-data diagnostics produce a concrete production logging checklist.

Evidence required:

- Each public dataset is mapped to D0/D1/D2 OPE readiness.
- Missing fields are tied to exact estimator limitations.
- The checklist is usable before internal data access.

## Dataset Plan

### Datasets to inspect first

1. Open Bandit Dataset / OBP
   - Role: estimator sanity baseline.
   - Strength: logged bandit data and OPE tooling.
   - Weakness: limited lifecycle semantics.

2. KuaiRand
   - Role: primary sequential/lifecycle-like dataset.
   - Strength: randomized exposure, timestamps, user and item features, multiple feedback signals.
   - Weakness: lifecycle states must be reconstructed from public fields.

3. KuaiRec
   - Role: oracle-style bias and support stress test.
   - Strength: fully observed matrix.
   - Weakness: small and less production-like for lifecycle transitions.

4. MIND
   - Role: impression-scale temporal stress test.
   - Strength: large impression logs and user histories.
   - Weakness: no known propensity scores; strict OPE claims should be avoided.

## Estimators

- Direct Method (DM)
- IPS/IPW
- SNIPS/self-normalized IPS
- Clipped IPS
- Doubly Robust (DR)
- Switch-style DR if implementation support is available

## Diagnostics

- Per-state sample size
- Effective sample size
- Support violation rate
- Max/percentile importance weight
- Weight concentration by policy, state, and action/item group
- Bootstrap confidence interval width
- Aggregate-vs-state conclusion disagreement
- D0/D1/D2 readiness label

## Run Order

### Phase A: Metadata and feasibility preflight

- Confirm data access, schema, and license.
- Create a dataset readiness table.
- Define candidate lifecycle-like states using only pre-exposure information.

### Phase B: Estimator sanity baseline

- Run OBP examples on Open Bandit Dataset.
- Confirm reproducible IPS/SNIPS/DR-style estimates.
- Record estimator API and required input schema.

### Phase C: Lifecycle-state construction

- Construct lifecycle-like cohorts on KuaiRand.
- Validate no post-exposure leakage.
- Stress test cohort balance and sparsity.

### Phase D: Sparse-support experiments

- Run estimators per state.
- Add controlled support thinning where needed.
- Compare aggregate and state-level conclusions.

### Phase E: Report and production checklist

- Freeze public conclusions.
- List exact fields required for internal production validation.
- Decide whether the public phase is paper-ready or should remain a tech report until stage 2.

## Stop Rules

- Stop if a dataset lacks enough schema transparency to support the intended claim.
- Stop if lifecycle-like states require post-outcome information.
- Do not expand to internal data until the public diagnostic protocol is fixed.
- Do not claim unbiased OPE without propensities, randomized exposure, or an explicit estimated-propensity limitation.
