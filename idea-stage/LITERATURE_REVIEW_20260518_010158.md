# Literature Review: Lifecycle Transition Preference Evidence

**Generated**: 2026-05-18 01:01:58 CST
**Skill**: /research-lit
**Scope**: quick landscape for a fresh idea-discovery pass; wiki evidence has priority over external trend-chasing.

## Research-Wiki Prior

The existing wiki defines the strongest internal prior:

- Time-gap adaptation is weak: GapMAML and rolling-window hybrid routing are closed negative lines.
- Support expansion is not deployment: CASP is positive because it protects existing-source hits and accounts for gross/cannibal/net gain.
- Representation adaptation is unsafe without stronger supervision: LC-STC candidate gains failed calibrated full-catalog retrieval.
- Catalog evolution has real signal but heavy infrastructure risk: GREC/LCP found local or weak diagnostic positives but failed transfer/general method gates.

This means the new search should not optimize for "more support" or "more lifecycle embeddings." It should ask how evidence from multiple sources becomes valid or invalid during lifecycle transitions.

## External Landscape

### Lifecycle-stage recommendation

STAN (Stage-Adaptive Network for Multi-Task Recommendation) is the closest lifecycle modeling anchor. It models users' lifecycle stages and reports both offline and online gains. This makes generic lifecycle-conditioned sequence modeling a weak novelty route. Any new paper must move from stage representation to stage-conditioned decision or evidence validity.

Source: https://arxiv.org/abs/2306.12232

### Churn-aware recommender planning

Recent work on online recommendation with churn and aggregated preference feedback frames recommendation as a sequential decision problem where actions can affect user continuation. This is close to lifecycle transition decision, but it is usually not centered on dormant-return evidence validity or source-protected list deployment.

Representative search anchor: Aggregated Preference Optimization for Online Recommender Systems with Churn.

### Preference drift and short/long-term interests

There is a broad literature on evolving user interests, drift, session-vs-long-term preference, and time-aware sequential recommendation. This literature makes "preferences change over time" too generic. The differentiator must be operational: identify which evidence source is still valid for a lifecycle-transition decision, and evaluate by deployable net gain rather than representation similarity.

### Multi-source and multi-behavior recommendation

Multi-behavior recommendation, multi-source fusion, and source gating are dangerous neighboring areas. A method that simply weights old behavior, current behavior, attributes, and semantic evidence will look incremental. The new contribution must include a lifecycle-transition validity criterion, source-protection/cannibalization accounting, or an intervention policy that existing multi-source fusion lacks.

### OPE and counterfactual evaluation

OPE remains relevant as a later validation layer, especially if Huawei logging-policy evidence becomes available. But public-only OPE overlaps strongly with DataCOPE, OBP/OBD, deficient-support OPE, high-confidence OPE, and subgroup diagnostics. It should not define the new idea space.

## Structural Gaps

1. **Evidence validity rather than evidence fusion**: existing models fuse sources; they rarely ask whether a source should be trusted, protected, suppressed, or probed under lifecycle transition.
2. **Deployability rather than candidate support**: candidate gains are insufficient; the wiki shows full-list net gain and cannibalization constraints are decisive.
3. **Transition decision rather than static state modeling**: lifecycle stages alone are not novel; the unresolved problem is what decision to make when state changes.
4. **Public-to-production bridge**: public datasets can screen mechanisms, but production logging is needed for online intervention claims.

## Literature-Grounded Constraints For Idea Generation

- Avoid generic lifecycle embeddings, gap buckets, and simple source weighting.
- Require every method idea to specify how it differs from STAN-style lifecycle modeling and multi-source fusion.
- Require every method idea to state how it survives full-catalog deployment or why it needs production evidence.
- Treat OPE as validation infrastructure, not the central idea.
