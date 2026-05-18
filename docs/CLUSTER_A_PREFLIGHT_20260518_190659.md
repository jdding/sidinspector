# Cluster A Preflight: GRID vs CARD

**生成时间**：2026-05-18 19:06:59 CST
**状态**：Cluster A public implementation path prepared, but not yet a Gate 0 pass

## Decision

Use this order on AutoDL:

1. **ReSID robustness matrix**: already has a known working path and validates Cluster B stability.
2. **CARD RQ-VAE fallback**: runnable fallback for a canonical RQ-VAE-style export path once `codes.npy + codes_item_ids.npy` are generated.
3. **GRID RQ-KMeans/RQ-VAE**: most representative Cluster A target, but heavier and should not block the first AutoDL batch.

This is still resource-first. A CARD feature-proxy run can validate the toolkit path and provide a fallback tokenizer artifact; it should not be described as a full CARD reproduction unless the upstream visual/collaborative data pipeline is run.

## Evidence

### GRID

GRID is the cleaner canonical SID candidate:

- README defines semantic-ID learning from item embeddings using RQ-KMeans, RQ-VAE, and RVQ.
- README provides the intended semantic-ID path: train `rkmeans_train_flat`, then infer `rkmeans_inference_flat`.
- `rkmeans_inference_flat.yaml` configures `LocalPickleWriter` with `prediction_name: cluster_ids`.
- `ResidualQuantization.predict_step` returns item IDs as keys and `cluster_ids` as predictions.
- `LocalPickleWriter` merges predictions into `merged_predictions.pkl` and `merged_predictions_tensor.pt`.

Current blocker:

- Local environment is missing GRID's main runtime stack: `lightning`, `hydra`, `omegaconf`, `tensorflow`, `torchmetrics`, and `google.cloud.bigquery`.
- The GRID path also needs prepared item TFRecords/items plus semantic embeddings and a trained SID checkpoint before an item-to-SID mapping exists.
- The existing AUDIT-SID GRID adapter has only passed a synthetic output-format smoke, not a real GRID export.

### CARD

CARD is a viable fallback implementation path:

- README gives a compact pipeline: process data, compose/encode visual units, train `nu-rq-vae`, then run `generate_code.py`.
- `rqvae4/main.py` trains an RQ-VAE over an `item_emb.parquet` input.
- `rqvae4/generate_code.py` exports integer code arrays and a parallel `_item_ids.npy` file when the input parquet has `ItemID`.
- `rqvae4/datasets.py` only requires an `embedding` column, which makes a bounded feature-proxy export feasible for Gate 0 plumbing.

Current limitation:

- A fast feature-proxy CARD run is not a faithful visual CARD reproduction.
- A full CARD reproduction needs the Amazon 2014/image/visual-unit/SASRec pipeline, which is too heavy for the first CIKM sprint batch unless Cluster A remains blocked.

## New Local Support

Added `src/audit_sid/adapters/card.py`:

- input: CARD `codes.npy`;
- item IDs: sibling `codes_item_ids.npy` by default, or explicit `--item-ids`;
- output: normalized `sid_assignments.parquet`.

Smoke status:

```bash
PYTHONPATH=src PYTHONPYCACHEPREFIX=/private/tmp/audit_sid_pycache \
python3 -m audit_sid.adapters.card \
  --codes-path _gate0_artifacts/card_synthetic/codes.npy \
  --output-dir _gate0_artifacts/card_synthetic/normalized \
  --dataset-name synthetic \
  --method card_smoke
```

Result: 3 rows normalized with explicit item IDs.

Added `tools/autodl_audit_sid/run_card_rqvae_export.sh`:

- builds a bounded `item_emb.parquet` from normalized ReSID item metadata using categorical one-hot feature vectors;
- trains CARD `rqvae4/main.py`;
- runs CARD `rqvae4/generate_code.py`;
- normalizes with `audit_sid.adapters.card`;
- runs D1-D5a metrics.

## Recommended AutoDL Queue

Fixed instance: 25 CPU cores, 90 GB RAM, 1 x RTX 5090.

Run these first:

```bash
MATRIX_MODE=robust DEVICE=cuda:0 NUM_WORKERS=8 \
bash tools/autodl_audit_sid/run_resid_matrix.sh
```

```bash
CARD_EPOCHS=20 DEVICE=cuda:0 NUM_WORKERS=8 BATCH_SIZE=1024 \
CODEBOOK_WIDTHS="32 40 19" LAYERS="128 64" \
bash tools/autodl_audit_sid/run_card_rqvae_export.sh
```

Optional only if time remains:

```bash
CARD_EPOCHS=50 DEVICE=cuda:0 NUM_WORKERS=8 BATCH_SIZE=1024 \
CODEBOOK_WIDTHS="32 40 19" LAYERS="256 128" \
EXP_ID=card_rqvae_feature_proxy_e50_seed42 \
bash tools/autodl_audit_sid/run_card_rqvae_export.sh
```

Do not run GRID first unless the above two paths finish or CARD fails at runtime. GRID needs a larger dependency/data setup and is more likely to burn the sprint budget before producing a usable mapping.

## Gate Impact

If CARD fallback runs successfully, Gate 0 will have:

- Cluster B real mapping: ReSID/GAOQ;
- sanity baselines;
- canonical-style fallback mapping: CARD RQ-VAE feature-proxy.

This is still weaker than GRID/RQ-KMeans. The CIKM decision should then depend on whether the case study is framed honestly as resource/toolkit coverage rather than as a complete benchmark of SID methods.
