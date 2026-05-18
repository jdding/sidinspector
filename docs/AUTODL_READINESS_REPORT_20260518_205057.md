# AUDIT-SID AutoDL Readiness Report

**Status**: QUICK_AND_CANONICAL_RESID_READY / FORMAL_GATE0_BLOCKED_CARD_SOURCE

## Bundle

- Path: `_gate0_artifacts/autodl_bundle/audit_sid_autodl_20260518_205057.tar.gz`
- Size bytes: `218460212`
- SHA256: `12a3671e7274f5de2a72b2905dc00508e8f1bc164ab23506c135f364aa9a2293`

## Input Artifacts

- item_metadata rows: `23742`
- interactions rows: `433164`
- item_metadata SHA256: `e409e21f57bb2296c116da69e6c5773e5c38ff87ec6dba901f4537f3b7e86045`
- interactions SHA256: `fde48d018175d5f416e1bdd4da5394b83495715819db6a23775a7b98b524b698`
- canonical verticals staged: `Sports_and_Outdoors`, `Beauty_and_Personal_Care`
- canonical storage: `_gate0_repos/ReSID-dataset` symlinked to external ReSID dataset root locally; bundle dereferences the symlink

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
| `canonical` | `P1` | 2 |
| `robust` | `P1` | 3 |
| `sweep` | `P2` | 5 |
| `quality` | `P3` | 2 |

## Queue Details

| Queue | Priority | Exp ID | Runner | Purpose |
|---|---|---|---|---|
| `quick` | `P0` | `g0_smoke_Musical_Instruments_resid_famae1_seed42` | `resid` | Remote dependency/runtime smoke only; not paper evidence |
| `quick` | `P0` | `card_rqvae_feature_proxy_e5_seed42` | `card` | CARD fallback path smoke; skipped if source incomplete |
| `canonical` | `P1` | `g0_canonical_Sports_and_Outdoors_resid_famae1_seed42` | `resid` | Canonical vertical smoke for paper-facing Gate 0 |
| `canonical` | `P1` | `card_rqvae_feature_proxy_e20_seed42` | `card` | CARD fallback on canonical vertical; skipped if source incomplete |
| `robust` | `P1` | `g0_canonical_Sports_and_Outdoors_resid_famae5_seed42` | `resid` | ReSID stronger export baseline on canonical vertical |
| `robust` | `P1` | `g0_canonical_Sports_and_Outdoors_resid_famae5_seed43` | `resid` | ReSID seed stability on canonical vertical |
| `robust` | `P1` | `card_rqvae_feature_proxy_e20_seed42` | `card` | CARD fallback baseline; skipped if source incomplete |
| `sweep` | `P2` | `g0_canonical_Sports_and_Outdoors_resid_famae5_seed42_cap_small` | `resid` | ReSID capacity sensitivity on canonical vertical |
| `sweep` | `P2` | `g0_canonical_Sports_and_Outdoors_resid_famae5_seed42_cap_large` | `resid` | ReSID capacity sensitivity on canonical vertical |
| `sweep` | `P2` | `card_rqvae_feature_proxy_e20_seed43` | `card` | CARD seed stability; skipped if source incomplete |
| `sweep` | `P2` | `card_rqvae_feature_proxy_e20_seed42_cap_small` | `card` | CARD capacity sensitivity; skipped if source incomplete |
| `sweep` | `P2` | `card_rqvae_feature_proxy_e20_seed42_cap_large` | `card` | CARD capacity sensitivity; skipped if source incomplete |
| `quality` | `P3` | `g0_canonical_Sports_and_Outdoors_resid_famae20_seed42` | `resid` | ReSID quality extension on canonical vertical |
| `quality` | `P3` | `card_rqvae_feature_proxy_e50_seed42` | `card` | CARD quality extension; skipped if source incomplete |

## Launch Command

Run quick smoke first; after it passes, run canonical Sports data-readiness:

```bash
cd /root/autodl-tmp/Sec_phrase
QUEUE_MODE=quick DEVICE=cuda:0 NUM_WORKERS=8 PYTHON_BIN=python3 \
bash tools/autodl_audit_sid/run_remote_audit_sid.sh
```

After quick passes, use `QUEUE_MODE=canonical` for `Sports_and_Outdoors`. Do not run `robust`, `sweep`, or `quality` unless CARD source is repaired, or unless `ALLOW_RESID_ONLY=1` is intentionally set for ReSID-only debugging.

Canonical follow-up command after quick succeeds:

```bash
cd /root/autodl-tmp/Sec_phrase
QUEUE_MODE=canonical DEVICE=cuda:0 NUM_WORKERS=8 PYTHON_BIN=python3 \
bash tools/autodl_audit_sid/run_remote_audit_sid.sh
```
