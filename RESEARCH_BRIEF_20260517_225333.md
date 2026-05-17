# Research Brief

## Working Title

Lifecycle-adaptive off-policy evaluation under sparse support in sequential recommendation.

## Problem Statement

We want to study whether off-policy evaluation (OPE) can give reliable offline evidence for recommendation policies when users move across lifecycle states such as onboarding, active use, pre-churn, and dormant return. The public phase should test a method-level hypothesis: global DR/switch/clipping rules are miscalibrated when support sparsity is lifecycle-structured, and lifecycle-adaptive shrinkage can improve worst-state reliability.

## Core Hypothesis

Lifecycle transitions create structured support and positivity failures. Standard aggregate OPE can look stable while specific lifecycle states have inflated variance, weak overlap, or invalid counterfactual support. A single global shrinkage, clipping, or switch threshold can be wrong in both directions: too conservative for well-supported states and too optimistic for sparse states.

The revised method hypothesis is that a lifecycle-adaptive DR/switch estimator, driven by state-level support diagnostics, can improve worst-state RMSE, coverage, and policy-ranking stability while preserving aggregate value accuracy.

## Context

This project follows a two-stage strategy:

1. Public research preflight: use public logged, randomized, or fully observed recommendation datasets to build and stress-test the methodology.
2. Production validation: only after the public protocol is stable, map the required logging schema to internal business data and compare OPE estimates against real deployment or A/B outcomes.

The public stage is not meant to make production claims. It should first decide whether a method paper is viable. The protocol/checklist package is supporting infrastructure, not the desired final ceiling.

## Constraints

- Data: start with public datasets only. No Huawei data in this repository.
- Compute: prefer reproducible CPU/small-GPU pilots first; avoid large training runs until the protocol is fixed.
- Timeline: first public preflight package should be useful within 2-4 months.
- Target venues for public phase: RecSys, WSDM, SIGIR, WWW/KDD only if the estimator/theory contribution is real. A resource-only fallback is explicitly lower priority.

## Candidate Public Datasets

- Open Bandit Dataset / Open Bandit Pipeline: logged bandit data and standard OPE tooling.
- KuaiRand: sequential recommendation with randomized exposure, timestamps, user/item features, and multiple feedback signals.
- KuaiRec: fully observed user-item matrix for oracle-style bias and support analysis.
- MIND: large-scale news impression logs; useful for temporal/impression analysis but weaker for strict OPE because logged propensities are not available.
- Yahoo R6A/R6B, Yahoo R3, Coat: older debiasing/OPE references; useful as secondary baselines or sanity checks.

## Non-Goals

- Do not claim unbiased production OPE from public-only evidence.
- Do not treat deterministic logged rankings without propensities as strict IPS/DR evidence.
- Do not mix this public OPE protocol line with dormant-return method-paper claims unless the overlap/support diagnostics explicitly justify it.
- Do not optimize for a standalone cold-start method paper in this branch.

## Immediate Outputs

- A public-dataset feasibility matrix.
- A lifecycle-like cohort definition for each selected dataset.
- An estimator benchmark plan covering DM, IPS/IPW, SNIPS, clipped IPS, DR, switch-style variants, and a lifecycle-adaptive shrinkage/switch candidate where supported.
- A sparse-support diagnostic kit: support violation rate, effective sample size, weight tail metrics, per-state confidence interval inflation, and aggregate-vs-state disagreement.
- A method-support decision: whether public datasets can support a lifecycle-adaptive OPE method claim, or whether the line should pause before becoming a resource-only paper.
- A logging checklist for the later production stage.
