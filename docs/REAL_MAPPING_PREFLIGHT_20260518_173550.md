# Real SID Mapping Preflight

**生成时间**：2026-05-18 17:35:50 CST
**状态**：real tokenizer mapping not available locally; Gate 0 remains open

## Question

Can the cloned public repos immediately provide a real item-to-SID mapping that can be normalized into `src/audit_sid/interface.py` without launching full training?

## Result

No. The adapter and metric plumbing are ready, but neither local clone contains a real pretrained/exported SID mapping.

| Method | Local export path | Immediate real mapping? | Blocker |
|---|---|---:|---|
| ReSID / GAOQ | `item_feature/item_code_mapping.parquet` | No | Requires FAMAE training checkpoint (`best_model.pth` or `model.pth`) before GAOQ can run. The clone has config defaults but no checkpoint artifacts. |
| GRID / RQ-VAE or RKMeans | `pickle/merged_predictions_tensor.pt` or `merged_predictions.pkl` | No | Requires P5/Amazon-formatted data, item embeddings, and a trained SID checkpoint before `rkmeans_inference_flat` can emit mappings. The clone has code/configs but no embeddings/checkpoints/exported mappings. |
| CARD fallback | `.npy` codes plus `_item_ids.npy` | Not checked in this preflight | Earlier repo audit found an export path, but preprocessing/checkpoint setup is heavier than ReSID/GRID and should stay fallback. |

## Evidence

ReSID:

- `run_pipelines.py` runs FAMAE first, finds `model.pth` or `best_model.pth`, then passes that path into GAOQ.
- `config/gaoq.yaml` requires `pretrained_model_path`.
- `model/gaoq.py` writes `item_feature/item_code_mapping.parquet`, but only after loading the pretrained FAMAE embedding parameters.
- The cloned ReSID repo has configs only; no `.pth`, `.pt`, or parquet mapping artifacts were found.

GRID:

- `README.md` requires data preparation, embedding generation, SID training, and then SID inference.
- `configs/experiment/rkmeans_inference_flat.yaml` requires `embedding_path` and `ckpt_path`.
- `LocalPickleWriter` writes `merged_predictions.pkl` and `merged_predictions_tensor.pt` after inference.
- The cloned GRID repo has configs only; no checkpoint, embedding, or merged prediction artifacts were found.

## Gate Interpretation

Gate 0 is not failed yet, but it is no longer an "immediate export" task. The remaining options are:

1. run a bounded ReSID FAMAE -> GAOQ export on `Musical_Instruments`;
2. obtain or generate GRID embeddings and a SID checkpoint, then run `rkmeans_inference_flat`;
3. switch to CARD fallback only if ReSID export is too slow or unstable;
4. stop by 2026-05-24 with a missing-asset list if no real mapping is produced.

## Recommendation

Try ReSID first because the processed `Musical_Instruments` dataset is already locally normalized and GAOQ writes the exact mapping table we need. Keep GRID as Cluster A if a public/pre-exported artifact appears quickly; otherwise it likely exceeds the CIKM sprint budget.
