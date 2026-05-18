# Method Representativeness Audit

**生成时间**：2026-05-18 16:00:32 CST
**目标**：为 AUDIT-SID CIKM 2026 Resource Track 确定方法代表性、artifact 可导出性、诊断维度覆盖关系。
**状态**：Gate 0A framework + repo artifact-path evidence ready；actual export smoke pending.

## 结论

用户提出的流程是必要的：

> research-lit 明确 SID 方法簇 -> 选择代表性方法 -> 与评测维度提前 mapping -> 再决定是否进入 CIKM sprint。

当前文献评阅和实验计划在修订后已经支持这个流程，但还需要本文件作为 Gate 0A 的执行表。后续不允许绕过本文件直接选择“能跑的 repo”。

## 硬规则

1. 如果方法不能导出 `item-to-SID mapping`，不能作为主实验方法，只能作为 literature-motivated / future-supported method。
2. 如果方法只能支持 D1 utilization，不能支持 D2-D4 中至少两个维度，不足以支撑 CIKM submission。
3. CIKM v0 至少需要 `Cluster A + Cluster B + sanity baseline`。
4. D5a deployment-cost proxy 是 required-light；D5b generator-output cost 和 D6 drift 是加分项。
5. 若最终只能得到浅层 `RQ-VAE + ReSID` 对比，不投 CIKM 2026。
6. `DRIL` 不再作为独立候选；它是 DIGER 的内部机制名。

## Cluster x Diagnostic Mapping

Legend: `M = must`, `O = optional`, `N/A = not primary fit`.

| Cluster | Role | D1 Utilization | D2 Collision Harm | D3 Semantic-Collab Alignment | D4 Head-Tail Capacity | D5 Deployment Cost | D6 Drift Stability |
|---|---|---:|---:|---:|---:|---:|---:|
| A Canonical RQ SID | baseline reference | M | M | M | M | O | N/A |
| B Recent tokenizer/codebook innovation | rec-native, collision, capacity, ranking-aware tokenizer | M | M | M | M | O | O |
| C Continual/drift-aware tokenizer | temporal stability | O | O | O | O | O | M |
| D Industrial retrieval/search SID | retrieval deployment | O | O | M | O | M | O |

判定：

- A/B 是 CIKM v0 主体；
- C/D 更适合作为扩展或 future-support；
- 如果 v0 只覆盖 A 和 sanity baseline，直接 no-go。

## Method Candidate x Diagnostic Feasibility Matrix

Legend:

- `direct`: 可直接由 artifact 计算；
- `proxy`: 可用近似诊断；
- `gen`: requires generator output；
- `train`: requires retraining；
- `NF`: not feasible / not for v0。

| Method | Cluster | Main condition | D1 | D2 | D3 | D4 | D5 | D6 | v0 role |
|---|---|---|---|---|---|---|---|---|---|
| RQ-VAE / TIGER-style | A | must export item-to-SID + levels | direct | direct | proxy/direct | direct | gen/proxy | NF | canonical must-run |
| ReSID | B | must expose rec-native SID artifact | direct | direct | direct/proxy | direct | direct/proxy | proxy | recent must-run candidate |
| DACT | C | needs before/after SID mapping | direct | proxy | proxy | proxy | proxy | direct | optional drift method |
| CapsID | B | needs variable/soft code assignment export | direct | direct | proxy | direct | proxy | proxy | strong optional |
| DIGER | B/D | needs differentiable SID artifact and runnable code | direct/proxy | proxy | direct | proxy | direct/proxy | NF | backup only |
| AsymRec | B | needs separate input/output SID or bottleneck artifact | direct/proxy | proxy | direct/proxy | proxy | gen/proxy | NF | optional, likely audit-only |
| AdaSID | B | needs adaptive/collision-aware mapping | direct | direct | proxy | direct | proxy | proxy | future/literature unless code appears |
| CARD | B | needs NU-RQ-VAE generated codes and item join | direct | direct | proxy | direct | direct/proxy | proxy | backup Cluster B candidate |
| CQ-SID | D | likely needs retrieval/search artifact | proxy | proxy | direct/proxy | proxy | direct/gen | NF | literature target unless code/export exists |
| Random SID | sanity | self-generated mapping | direct | direct | proxy | direct | proxy | NF | required lower bound |
| Popularity-balanced SID | sanity | self-generated mapping + popularity | direct | direct | proxy | direct | proxy | NF | required sanity |
| Category-prefix SID | sanity | metadata category available | direct | direct | direct/proxy | direct | proxy | NF | required if metadata exists |

