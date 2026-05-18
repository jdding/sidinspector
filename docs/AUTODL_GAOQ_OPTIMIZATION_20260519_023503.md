# AutoDL GAOQ Optimization Plan

Timestamp: 2026-05-19 02:35:03 CST

## Status

`PATCH_READY_LOCAL_VALIDATED`

This is an optimization patch for the ReSID GAOQ export stage. It is not yet
deployed to AutoDL and does not change the currently running canonical
`Sports_and_Outdoors` balanced GAOQ job.

## Current Bottleneck

The active AutoDL run is:

- screen: `audit_sid_gate0a_resid_sports_20260519_0148`
- exp id: `gate0a_resid_Sports_and_Outdoors_famae1_seed42_balanced_v2`
- dataset: ReSID processed Amazon-2023 `Sports_and_Outdoors`
- mode: balanced GAOQ, CPU

As of 2026-05-19 02:34:53 CST:

- no `item_code_mapping.parquet` yet;
- no `Traceback`, `ERROR`, or `Exception` in the run directory;
- GAOQ main process elapsed about 49 minutes;
- only three loky workers are active, each around 127-128% CPU.

This means the 30-core AutoDL allocation is not being used effectively. The
reason is that `KMeansConstrained(n_init=3, n_jobs=30)` primarily parallelizes
the three initializations, so it launches about three heavy workers rather than
using all available cores.

## Patch

Local files changed:

- `tools/autodl_audit_sid/patch_resid_runtime.py`
- `tools/autodl_audit_sid/run_resid_gate0_export.sh`

The patch adds three explicit runtime controls:

- `GAOQ_LEVEL2_PARALLEL_JOBS`: number of independent level-2 groups to process
  in parallel;
- `GAOQ_LEVEL2_PARALLEL_BACKEND`: joblib backend, default `loky`;
- `GAOQ_KMEANS_N_INIT`: constrained k-means initialization count, default `3`.

Default behavior remains faithful:

```bash
GAOQ_LEVEL2_PARALLEL_JOBS=1
GAOQ_LEVEL2_PARALLEL_BACKEND=loky
GAOQ_KMEANS_N_INIT=3
```

Only an explicit optimized launch changes behavior.

## Why This Should Help

GAOQ level-2 runs one independent constrained k-means per level-1 cluster. On
`Sports_and_Outdoors`, `b1=128`, so there are up to 128 independent level-2
groups. Parallelizing those groups can use many more CPU cores than the current
three-worker `n_init=3` pattern.

To avoid nested oversubscription, each level-2 group temporarily forces
`GAOQ_KMEANS_N_JOBS=1` when group-level parallelism is enabled. This gives
parallelism across groups rather than launching many nested worker pools.

## Local Validation

Passed:

- `bash -n tools/autodl_audit_sid/run_resid_gate0_export.sh`
- `python3 -m py_compile tools/autodl_audit_sid/patch_resid_runtime.py`
- patch application plus `py_compile` of local patched
  `_gate0_repos/ReSID/model/gaoq.py`
- monkeypatched local GAOQ control-flow smoke with
  `GAOQ_LEVEL2_PARALLEL_JOBS=2`, confirming SID dataframe shape and columns.

Local real `k_means_constrained` smoke could not be used because the local
macOS Python environment has a numpy ABI mismatch for the installed wheel. The
remote AutoDL environment has already run real `k_means_constrained`, so the
next validation step should be a remote tiny smoke after approval.

## Recommended Remote Smoke

Do not disturb the currently running canonical screen unless explicitly
approved.

Recommended first smoke after approval:

```bash
GAOQ_LEVEL2_PARALLEL_JOBS=8
GAOQ_LEVEL2_PARALLEL_BACKEND=loky
GAOQ_KMEANS_N_JOBS=1
GAOQ_KMEANS_N_INIT=1
```

Run this only on a bounded/tiny ReSID GAOQ export first. If it produces a
mapping and shows more CPU utilization, run the formal optimized variant with:

```bash
GAOQ_LEVEL2_PARALLEL_JOBS=24
GAOQ_LEVEL2_PARALLEL_BACKEND=loky
GAOQ_KMEANS_N_JOBS=1
GAOQ_KMEANS_N_INIT=3
```

The `n_init=3` formal variant preserves the current faithful initialization
count while using CPU parallelism across level-2 groups.

## Gate Impact

This patch does not itself close Gate 0A. It only prepares a faster path to
obtain the canonical ReSID `Sports_and_Outdoors` balanced GAOQ mapping if the
current serial-like run remains too slow.
