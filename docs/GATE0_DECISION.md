# Gate 0 Decision Re-Audit

Timestamp: 2026-05-18 23:49:58 CST

## Decision

Gate 0 is **not passed** under the literal criteria in `docs/PROJECT_SPEC.md`.

The 2026-05-18 Sports matrix proves that the diagnostic pipeline is unblocked,
but it does not prove that AUDIT-SID has the required real-method coverage:

- real Cluster A canonical SID baseline: **missing**
- real Cluster B named tokenizer/codebook artifact on the formal case-study path:
  **not yet accepted**
- sanity baselines: **present**
- normalized toolkit metrics: **present**

## Root Cause of the Previous Misclassification

The previous `docs/GATE0_RESULTS.md` verdict conflated two different states:

- **Pipeline-unblocked**: adapters, joins, SID normalization, and D1-D5a metric
  runners can operate over Sports-scale SID tables.
- **Gate 0 passed**: at least one real Cluster A method and one real Cluster B
  method export joinable item-to-SID artifacts.

Only the first state is supported by the current evidence.

## Evidence That Does Not Count as Formal Gate 0 Pass

| Row | Why it is useful | Why it cannot satisfy Gate 0 |
|---|---|---|
| `card_rqvae_feature_proxy` | controlled failure case for collision/capacity diagnostics | repaired compact feature-proxy, not upstream CARD and not TIGER/RQ-VAE/GRID |
| `resid_gaoq_unbalanced_proxy` | pipeline-scale ReSID-shaped SID export on Sports | not faithful balanced ReSID/GAOQ; zero collision is structurally induced |
| sanity baselines | metric sensitivity and debugging controls | sanity rows cannot replace a named tokenizer method |

The local `Musical_Instruments` ReSID smoke remains useful as evidence that a
ReSID export path exists, but it does not close Gate 0A because Cluster A is still
missing and the paper-facing Sports result is currently a proxy.

## Required Corrections

1. Keep the current Sports matrix as pipeline evidence only.
2. Label all proxy rows explicitly in future tables.
3. Re-open Gate 0 and Gate 0A in the tracker.
4. Prioritize a real Cluster A export: TIGER/RQ-VAE/GRID-style SID.
5. Accept `Sports_and_Outdoors` as the preferred canonical vertical only after
   documenting the dataset-scope change from the original `Musical_Instruments`
   primary.
6. Do not submit a CIKM abstract unless real Cluster A and real Cluster B exports
   are available with joinable artifacts and at least two meaningful diagnostics.

## Current Operational Status

AutoDL follow-up proxy strengthening is paused. The next GPU spend should target
a real Cluster A export or a strictly bounded smoke that directly de-risks that
export. Further CARD compact proxy runs are lower priority because they would
not fix the Gate 0 coverage gap.
