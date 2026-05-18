# ReSID Run Preflight

**生成时间**：2026-05-18 17:37:48 CST
**状态**：local ReSID execution is not ready

## Purpose

Check whether ReSID can be launched locally for a bounded FAMAE -> GAOQ export on `Musical_Instruments`.

## Dependency Check

Current Python package availability:

| Package | Available |
|---|---:|
| `torch` | yes |
| `pandas` | yes |
| `numpy` | yes |
| `sklearn` | yes |
| `pyarrow` | yes |
| `yaml` | yes |
| `k_means_constrained` | no |

Direct import failure:

```text
ModuleNotFoundError: No module named 'k_means_constrained'
```

This blocks `model/gaoq.py` at import time because it imports `KMeansConstrained` at module scope.

## Config/Path Check

ReSID's default configs are not directly aligned with the downloaded dataset:

| Item | Current state |
|---|---|
| Downloaded dataset path | `_gate0_repos/ReSID-dataset/Musical_Instruments/leave_one_out/dataset` |
| `run_pipelines.py` expected path | `./dataset/{dataset}/last_one_out/dataset/` |
| `famae.yaml` default epochs | `500` |
| `famae.yaml` default device | `cuda:0` |
| `gaoq.yaml` requirement | `pretrained_model_path` pointing to a FAMAE checkpoint |

## Implication

ReSID remains the best first real-mapping target, but a responsible bounded export needs a setup step before launch:

1. install or vendor `k_means_constrained`;
2. create a local dataset path expected by ReSID or patch config paths to `leave_one_out`;
3. create a bounded FAMAE config with CPU/GPU device explicit, low epoch cap, and artifact-only goal;
4. run GAOQ only after a checkpoint exists;
5. normalize `item_feature/item_code_mapping.parquet` with `src/audit_sid/adapters/resid.py`.

## Gate Status

This is not a scientific no-go. It is an execution blocker. Gate 0 remains open until either:

- ReSID bounded export produces a real `item_code_mapping.parquet`;
- GRID produces or supplies a real `merged_predictions_tensor.pt`;
- CARD fallback produces a real code array and item-id array;
- or the sprint reaches 2026-05-24 without a real mapping.
