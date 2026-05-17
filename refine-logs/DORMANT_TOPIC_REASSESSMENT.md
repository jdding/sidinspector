# Dormant-User Recommendation Topic Reassessment

**Generated**: 2026-05-18 00:50:53 CST
**Skill**: /research-refine
**Evidence base**: `/Volumes/TU280Pro/Research/research-wiki`
**Scope**: direction reassessment before upgrading this workspace; no new experiment launched.

## Executive Verdict

The next step should not be "continue OPE" and should not be "invent another dormant-return method variant." The wiki shows that the natural method space around dormant-return has already been heavily explored:

- gap-duration adaptation is weak;
- representation/candidate-level improvements often fail full-catalog deployment gates;
- semantic or metadata support is real, but converting it into protected net gain is the hard part;
- protocol/resource work is valuable but below the desired method-paper ambition.

Therefore the correct next move is a problem-level reset:

> Reframe from "dormant-user recommendation method" to "lifecycle transition decision under stale, sparse, and conflicting preference evidence."

OPE should remain a future production-validation/methodology line, not the main problem source for the next method paper.

## Problem Anchor

**Bottom-line problem**: identify a next research direction that is not already exhausted by the existing dormant-return portfolio and can plausibly support a method-level paper.

**Must-solve bottleneck**: dormant-return methods often find support or candidate gains, but those gains do not reliably become deployable full-list net gains under source protection, catalog turnover, and validation-safe evaluation.

**Non-goals**:

- Do not force an OPE paper because production logging assets exist.
- Do not restart gap-bucket, hybrid-routing, LC-STC, or LCP tuning as incremental variants.
- Do not downgrade automatically to a resource/protocol paper.
- Do not claim online deployment without internal logging/A-B evidence.

**Success condition**: a direction is worth upgrading into its own workspace only if it defines a hard problem not already covered by the 5+1 papers, has a plausible method mechanism, and can be validated without relying only on weak candidate-level or protocol-only evidence.

## What The Wiki Says

### 1. Time-gap adaptation is mostly exhausted as a method source

Evidence:

- `idea_gapmaml.md`: gap buckets failed as meta-learning tasks; intra/inter variance ratio was `132.2`, ANOVA `p=0.106`, effect sizes small.
- `idea_hybrid_routing_rolling.md`: no routing crossover point; SASRec beat LT-AGKNet in all rolling-window gap buckets.
- `idea_semantic_deltagate.md`: positive signal exists for `>365d`, but the stronger claim is not "gap alone matters"; it is that behavior collapses while semantic signal may remain usable.

Implication: do not define the next method around gap duration, gap buckets, or simple lifecycle embeddings. The signal is too weak or too easy to absorb into existing DeltaGate-style work.

### 2. Support expansion is real, but deployment conversion is the true bottleneck

Evidence:

- `claim_support_not_deployment.md`: oracle support, candidate gains, or gross-positive reranking can become net-negative after list insertion.
- `idea_casp_semantic_promotion.md`: CASP succeeds because it separates bridge support from deployable promotion and uses gross/cannibal/net accounting.
- `exp_casp_rees46_tmall_synerise.md`: CASP has positive net gains across REES46, Tmall, and Synerise, but REES46 anchor gain is modest and the paper framing is a constrained decision framework, not a heavy algorithmic leap.

Implication: any new method that only creates more auxiliary support is likely low value. The next method must directly address conversion from conflicting evidence sources to deployable decisions.

### 3. Representation adaptation is risky without a new supervision source

Evidence:

- `idea_lc_stc.md`: a qualified small adapter existed at candidate level, but full-gate hits `270/265/261` underperformed frozen BGE `284`.
- `claim_lcstc_not_paper_ready.md`: do not continue threshold, slotting, scalar-loss, or post-hoc sweeps without a materially new source, protocol, or method class.

Implication: "learn a better dormant representation" is not enough. A new method must explain why it survives full-catalog deployment, not only why it improves restricted candidate sets.

### 4. Catalog evolution is promising but infrastructure-heavy

Evidence:

- `idea_grec_catalog_evolution_sid.md`: semantic-ID catalog evolution stopped at FD-6 because utilization/collision/MSE gates failed.
- LCP runs: H&M local signal existed, Tmall transfer failed, lifecycle diagnostic was weak-positive but not enough to rescue the line.

Implication: catalog evolution remains a real problem, but it should not be reopened as a frozen semantic-ID method unless the representation infrastructure is materially improved. It is better as a component of a larger lifecycle-transition problem.

### 5. OPE is valuable but currently not the right mainline

Evidence from this workspace:

- The public OPE novelty check gave the strongest public idea only `5/10` novelty and flagged close overlap with DataCOPE, OBP, deficient-support OPE, high-confidence/pessimistic OPE, and subgroup diagnostics.
- OPE becomes strong only with production logging-policy provenance, propensities/randomization, and online or gray-release ground truth.

Implication: OPE should be kept as a later validation line for lifecycle transitions, not as the next public method engine.

## Reassessment Of The Previous Top-2 Suggestions

### Direction 1: OPE for sequential and temporal recommendation

**Revised status**: hold / future production methodology line.

The prior recommendation was correct that Huawei logging assets can create a differentiator. But it overestimated how much can be done in the public phase and underestimated how crowded OPE methodology already is. Without internal logging-policy provenance and deployment evidence, the line becomes protocol/resource-like. That does not match the current method ambition.

Best future use:

- sparse-positivity OPE for lifecycle transitions;
- logging-policy bias audit for AUDIT-T-style claims;
- production-grounded synthetic trace benchmark only after internal logging abstractions are clear.

Do not make this the next workspace upgrade unless internal data access, compliance, and logging-policy fields are ready.

