# SID Method Cluster Audit for AUDIT-SID

**生成时间**：2026-05-18 14:41:28 CST  
**目的**：在 CIKM 2026 Resource Track 目标下，先基于 literature review 明确 SID/tokenizer 方法簇，再决定哪些方法有代表性、哪些必须跑、评测什么。

## 结论

当前 `LITERATURE_REVIEW.md` 和 `EXPERIMENT_PLAN.md` 已经支持“不要浅跑两个 repo”的方向，但还不完整。缺失的是：

> method cluster -> representative candidates -> artifact feasibility -> diagnostic coverage -> must-run selection

这一层。

本文件补上这层决策。后续 Gate 0 / Gate 0A 必须按这里执行。

## SID 方法簇

### Cluster A: Canonical Residual-Quantization SID

**代表什么**：最经典的 generative recommendation semantic-ID 路线，用 residual/vector quantization 或类似机制把 item 映射为多 token SID。

**候选方法**：

- TIGER / RQ-VAE style SID；
- GenRec-style SID；
- GRID-style SID；
- LC-Rec / TIGER-derived implementations。

**为什么必须有**：

- 它是社区默认 baseline；
- D1 utilization、D2 collision harm、D4 head-tail capacity 在这一类方法上最容易解释；
- 没有它，AUDIT-SID 缺少 reference point。

**CIKM v0 状态**：must-run，除非找不到任何可导出 item-to-SID mapping 的实现。

### Cluster B: Recommendation-Native / Predictability-Aware Tokenizer

**代表什么**：不再把 SID 当作 generic semantic quantization，而是让 tokenizer 服务推荐行为、collaborative signal、sequence predictability 或 ranking objective。

**候选方法**：

- ReSID；
- DIG；
- AsymRec；
- DRIL-style / discriminative tokenizer variants。

**为什么重要**：

- 这是 2026 年最核心的方法变化之一；
- 它直接挑战 canonical RQ-VAE SID 的假设；
- 最适合 AUDIT-SID 的 D3 semantic-collaborative alignment 和 token predictability 诊断。

**CIKM v0 状态**：must-have cluster。优先 ReSID，因为代码和 processed dataset 更现实；若 ReSID artifact 不可解释，则寻找 DIG/AsymRec/DRIL 的可导出实现或放弃 CIKM。

### Cluster C: Collision / Utilization / Variable-Length Codebook Design

**代表什么**：直接优化 collision、codebook utilization、adaptive code assignment、variable length 或 soft routing。

**候选方法**：

- CapsID；
- AdaSID；
- CARD；
- DIGER；
- variable-length SID variants。

**为什么重要**：

- 它和 AUDIT-SID 的 D1/D2/D4 最直接相关；
- 如果代码可用，这类方法比 ReSID 更能证明 AUDIT-SID 的诊断价值；
- 但实现可得性和时间风险较高。

**CIKM v0 状态**：preferred optional。如果 2026-05-24 前可导出 artifact，应优先纳入；否则作为 method coverage table 中的 supported future cluster。

### Cluster D: Continual / Drift-Aware Tokenizer

**代表什么**：关注 new item、catalog shift、collaborative drift、tokenizer refresh 后的稳定性。

**候选方法**：

- DACT；
- SID staleness / continual tokenizer variants；
- controlled tokenizer refresh simulation。

**为什么重要**：

- 这是 deployment-facing 的关键问题；
- 对 D6 drift stability 最自然；
- 但 CIKM 4-page v0 不应被 drift pipeline 绑架。

**CIKM v0 状态**：optional only。只有在 DACT 可轻量导出 updated SID mapping 时纳入；否则不作为 go/no-go。

### Cluster E: Industrial Generative Retrieval / Search-Oriented SID

**代表什么**：把 semantic cluster ID / SID 推入 retrieval/search/recall 场景，关注 ranking alignment、beam cost、latency、candidate generation。

**候选方法**：

- CQ-SID；
- DIG retrieval/ranking framing；
- GenRec industrial variants；
- search-oriented semantic cluster ID methods。

**为什么重要**：

- 这是 SIGIR/CIKM audience 最容易理解的工业牵引点；
- 对 D5 deployment-cost proxy 和 D3 ranking alignment 很关键；
- 但公开复现难度和线上指标不可得。

**CIKM v0 状态**：literature-motivated diagnostic target，不作为 must-run。可以在 paper 里说明 AUDIT-SID 的 interface 未来可接 search/retrieval SID artifacts。

## Must-Run 决策规则

CIKM v0 的 must-run 不再按具体论文名固定，而按 cluster coverage 决定：

| Role | 必须覆盖 | 推荐候选 | 替代候选 | 失败后动作 |
|---|---|---|---|---|
| Canonical baseline | Cluster A | RQ-VAE/TIGER-style SID | GenRec/GRID/LC-Rec SID | 找不到 artifact 则停止 |
| Recent innovation | Cluster B or C | ReSID | CapsID/AdaSID/CARD/DIG/AsymRec if artifact available | 找不到可解释 artifact 则停止 |
| Sanity lower bound | diagnostic lower bound | random SID | popularity-balanced/category-prefix SID | 必须自己实现 |

