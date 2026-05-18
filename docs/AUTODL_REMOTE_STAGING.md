# AutoDL Remote Staging Status

**Time**: 2026-05-18 21:20:37 CST
**Remote**: `ssh -p 10197 root@connect.westc.seetacloud.com`
**Workspace**: `/root/autodl-tmp/Sec_phrase`
**Status**: `TRANSFER_VERIFIED / ASSETS_READY / RUNNER_READY / FULL_REPRO_BLOCKED_NO_GPU`

## Skill State

This follows `autodl-cloud-deploy` Phase B/B.5:

- active workspace is `/root/autodl-tmp/Sec_phrase`;
- `/root/autodl-fs` / `/autodl-fs/data` is not used for active execution;
- no GPU queue was launched;
- no manual shutdown command was issued;
- full GPU reproduction remains blocked because the current instance has no usable GPU.

## Transfer

The full 208M bundle was too slow over the local SSH route and was intentionally stopped. The adopted staging route is:

1. transfer a slim code bundle;
2. unpack it under `/root/autodl-tmp/Sec_phrase`;
3. download ReSID processed parquet shards from `hf-mirror.com` directly on AutoDL.

Slim bundle:

```text
audit_sid_autodl_slim_20260518_210659.tar.gz
```

Remote checksum:

```text
2e4a73e0e9ebe98af395b902700224d1bbbceedbf0eefae9bf29b42460f9980f
```

Remote upload directory after cleanup:

```text
/root/autodl-tmp/audit_sid_uploads/audit_sid_autodl_slim_20260518_210659.tar.gz
```

## Remote Environment

```text
host: autodl-container-46d0448b13-75634efc
python: /root/miniconda3/bin/python
python version: 3.12.3
torch: 2.7.0+cu128
torch.cuda.is_available: False
```

Disk:

```text
/root/autodl-tmp: 100G total, 26G available
/autodl-fs/data: 200G total, 87G available
```

Remote `preflight_autodl.sh` result:

```text
ASSETS_READY RUNNER_READY
```

CARD source remains incomplete:

```text
_gate0_repos/CARD/rqvae4/models/rq.py
_gate0_repos/CARD/rqvae4/models/vq.py
```

## Dataset Assets

Remote ReSID processed datasets were downloaded from `hf-mirror.com`.

| Category | Dataset shard size | Normalized item metadata rows | Normalized interaction rows | Unique interaction items |
|---|---:|---:|---:|---:|
| `Musical_Instruments` | 12M | 23,742 | 433,164 | 23,736 |
| `Sports_and_Outdoors` | 87M | 151,411 | 2,924,461 | 151,356 |
| `Beauty_and_Personal_Care` | 150M | 193,383 | 5,072,879 | 193,231 |

Remote dataset manifest:

```text
_gate0_artifacts/resid_dataset_download_manifest_remote.json
manifest_entries=29
manifest_size=259,698,091 bytes
categories=Beauty_and_Personal_Care, Musical_Instruments, Sports_and_Outdoors
```

Normalized artifacts:

```text
_gate0_artifacts/resid_Musical_Instruments_normalized/
_gate0_artifacts/resid_Sports_and_Outdoors_normalized/
_gate0_artifacts/resid_Beauty_and_Personal_Care_normalized/
_gate0_artifacts/resid_musical_normalized -> resid_Musical_Instruments_normalized
```

## Next GPU Action

When GPU is available, first re-run read-only preflight:

```bash
cd /root/autodl-tmp/Sec_phrase
REQUIRE_CUDA=1 PYTHON_BIN=/root/miniconda3/bin/python \
bash tools/autodl_audit_sid/preflight_autodl.sh
```

Then launch quick smoke only:

```bash
cd /root/autodl-tmp/Sec_phrase
QUEUE_MODE=quick DEVICE=cuda:0 NUM_WORKERS=8 PYTHON_BIN=/root/miniconda3/bin/python \
bash tools/autodl_audit_sid/run_remote_audit_sid.sh
```

After quick passes, launch canonical Sports data-readiness:

```bash
cd /root/autodl-tmp/Sec_phrase
QUEUE_MODE=canonical DEVICE=cuda:0 NUM_WORKERS=8 PYTHON_BIN=/root/miniconda3/bin/python \
bash tools/autodl_audit_sid/run_remote_audit_sid.sh
```

Do not run `robust`, `sweep`, or `quality` until canonical Sports passes and the CARD/Cluster-A blocker is resolved or explicitly scoped as ReSID-only debugging.
