# AUDIT-SID Venue Plan

**生成时间**：2026-05-18 13:36:45 CST  
**当前假设**：如果接下来约 28 天完成 v0 工作，则可在 2026-06-15 左右形成 arXiv + open-source artifact。

## 结论

AUDIT-SID 的投稿目标不应按普通 recommender algorithm paper 选择。它更像：

> evaluation / diagnostic / resource / reproducibility paper for generative recommendation and retrieval.

因此主目标应优先考虑有明确 **Resource / Reproducibility / Evaluation / Datasets / Benchmark** 入口的 track，而不是强行按新模型方法投。

更精确地说：

> AUDIT-SID 只有在 venue 明确接收 evaluation resource、reproducibility analysis、benchmark suite、software toolkit 或 evaluation methodology 时才是自然投稿对象。

如果某个会议只有普通 research track，而没有类似 track，则 AUDIT-SID 必须升级成强 empirical finding full paper，否则不应作为主目标。

**2026-05-18 更新**：考虑到 SIGIR 2027 太晚，会导致持续追新疲劳，当前执行目标应改为：

> CIKM 2026 Resource Track.

理由很直接：CIKM 2026 Resource Track 明确接收 dataset/protocol、software resources、open-source frameworks、tools/libraries for evaluation and exploration；deadline 也最近，能迫使 AUDIT-SID 收敛成一个可交付的 v0 resource paper。

关键日期：

- Abstract deadline: 2026-05-30 AoE
- Paper deadline: 2026-06-06 AoE
- Notification: 2026-08-07
- Camera-ready: 2026-08-20

这意味着原本“28 天完成”不够；如果选择 CIKM 2026，必须按 **19 天 full-paper sprint** 执行。

## 28 天版本的定位

如果 2026-06-15 前完成，最现实的产物是：

1. arXiv preprint；
2. GitHub artifact；
3. AUDIT-SID diagnostic toolkit v0；
4. 一到两个公开数据集上的 feasibility evidence；
5. 两到三个 tokenizer family 的 artifact extraction 结果；
6. 初步 diagnostic finding。

这不应直接包装成“完整 top-tier full paper”。更合理是先公开占位并收敛方法论，然后用 2-4 个月补强 full paper。

## Track-Fit Matrix

| Venue / Track | 是否自然接收 AUDIT-SID | 当前判断 |
|---|---|---|
| CIKM 2026 Resource Track | 是 | 最近可投；当前应作为 primary execution target |
| SIGIR Resource & Reproducibility-style track | 是 | 最自然主目标；需要等 SIGIR 2027 CFP 确认是否延续 |
| RecSys Reproducibility / Resource | 是，但 2026 已错过 paper deadline | 2027 适合；2026 只剩 R&P / demo 可做曝光 |
| CIKM Resource Track | 是 | 稳健目标；资源/toolkit/benchmark 形态匹配 |
| NeurIPS Evaluations & Datasets | 概念上是，但 recsys-specific 风险高，且 2026 已过 deadline | 可作高上限远期备选，不是当前主线 |
| KDD Datasets & Benchmarks | 部分匹配 | 更偏 data mining benchmark/tool；需要更强通用性 |
| WSDM Main Track | 仅在有强 empirical finding 时匹配 | 不应只按 resource/toolkit 投；需转成 ranking/retrieval evaluation full paper |
| WWW / TheWebConf Research Track | 弱到中 | 需要明确 Web/recommendation scientific challenge；单纯 resource 容易被认为不匹配 |
| RecSys Main Track | 中 | 只有当 methodology 很强且推荐系统问题足够中心时才适合 |

## Venue Ranking

### Immediate Target: CIKM 2026 Resource Track

**推荐度**：当前最高。

理由：

- track 类型明确匹配：resource / protocol / open-source framework / tool / evaluation library；
- deadline 最近，可以避免 AUDIT-SID 被后续 SID 方法持续刷新拖垮；
- 4-page resource paper 适合 v0：不要求展开完整 full-paper 级别的理论和大规模实验；
- CIKM audience 覆盖 information retrieval、data mining、knowledge management、machine learning，AUDIT-SID 的 generative retrieval / recommendation tokenizer diagnostic 能自然落进去。

应投的版本：

> AUDIT-SID: An Open Diagnostic Toolkit for Semantic-ID Tokenizers in Generative Recommendation and Retrieval

核心交付：

1. 一个 public toolkit；
2. 一个清楚的 diagnostic taxonomy；
3. 至少两个 tokenizer family 的 artifact extraction；
4. 至少一个公开数据集上的 non-trivial diagnostic case study；
5. 文档、examples、reproducible scripts。

不应承诺：

