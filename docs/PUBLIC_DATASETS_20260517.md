# Public Dataset Feasibility Matrix

## Purpose

This matrix records which public datasets can support lifecycle-stratified OPE claims and which claims must remain limited. It is a preflight artifact, not a final literature review.

| Dataset | Primary Role | Useful Fields | OPE Readiness | Lifecycle Fit | First Use |
|---|---|---|---|---|---|
| Open Bandit Dataset / OBP | Estimator sanity baseline | logged bandit feedback, actions, rewards, behavior policies, OPE tooling | D2-like for supported bandit setting | Weak; limited user lifecycle semantics | Confirm estimator implementation and reporting conventions. |
| KuaiRand | Main sequential public dataset | random exposure, timestamps, user/item features, multiple feedback signals, policy/scenario metadata | D1/D2 candidate depending on exact randomization field use | Strongest public fit | Construct lifecycle-like cohorts and test state-level estimator reliability. |
| KuaiRec | Oracle-style stress test | near fully observed user-item interactions | Oracle/bias stress test rather than logged-policy OPE | Moderate | Compare aggregate vs state-level conclusions under controlled missingness/support thinning. |
| MIND | Impression-scale temporal dataset | user history, timestamped impressions, clicked and non-clicked news | D0/D1 only; no known logged propensity | Moderate for temporal states, weak for strict OPE | Use only for impression-scale diagnostics unless propensity proxy is explicitly justified. |
| Yahoo R6A/R6B | Classic contextual bandit reference | randomized news recommendation logs | D2-style classic OPE reference if accessible | Weak | Optional sanity reference. |
| Yahoo R3 / Coat | Debiasing and MNAR reference | random ratings / exposure correction setting | Useful for debiasing baselines, not lifecycle OPE | Weak | Optional appendix-level baseline. |

## Recommended First Three

1. **Open Bandit Dataset / OBP**
   - Reason: fastest route to a correct OPE estimator implementation.
   - Expected output: estimator API map and a reproducible baseline script.

2. **KuaiRand**
   - Reason: best public match for sequential recommendation under randomized exposure.
   - Expected output: lifecycle-like cohort feasibility report.

3. **KuaiRec**
   - Reason: fully observed matrix enables controlled stress tests of exposure bias and aggregate-vs-state disagreement.
   - Expected output: oracle-style diagnostic report.

## Dataset Readiness Labels

- **D0: observational audit only**
  - Impression/reward logs exist, but no logged propensities or defensible randomization.
  - Permitted claim: exposure or metric bias diagnosis.
  - Forbidden claim: unbiased OPE.

- **D1: estimated-propensity OPE**
  - Candidate set, policy score, policy version, or randomization metadata can support a propensity model.
  - Permitted claim: OPE with explicit estimated-propensity limitation.
  - Required reporting: propensity model diagnostics and sensitivity analysis.

- **D2: strict or near-strict public OPE**
  - Logged propensity or clear random exposure is available.
  - Permitted claim: estimator comparison under recorded/randomized logging policy.
  - Required reporting: support checks, effective sample size, and confidence intervals.

## Initial Source Notes

- Open Bandit Dataset was designed to enable realistic and reproducible OPE comparisons and is paired with Open Bandit Pipeline.
- KuaiRand is a sequential recommendation dataset with randomly exposed items inserted in normal recommendation feeds, plus timestamps, user/item features, and multiple feedback signals.
- KuaiRec contains a fully observed real-world matrix where almost all selected users were exposed to all selected items.
- MIND contains large news impression logs with user histories and clicked/non-clicked impressions, but its public schema does not expose propensities.

## Next Checks

- Verify the exact downloadable schema for KuaiRand and whether the random-exposure rows expose enough information for direct or near-direct propensity assignment.
- Verify whether OBP can be used without large downloads for a first estimator smoke.
- Decide whether MIND adds enough beyond scale to justify inclusion in phase 1.
