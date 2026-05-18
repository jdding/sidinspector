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

## Interpretation

This is materially stronger than the previous CARD compact row because it uses
GRID's public residual k-means implementation path for the SID learner. It can
be treated as a **Cluster A candidate export path**.

It is not yet a formal Gate 0 pass:

- the smoke is only 32 items;
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
