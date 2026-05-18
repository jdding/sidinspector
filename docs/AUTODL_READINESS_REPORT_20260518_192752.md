# AUDIT-SID AutoDL Readiness Report

**Status**: TRANSFER_READY / RUNNER_READY / FULL_REPRO_BLOCKED_NO_GPU

## Bundle

- Path: `_gate0_artifacts/autodl_bundle/audit_sid_autodl_20260518_192752.tar.gz`
- Size bytes: `31111660`
- SHA256: `44c6fe8e76b250f2d2916b84ada66fcf768fd6e4516b6c6a5b34a83d2e1c553e`

## Input Artifacts

- item_metadata rows: `23742`
- interactions rows: `433164`
- item_metadata SHA256: `e409e21f57bb2296c116da69e6c5773e5c38ff87ec6dba901f4537f3b7e86045`
- interactions SHA256: `fde48d018175d5f416e1bdd4da5394b83495715819db6a23775a7b98b524b698`

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
| `quick` | `P0` | `card_rqvae_feature_proxy_e5_seed42` | `card` | CARD fallback path smoke |
| `robust` | `P1` | `g0_e2_resid_famae5_seed42` | `resid` | ReSID stronger export baseline |
| `robust` | `P1` | `g0_e3_resid_famae5_seed43` | `resid` | ReSID seed stability |
| `robust` | `P1` | `card_rqvae_feature_proxy_e20_seed42` | `card` | CARD fallback baseline |
| `sweep` | `P2` | `g0_e4_resid_famae5_seed42_cap_small` | `resid` | ReSID capacity sensitivity |
| `sweep` | `P2` | `g0_e5_resid_famae5_seed42_cap_large` | `resid` | ReSID capacity sensitivity |
| `sweep` | `P2` | `card_rqvae_feature_proxy_e20_seed43` | `card` | CARD seed stability |
| `sweep` | `P2` | `card_rqvae_feature_proxy_e20_seed42_cap_small` | `card` | CARD capacity sensitivity |
| `sweep` | `P2` | `card_rqvae_feature_proxy_e20_seed42_cap_large` | `card` | CARD capacity sensitivity |
| `quality` | `P3` | `g0_e4_resid_famae20_seed42` | `resid` | ReSID quality extension |
| `quality` | `P3` | `card_rqvae_feature_proxy_e50_seed42` | `card` | CARD quality extension |

## Launch Command

Preferred robust runner:

```bash
cd /root/autodl-tmp/Sec_phrase
QUEUE_MODE=robust DEVICE=cuda:0 NUM_WORKERS=8 PYTHON_BIN=python3 \
bash tools/autodl_audit_sid/run_remote_audit_sid.sh
```

Use `QUEUE_MODE=sweep` only after quick or robust passes.