- 完整覆盖所有 SID 方法；
- 工业部署结论；
- 大规模 benchmark leaderboard；
- 新 tokenizer algorithm。

Go/No-Go：

- **2026-05-24 前**必须确认两个 tokenizer implementation 可导出 item-to-SID mapping；
- **2026-05-28 前**必须有一个 dataset 上的 diagnostic table；
- **2026-05-30 前**提交 abstract；
- **2026-06-06 前**提交 4-page paper + artifact link。

如果 2026-05-24 Gate 0 不过，放弃 CIKM 2026 Resource，不硬投。

### Tier 1: Later Formal Targets

#### SIGIR 2027 Resource & Reproducibility-style Track

**推荐度**：长期最高，但不是当前执行目标。

理由：

- AUDIT-SID 连接 recommendation、retrieval、ranking alignment、semantic IDs 和 generative retrieval；
- SIGIR 历史上有 Resource and Reproducibility Papers track，明确接收 evaluation-task protocols、software tools、evaluation/analyzing tools，以及对 prior IR work 的 generalization / error modes / unexpected conclusions 分析；
- CQ-SID / DIG 这类 retrieval-facing 论文使 AUDIT-SID 的问题更自然；
- 如果最终主贡献是 diagnostic suite，而不是新 tokenizer，SIGIR Resource/Reproducibility-style track 比普通 recommender main track 更合适。

理想投稿形态：

- resource paper：AUDIT-SID toolkit + protocol + public artifacts；
- reproducibility paper：复现/泛化若干 SID tokenizer 的 claims，分析哪些假设成立、哪些 failure modes 被忽略；
- full paper 仅在结果显示 diagnostics 对下游失败模式有强解释力时考虑。

需要补强：

- 至少 3 个 tokenizer variants；
- 至少 2-3 个数据集；
- diagnostic-to-downstream correlation 或 counterexample；
- artifact release。

关键依赖：

- SIGIR 2027 必须继续设置 Resource/Reproducibility 或类似 track；若没有，则转 WSDM/SIGIR main 需要更强 empirical finding。
- 如果 CIKM 2026 Resource 已投或已中，SIGIR 2027 只能作为显著扩展版，避免 self-plagiarism 和贡献重复。

#### RecSys 2027 Reproducibility / Resource Track

**推荐度**：高。

理由：

- RecSys 2026 明确设置 Reproducibility and Replicability papers 与 Resource papers；
- Resource papers 包含 open-source software frameworks for evaluating recommender systems；
- AUDIT-SID 如果做成 recommender-system evaluation framework，非常贴合这个入口。

风险：

- 2026 paper deadline 已在 2026-05-05 过去，无法作为本轮 28 天后正式投稿目标；
- RecSys 2026 R&P Notes / Demo 仍可作为曝光，但不等同正式主论文。

#### CIKM 2027 Resource Track

**推荐度**：中高。

理由：

- CIKM Resource Track 明确接收 software resources、open-source frameworks、tools/libraries for evaluation、benchmark tasks；
- 对 applied IR / data mining / ML tooling 较友好；
- 如果 AUDIT-SID 的 artifact/toolkit 完整，但 empirical finding 没强到 SIGIR full paper，CIKM Resource 是稳健目标。

适配版本：

- 4-page resource paper 版本；
- 必须提供公开 artifact、文档、examples、可复现 scripts；
- 如果是 dataset/benchmark，需考虑 DOI/metadata/provenance。

如果 CIKM 2026 没赶上或 Gate 0 未过，CIKM 2027 才重新成为稳健目标。

#### NeurIPS 2027 Evaluations & Datasets

**推荐度**：中等偏高，但不是最自然。

理由：

- NeurIPS 2026 已将 Datasets & Benchmarks 扩展为 Evaluations & Datasets，明确把 evaluation 作为 scientific object；
- 如果 AUDIT-SID 做成通用 evaluation suite，而不是 recommender-specific toolkit，它可匹配；
- 但 recsys/generative retrieval tokenizer diagnostics 可能对 SIGIR/RecSys/CIKM 社区更自然。

风险：

- 需要更强的 general ML evaluation framing；
- 需要高质量 artifact，且如果 benchmark suite 是主贡献，submission 时需要释放 code。

### Tier 1.5: 需要强 empirical finding 才适合

#### WSDM 2027 Main Track

**推荐度**：条件性高。

WSDM 接收 search/data mining/recommendation/evaluation 相关 research，但它不是 resource track。AUDIT-SID 要投 WSDM，不能只写 toolkit，而必须变成：

> semantic-ID tokenizer diagnostics reveal systematic ranking/retrieval failure modes.

也就是说，WSDM 版本需要一个强 finding，例如：

