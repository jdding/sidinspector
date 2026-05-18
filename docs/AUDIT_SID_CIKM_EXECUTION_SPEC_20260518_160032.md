# AUDIT-SID CIKM 2026 Resource Execution Spec

**生成时间**：2026-05-18 16:00:32 CST
**目标 venue**：CIKM 2026 Resource Track
**Abstract deadline**：2026-05-30 AoE
**Paper deadline**：2026-06-06 AoE
**Paper budget**：4 pages including appendices and acknowledgments, plus references / GenAI Usage Disclosure.

## 执行结论

CIKM 2026 版本必须收敛为：

> 一个开源 AUDIT-SID diagnostic toolkit + 一个小但可信的 case study。

不能做成：

- 全量 SID benchmark；
- 新 tokenizer 方法；
- 覆盖所有 2026 新论文的 survey；
- 工业部署结论。

**2026-05-18 16:00 重要修正**：吸收外部评审后，CIKM 版本明确改成 **resource-first sprint**。强 empirical finding 是 stretch goal；硬目标是 open toolkit + interface contract + method coverage table + 小 case study。RQ-VAE/TIGER-style SID + ReSID 不能自动视为“足够代表社区”，必须先过 **Method Representativeness Gate**。

如果最终只是：

> 两个容易跑的 tokenizer + 浅层 utilization/collision 表格，

则不应投 CIKM Resource Track。这个版本对社区贡献不足，会浪费时间。

## CIKM Resource Paper 的最小贡献

4-page 版本只保留三个贡献：

1. **Diagnostic taxonomy**：定义 semantic-ID tokenizer/codebook 的 D1-D5a 核心诊断。
2. **Open toolkit**：提供可复现脚本和稳定输入接口，输入 `item-to-SID mapping`、item metadata、interaction histories，输出 diagnostic tables。
3. **Method coverage table**：说明哪些近期 SID/tokenizer artifact 可以接入，哪些只能 future support。
4. **Case study**：在一个公开数据集上比较至少两个 tokenizer family，展示一个非冗余诊断案例；若出现强 finding，再加码。

## 数据集决策

### Primary Dataset: ReSID processed Amazon-2023 subset

**选择**：优先使用 ReSID 官方 Hugging Face dataset 中的 `Musical_Instruments` 或同等小型 Amazon-2023 category。

**理由**：

- ReSID 官方 README 明确提供 processed dataset；
- ReSID 官方示例使用 `Musical_Instruments`；
- Amazon-2023 有 metadata / category / sequential histories，适合 utilization、collision、semantic-collaborative alignment、head-tail diagnostics；
- 处理成本低，适合 19 天 sprint。

**需要确认**：

- dataset 是否可直接下载；
- item metadata 是否完整；
- interaction split 是否可复用；
- item id 与 tokenizer 输出是否可 join。

### Secondary Dataset: Amazon 2014 Beauty or Sports

**选择**：仅作为 backup / optional robustness。

**理由**：

- GenRec 支持 Amazon 2014 Beauty / Sports / Toys；
- 传统 generative recommendation 论文常用这些 splits；
- 如果 ReSID dataset 与 GenRec pipeline 不易对齐，可用 Amazon 2014 Beauty 做 RQ-VAE/TIGER sanity case。

**边界**：

- CIKM 4-page 版本不强求两个数据集；
- 如果 Gate 0 时间紧，优先一个 dataset 做深诊断。

### Portability Smoke: MovieLens-1M

**选择**：只作为 half-day toolkit portability smoke，不作为主实验数据集。

**理由**：

- 外部评审指出单一 Amazon 数据会被 resource reviewer 攻击；
- MovieLens-1M schema 简单，可用 title/genre 和 interactions 检查 toolkit interface 是否非 Amazon 特化；
- 不新增 tokenizer，只验证 `sid_assignments` / metadata / interactions schema 和 sanity SID baseline 是否可运行。

**放弃条件**：

- Gate 0 在 2026-05-24 前未通过；
- 需要训练新 tokenizer；
- 会挤压主 case study。

### 不纳入 CIKM v0 的数据集

- MIND：文本丰富，但从 recommender SID tokenizer 切入会增加任务适配成本。
- H&M：catalog churn 很有价值，但 drift/cold/catalog logic 会扩大 scope。
- KuaiRec/KuaiRand：exposure-aware 有价值，但 item semantic metadata 和 SID pipeline 适配成本不适合 CIKM sprint。

