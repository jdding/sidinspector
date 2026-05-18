# CARD Source Repair

Created: 2026-05-18 22:07:26 Asia/Shanghai

## Summary

The public CARD clone in `_gate0_repos/CARD` was incomplete for RQ-VAE export:

- `rqvae4/models/rq.py` was missing, while `rqvae4/models/rqvae.py` imports `from .rq import ResidualVectorQuantizer`.
- `rqvae4/models/vq.py` was missing, while the released residual quantizer expects `VectorQuantizer`.
- `rqvae4/generate_code.py` used `torch.load(...)` without `weights_only=False`, which fails on PyTorch 2.6+ for CARD checkpoints containing `argparse.Namespace`.

This is repairable without GPU. The local fix adds tracked repair templates and an idempotent repair command:

```bash
python3 tools/autodl_audit_sid/repair_card_source.py --card-dir _gate0_repos/CARD
python3 tools/autodl_audit_sid/check_card_source.py --card-dir _gate0_repos/CARD
```

`preflight_autodl.sh` and `run_autodl_gate0_queue.sh` now apply the repair before checking CARD readiness, so the AutoDL queue can reconstruct the missing files from tracked repo contents instead of relying on ignored local clone edits.

## Scope Boundary

This is a compatibility repair for the sprint fallback path, not a claim of faithful CARD reproduction. The supplied `VectorQuantizer` implements nearest-neighbor VQ with straight-through gradients and accepts the released CARD `use_sk`, `sk_epsilon`, and k-means constructor arguments. It does not implement CARD-specific Sinkhorn balancing. Paper-facing wording should keep this line as `CARD RQ-VAE feature-proxy fallback` unless we later replace it with an upstream-complete implementation.

## Local Validation

Passed no-GPU checks:

- Source integrity plus import/forward smoke:

```bash
python3 tools/autodl_audit_sid/check_card_source.py --card-dir _gate0_repos/CARD
```

Result: `[CARD source check] OK`

- Root import compatibility:

```bash
PYTHONPATH=_gate0_repos/CARD PYTHONPYCACHEPREFIX=/tmp/audit_sid_pycache python3 - <<'PY'
from rqvae4.rq import ResidualVectorQuantizer
from rqvae4.models.vq import VectorQuantizer
print('root rq import OK', ResidualVectorQuantizer.__name__, VectorQuantizer.__name__)
PY
```

Result: `root rq import OK ResidualVectorQuantizer VectorQuantizer`

- `NURQVAE` CPU forward smoke via importlib:

Result: `NURQVAE forward OK (5, 8) (5, 2) 0.2538292109966278`

- Full tiny CARD runner smoke on 32 Musical items:

```bash
SKIP_PIP_INSTALL=1 DEVICE=cpu NUM_WORKERS=0 CARD_EPOCHS=1 BATCH_SIZE=8 \
  CODEBOOK_WIDTHS="4 4" LAYERS="8" \
  ITEM_METADATA=_gate0_artifacts/card_cpu_smoke/input/item_metadata.parquet \
  INTERACTIONS=_gate0_artifacts/card_cpu_smoke/input/interactions.parquet \
  RUN_ROOT=_gate0_artifacts/card_cpu_smoke/runs \
  EXP_ID=card_cpu_smoke_20260518_retry \
  bash tools/autodl_audit_sid/run_card_rqvae_export.sh
```

Generated:

- `best_collision_model.pth`
- `card_rqvae_codes.npy`
- `card_rqvae_codes_item_ids.npy`
- `normalized/sid_assignments.parquet`
- `metrics/coverage_report.csv`
- `metrics/d1_utilization.csv`
- `metrics/d2_collision.csv`
- `metrics/d3_alignment.csv`
- `metrics/d4_head_tail.csv`
- `metrics/d5a_deployment_cost.csv`

## Gate Impact

The previous `FORMAL_GATE0_BLOCKED` state for CARD source integrity is cleared at the source/import/CPU-smoke level. Gate 0 still remains open because a paper-facing Cluster A/CARD mapping needs an actual GPU-scale run on canonical data and should be reviewed as a compatibility fallback, not as full CARD reproduction.

## Remote No-GPU Verification

The same repair was synced to the no-GPU AutoDL staging workspace at `/root/autodl-tmp/Sec_phrase` on `ssh -p 10197 root@connect.westc.seetacloud.com`.

Remote commands passed:

```bash
cd /root/autodl-tmp/Sec_phrase
/root/miniconda3/bin/python tools/autodl_audit_sid/repair_card_source.py --card-dir _gate0_repos/CARD
/root/miniconda3/bin/python tools/autodl_audit_sid/check_card_source.py --card-dir _gate0_repos/CARD
REQUIRE_CUDA=0 PYTHON_BIN=/root/miniconda3/bin/python bash tools/autodl_audit_sid/preflight_autodl.sh
```

Remote preflight now reports:

```text
[CARD source check] OK
[AUDIT-SID preflight] CARD_SOURCE_READY
[AUDIT-SID preflight] ASSETS_READY RUNNER_READY
```

CUDA remains unavailable on that instance state: `torch.cuda.is_available=False`.
