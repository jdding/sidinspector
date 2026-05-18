# GRID Adapter Smoke

**生成时间**：2026-05-18 17:34:21 CST
**状态**：GRID SID mapping adapter format smoke passed on synthetic tensor

## Purpose

GRID's `rkmeans_inference_flat` path writes item-keyed semantic IDs through `LocalPickleWriter`. The merged tensor can be stored as `merged_predictions_tensor.pt`, and GRID's post-processing may transpose the tensor so rows are SID levels and columns are item ids.

This smoke verifies that `src/audit_sid/adapters/grid.py` can normalize that tensor shape into the AUDIT-SID `sid_assignments` contract.

## Commands

```bash
python3 -c "from pathlib import Path; import torch; p=Path('_gate0_artifacts/grid_synthetic'); p.mkdir(parents=True, exist_ok=True); torch.save(torch.tensor([[1,1,2,2],[7,8,7,9],[0,0,1,0]]), p/'merged_predictions_tensor.pt')"

PYTHONPATH=src PYTHONPYCACHEPREFIX=/private/tmp/audit_sid_pycache \
python3 -m audit_sid.adapters.grid \
  --artifact-path _gate0_artifacts/grid_synthetic/merged_predictions_tensor.pt \
  --output-dir _gate0_artifacts/grid_synthetic/normalized \
  --dataset-name synthetic \
  --method grid_synthetic \
  --layout auto \
  --unsafe-assume-dense-zero-indexed
```

## Output Contract

The adapter emitted:

| Artifact | Rows | Columns |
|---|---:|---|
| `_gate0_artifacts/grid_synthetic/normalized/sid_assignments.parquet` | 4 | `item_id`, `method`, `dataset`, `sid_level_0..2`, `sid` |

Sample normalized rows:

| item_id | method | dataset | sid_level_0 | sid_level_1 | sid_level_2 | sid |
|---:|---|---|---:|---:|---:|---|
| 0 | `grid_synthetic` | `synthetic` | 1 | 7 | 0 | `1-7-0` |
| 1 | `grid_synthetic` | `synthetic` | 1 | 8 | 0 | `1-8-0` |
| 2 | `grid_synthetic` | `synthetic` | 2 | 7 | 1 | `2-7-1` |
| 3 | `grid_synthetic` | `synthetic` | 2 | 9 | 0 | `2-9-0` |

## Interpretation Boundary

This validates the adapter path for GRID output format only. It does not prove GRID can produce a real SID mapping locally, because the cloned repo does not include pretrained embeddings, trained RKMeans/RQ-VAE checkpoints, or a pre-exported `merged_predictions_tensor.pt`.

Update: after code review, the GRID adapter requires a real `--item-ids` file by default. The synthetic smoke uses `--unsafe-assume-dense-zero-indexed` explicitly because the synthetic tensor has dense toy item ids.

The remaining GRID blocker is upstream artifact generation: either download/prepare the expected Amazon data and embeddings plus train SID centroids, or obtain a public pre-exported SID mapping.