## Public Availability Screen on 2026-05-18

This is not yet Gate 0 export evidence. It is a pre-audit screen used to set the 2026-05-19 local probing order.

| Candidate | Public status | Immediate decision | Evidence to verify locally |
|---|---|---|---|
| GRID / RQ-VAE-style SID | Public GitHub; README shows semantic-ID learning and SID generation commands for RQ-KMeans/RQ-VAE/RVQ plus TIGER inference | Cluster A first probe | whether `rkmeans_inference_flat` / RQ-VAE output can be converted to `sid_assignments` |
| ReSID | Public GitHub + Hugging Face processed Amazon-2023 dataset; README shows one-command pipeline on `Musical_Instruments` | Cluster B first probe | whether GAOQ/per-item SID assignments and item feature joins are saved or can be exported |
| CARD | Public GitHub; README includes Amazon 2014 preprocessing, `nu-rq-vae/main.py`, and `generate_code.py` | Cluster B fallback after ReSID | whether generated codes are easy to export without full multimodal rebuild |
| DIGER | Public GitHub, but README says current release is illustrative/reference and full runnable code/checkpoints are planned before SIGIR 2026 | Low-priority backup; not main sprint candidate | whether any checkpoint-free smoke can export SIDs |
| CapsID | arXiv paper exists; quick search/CatalyzeX shows request-code state, no confirmed runnable repo | literature/future support only | do not spend sprint time unless code appears |
| AdaSID | arXiv paper exists; quick search did not find confirmed public repo | literature/future support only | record facet B2, no local probe yet |
| AsymRec | arXiv paper says code will be released | literature/future support only | no local probe until code is actually public |
| DACT | Public GitHub with tokenizer train/tokenize scripts | Optional D6 only | only probe after A+B path is stable |

## Gate 0A Scoring Rule

每个候选方法打 4 项，满分 10。

| Dimension | Points | Criteria |
|---|---:|---|
| Representativeness | 0-3 | 3=清楚代表 A/B/C/D 中关键方法簇或 Cluster B 的关键 facet；2=代表性合理但非 canonical；1=边缘变体；0=不清楚 |
| Artifact availability | 0-3 | 3=item-to-SID + level codes + metadata join；2=item-to-SID only；1=需重训才可能导出；0=无可用 artifact |
| Diagnostic coverage | 0-3 | 3=支持 D1-D5a 至少三项；2=支持 D1-D5a 两项；1=只支持 D1 或浅层统计；0=不可诊断 |
| Sprint cost | 0-1 | 1=1 天内 smoke/export；0=环境或训练成本不适合 CIKM sprint |

Method-level decision:

| Score | Decision |
|---:|---|
| 8-10 | main candidate |
| 6-7 | optional / backup candidate |
| 4-5 | literature coverage only |
| <=3 | exclude from v0 |

Set-level go/no-go:

| Condition | Decision |
|---|---|
| At least one Cluster A method score >= 8 | required |
| At least one Cluster B method score >= 8 | required |
| At least one sanity baseline implemented | required |
| Main pair jointly covers D1-D5a | required |
| At least one D2/D3/D4/D5a case study expected | required |
| Only D1 utilization table available | no-go |
| No recent tokenizer method with exportable SID mapping | no-go |
| All recent methods require full retraining beyond sprint budget | no-go |

## Method Coverage Table Template

This table must be filled after repo/artifact audit.

