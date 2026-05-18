# Gate 0 Repo / Artifact Audit: AUDIT-SID

**生成时间**：2026-05-18 16:25:09 CST
**状态**：repo artifact-path audit complete；actual SID export smoke still pending
**范围**：只读审计公开 repo，不安装依赖、不启动训练、不下载完整数据集。

## Executive Decision

Gate 0 repo audit 支持继续进入 **bounded export smoke**，但还不能宣称 Gate 0 全通过。

当前可行路径：

1. **Cluster A**：`GRID / RQ-VAE-style SID` 作为 canonical baseline。
2. **Cluster B**：`ReSID / GAOQ` 作为 recent tokenizer/codebook innovation。
3. **Fallback B**：`CARD` 只在 ReSID export smoke 卡住时启用。

硬边界：

- 不审计更多 2026 tokenizer，除非 ReSID 和 CARD 都失败；
- 不启动完整 TIGER/T5 downstream training；
- 第一阶段只要导出 `item_id -> SID` 和 per-level code assignments；
- D5b generator-output diagnostics 后置。

## Cloned Revisions

| Repo | Local path | Commit | Role |
|---|---|---:|---|
| `snap-research/GRID` | `_gate0_repos/GRID` | `2fe3475` | Cluster A canonical RQ/RQ-VAE-style SID |
| `FuCongResearchSquad/ReSID` | `_gate0_repos/ReSID` | `45c1c6a` | Cluster B recsys-native tokenizer |
| `HAI-UESTC/CARD` | `_gate0_repos/CARD` | `b8ce097` | Cluster B fallback |

`_gate0_repos/` is ignored by `.gitignore` and must not be committed.

## Method Audit

### GRID / RQ-VAE-style SID

**Decision**：Cluster A main candidate.

Evidence:

- README exposes the expected pipeline: embedding generation -> semantic ID learning -> SID generation -> TIGER training/inference.
- `configs/experiment/rkmeans_inference_flat.yaml` configures `LocalPickleWriter` with `prediction_key_name=item_id` and `prediction_name=cluster_ids`.
- `src/modules/clustering/residual_quantization.py` `predict_step` returns `OneKeyPerPredictionOutput(keys=item_ids, predictions=cluster_ids, key_name="item_id", prediction_name="cluster_ids")`.
- `src/utils/inference_utils.py` merges prediction rows into `merged_predictions.pkl` and tensor form `merged_predictions_tensor.pt`.
- TIGER inference can generate user-keyed SID candidates via `SemanticIDEncoderDecoder.predict_step`, but this is D5b optional.

Artifact mapping:

| AUDIT-SID table | GRID source | Status |
|---|---|---|
| `sid_assignments` | `rkmeans_inference_flat` output: `item_id`, `cluster_ids` | feasible after SID inference |
| `item_metadata` | P5/Amazon item text files or ReSID metadata if adapter is written | needs dataset join |
| `interactions` | GRID expected `train/validation/test` sequence folders | feasible |
| `generator_outputs` | `tiger_inference_flat` output keyed by `user_id` | optional, requires trained TIGER |

Gate 0A score:

| Dimension | Score | Reason |
|---|---:|---|
| Representativeness | 3/3 | canonical RQ/RQ-VAE/RVQ-style SID baseline |
| Artifact availability | 3/3 | item-id keyed cluster IDs are explicitly written |
| Diagnostic coverage | 3/3 | D1-D5a direct from SID mapping plus interactions |
| Sprint cost | 0.5/1 | repo path is clear, but embeddings/checkpoint/data alignment still need smoke |
| **Total** | **9.5/10** | main Cluster A candidate |

### ReSID / GAOQ

**Decision**：Cluster B first candidate.

Evidence:

- README recommends processed Hugging Face dataset and one-command run on `Musical_Instruments`.
- `run_pipelines.py` runs FAMAE -> GAOQ -> T5 and passes GAOQ output as `feature_mapping` into T5.
- `model/gaoq.py` builds a dataframe with `item_id`, `codebook1_id`, `codebook2_id`, `codebook3_id`.
- `model/gaoq.py` writes `item_feature/item_code_mapping.parquet` and `item_feature_explain.json` under `args.log_dir`.
- `utils.py` reads the GAOQ `feature_mapping` parquet as item features for T5; this confirms the mapping is a first-class artifact, not only an internal tensor.
- T5 evaluation computes beam outputs in memory for metrics, but does not obviously persist per-user generated candidates; D5b would need an export hook.

Artifact mapping:

