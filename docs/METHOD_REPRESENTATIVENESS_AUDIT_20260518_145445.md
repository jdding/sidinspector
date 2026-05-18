# Method Representativeness Audit

**生成时间**：2026-05-18 14:54:45 CST  
**目标**：为 AUDIT-SID CIKM 2026 Resource Track 确定方法代表性、artifact 可导出性、诊断维度覆盖关系。  
**状态**：Gate 0A framework ready；具体 repo artifact evidence 待 Gate 0 repo audit 填充。

## 结论

用户提出的流程是必要的：

> research-lit 明确 SID 方法簇 -> 选择代表性方法 -> 与评测维度提前 mapping -> 再决定是否进入 CIKM sprint。

当前文献评阅和实验计划在修订后已经支持这个流程，但还需要本文件作为 Gate 0A 的执行表。后续不允许绕过本文件直接选择“能跑的 repo”。

## 硬规则

1. 如果方法不能导出 `item-to-SID mapping`，不能作为主实验方法，只能作为 literature-motivated / future-supported method。
2. 如果方法只能支持 D1 utilization，不能支持 D2-D4 中至少两个维度，不足以支撑 CIKM submission。
3. CIKM v0 至少需要 `Cluster A + Cluster B/C + sanity baseline`。
4. D5/D6 是加分项，不应绑架 4-page sprint。
5. 若最终只能得到浅层 `RQ-VAE + ReSID` 对比，不投 CIKM 2026。

## Cluster x Diagnostic Mapping

Legend: `M = must`, `O = optional`, `N/A = not primary fit`.

| Cluster | Role | D1 Utilization | D2 Collision Harm | D3 Semantic-Collab Alignment | D4 Head-Tail Capacity | D5 Deployment Cost | D6 Drift Stability |
|---|---|---:|---:|---:|---:|---:|---:|
| A Canonical RQ SID | baseline reference | M | M | M | M | O | N/A |
| B Rec-native tokenizer | recent innovation | M | M | M | M | O | O |
| C Collision/utilization/codebook design | capacity/control methods | M | M | O | M | O | O |
| D Continual/drift-aware tokenizer | temporal stability | O | O | O | O | O | M |
| E Industrial retrieval/search SID | retrieval deployment | O | O | M | O | M | O |

判定：

- A/B/C 是 CIKM v0 主体；
- D/E 更适合作为扩展或 future-support；
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
| ReSID | B | must expose rec-native SID artifact | direct | direct | direct/proxy | direct | gen/proxy | proxy | recent must-run candidate |
| DACT | D | needs before/after SID mapping | direct | proxy | proxy | proxy | proxy | direct | optional drift method |
| CapsID | C | needs variable/soft code assignment export | direct | direct | proxy | direct | proxy | proxy | strong optional |
| DIG | B/E | needs ranking-aligned tokenizer artifact | direct/proxy | proxy | direct | proxy | gen/proxy | NF | optional if artifact exists |
| AsymRec | B | needs separate input/output SID or bottleneck artifact | direct/proxy | proxy | direct/proxy | proxy | gen/proxy | NF | optional, likely audit-only |
| AdaSID / CARD | C | needs adaptive/collision-aware mapping | direct | direct | proxy | direct | proxy | proxy | optional replacement for ReSID/CapsID |
| CQ-SID | E | likely needs retrieval/search artifact | proxy | proxy | direct/proxy | proxy | direct/gen | NF | literature target unless code/export exists |
| Random SID | sanity | self-generated mapping | direct | direct | proxy | direct | proxy | NF | required lower bound |
| Popularity-balanced SID | sanity | self-generated mapping + popularity | direct | direct | proxy | direct | proxy | NF | required sanity |
| Category-prefix SID | sanity | metadata category available | direct | direct | direct/proxy | direct | proxy | NF | required if metadata exists |

## Gate 0A Scoring Rule

每个候选方法打 4 项，满分 10。

| Dimension | Points | Criteria |
|---|---:|---|
| Representativeness | 0-3 | 3=清楚代表 A/B/C/D/E 中关键方法簇；2=代表性合理但非 canonical；1=边缘变体；0=不清楚 |
| Artifact availability | 0-3 | 3=item-to-SID + level codes + metadata join；2=item-to-SID only；1=需重训才可能导出；0=无可用 artifact |
| Diagnostic coverage | 0-3 | 3=支持 D1-D4 至少三项；2=支持 D1-D4 两项；1=只支持 D1 或浅层统计；0=不可诊断 |
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
| At least one Cluster B or C method score >= 8 | required |
| At least one sanity baseline implemented | required |
| Main pair jointly covers D1-D4 | required |
| At least one non-trivial D2/D3/D4 finding expected | required |
| Only D1 utilization table available | no-go |
| No recent tokenizer method with exportable SID mapping | no-go |
| All recent methods require full retraining beyond sprint budget | no-go |

## Method Coverage Table Template

This table must be filled after repo/artifact audit.

| Method | Cluster | Representative role | Artifact status | item-to-SID | Per-level code | Generator output | D1-D6 supported | Used in v0 | Reason |
|---|---|---|---|---|---|---|---|---|---|
| RQ-VAE / TIGER-style | A | canonical baseline | TBD | TBD | TBD | TBD | TBD | TBD | Needs repo audit |
| ReSID | B | rec-native tokenizer | TBD | TBD | TBD | TBD | TBD | TBD | Needs repo audit |
| DACT | D | drift-aware tokenizer | TBD | TBD | TBD | TBD | TBD | optional/future | Include only if export is cheap |
| CapsID | C | variable/soft SID | TBD | TBD | TBD | TBD | TBD | optional/future | Strong if artifact available |
| DIG | B/E | ranking-aligned tokenizer | TBD | TBD | TBD | TBD | TBD | optional/future | Likely literature target unless code exists |
| AdaSID / CARD | C | collision/utilization design | TBD | TBD | TBD | TBD | TBD | optional/future | Strong if code available |
| Random SID | sanity | lower bound | self-generated | yes | yes | no | D1-D4 | sanity | Required |
| Popularity-balanced SID | sanity | lower bound | self-generated | yes | yes | no | D1-D4 | sanity | Required if popularity available |
| Category-prefix SID | sanity | lower bound | self-generated | yes | yes | no | D1-D4 | sanity | Required if metadata category available |

## Diagnostic Feasibility Matrix Template

This table must be filled after artifact audit.

| Method | D1 Utilization | D2 Collision Harm | D3 Semantic-Collab Alignment | D4 Head-Tail Capacity | D5 Deployment Cost | D6 Drift Stability | Minimum viable? | Blocking issue |
|---|---|---|---|---|---|---|---|---|
| RQ-VAE / TIGER-style | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| ReSID | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| DACT | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| CapsID | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| DIG | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| AdaSID / CARD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Sanity baselines | direct | direct | proxy/direct | direct | proxy | NF | yes | self-generated |

## Gate 0A Audit Procedure

1. Read `docs/SID_METHOD_CLUSTER_AUDIT.md`.
2. For each candidate repo/paper, assign cluster A-E.
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
- recent tokenizer Cluster B/C repo audit;
- local dataset schema audit on external drive;
- sanity baseline generation check.

No training should start before this table is filled.