## 对比方法决策

### Method Representativeness Gate

CIKM v0 的方法选择必须覆盖至少两个不同代表性层级：

| Layer | 代表什么 | 候选方法 | CIKM v0 要求 |
|---|---|---|---|
| Canonical baseline | generative recommendation 中经典 residual quantization / semantic ID 路线 | TIGER / RQ-VAE / GenRec-style SID / GRID-style SID | 必须至少一个 |
| Recent tokenizer/codebook innovation | 2026 年围绕 tokenizer/codebook 的新设计，包括 rec-native、collision/capacity、ranking-aligned facet | ReSID, CARD, DIGER, CapsID, AsymRec, AdaSID | 必须至少一个可导出 artifact 且支撑至少两个核心诊断 |
| Drift/retrieval extension | temporal drift 或 industrial retrieval/search-oriented SID | DACT, CQ-SID-inspired artifact | optional；不作为 CIKM v0 go/no-go |
| Diagnostic sanity lower bound | 验证 metrics 是否有基本区分度 | Random SID, popularity-balanced SID, category-prefix SID | 必须至少一个 |

Gate 通过条件：

1. 能解释为什么 chosen methods 分别代表 canonical baseline 与 recent tokenizer innovation；
2. chosen recent method 的技术点必须和 AUDIT-SID diagnostics 有直接关系，如 recsys-native quantization、drift stability、soft routing、ranking alignment、collision adaptation；
3. 至少一个诊断结果必须揭示方法间非冗余、可解释的 artifact-level 差异，而不是“ReSID 比 RQ-VAE 分数高”；
4. paper 中必须有一张 **Method Coverage Table**，说明当前 toolkit 支持的 artifact interface 能覆盖更多近期方法，即使 CIKM v0 未全部复现。

更精确地说，CIKM v0 的 must-run 是：

> Cluster A canonical SID + Cluster B recent tokenizer/codebook innovation + sanity lower bound.

不是固定的 `RQ-VAE + ReSID`。如果 ReSID 不足以代表 recent innovation 或 artifact 不可解释，应优先审计 CARD，再把 DIGER 作为低优先级 backup；CapsID / AdaSID / AsymRec 暂按 literature/future support 处理，除非今天发现可运行代码。DACT/CQ-SID 类扩展只作为 optional。若没有任何 Cluster B 候选可用，应停止 CIKM 2026。

Gate 失败条件：

- 只能跑 RQ-VAE + sanity baseline；
- ReSID 跑通但无法导出可解释 tokenizer artifact；
- 两个方法都属于同一类 quantization family，无法覆盖近期 tokenizer innovation；
- 诊断结果只是浅层 utilization table，没有 collision harm / head-tail / alignment 发现。

### Preferred Must-run Method 1: RQ-VAE / TIGER-style SID

**实现入口**：GenRec 或同类 RQ-VAE/TIGER implementation。

**角色**：classical semantic-ID baseline。

**需要导出**：

- item-to-SID mapping；
- per-level code assignments；
- optional: generated candidate lists / TIGER outputs；
- optional: Recall@K / NDCG@K。

**为什么必须有**：

- 它是 SID generative recommendation 的基础对照；
- utilization / collision / prefix imbalance 在 RQ-VAE 上最容易解释；
- 即使 ReSID/DACT 出问题，RQ-VAE baseline 也能支撑 toolkit demo。

### Preferred Must-run Method 2: ReSID

**实现入口**：`FuCongResearchSquad/ReSID` 官方实现。

**角色**：recommendation-native tokenizer。

**需要导出**：

- item-to-SID mapping；
- codebook assignments；
- tokenizer output artifact；
- optional: downstream evaluation outputs。

**为什么必须有**：

- ReSID 是近期最直接针对 tokenizer/codebook 的 recommendation-native 方法之一；
- 它有官方代码和 processed dataset；
- 它可以与 RQ-VAE/TIGER-style baseline 形成清晰 contrast：generic quantization vs recommendation-native quantization。

**代表性风险**：

- 如果 ReSID 的 artifact 只能展示它自己方法的 pipeline，而不能映射到通用 SID diagnostics，则代表性不足；
- 如果无法导出 per-item SID / codebook assignments，它不能作为 CIKM v0 的主要 recent tokenizer method。

### Alternative Recent Tokenizer Candidates

