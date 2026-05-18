# AutoDL Prelaunch Code Review

**Time**: 2026-05-18 19:53:02 CST
**Scope**: AutoDL Gate 0 launch scripts, summary path, readiness report, and D1-D5a metric plumbing.
**Decision**: quick smoke is ready; formal Gate 0 queues remain blocked until Cluster A/CARD source integrity is repaired or an explicit ReSID-only debug override is chosen.

## Review Method

- Used two code-review subagents before launch:
  - shell/AutoDL path: remote runner, preflight, queue orchestration, archive/shutdown safety;
  - Python/data path: metric summarizer, diagnostic semantics, data coverage, readiness logic.
- Re-ran local verification after fixes:
  - `bash -n` on AutoDL shell runners;
  - `python3 -m py_compile` on toolkit, adapters, metrics, and AutoDL Python helpers;
  - `git diff --check`;
  - local non-strict summary on `_gate0_artifacts/resid_real_runs`.

## Critical Findings Fixed

1. Preflight was too soft for paid GPU launch.
   - `tools/autodl_audit_sid/preflight_autodl.sh` now hard-fails when `REQUIRE_CUDA=1` and `nvidia-smi` or `torch.cuda.is_available()` is missing.
   - Missing required Python modules are collected and returned as a nonzero preflight failure.

2. Remote archive/shutdown path could hide failure.
   - `tools/autodl_audit_sid/run_remote_audit_sid.sh` now checks workspace and queue runner before creating logs.
   - Queue failure, strict summary failure, or archive verification failure exits nonzero and skips shutdown, leaving the instance inspectable.
   - Automatic shutdown only happens after queue, summary, and archive verification all succeed.

3. Robust/sweep/quality could waste GPU as ReSID-only runs while CARD is broken.
   - `tools/autodl_audit_sid/run_autodl_gate0_queue.sh` now checks CARD source integrity before non-quick queues.
   - If CARD is incomplete and `ALLOW_RESID_ONLY=1` is not set, robust/sweep/quality hard-stop before launching.
   - Quick smoke may still run ReSID and record CARD as skipped.

4. Summary could silently accept incomplete metric outputs.
   - `tools/autodl_audit_sid/summarize_gate0_runs.py` now supports `--strict` and requires coverage plus D1-D5a metric files.
   - The remote runner uses strict summary by default.
   - The summary now understands current D2/D3 metric columns and skipped CARD runs.
   - Strict mode skips auxiliary `configs/` and `logs/` directories instead of treating them as failed runs.

5. Readiness report overstated launch readiness.
   - `tools/autodl_audit_sid/write_readiness_report.py` now reports `QUICK_SMOKE_READY / FORMAL_GATE0_BLOCKED_CARD_SOURCE` when CARD source is incomplete.
   - It recommends `QUEUE_MODE=quick` only, and blocks robust/sweep/quality unless CARD is repaired or ReSID-only debugging is explicitly requested.

## Remaining Known Limits

- CARD public clone is incomplete locally: missing `rqvae4/models/rq.py` and `rqvae4/models/vq.py`.
- GRID remains the preferred canonical Cluster A path but is still too heavy/unresolved for immediate launch.
- D2/D3 are currently artifact-level diagnostic proxies, not a causal downstream harm estimate or a full collaborative-alignment oracle.
- Future non-contiguous/string item IDs need an explicit mapping path; current ReSID `Musical_Instruments` IDs are contiguous integer IDs.

## Current Launch Contract

Allowed:

```bash
cd /root/autodl-tmp/Sec_phrase
QUEUE_MODE=quick DEVICE=cuda:0 NUM_WORKERS=8 PYTHON_BIN=python3 \
bash tools/autodl_audit_sid/run_remote_audit_sid.sh
```

Do not run `robust`, `sweep`, or `quality` yet. Those queues are intentionally blocked while CARD/Cluster-A source is incomplete, because a ReSID-only robustness batch cannot pass Gate 0.

## Verification

- Shell syntax: passed.
- Python compile: passed.
- Diff whitespace check: passed.
- Local summary smoke: passed on real ReSID plus sanity/proxy artifacts.
- Local no-GPU queue guard: passed by failing fast with exit code 4 when `REQUIRE_CUDA=1` and `nvidia-smi` is unavailable.
- Refreshed bundle: `_gate0_artifacts/autodl_bundle/audit_sid_autodl_20260518_195614.tar.gz`.
- Bundle SHA256: `bb5031a8a812ad03472fbd02e34f21c8757a06e84591f577a1a27682da59d4f5`.