- final Recall@K 接近的 tokenizers 在 collision harm / beam cost / drift stability 上差异巨大；
- ranking-aligned tokenizer 在某些 regime 下牺牲 semantic purity 反而更可靠；
- popular codebook utilization 指标在 tail recommendation 下系统性误导。

没有这类 finding，就不建议 WSDM main。

### Tier 2: 辅助目标

#### RecSys 2026 Research & Practice / Demo / Workshop

**推荐度**：中等，适合作为短期可见性，不建议作为唯一目标。

理由：

- RecSys 2026 main research paper 已不是现实目标；
- Research & Practice / demo / workshop 可能仍有夏季节点；
- 适合把 AUDIT-SID v0 做成 diagnostic toolkit 展示。

风险：

- 两页 note 或 demo 不足以承载完整 methodology；
- 对职业组合价值不如 SIGIR/WSDM full paper。

建议：

- 如果 6 月中旬 artifact 已经干净，可以考虑 RecSys 2026 short/demo/workshop 作为 visibility；
- 但正式论文主线仍应瞄准 SIGIR/WSDM/CIKM。

#### NeurIPS Datasets and Benchmarks

**推荐度**：改为 NeurIPS Evaluations & Datasets 远期备选，2026 不现实。

理由：

- 2026 deadline 已在当前日期前结束；
- 远期可考虑 2027；
- 需要把贡献从 recommender-specific diagnostic 扩展成更一般的 evaluation science。

## 不推荐作为主目标

### KDD Research

除非 AUDIT-SID 最终产出非常强的 empirical law 或方法论发现，否则 KDD Research 对一个 diagnostic suite 可能不如 SIGIR/WSDM 友好。

### KDD ADS

如果后续引入内部真实业务证据，可以考虑。但 public-only AUDIT-SID 不适合按 ADS 主线投。

### RecSys Main

不是不能投，而是风险更高。RecSys main 更容易期待 recommender-specific method 或 strong user-facing experiment；AUDIT-SID 如果偏 retrieval/tokenizer diagnostics，SIGIR/WSDM 更合适。

### WSDM Main Without Strong Finding

不建议。WSDM 没有显式 resource/reproducibility track 时，toolkit/resource 形态不够自然。

## 建议路线

### Phase 0: 2026-05-18 至 2026-06-06

目标：

- 完成 Gate 0；
- 导出至少两个 tokenizer family 的 item-to-SID mappings；
- 完成 diagnostic toolkit v0；
- 提交 CIKM 2026 Resource abstract and paper；
- 明确至少 1 个非平凡 diagnostic case study。

结果判定：

- 如果 2026-05-24 Gate 0 未过：不投 CIKM 2026；
- 如果只有 toolkit，没有 finding：可投 CIKM Resource，但风险较高；
- 如果有至少一个 diagnostic finding：正常投 CIKM Resource；
- paper 后再发布 arXiv/GitHub，注意与 CIKM policy 一致。

### Phase 1: 2026-06 至 2026-08

目标：

- 扩展到 2-3 datasets；
- 补至少 3 个 tokenizer variants；
- 完成 diagnostic-to-downstream evidence；
- 根据结果选择 track:
  - 如果 artifact/toolkit 最强：准备 SIGIR/RecSys/CIKM Resource/Reproducibility；
  - 如果 empirical finding 最强：准备 WSDM/SIGIR main；
  - 如果只有 v0：只 arXiv，不急投。

### Phase 2: 2026-09 至 2027-01

目标：

- 形成 full paper；
- 主攻 SIGIR 2027；
- WSDM/CIKM 作为备选，取决于实际 deadlines 和结果强度。

## 投稿前 Go/No-Go

只有出现以下至少一种结果，才值得投 full paper：

1. 某个 diagnostic 能稳定预测 downstream failure；
2. 两个 tokenizer final Recall@K 接近，但 AUDIT-SID 暴露出不同的 collision/drift/cost risk；
3. 现有常用 tokenizer metric 被证明在某些 regime 下误导；
4. drift/cost/head-tail 诊断改变了方法比较结论。

如果以上都没有，AUDIT-SID 应保持 arXiv/toolkit 状态，不急投主会。

## 当前推荐

短期：

> 2026-06-06 前冲 CIKM 2026 Resource Track；是否 arXiv/GitHub v0 放在投稿策略之后处理。

正式目标：

> 当前 primary execution target 是 CIKM 2026 Resource Track。SIGIR 2027 / RecSys 2027 / CIKM 2027 作为后续扩展或错过 CIKM 2026 后的备选。

可选曝光：

> 如果 RecSys 2026 workshop/demo/R&P 时间合适，可以投一个轻量版本，但不要让它替代主论文目标。
