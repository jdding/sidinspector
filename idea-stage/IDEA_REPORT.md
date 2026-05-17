# Idea Discovery Report

**Direction**: public OPE preflight for lifecycle-transition recommendation  
**Date**: 2026-05-17  
**Pipeline status**: Phase 0/1 initialized; public-data landscape and candidate directions drafted.

## Executive Summary

The recommended public-stage idea is a lifecycle-stratified OPE protocol for sequential recommendation under sparse support. The core contribution is not another generic OPE benchmark, but a state-aware reliability audit: when users are cold, active, pre-churn, or returning, policy overlap and estimator variance can change enough that aggregate OPE is misleading.

The public stage should be treated as a preflight for later production validation. It should freeze estimator choices, diagnostics, dataset-specific lifecycle cohorts, and internal logging requirements before touching Huawei business data.

## Literature Landscape

### Public anchors

- Open Bandit Dataset / OBP provides a standard logged bandit benchmark and implementation path for OPE estimators.
- KuaiRand provides sequential recommendation logs with randomized exposure, timestamps, user/item features, and multiple feedback signals.
- KuaiRec provides a fully observed matrix that can act as a small oracle-style stress test for exposure bias and ranking disagreement.
- MIND provides large impression logs with user histories and clicked/non-clicked impressions, but it is weaker for strict OPE because logging propensities are not available.

### Gap

Existing OPE benchmarks usually evaluate estimator behavior at the whole-population level or under generic context segmentation. They do not center user lifecycle transitions as a structured source of support failure. This leaves a plausible gap: aggregate OPE can pass while lifecycle-state OPE fails.

## Ranked Ideas

### Idea 1: Lifecycle-stratified OPE reliability protocol -- RECOMMENDED

**Thesis**: A target policy can look credible under aggregate OPE while failing support, variance, or confidence diagnostics in specific lifecycle states.

**Public implementation**:

- Use Open Bandit Dataset for standard OPE estimator sanity checks.
- Use KuaiRand to define lifecycle-like cohorts from history length, inactivity gaps, exposure frequency, and recent engagement decay.
- Use KuaiRec to compare logged-policy-style estimates against fully observed or near-oracle policy values.
- Use MIND only as an impression-log stress test unless a defensible propensity proxy is defined.

**Expected contribution**:

- Reliability taxonomy: credible, weakly credible, observational-only.
- Per-state diagnostic suite: support violation, effective sample size, weight tail, confidence inflation, aggregate-vs-state reversal.
- Dataset-to-production logging checklist.

**Risk**:

- If lifecycle-like cohorts are too artificial in public data, the paper becomes a general sparse-support OPE benchmark rather than a lifecycle paper.

### Idea 2: Sparse-positivity estimator benchmark for sequential recommendation -- BACKUP

**Thesis**: Existing estimators degrade differently as lifecycle-like support becomes sparse; clipped/SNIPS/DR variants have predictable failure regimes.

**Public implementation**:

- Controlled support thinning on KuaiRec and KuaiRand.
- Compare DM, IPS/IPW, SNIPS, clipped IPS, DR, and switch-style variants.
- Report estimator bias, variance, rank correlation with oracle/heldout policy value, and confidence coverage.

**Risk**:

- Without a stronger lifecycle framing, this can look like an incremental OPE benchmark.

### Idea 3: Logging schema for deployable recommendation OPE -- INFRASTRUCTURE LINE

**Thesis**: Many recommender logs cannot support strict OPE because they miss propensities, candidate sets, policy versions, or reward-window provenance.

**Public implementation**:

- Build a manifest/validator that labels a dataset or production log extract as D0, D1, or D2.
- D0: observational audit only.
- D1: estimated-propensity OPE.
- D2: strict OPE with recorded propensities or randomized exposure plus deployment/A-B validation.

**Risk**:

- More likely to fit a resource/tooling track than a method track unless paired with Idea 1.

## Eliminated Or Deferred Ideas

- Pure cold-start attribute-conditioned methods: useful but not central to OPE and does not exploit the evaluation-methodology asset.
- Generic generative retrieval: can be a future target policy, but should not define this branch.
- Production-only OPE first: deferred until public diagnostics and logging requirements are stable.

## First Decision Gates

1. Can KuaiRand support non-trivial lifecycle-like state definitions without leaking post-exposure feedback?
2. Can Open Bandit Dataset and OBP provide a clean estimator sanity baseline quickly?
3. Can KuaiRec provide a meaningful oracle-style comparison for support and aggregate-vs-state reversal?
4. Does MIND add value beyond impression-scale illustration, given missing propensities?
5. Does the public package produce a strong enough claim for RecSys/WSDM/SIGIR Resource, or should it remain a technical report until production validation?

## Next Steps

- Create dataset feasibility matrix.
- Implement a small metadata-only preflight for each dataset before downloading large assets.
- Freeze lifecycle cohort definitions before estimator tuning.
- Build diagnostics before training any new recommender policy.
