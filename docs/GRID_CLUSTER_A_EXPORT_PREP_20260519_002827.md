# GRID Cluster-A Export Prep

Timestamp: 2026-05-19 00:08:04 CST

## Status

`LOCAL_SMOKE_PASSED`

After the Gate 0 re-audit, the next required evidence is a real Cluster A
canonical SID export. I added a bounded GRID/RQ-KMeans path that uses the public
GRID clone instead of CARD/ReSID proxy rows.

## What Changed

- `tools/autodl_audit_sid/prepare_amazon_text_grid_inputs.py`
  - reads Amazon-2023 metadata/reviews;
  - builds AUDIT-SID `item_metadata.parquet` and `interactions.parquet`;
  - encodes item text with a local sentence-transformer model;
  - writes row-aligned `item_embeddings.pt` and `item_ids.npy`.
- `tools/autodl_audit_sid/run_grid_rqkmeans_direct_export.py`
  - imports official GRID classes from `_gate0_repos/GRID`;
  - uses GRID `MiniBatchKMeans`, `SquaredEuclideanDistance`, and
    `KMeansPlusPlusInitInitializer`;
  - trains residual k-means layers directly over prepared embeddings;
  - writes `normalized/sid_assignments.parquet` and D1-D5a metrics.
- `tools/autodl_audit_sid/run_grid_cluster_a_smoke.sh`
  - wraps the full path for local or AutoDL bounded smoke runs.

## Local Smoke

### Smoke-32

Command shape:

```bash
SKIP_PIP_INSTALL=1 MAX_ITEMS=32 CODEBOOK_WIDTH=8 NUM_HIERARCHIES=2 \
  STEPS_PER_LAYER=2 GRID_DEVICE=cpu EMBED_DEVICE=cpu \
  META_JSONL_GZ=/Volumes/TU280Pro/Research/DataSet/amazon_2023/meta_All_Beauty.jsonl.gz \
  REVIEWS_JSONL_GZ=/Volumes/TU280Pro/Research/DataSet/amazon_2023/All_Beauty.jsonl.gz \
  MODEL_PATH=/Volumes/TU280Pro/Research/LLMs/all_MiniLM_L6_v2 \
  RUN_ROOT=_gate0_artifacts/grid_cluster_a_runs \
  EXP_ID=grid_official_rqkmeans_All_Beauty_text_smoke32_local \
  bash tools/autodl_audit_sid/run_grid_cluster_a_smoke.sh
```

Output:

- run directory:
  `_gate0_artifacts/grid_cluster_a_runs/grid_official_rqkmeans_All_Beauty_text_smoke32_local/`
- GRID commit:
  `2fe3475b2d369580234093f35d52b1a2f54d0472`
- items: `32`
- interactions over those items: `857`
- embedding dim: `384`
- codebook: `8 x 2`
- coverage: `32 / 32`, no missing metadata or interaction SID rows
- D5a: `unique_sid=18`, `duplicate_sid_rate=0.4375`, `prefix_counts=8;18`

### Smoke-512

Command shape:

```bash
SKIP_PIP_INSTALL=1 MAX_ITEMS=512 CODEBOOK_WIDTH=32 NUM_HIERARCHIES=3 \
  STEPS_PER_LAYER=5 GRID_BATCH_SIZE=512 INIT_BUFFER_SIZE=512 \
  GRID_DEVICE=cpu EMBED_DEVICE=cpu EMBED_BATCH_SIZE=64 \
  META_JSONL_GZ=/Volumes/TU280Pro/Research/DataSet/amazon_2023/meta_All_Beauty.jsonl.gz \
  REVIEWS_JSONL_GZ=/Volumes/TU280Pro/Research/DataSet/amazon_2023/All_Beauty.jsonl.gz \
  MODEL_PATH=/Volumes/TU280Pro/Research/LLMs/all_MiniLM_L6_v2 \
  RUN_ROOT=_gate0_artifacts/grid_cluster_a_runs \
  EXP_ID=grid_official_rqkmeans_All_Beauty_text_smoke512_local \
  bash tools/autodl_audit_sid/run_grid_cluster_a_smoke.sh
```

Output:

- run directory:
  `_gate0_artifacts/grid_cluster_a_runs/grid_official_rqkmeans_All_Beauty_text_smoke512_local/`
- items: `512`
- embedding dim: `384`
- codebook: `32 x 3`
- per-level unique codes: `32;32;32`
- coverage: `512 / 512`, no missing metadata or interaction SID rows
- D5a: `unique_sid=471`, `duplicate_sid_rate=0.080078125`,
  `prefix_counts=32;312;471`

### Smoke-5000

Command shape:

```bash
SKIP_PIP_INSTALL=1 MAX_ITEMS=5000 CODEBOOK_WIDTH=64 NUM_HIERARCHIES=3 \
  STEPS_PER_LAYER=20 GRID_BATCH_SIZE=2048 INIT_BUFFER_SIZE=4096 \
  GRID_DEVICE=cpu EMBED_DEVICE=cpu EMBED_BATCH_SIZE=128 \
  META_JSONL_GZ=/Volumes/TU280Pro/Research/DataSet/amazon_2023/meta_All_Beauty.jsonl.gz \
  REVIEWS_JSONL_GZ=/Volumes/TU280Pro/Research/DataSet/amazon_2023/All_Beauty.jsonl.gz \
  MODEL_PATH=/Volumes/TU280Pro/Research/LLMs/all_MiniLM_L6_v2 \
  RUN_ROOT=_gate0_artifacts/grid_cluster_a_runs \
  EXP_ID=grid_official_rqkmeans_All_Beauty_text_smoke5000_local \
  bash tools/autodl_audit_sid/run_grid_cluster_a_smoke.sh
```

Output:

- run directory:
  `_gate0_artifacts/grid_cluster_a_runs/grid_official_rqkmeans_All_Beauty_text_smoke5000_local/`
- items: `5000`
- interactions over those items: `40409`
- embedding dim: `384`
- GRID commit:
  `2fe3475b2d369580234093f35d52b1a2f54d0472`
- codebook: `64 x 3`
- per-level unique codes: `64;64;64`
- coverage: `5000 / 5000`, no missing metadata or interaction SID rows
- D5a: `unique_sid=4281`, `duplicate_sid_rate=0.1438`,
  `prefix_counts=64;1895;4281`
- D1: per-level entropy `5.6697;5.8749;5.9250`, Gini
  `0.3665;0.2294;0.1808`

## Interpretation

This is materially stronger than the previous CARD compact row because it uses
GRID's public residual k-means implementation path for the SID learner. It can
be treated as a **real Cluster A export path for Gate 0 artifact feasibility**.

It is not yet paper-ready case-study evidence:

- it uses All_Beauty text, while the main paper-facing vertical decision still
  needs to be frozen and aligned with Cluster B;
- the wrapper bypasses GRID's Hydra/TFRecord input stack, although it imports
  the official GRID k-means modules and records the GRID commit;
- full AutoDL smoke needs dependency/model/data staging before launch.

## Next

1. Code-review this path before remote launch.
2. Stage Amazon-2023 All_Beauty raw files and MiniLM model on AutoDL if absent.
3. Run a bounded AutoDL Cluster A smoke, initially `MAX_ITEMS=5000`,
   `CODEBOOK_WIDTH=64`, `NUM_HIERARCHIES=3`.
4. If stable, decide whether this closes the Cluster A side or whether a stricter
   GRID Hydra run is still required.