### Direction 2: User lifecycle modeling at production scale

**Revised status**: strongest umbrella, but original method framing is too weak.

The narrative roof is valuable: dormant-return is one vertical inside lifecycle recommendation. But "lifecycle-conditioned sequence modeling" as a first paper is risky because it can collapse into adding lifecycle embeddings/gates, which repeats the weak gap/lifecycle-signal pattern.

Better framing:

> lifecycle transition decision under stale, sparse, and conflicting preference evidence.

This turns lifecycle from a representation feature into a decision problem: when a user enters a transition state, what evidence should be trusted, protected, explored, or suppressed?

## Candidate Directions After Reassessment

### D1: Preference Evidence Validity for Lifecycle Transitions

**Question**: In dormant or lifecycle-transition states, which preference evidence remains valid, which has expired, and which becomes misleading for deployment?

**Why this fits the wiki**:

- Avoids the failed "gap duration is the task" framing.
- Generalizes CASP's source-protection insight beyond one promotion policy.
- Explains LC-STC failure: candidate evidence can be locally plausible but globally invalid.
- Absorbs DeltaGate as a component, not the whole paper.

**Possible method shape**:

- Define evidence sources: old ID behavior, semantic/attribute evidence, current-session evidence, catalog-trend evidence, protected existing-source hits.
- Learn or estimate an evidence-validity score per source and lifecycle state.
- Use validity scores to decide retention, suppression, promotion, or exploration.
- Evaluate by net gain, cannibalization, protected-hit preservation, and full-catalog retrieval.

**Novelty risk**: medium. If written as "source gating," it is too close to CASP/CALB. It must be framed as validity estimation under lifecycle transition, not just another gate.

**Recommended status**: top candidate for a new method direction.

### D2: Lifecycle Transition Decision Policy

**Question**: Around onboarding, pre-churn, dormant return, and reactivation, how should a recommender trade off familiar exploitation, safe promotion, and preference probing?

**Why this fits the wiki**:

- Moves beyond static "recommend top-K for dormant users."
- Connects to Huawei production reality where lifecycle states and operations already exist.
- Provides a natural place for internal online evidence later.

**Possible method shape**:

- Model lifecycle transition as a constrained decision policy over source categories or slate regions.
- Actions are not only items, but list interventions: protect, promote, probe, diversify, or suppress.
- Objective includes immediate hit, cannibalization, retention proxy, and exploration cost.

**Novelty risk**: medium-high in public data because true intervention feedback is hard to observe. Stronger with internal logging/A-B evidence.

**Recommended status**: second candidate; best production-aligned line.

### D3: Deployable Support Conversion

**Question**: Given multiple candidate sources with partial support, what intervention converts source support into net list gain under preservation constraints?

**Why this fits the wiki**:

- This is the cleanest abstraction of CASP's real contribution.
- It directly targets the strongest supported claim: support expansion is not deployment.

**Possible method shape**:

- A constrained list-intervention layer with source-level reliability, cannibalization prediction, and protected-hit constraints.
- Strong baselines include CASP, unconstrained learned gates, MMR/rerankers, and exact fusion.

**Novelty risk**: high if too close to CASP. Needs a new mechanism, such as calibrated source validity, regret-aware intervention, or explicit uncertainty over cannibalization.

**Recommended status**: use as a unifying abstraction or CASP extension, not automatically as a fresh standalone paper.

### D4: Production OPE For Lifecycle Transitions

**Question**: How reliable are offline estimates for lifecycle-transition interventions under production logging policies?

**Why this fits**:

- Huawei logging assets may create a unique contribution.
- It can validate D1/D2 later.

**Novelty risk**: high in public-only phase, lower with real logging-policy provenance and A/B ground truth.

**Recommended status**: future methodology line, not next public method line.

## Directions To Avoid

| Direction | Reason |
|---|---|
| Gap-bucket meta-learning | Already failed; gap signal too weak. |
| Simple hybrid routing | Rolling-window test invalidated the crossover premise. |
| Another representation adapter over frozen embeddings | LC-STC showed candidate gains do not survive full-catalog gate. |
| Another semantic-ID catalog-evolution pilot | GREC FD-6/LCP closeout shows infrastructure and transfer risks are too high without a materially new setup. |
| Public-only OPE resource paper | Novelty is low and does not match the target method ambition. |
| Generic lifecycle-conditioned SASRec/BERT4Rec | Likely too incremental unless tied to transition decisions and deployable constraints. |

## Recommended Workspace Upgrade

Do not upgrade the current repo into an OPE workspace.

Upgrade into:

> Dormant / Lifecycle Recommendation Reassessment

or more method-facing:

> Lifecycle Transition Decision for Stale Preference Evidence

Suggested branch name:

`codex/lifecycle-transition-reassessment`

Suggested immediate deliverables:

1. `DORMANT_TOPIC_REASSESSMENT.md` as the direction source of truth.
2. A new idea report focused on D1/D2 only, not OPE.
3. A novelty check for:
   - preference evidence validity;
   - lifecycle transition decision policy;
   - deployable support conversion beyond CASP.
4. Only after novelty check, write an experiment plan.

## Current Recommendation

The next serious direction should be:

> Preference Evidence Validity for Lifecycle Transitions.

This has the best fit with the wiki evidence because it keeps the true hard problem: stale and conflicting evidence must be converted into deployable decisions. It also avoids the low-novelty OPE trap and the exhausted gap-duration framing.

However, method difficulty is real. The first validation should be conceptual and novelty-based, not a quick experiment. If novelty check says D1 collapses into CASP/CALB/source gating, then the correct move is not to force another dormant method paper; it is to wait for lifecycle-transition production evidence or shift to the journal/TORS/TOIS consolidation path.
