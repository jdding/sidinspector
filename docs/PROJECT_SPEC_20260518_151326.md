# AUDIT-SID Project Spec

**生成时间**：2026-05-18 15:13:26 CST  
**项目状态**：public-first Gate 0 / Gate 0A 阶段  
**目标 venue**：CIKM 2026 Resource Track  
**提交窗口**：Abstract 2026-05-30 AoE；Paper 2026-06-06 AoE  
**边界**：不得使用 Huawei 内部数据、业务日志或 proprietary implementation details。

## 1. Project Thesis

AUDIT-SID 不是一个新的 SID tokenizer，也不是一个普通 leaderboard。它的核心 thesis 是：

> Semantic-ID tokenizer/codebook 不能只用 final Recall@K / NDCG 评估；一个可复用的 artifact-level diagnostic suite 能揭示 utilization collapse、harmful collision、semantic-collaborative mismatch 和 head-tail capacity allocation 等隐藏 failure mode。

CIKM 版本的目标是提交一个小而可信的 resource paper：

- open diagnostic toolkit；
- public Amazon case study；
- method coverage table；
- 至少一个非平凡诊断发现。

## 2. Non-Goals

当前 CIKM v0 不做：

- 新 tokenizer / 新生成式推荐方法；
- 全量 SID benchmark；
- 2026 SID 论文 survey；
- 工业部署结论；
- Huawei 内部上线或业务数据分析；
- 长周期 drift / online / A-B 实验。

如果 Gate 0A 只能形成浅层 `RQ-VAE + ReSID + utilization table`，应停止 CIKM 2026，而不是硬投。

## 3. Required Method Coverage

方法选择不按“哪个 repo 好跑”决定，而按代表性 coverage 决定。

| Cluster | Role | CIKM v0 要求 |
|---|---|---|
| A Canonical SID baseline | TIGER / RQ-VAE / GenRec / GRID-style residual quantization SID | 必须至少一个 |
| B Recent tokenizer/codebook innovation | ReSID / CapsID / DIG / AdaSID / CARD / AsymRec / DRIL 等 | 必须至少一个 artifact 可导出的方法 |
| Sanity lower bound | random / popularity-balanced / category-prefix ID | 必须至少一个 |
| C Drift-aware tokenizer | DACT / SID staleness variants | optional |
| D Industrial retrieval/search SID | CQ-SID-inspired retrieval/search artifact | optional / literature target |

Cluster B 内部只保留 facet，不再拆成独立 must-run cluster：

- B1 rec-native / predictability-aware；
- B2 collision / capacity / adaptive codebook；
- B3 ranking / retrieval-aligned。

Gate 0A 的硬条件：

> Cluster A + Cluster B + sanity lower bound.

如果没有可解释的 Cluster B artifact，CIKM v0 no-go。

## 4. Required Artifact Interface

主实验方法必须尽量导出：

- `item_id -> SID` mapping；
- per-level code assignments；
- item metadata join key；
- item popularity / head-mid-tail bucket；
- user-item interaction histories；
- optional generator outputs / candidates / beam traces。

不能导出 `item-to-SID mapping` 的方法只能作为 literature-motivated future support，不能作为主实验方法。

## 5. Required Diagnostics

CIKM v0 必须实现 D1-D4。

| ID | Diagnostic | Core question | Required |
|---|---|---|---|
| D1 | Codebook utilization | code space 是否塌缩或严重不均衡？ | yes |
| D2 | Collision harm | collision 是否造成 recommendation-relevant harm？ | yes |
| D3 | Semantic-collaborative alignment | SID/code neighborhood 是否匹配 collaborative neighborhood？ | yes |
| D4 | Head-tail capacity allocation | tail item 是否被过度压缩或 collision？ | yes |
| D5 | Deployment-cost proxy | SID trie / beam / candidate cost 是否可诊断？ | optional |
| D6 | Drift stability | tokenizer refresh 是否造成 SID churn？ | optional |

至少一个 D2/D3/D4 结果必须形成 case study，不能只给 D1 utilization summary。

## 6. Dataset Scope

Primary：

- ReSID processed Amazon-2023 `Musical_Instruments` 或同等小型 Amazon-2023 category。

Backup：

- Amazon 2014 Beauty / Sports。

暂不纳入 CIKM v0：

- MIND；
- H&M；
- KuaiRec / KuaiRand；
- internal Huawei data。

## 7. Gates

| Gate | Question | Pass condition | Stop condition |
|---|---|---|---|
| Gate 0 | public code/artifact 是否能导出 SID mappings？ | 至少 A+B 两类方法可导出可 join 的 SID artifact | 只能跑一个方法或只能跑 sanity |
| Gate 0A | 方法代表性是否足够？ | A + B + sanity；B 方法支持 D1-D4 至少两个以上诊断 | 只是两个 repo 跑通，或 B artifact 不可解释 |
| Gate 1 | dataset schema 是否支持诊断？ | metadata、interaction、popularity、SID mapping 可 join | primary/backup 都无法支撑 D1-D4 |
| Gate 2 | metrics 是否稳定可解释？ | D1-D4 输出稳定表格和 failure cases | 只有浅层统计，无 case study |
| Gate 3 | empirical finding 是否非平凡？ | 诊断揭示 final metrics 隐藏的机制差异 | diagnostics 只是 final metric 复述 |
| Gate 4 | paper viability | 有 toolkit + case study + coverage table | 贡献不足以支撑 CIKM Resource |

## 8. Timeline

| Date | Milestone | Output |
|---|---|---|
| 2026-05-19 | repo/artifact audit | `docs/GATE0_REPO_AUDIT.md` |
| 2026-05-20 | dataset schema audit | `docs/DATASET_SCHEMA_AUDIT.md` |
| 2026-05-21 | first SID mapping export | sample artifact |
| 2026-05-22 | second SID mapping export | sample artifact |
| 2026-05-23 | D1-D4 metrics v0 | diagnostic tables |
| 2026-05-24 | formal Gate 0 decision | `docs/GATE0_DECISION.md` |
| 2026-05-30 | CIKM abstract | submission abstract |
| 2026-06-06 | CIKM paper | 4-page resource paper + artifact |

## 9. Current Next Step

不要先训练。下一步是填充 Gate 0A evidence：

1. audit RQ-VAE / TIGER-style implementation；
2. audit ReSID first；
3. if ReSID artifact is weak, audit CapsID / DIG / AdaSID / CARD / AsymRec alternatives；
4. fill `docs/METHOD_REPRESENTATIVENESS_AUDIT.md` with real artifact scores；
5. only after Gate 0 / 0A pass, implement D1-D4 metrics.

