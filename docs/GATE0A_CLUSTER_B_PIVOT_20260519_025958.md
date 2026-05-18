# Gate 0A Cluster B Pivot

Timestamp: 2026-05-19 02:59:58 CST

## Decision

`PIVOT_FROM_SPORTS_EXACT_BALANCED_GAOQ`

Do not keep Gate 0A blocked on ReSID `Sports_and_Outdoors` exact balanced
GAOQ. The ReSID line is retained as real Cluster B evidence on the smaller
`Musical_Instruments` dataset, while the paper-facing canonical vertical story
must either:

1. use ReSID smaller-dataset evidence honestly; or
2. add a more controllable same-cluster tokenizer/codebook method; or
3. present the Sports exact balanced GAOQ failure as a resource/toolkit
   reproducibility finding rather than as a missing result.

## Evidence

The following AutoDL screens were preserved and stopped:

| Screen | Action | Hardcopy |
|---|---|---|
| `audit_sid_gate0a_resid_sports_20260519_0148` | stopped | `/root/autodl-tmp/Sec_phrase/_gate0_artifacts/autodl_runs/logs/audit_sid_gate0a_resid_sports_20260519_0148_20260519_025941.hardcopy` |
| `audit_sid_gate0a_resid_sports_parallel_v2_20260519_0249` | stopped | `/root/autodl-tmp/Sec_phrase/_gate0_artifacts/autodl_runs/logs/audit_sid_gate0a_resid_sports_parallel_v2_20260519_0249_20260519_025941.hardcopy` |

Observed bottleneck:

- the original Sports exact balanced GAOQ ran for over 70 minutes without
  writing `item_code_mapping.parquet`;
- it had no traceback/error, but only three heavy loky workers were active;
- the local/remote optimization patch passed a synthetic tiny smoke;
- the optimized v2 still hit the same level-1 `KMeansConstrained` bottleneck:
  `n_init=3` effectively creates three heavy CPU workers before the intended
  level-2 group parallelism can help.

## Technical Interpretation

The bottleneck is not FAMAE or GPU training. It is ReSID GAOQ's exact balanced
assignment through `KMeansConstrained`, which relies on CPU optimization
machinery. This is not naturally GPU-portable while preserving faithful ReSID
balanced GAOQ semantics.

GPU alternatives would require changing the method:

- ordinary GPU k-means: fast but unbalanced, not faithful;
- GPU k-means plus greedy balance repair: approximate, not named ReSID GAOQ;
- unbalanced GAOQ: useful as a proxy/stressor, but not formal Cluster B
  evidence.

## Current Gate 0A Position

Gate 0 remains passed for artifact feasibility:

- Cluster A: GRID official-module RQ-KMeans on All_Beauty exports real SID
  artifacts and D1-D5a metrics;
- Cluster B: ReSID balanced GAOQ on Musical_Instruments exports real SID
  artifacts and D1-D5a metrics.

Gate 0A remains open, but the open item is no longer "wait for Sports exact
balanced GAOQ." The open item is now:

- decide whether smaller-dataset ReSID evidence is enough for the CIKM resource
  submission; or
- replace/add another same-cluster tokenizer/codebook method with a tractable
  export path; and
- finish the non-proxy D3 semantic-collaborative diagnostic.

## Next Recommended Work

1. Treat `Musical_Instruments` ReSID balanced GAOQ as the real Cluster B smoke,
   not as paper-facing generalization proof.
2. Keep the ReSID Sports FAMAE checkpoints as reusable assets, but do not spend
   more CPU on exact balanced GAOQ unless there is a new algorithmic path.
3. Prioritize a controlled same-cluster replacement candidate over more ReSID
   Sports exact GAOQ tuning.
4. Update Gate 0A wording so reviewer-facing claims do not imply that Sports
   ReSID balanced GAOQ was successfully reproduced.