因此，`RQ-VAE + ReSID` 只是当前候选组合，不是理论上固定的 must-run。真正的 must-run 是：

> Cluster A + Cluster B/C + sanity lower bound.

## 代表性验收标准

一个方法能被算作 representative，必须满足：

1. **Cluster identity 清楚**：能说明它代表哪个 SID/tokenizer 方法簇。
2. **Artifact 可导出**：能导出 item-to-SID mapping，最好有 per-level code assignment。
3. **诊断轴相关**：至少对应 D1-D4 中两个诊断轴。
4. **Case study 可解释**：能产生一个具体诊断发现，而不是只给最终 Recall@K。
5. **可复现成本可控**：CIKM sprint 内可以运行或复用 artifact。

## 评测内容设计

### 必评：D1 Codebook Utilization

适用 cluster：A, B, C。

回答问题：

- codebook 是否塌缩？
- 表达容量是否集中在少数 prefix？
- 不同方法的有效 token 空间是否明显不同？

输出：

- per-level unique code count；
- dead-code rate；
- usage entropy；
- prefix fan-out；
- branch imbalance / Gini。

### 必评：D2 Collision Harm

适用 cluster：A, B, C。

回答问题：

- collision 是语义上合理合并，还是把行为上应区分的 item 压到一起？
- harmful collision 是否集中在 tail item？

输出：

- same-code / same-prefix item pair 的 behavioral similarity；
- harmful collision rate；
- tail harmful collision rate；
- top harmful collision cases。

### 必评：D3 Semantic-Collaborative Alignment

适用 cluster：A, B, E。

回答问题：

- semantic ID 的邻域是否匹配 collaborative neighborhood？
- recsys-native tokenizer 是否真的比 generic semantic tokenizer 更贴近用户行为？

输出：

- SID-prefix neighborhood vs co-occurrence neighborhood overlap；
- category purity；
- semantic-near/collaborative-far cases；
- collaborative-near/semantic-far cases。

### 必评：D4 Head-Tail Capacity Allocation

适用 cluster：A, B, C。

回答问题：

- head item 是否占用过多表达容量？
- tail item 是否被过度 collision 或压缩？

输出：

- bucket-level code entropy；
- head/mid/tail unique prefix ratio；
- tail collision rate；
- tail harmful collision examples。

### 选评：D5 Deployment-Cost Proxy

适用 cluster：A, E。

纳入条件：

- 能导出 candidate list、beam outputs 或至少 SID trie。

输出：

- SID length；
- trie fan-out；
- candidate duplication；
- invalid generation；
- beam/candidate coverage proxy。

### 选评：D6 Drift Stability

适用 cluster：D。

纳入条件：

- DACT 或 controlled tokenizer refresh 能在 2026-05-28 前跑通。

输出：

- SID churn；
- prefix churn by popularity bucket；
- stable vs drifting item analysis。

## CIKM Paper 中必须出现的表

### Table 1: Method Coverage Table

列：

- Method；
- Cluster；
- Artifact available；
- SID mapping；
- code level；
- generator output；
- diagnostics supported；
- used in CIKM v0 or future support。

### Table 2: Diagnostic Summary Table

列：

- Method；
- utilization entropy；
- dead-code rate；
- harmful collision rate；
- semantic-collaborative overlap；
- tail unique-prefix ratio。

### Table 3 或 Figure 1: Failure Case Study

展示一个非平凡发现：

- RQ-VAE 与 recent tokenizer final metric 可能接近，但 tail harmful collision 不同；
- 或 ReSID 改善 collaborative alignment，但牺牲 prefix balance；
- 或 random/category baseline 揭示某个 diagnostic 的 sanity behavior。

## 当前文档是否支持该思路

### 支持的部分

- `LITERATURE_REVIEW.md` 已经有初步 landscape map；
- `EXPERIMENT_PLAN.md` 已经有 Gate 0A；
- `AUDIT_SID_CIKM_EXECUTION_SPEC.md` 已经把 shallow comparison 设为失败条件。

### 不足的部分

- 原 literature review 没有把方法簇转化为 must-run 选择规则；
- 原 experiment plan 没有明确“Cluster A + Cluster B/C + sanity lower bound”才是 must-run；
- 原评测维度没有按方法簇说明每个 diagnostic 在回答什么问题。

### 本文件的修正

本文件补齐：

1. SID 方法簇；
2. representative method 验收标准；
3. must-run cluster coverage；
4. D1-D6 与方法簇的对应关系；
5. CIKM paper 必须出现的表。

## Next Step

Gate 0 / 0A 的第一步不应是训练，而是生成：

`docs/METHOD_REPRESENTATIVENESS_AUDIT.md`

其中必须列出：

- 每个候选 repo 属于哪个 cluster；
- 是否可导出 artifact；
- 是否能支撑 D1-D4；
- 最终 CIKM v0 选中的方法组合；
- 如果组合不够代表性，明确 no-go。