如果 ReSID 不够稳，按下面顺序替换或补充：

1. **CARD**：代表 non-uniform quantization / multimodal-collaborative fusion；有公开 GitHub 和 `generate_code.py`，但 multimodal pipeline 成本需实测。
2. **DIGER**：代表 differentiable SID / recommendation-loss-aligned tokenizer；当前 repo 自称 reference implementation，缺完整 end-to-end release，因此只做 backup。
3. **CapsID**：代表 soft-routed variable-length SID；arXiv 已出但当前未发现代码，不作为 CIKM v0 主实验。
4. **AdaSID / AsymRec**：代表 collision-adaptive 或 asymmetric tokenizer design；当前 public code 不明确，放入 Method Coverage Table / future support。
5. **DACT**：代表 drift-aware continual tokenization；适合 D6 drift stability，但属于 optional extension，不应替代 Cluster B 的 recent tokenizer/codebook innovation。

CIKM v0 不需要覆盖这些全部方法，但必须在文档和 paper 中解释：

> AUDIT-SID 的资源价值在于提供 artifact-level diagnostics，使后续方法可以被快速接入，而不是在 v0 复现所有新 tokenizer。

### Sanity Baseline: Frequency / Random / Category ID

**角色**：diagnostic lower bound and sanity check。

建议实现：

- Random SID：随机分配同长度 code；
- Popularity-balanced SID：按 popularity bucket 分配 prefix；
- Category-prefix SID：metadata category 作为 high-level prefix，如果 category 可用。

**为什么需要**：

- CIKM resource paper 不能完全依赖复杂开源 repo；
- 这些 baseline 能验证 AUDIT-SID metrics 是否有基本区分度；
- 如果两个复杂方法结果不稳定，sanity baseline 仍能展示 toolkit utility。

### Optional Method: DACT

**角色**：drift/stability extension。

**实现入口**：`HomesAmaranta/DACT`。

**纳入条件**：

- 2026-05-24 前能导出 DACT updated SID mapping；
- 不需要完整训练 LC-Rec/TIGER downstream；
- 能提供 churn / stability table。

**不纳入条件**：

- 环境配置超过 1 天；
- 只能跑 full pipeline，不能直接导出 tokenizer artifact；
- 影响 CIKM 4-page 主线。

## 评测维度决策

CIKM v0 只保留四个 must-have diagnostics，加两个 optional diagnostics。

评测内容不是“最终推荐指标谁高”，而是回答四个 resource paper 问题：

1. tokenizer 是否有效利用了 code space；
2. collision 是否造成 recommendation harm；
3. semantic/code neighborhood 是否和 collaborative neighborhood 对齐；
4. head/tail item 是否获得合理表达容量。

### D1. Codebook Utilization

**输入**：item-to-SID mapping。

**指标**：

- per-level unique code count；
- dead-code rate；
- usage entropy；
- prefix fan-out；
- branch imbalance / Gini。

**作用**：判断 tokenizer 是否塌缩、是否表达容量分配不均。

### D2. Collision Harm

**输入**：item-to-SID mapping + user-item interactions。

**指标**：

- same-code / same-prefix item pair 的 co-occurrence similarity；
- collision pairs 的 behavioral dissimilarity；
- tail collision rate；
- harmful collision examples。

**核心贡献点**：

> collision 不应只看是否共享 code，而要看共享 code 的 item 是否在用户行为上应被区分。

### D3. Semantic-Collaborative Alignment

**输入**：metadata/category/text embedding optional + interaction co-occurrence。

**指标**：

- SID-prefix neighborhood vs co-occurrence neighborhood 的 Jaccard / Recall@K；
- category purity；
- semantic-near but collaborative-far case count；
- collaborative-near but semantic-far case count。

**作用**：诊断 semantic ID 是否真的服务 recommendation，而不是只产生语义好看的 clusters。

### D4. Head-Tail Capacity Allocation

**输入**：item popularity + SID mapping。

**指标**：

- head/mid/tail bucket 的 code entropy；
- tail item prefix collision；
- bucket-level unique prefix ratio；
- tail harmful collision rate。

**作用**：这是 CIKM v0 最容易出 insight 的维度。很多 SID 方法 aggregate metric 好看，但 tail capacity 可能差异明显。

### D5. Deployment-Cost Proxy

**输入**：SID mapping；如果有 generator outputs，则加入 candidate list。