| AUDIT-SID table | ReSID source | Status |
|---|---|---|
| `sid_assignments` | `logs/.../item_feature/item_code_mapping.parquet` with `item_id`, `codebook1_id`, `codebook2_id`, `codebook3_id` | feasible after GAOQ |
| `item_metadata` | processed dataset `item_feature` and `item_feature_explain.json` | feasible if dataset downloaded |
| `interactions` | processed `train`, `valid`, `test` parquet under `last_one_out/dataset` | feasible |
| `generator_outputs` | T5 evaluation `outputs` tensor in `trainer.evaluate`; not saved | optional, requires hook |

Gate 0A score:

| Dimension | Score | Reason |
|---|---:|---|
| Representativeness | 3/3 | recsys-native encoding + GAOQ directly targets tokenizer/codebook design |
| Artifact availability | 3/3 | per-item codebook parquet is explicitly saved |
| Diagnostic coverage | 3/3 | D1-D5a direct; D3/D4 supported by processed features/interactions |
| Sprint cost | 0.5/1 | clear artifact path, but FAMAE/GAOQ smoke still requires environment/data |
| **Total** | **9.5/10** | main Cluster B candidate |

### CARD

**Decision**：Cluster B fallback only.

Evidence:

- README exposes preprocessing -> collaborative data -> visual semantic units -> NU-RQ-VAE -> `generate_code.py` -> model training.
- `nu-rq-vae/generate_code.py` loads a trained NU-RQ-VAE checkpoint, calls `model.get_indices`, saves generated codes to `--out_path`, and saves parallel item IDs to `<out_path>_item_ids.npy`.
- `model/dataset.py` consumes those `.npy` codes and `_item_ids.npy` to build `item_to_code` / `code_to_item`.
- Artifact export is explicit, but the front half requires Amazon 2014 raw data, image/title processing, embeddings, and NU-RQ-VAE checkpoint.

Artifact mapping:

| AUDIT-SID table | CARD source | Status |
|---|---|---|
| `sid_assignments` | `generate_code.py --out_path *.npy` plus `*_item_ids.npy` | feasible after checkpoint |
| `item_metadata` | Amazon 2014 metadata processed by `process_data.py` | feasible but heavier |
| `interactions` | generated train/valid/test parquet or RecBole `.inter` files | feasible |
| `generator_outputs` | `model/main.py` generation path | optional, not needed |

Gate 0A score:

| Dimension | Score | Reason |
|---|---:|---|
| Representativeness | 2.5/3 | non-uniform quantization / multimodal collaborative SID is relevant |
| Artifact availability | 3/3 | codes and item IDs are explicitly saved |
| Diagnostic coverage | 3/3 | D1-D5a direct once codes exist |
| Sprint cost | 0/1 | preprocessing and multimodal dependencies are too heavy for first-line sprint |
| **Total** | **8.5/10** | valid fallback, not first probe |

## Dataset Audit Implications

The ReSID Hugging Face dataset remains the primary dataset target:

- official dataset page lists tabular/text parquet format;
- size is about 924 MB;
- includes `Musical_Instruments` and nine other Amazon-2023 categories;
- license is MIT;
- modality/tags match recommender-system sequential recommendation and side-information.

Do not download the full 924 MB dataset until the immediate export-smoke script is ready. First local dataset task should be a file-list / schema probe or a targeted `Musical_Instruments` download if supported.

## Gate 0 / 0A Status

| Requirement | Status | Notes |
|---|---|---|
| At least one Cluster A export path | PASS-CANDIDATE | GRID explicitly writes item-keyed cluster IDs |
| At least one Cluster B export path | PASS-CANDIDATE | ReSID explicitly writes `item_code_mapping.parquet` |
| Sanity baseline | READY | self-generated after dataset schema |
| D1-D5a from mapping only | PASS-CANDIDATE | all three repos expose per-item code arrays |
| D5b generator output | DEFER | GRID/ReSID can generate, but export hooks/checkpoints are not v0-critical |
| Dataset join | PENDING | requires ReSID dataset schema probe |
| Actual SID export smoke | PENDING | no training/inference run yet |

## Go / No-Go

**Decision now**：continue to bounded export smoke.

This is not a full Gate 0 pass because no SID mapping has been generated locally yet. It is enough to justify the next step:

1. write adapters for GRID/ReSID mapping artifacts into `src/audit_sid/interface.py` schema;
2. perform ReSID dataset schema probe for `Musical_Instruments`;
3. attempt a minimal GAOQ/ReSID export or identify whether pretrained artifacts are absent;
4. only if ReSID blocks, switch to CARD fallback.

## Immediate Next Step

Create:

- `docs/DATASET_SCHEMA_AUDIT.md`;
- `src/audit_sid/adapters/resid.py`;
- `src/audit_sid/adapters/grid.py`;

Then run a bounded smoke that either exports one real `sid_assignments` table or produces a concrete missing-asset list by 2026-05-20.