| Method | Cluster | Representative role | Artifact status | item-to-SID | Per-level code | Generator output | D1-D6 supported | Used in v0 | Reason |
|---|---|---|---|---|---|---|---|---|---|
| GRID / RQ-VAE / TIGER-style | A | canonical baseline | repo audit pass-candidate; export smoke pending | yes via `item_id` keyed `cluster_ids` | yes | optional via TIGER inference | D1-D5a direct; D5b optional | first probe | `rkmeans_inference_flat` writes merged predictions |
| ReSID | B | rec-native tokenizer | repo audit pass-candidate; export smoke pending | yes via `item_code_mapping.parquet` | yes: `codebook1_id..3_id` | not persisted by default | D1-D5a direct; D5b hook needed | first B probe | GAOQ saves first-class item-code artifact |
| DACT | C | drift-aware tokenizer | TBD | TBD | TBD | TBD | TBD | optional/future | Include only if export is cheap |
| CARD | B | non-uniform quantization / multimodal SID | repo audit pass-candidate; heavy | yes via `.npy` + `_item_ids.npy` | yes | optional | D1-D5a direct once codes exist | backup B | explicit artifact but heavier preprocessing/checkpoint path |
| DIGER | B/D | differentiable SID | reference repo; full release not yet available | TBD | TBD | TBD | D1/D3 proxy only if runnable | backup/future | Not main sprint unless surprisingly exportable |
| CapsID | B | variable/soft SID | no confirmed code in quick screen | no | no | no | future | future | Do not spend sprint time |
| AdaSID | B | adaptive collision handling | no confirmed code in quick screen | no | no | no | future | future | Method coverage only |
| AsymRec | B | asymmetric continuous/discrete SID | code promised but not public in quick screen | no | no | no | future | future | Method coverage only |
| Random SID | sanity | lower bound | self-generated | yes | yes | no | D1-D5a | sanity | Required |
| Popularity-balanced SID | sanity | lower bound | self-generated | yes | yes | no | D1-D5a | sanity | Required if popularity available |
| Category-prefix SID | sanity | lower bound | self-generated | yes | yes | no | D1-D5a | sanity | Required if metadata category available |

## Diagnostic Feasibility Matrix Template

This table must be filled after artifact audit.

| Method | D1 Utilization | D2 Collision Harm | D3 Semantic-Collab Alignment | D4 Head-Tail Capacity | D5a Deployment Cost | D5b/D6 Optional | Minimum viable? | Blocking issue |
|---|---|---|---|---|---|---|---|---|
| GRID / RQ-VAE / TIGER-style | direct after `cluster_ids` export | direct | proxy/direct with metadata/interactions | direct | direct from SID trie | D5b candidate export optional | yes | local SID export smoke pending |
| ReSID | direct after GAOQ parquet | direct | direct/proxy with processed features/interactions | direct | direct from SID trie | D5b requires T5 output hook; D6 not needed | yes | local dataset + GAOQ smoke pending |
| DACT | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| CARD | direct after `.npy` code export | direct | proxy/direct with Amazon metadata | direct | direct from code trie | optional model generation | yes as fallback | preprocessing/checkpoint path heavy |
| DIGER | TBD | TBD | TBD | TBD | TBD | TBD | likely no | release incomplete |
| CapsID | literature only | literature only | literature only | literature only | literature only | literature only | no | no confirmed code |
| AdaSID | literature only | literature only | literature only | literature only | literature only | literature only | no | no confirmed code |
| AsymRec | literature only | literature only | literature only | literature only | literature only | literature only | no | code not public yet |
| Sanity baselines | direct | direct | proxy/direct | direct | proxy | NF | yes | self-generated |

## Gate 0A Audit Procedure

1. Read `docs/SID_METHOD_CLUSTER_AUDIT.md`.
2. For each candidate repo/paper, assign cluster A-D and, for Cluster B, assign facet B1/B2/B3.
3. Verify artifact export:
   - item-to-SID mapping;
   - per-level code assignment;
   - metadata join key;
   - optional generator output.
4. Fill Method Coverage Table.
5. Fill Diagnostic Feasibility Matrix.
6. Score each candidate using Gate 0A scoring.
7. Select CIKM v0 method set only if set-level go/no-go passes.
8. If no set passes, stop CIKM 2026 submission.

## Current Status

This audit framework is ready. Concrete method scores are pending:

- canonical Cluster A repo audit;
- recent tokenizer Cluster B repo audit;
- local dataset schema audit on external drive;
- sanity baseline generation check.

No training should start before this table is filled.
