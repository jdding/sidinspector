# AUDIT-SID AutoDL Readiness Report

**Status**: TRANSFER_READY / RUNNER_READY / FULL_REPRO_BLOCKED_NO_GPU

## Bundle

- Path: `_gate0_artifacts/autodl_bundle/audit_sid_autodl_20260518_193310.tar.gz`
- Size bytes: `31120827`
- SHA256: `e052e148b69169da888bee60a745bdee7a7242b8801c8548a1f16c12f60549c5`

## Input Artifacts

- item_metadata rows: `23742`
- interactions rows: `433164`
- item_metadata SHA256: `e409e21f57bb2296c116da69e6c5773e5c38ff87ec6dba901f4537f3b7e86045`
- interactions SHA256: `fde48d018175d5f416e1bdd4da5394b83495715819db6a23775a7b98b524b698`

## Source Integrity

- CARD source status: `INCOMPLETE`
- CARD missing files:
  - `_gate0_repos/CARD/rqvae4/models/rq.py`
  - `_gate0_repos/CARD/rqvae4/models/vq.py`
- AutoDL queue default: `CARD_SOURCE_FAIL=skip`; ReSID runs continue and CARD runs write `SKIPPED.txt`.

## Experiment Matrix

| Queue | Priority | Runs |
|---|---:|---:|
| `quick` | `P0` | 2 |
| `robust` | `P1` | 3 |
| `sweep` | `P2` | 5 |
| `quality` | `P3` | 2 |

## Queue Details

| Queue | Priority | Exp ID | Runner | Purpose |
|---|---|---|---|---|
| `quick` | `P0` | `g0_e1_resid_famae1_seed42` | `resid` | Remote dependency/runtime smoke |
| `quick` | `P0` | `card_rqvae_feature_proxy_e5_seed42` | `card` | CARD fallback path smoke; skipped if source incomplete |
| `robust` | `P1` | `g0_e2_resid_famae5_seed42` | `resid` | ReSID stronger export baseline |
| `robust` | `P1` | `g0_e3_resid_famae5_seed43` | `resid` | ReSID seed stability |
| `robust` | `P1` | `card_rqvae_feature_proxy_e20_seed42` | `card` | CARD fallback baseline; skipped if source incomplete |
| `sweep` | `P2` | `g0_e4_resid_famae5_seed42_cap_small` | `resid` | ReSID capacity sensitivity |
| `sweep` | `P2` | `g0_e5_resid_famae5_seed42_cap_large` | `resid` | ReSID capacity sensitivity |
| `sweep` | `P2` | `card_rqvae_feature_proxy_e20_seed43` | `card` | CARD seed stability; skipped if source incomplete |
| `sweep` | `P2` | `card_rqvae_feature_proxy_e20_seed42_cap_small` | `card` | CARD capacity sensitivity; skipped if source incomplete |
| `sweep` | `P2` | `card_rqvae_feature_proxy_e20_seed42_cap_large` | `card` | CARD capacity sensitivity; skipped if source incomplete |
| `quality` | `P3` | `g0_e4_resid_famae20_seed42` | `resid` | ReSID quality extension |
| `quality` | `P3` | `card_rqvae_feature_proxy_e50_seed42` | `card` | CARD quality extension; skipped if source incomplete |

## Launch Command

Preferred robust runner:

```bash
cd /root/autodl-tmp/Sec_phrase
QUEUE_MODE=robust DEVICE=cuda:0 NUM_WORKERS=8 PYTHON_BIN=python3 \
bash tools/autodl_audit_sid/run_remote_audit_sid.sh
```

Use `QUEUE_MODE=sweep` only after quick or robust passes.
