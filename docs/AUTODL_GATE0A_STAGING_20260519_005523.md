# AutoDL Gate 0A Staging

Timestamp: 2026-05-19 00:34:00 CST

## Status

`TRANSFER_VERIFIED / PREFLIGHT_READY / GPU_NOT_REQUIRED_NOW`

Gate 0 artifact feasibility is already passed locally. AutoDL should not be used
for proxy strengthening. The next GPU-worthy work is Gate 0A/paper-strengthening:
larger or dataset-aligned real Cluster A/B exports.

## Current Remote State

Host:

```bash
ssh -p 10197 root@connect.westc.seetacloud.com
```

Observed at 2026-05-19 00:31-00:52 CST:

- `/root/autodl-tmp/Sec_phrase` exists.
- `/root/autodl-tmp/hf_models/all_MiniLM_L6_v2` exists.
- `nvidia-smi` returned no GPU rows, consistent with no-GPU mode.
- Synced small files to:
  `/root/autodl-tmp/Sec_phrase/audit_sid_gate0_sync_20260519/`
- Synced runnable scripts to:
  `/root/autodl-tmp/Sec_phrase/tools/autodl_audit_sid/`
- Synced GRID clone to:
  `/root/autodl-tmp/Sec_phrase/_gate0_repos/GRID`
- Synced Amazon raw files to:
  `/root/autodl-tmp/amazon_2023/`

Synced files include:

- `GATE0_DECISION.md`
- `GRID_CLUSTER_A_EXPORT_PREP.md`
- `prepare_amazon_text_grid_inputs.py`
- `run_grid_rqkmeans_direct_export.py`
- `run_grid_cluster_a_smoke.sh`
- `src/audit_sid/` modules copied flat/with subdirectories under the sync dir

Additional Gate 0A helpers prepared locally:

- `tools/autodl_audit_sid/preflight_gate0a_grid.sh`
- `tools/autodl_audit_sid/run_gate0a_grid_batch.sh`

## Missing for Remote GRID Gate 0A Runs

Required before a remote GRID run:

| Path | Status | Notes |
|---|---|---|
| `/root/autodl-tmp/Sec_phrase/_gate0_repos/GRID` | present | copied local clone; commit fallback reports `2fe3475b2d369580234093f35d52b1a2f54d0472` |
| `/root/autodl-tmp/amazon_2023/meta_All_Beauty.jsonl.gz` | present | 39 MB |
| `/root/autodl-tmp/amazon_2023/All_Beauty.jsonl.gz` | present | 91 MB |
| `/root/autodl-tmp/hf_models/all_MiniLM_L6_v2` | present | local text embedding model exists remotely |

Remote preflight result:

```text
[GATE0A preflight] READY
python_imports=OK
```

## Transfer Commands Used

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

Once GPU is available and paths are present, first run:

```bash
cd /root/autodl-tmp/Sec_phrase
bash tools/autodl_audit_sid/preflight_gate0a_grid.sh
```

Then run:

```bash
cd /root/autodl-tmp/Sec_phrase
SKIP_PIP_INSTALL=1 MAX_ITEMS=50000 CODEBOOK_WIDTH=128 NUM_HIERARCHIES=3 \
  STEPS_PER_LAYER=40 GRID_BATCH_SIZE=4096 INIT_BUFFER_SIZE=8192 \
  DEVICE=cuda EMBED_BATCH_SIZE=256 \
  EXP_ID=grid_official_rqkmeans_All_Beauty_text_50k_cuda_seed42 \
  bash tools/autodl_audit_sid/run_gate0a_grid_batch.sh
```

This is Gate 0A strengthening, not Gate 0 itself. If it is too slow, reduce to
`MAX_ITEMS=20000` before changing method logic.

## Gate 0A Readiness Criteria

The next remote GRID run should be evaluated against:

- no missing item metadata or interaction SID joins;
- D1-D5a CSVs present;
- SID depth fixed at 3 for GRID and explicitly caveated against ReSID depth;
- no proxy rows counted as method evidence;
- elapsed time and GPU utilization recorded in the run log;
- if 50k is too slow, one successful 20k run is still useful as a stronger
  paper-facing Cluster A artifact than the local 5k smoke.
