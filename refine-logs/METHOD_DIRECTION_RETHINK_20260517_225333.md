# Method Direction Rethink

**Generated**: 2026-05-17 22:53:33 CST
**Skill**: /research-refine
**Problem anchor**: public OPE should be a stage-1 de-risking path toward a publishable method paper, not a resource-only paper.
**Constraint**: no Huawei/internal data in this phase; later production validation is a separate stage.

## Bottom-Line Judgment

The previous novelty result should not be interpreted as "this project can only be a resource paper." It only shows that the first three ideas, as written, are not method contributions. The direction should pivot from:

> lifecycle-state OPE credibility protocol

to:

> lifecycle-structured sparse-support OPE method, with the protocol as a diagnostic and validation layer.

The protocol remains useful, but it should become evidence infrastructure, not the dominant contribution.

## Recommended Top-1 Method Route

### Lifecycle-Adaptive Shrinkage DR for Sparse-Support Sequential Recommendation

**One-sentence method thesis**: When support deficiency is structured by user lifecycle state, a single global DR/switch/clipping rule is miscalibrated; an estimator that learns state-specific shrinkage/switching from support diagnostics can reduce worst-state error while preserving aggregate value accuracy.

**Core technical contribution**:

- Partition logs into pre-exposure lifecycle states.
- Estimate per-state support reliability: effective sample size, weight tail, action coverage, model uncertainty, and state mass.
- Use these diagnostics to choose a state-specific interpolation between direct method, clipped IPS/SNIPS, and DR/switch-DR.
- Optimize a worst-state or risk-regularized objective, not only aggregate MSE.

**Why this is more method-like than the resource route**:

- The paper has an estimator/mechanism, not only a checklist.
- The central claim is falsifiable: state-adaptive shrinkage should beat global clipping/switch and standard DR under lifecycle-structured support sparsity.
- The resource/protocol artifacts become necessary diagnostics and ablations rather than the main novelty.

**Closest risks**:

- Existing switch estimators, DRos, MRDR, deficient-support OPE, and group-robust OPE.
- The method will look incremental unless it includes either a clean risk decomposition or a strong oracle stress test showing global rules fail specifically under lifecycle-structured support.

**Minimum theory target**:

Show a decomposition of aggregate OPE error into lifecycle-state terms and argue that a global switch/clipping threshold is suboptimal when state-level variance/support differs sharply. A modest oracle inequality or state-wise MSE bound is enough for a first method paper; full causal-theory novelty is not required.

## Backup Method Route

### Lifecycle-Conditioned Kernel Support Repair

**One-sentence method thesis**: In sparse lifecycle states, exact action overlap is too brittle; item/user attribute kernels can transfer support locally, but only when a state-level support certificate says the induced bias is bounded.

**Why it fits your portfolio**:

- Reuses AGKNet / kernel / metadata-bridge instincts.
- Turns your existing "attribute-conditioned kernel" asset into an OPE estimator/support-repair mechanism.
- More differentiated from generic group-robust OPE than conservative selection.

**Main risk**:

OPE with embedded actions and side information already exists. This route needs a sharper lifecycle-conditioned support certificate, otherwise reviewers may see it as kernel smoothing plus OPE.

## Revised Research Strategy

1. Keep the current protocol plan only as Gate A/B infrastructure.
2. Add a method gate before paper commitment:
   - Can state-adaptive shrinkage beat global DR/switch/clipping on OBP and KuaiRec stress tests?
   - Does the gain concentrate in sparse lifecycle states rather than generic arbitrary bins?
   - Can we express the improvement with a simple risk decomposition?
3. If yes, write method paper:
   - main contribution: lifecycle-adaptive OPE estimator;
   - supporting contribution: lifecycle credibility protocol;
   - optional module: exploration/logging-design simulator.
4. If no, do not settle for resource-only by default. Either pivot to the kernel support-repair route or wait for internal logging evidence.

## Immediate Next Step

Run Gate A schema feasibility, but add one method-specific question to every dataset audit:

> Does this dataset allow us to compare global vs lifecycle-adaptive DR/switch/clipping under measurable or oracle support sparsity?

If the answer is no for all public datasets, the public phase should stop at de-risking and not become a standalone resource paper.