**指标**：

- average SID length；
- trie branching factor；
- duplicate candidate rate；
- invalid generation rate；
- beam size needed for fixed candidate coverage。

**v0 拆分**：

- **D5a required-light**：只基于 SID mapping，必须实现 average SID length、trie branching factor、duplicate/ambiguous SID rate；
- **D5b optional**：只有 TIGER/GenRec 能导出 generated candidates 时，才做 invalid generation、duplicate candidate rate、beam coverage。

### Optional D6. Drift Stability

**输入**：static vs refreshed SID mappings 或 temporal split。

**指标**：

- SID churn rate；
- prefix churn by popularity bucket；
- stable item vs drifting item code change；
- churn vs downstream metric proxy。

**纳入条件**：DACT 或 controlled tokenizer refresh 能在 2026-05-28 前跑通。

## CIKM 4-Page Paper Structure

### Title

AUDIT-SID: An Open Diagnostic Toolkit for Semantic-ID Tokenizers in Generative Recommendation

### Abstract

强调三点：

- semantic-ID tokenizer 已成为 generative recommendation/retrieval 的核心瓶颈；
- 现有论文主要看 final ranking metrics，缺少 tokenizer-level diagnostic tooling；
- AUDIT-SID 提供 open toolkit 和 case study。

### Section 1: Motivation

1 page 内完成：

- SID/tokenizer/codebook trend；
- 为什么 leaderboard 不够；
- CIKM Resource 贡献。

### Section 2: Toolkit and Diagnostics

1.2 pages：

- 输入格式；
- D1-D5a 核心 diagnostics；
- 输出 tables/plots；
- 支持 tokenizer artifacts。

### Section 3: Case Study

1.2 pages：

- dataset；
- methods；
- 关键 diagnostic table；
- 1-2 个 non-redundant diagnostic case findings。

### Section 4: Resource Availability and Limitations

0.5 pages：

- GitHub；
- reproducibility；
- limitations；
- future extension。

## 19-Day Execution Schedule

| Date | Milestone | Output | Decision |
|---|---|---|---|
| 2026-05-18 | freeze CIKM spec | this document | done |
| 2026-05-18 | external review absorption + public code screen | review absorption doc | done |
| 2026-05-19 | clone/probe ReSID + GRID/RQ-VAE + CARD fallback | Gate 0 repo audit | continue only if artifacts exportable |
| 2026-05-20 | dataset download / schema audit | dataset manifest | choose primary dataset |
| 2026-05-21 | export first item-to-SID mapping | artifact sample | toolkit input format frozen |
| 2026-05-22 | export second item-to-SID mapping | artifact sample | Gate 0 likely pass |
| 2026-05-23 | implement D1-D5a metrics | diagnostic v0 tables | decide if enough for CIKM |
| 2026-05-24 | Gate 0 formal decision | go/no-go note | abandon CIKM if failed |
| 2026-05-25 | case study table + plots | paper figures | start writing |
| 2026-05-26 | resource docs/examples | GitHub-ready artifact | artifact polish |
| 2026-05-27 | first 4-page draft | paper v0 | review |
| 2026-05-28 | final diagnostic table | paper v1 | submit-ready direction |
| 2026-05-30 | abstract submission | CIKM abstract | must submit |
| 2026-06-03 | full paper near-final | CIKM draft | freeze claims |
| 2026-06-06 | full submission | 4-page paper + artifact | submit |

## Gate 0 Acceptance Criteria

Gate 0 passes only if all are true:

1. at least two SID sources produce item-to-SID mappings;
2. the two SID sources cover canonical baseline and recent tokenizer innovation, not merely two variants of the same family;
3. one primary dataset has joinable item ids, metadata, interactions, and popularity;
4. D1-D5a metrics can run without downstream model training;
5. artifact extraction can be documented in commands/scripts;
6. no proprietary or internal data is involved.

If Gate 0 fails, stop CIKM 2026 submission.

## Current Decision

Use this minimal CIKM configuration:

- **Dataset**: ReSID processed Amazon-2023 `Musical_Instruments` first; Amazon 2014 Beauty/Sports as backup.
- **Methods**: RQ-VAE/TIGER-style SID + ReSID + sanity ID baseline.
- **Diagnostics**: D1-D4 plus D5a must-have; D5b/D6 optional.
- **Paper type**: CIKM 2026 Resource Track, 4 pages.
