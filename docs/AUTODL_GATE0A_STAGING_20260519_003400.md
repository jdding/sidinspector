# AutoDL Gate 0A Staging

Timestamp: 2026-05-19 00:34:00 CST

## Status

`TRANSFER_PARTIAL / RUNBOOK_READY / GPU_NOT_REQUIRED_NOW`

Gate 0 artifact feasibility is already passed locally. AutoDL should not be used
for proxy strengthening. The next GPU-worthy work is Gate 0A/paper-strengthening:
larger or dataset-aligned real Cluster A/B exports.

## Current Remote State

Host:

```bash
ssh -p 10197 root@connect.westc.seetacloud.com
```

Observed at 2026-05-19 00:31 CST:

- `/root/autodl-tmp/Sec_phrase` exists.
- `/root/autodl-tmp/hf_models/all_MiniLM_L6_v2` exists.
- `nvidia-smi` returned no GPU rows, consistent with no-GPU mode.
- Synced small files to:
  `/root/autodl-tmp/Sec_phrase/audit_sid_gate0_sync_20260519/`

Synced files include:

- `GATE0_DECISION.md`
- `GRID_CLUSTER_A_EXPORT_PREP.md`
- `prepare_amazon_text_grid_inputs.py`
- `run_grid_rqkmeans_direct_export.py`
- `run_grid_cluster_a_smoke.sh`
- `src/audit_sid/` modules copied flat/with subdirectories under the sync dir

## Missing for Remote GRID Gate 0A Runs

Required before a remote GRID run:

| Path | Status | Notes |
|---|---|---|
| `/root/autodl-tmp/Sec_phrase/_gate0_repos/GRID` | missing in last preflight | copy local clone or git clone exact commit `2fe3475b2d369580234093f35d52b1a2f54d0472` |
| `/root/autodl-tmp/amazon_2023/meta_All_Beauty.jsonl.gz` | missing in last preflight | needed to reproduce local 5k GRID run |
| `/root/autodl-tmp/amazon_2023/All_Beauty.jsonl.gz` | missing in last preflight | needed for interactions |
| `/root/autodl-tmp/hf_models/all_MiniLM_L6_v2` | present | local text embedding model exists remotely |

## Recommended Transfer Commands

From local workspace:

```bash
rsync -avz -e 'ssh -p 10197' \
  _gate0_repos/GRID \
  root@connect.westc.seetacloud.com:/root/autodl-tmp/Sec_phrase/_gate0_repos/

rsync -avz -e 'ssh -p 10197' \
  /Volumes/TU280Pro/Research/DataSet/amazon_2023/meta_All_Beauty.jsonl.gz \
  /Volumes/TU280Pro/Research/DataSet/amazon_2023/All_Beauty.jsonl.gz \
  root@connect.westc.seetacloud.com:/root/autodl-tmp/amazon_2023/
```

These are data/code transfer commands only. Do not launch GPU training from a
no-GPU session.

## Next GPU-Worthy Command

Once GPU is available and paths are present:

```bash
cd /root/autodl-tmp/Sec_phrase
PYTHONPATH=/root/autodl-tmp/Sec_phrase/src \
SKIP_PIP_INSTALL=1 MAX_ITEMS=50000 CODEBOOK_WIDTH=128 NUM_HIERARCHIES=3 \
  STEPS_PER_LAYER=40 GRID_BATCH_SIZE=4096 INIT_BUFFER_SIZE=8192 \
  GRID_DEVICE=cuda EMBED_DEVICE=cuda EMBED_BATCH_SIZE=256 \
  META_JSONL_GZ=/root/autodl-tmp/amazon_2023/meta_All_Beauty.jsonl.gz \
  REVIEWS_JSONL_GZ=/root/autodl-tmp/amazon_2023/All_Beauty.jsonl.gz \
  MODEL_PATH=/root/autodl-tmp/hf_models/all_MiniLM_L6_v2 \
  RUN_ROOT=/root/autodl-tmp/Sec_phrase/_gate0_artifacts/grid_cluster_a_runs \
  EXP_ID=grid_official_rqkmeans_All_Beauty_text_50k_cuda_seed42 \
  bash tools/autodl_audit_sid/run_grid_cluster_a_smoke.sh
```

This is Gate 0A strengthening, not Gate 0 itself. If it is too slow, reduce to
`MAX_ITEMS=20000` before changing method logic.
