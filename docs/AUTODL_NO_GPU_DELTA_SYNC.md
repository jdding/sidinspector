# AutoDL No-GPU Delta Sync

Timestamp: 2026-05-19 09:56:33 CST

## Status

`TRANSFER_VERIFIED_NO_GPU / ASSETS_READY / RUNNER_READY / FULL_REPRO_BLOCKED_NO_GPU`

Remote:

```text
ssh -p 10197 root@connect.westc.seetacloud.com
```

Workspace:

```text
/root/autodl-tmp/Sec_phrase
```

## What Was Synced

Small-file delta sync only; no large dataset transfer and no queue launch.

Synced paths:

- `AGENTS.md`
- `README.md`
- `START_HERE_AUDIT_SID.md`
- `MANIFEST.md`
- `findings.md`
- `docs/`
- `refine-logs/`
- `src/`
- `tools/`
- `tests/`
- `_gate0_artifacts/dact_tools_smoke/`

DACT artifacts were first copied once to the remote workspace root by the broad
rsync command, then copied again to the documented path:

```text
/root/autodl-tmp/Sec_phrase/_gate0_artifacts/dact_tools_smoke/
```

The root-level duplicate was left untouched because it is small and deleting it
is unnecessary for the no-GPU staging goal.

## Remote Verification

Read-only remote precheck:

```text
host=autodl-container-46d0448b13-75634efc
torch=2.7.0+cu128
torch.cuda.is_available=False
```

Remote tests:

```bash
PYTHONPATH=src /root/miniconda3/bin/python -m unittest tests/test_metrics.py tests/test_sid_churn.py
```

Result:

```text
Ran 4 tests in 0.186s
OK
```

Remote D6 recomputation:

```bash
PYTHONPATH=src /root/miniconda3/bin/python tools/autodl_audit_sid/compute_sid_churn.py \
  --old-sid _gate0_artifacts/dact_tools_smoke/dact_cf_0.6/normalized/sid_assignments.parquet \
  --new-sid _gate0_artifacts/dact_tools_smoke/dact_0.7/normalized/sid_assignments.parquet \
  --output /tmp/d6_churn_verify.csv
```

Key row:

```text
prefix_depth=1 common_items=9610 changed_items=2271 churn_rate_common=0.236316
```

Remote no-GPU preflight:

```bash
REQUIRE_CUDA=0 PYTHON_BIN=/root/miniconda3/bin/python \
bash tools/autodl_audit_sid/preflight_autodl.sh
```

Result:

```text
ASSETS_READY RUNNER_READY
cuda False
```

## Next Action Boundary

While the remote remains no-GPU:

- do file syncs;
- run unit tests / import checks / manifest checks;
- run no-GPU preflight;
- prepare paper/package artifacts.

Do not launch:

- `QUEUE_MODE=quick`;
- `QUEUE_MODE=canonical`;
- `robust`, `sweep`, or `quality`;
- any script that assumes `torch.cuda.is_available=True`.

When GPU returns, first rerun:

```bash
cd /root/autodl-tmp/Sec_phrase
REQUIRE_CUDA=1 PYTHON_BIN=/root/miniconda3/bin/python \
bash tools/autodl_audit_sid/preflight_autodl.sh
```

Only after that passes should any GPU queue be considered.
