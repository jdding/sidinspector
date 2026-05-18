# Literature Review：AUDIT-SID

**生成时间**：2026-05-18 13:19:39 CST  
**主题**：semantic-ID tokenizer / codebook 在 generative recommendation / retrieval 中的 public-first 诊断框架。

## 一句话结论

近期文献已经把瓶颈从单纯的 sequence model 推到 tokenizer/codebook 层。AUDIT-SID 有 public-first 空间，但必须做成诊断方法论，而不是普通榜单。

可行的核心是把 tokenizer 内部性质和下游行为连接起来：

- accuracy / retrieval quality；
- codebook utilization 与 collapse；
- collision harm；
- head-tail capacity allocation；
- semantic-collaborative alignment；
- beam search / decoding cost；
- catalog drift 下的 stability。

## 关键文献

### ReSID

`Rethinking Generative Recommender Tokenizer: Recsys-Native Encoding and Semantic Quantization Beyond LLMs` 指出，很多 SID 方法依赖 semantic embeddings 和 generic quantization，但这些设计和 collaborative prediction 耦合不强。它强调 information preservation、sequential predictability 和 tokenization cost。

对 AUDIT-SID 的意义：ReSID 把 predictability 和 quantization efficiency 显式化，但仍是 method paper 内部自证。AUDIT-SID 可以检验这些内部指标是否跨 tokenizer / dataset / stress regime 成立。

Source: https://arxiv.org/abs/2602.02338

### DACT

`Drift-Aware Continual Tokenization for Generative Recommendation` 关注动态环境：new item 会导致 identifier collision/shift，new interaction 会导致 collaborative drift；naive tokenizer fine-tuning 还可能破坏已有 token-embedding alignment。

对 AUDIT-SID 的意义：DACT 暴露了 deployment-critical 的 stability/plasticity 轴，公开静态 split 通常测不出来。

Source: https://arxiv.org/abs/2603.29705

### CapsID

`CapsID: Soft-Routed Variable-Length Semantic IDs for Generative Recommendation` 明确说主要瓶颈是 tokenizer，而不是 Transformer；问题包括 hard residual quantization、cluster boundary collapse 和 early-error propagation。

对 AUDIT-SID 的意义：这支持 boundary sensitivity、variable length、error propagation、tail item representation 等诊断轴。

Source: https://arxiv.org/abs/2605.05096

### AsymRec

`Asymmetric Generative Recommendation via Multi-Expert Projection and Multi-Faceted Hierarchical Quantization` 把 discrete semantic ID 的问题拆成 input bottleneck 和 output bottleneck，包括 lossy quantization、popularity bias、imprecise discrete targets。

对 AUDIT-SID 的意义：这些正好可以转化为 quantization loss、popularity skew、target precision、tail generalization 等外部诊断。

Source: https://arxiv.org/abs/2605.14512

### DIG

`Discrimination Is Generation: Unifying Ranking and Retrieval from a Tokenizer Perspective` 认为 SIDs 定义了 generation space 和 personalization ceiling，并批评 independent tokenizer 让 personalization signal 和 SID construction 脱耦。

对 AUDIT-SID 的意义：ranking alignment 必须成为 tokenizer 诊断指标，而不仅是 semantic clustering 指标。

Source: https://arxiv.org/abs/2605.14853

### CQ-SID

`Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL` 将 generative retrieval 定位为工业电商 recall-stage supplement，强调 dynamic catalog、latency、ranking alignment、semantic cluster IDs、beam-search reduction 和 online evidence。

对 AUDIT-SID 的意义：这是最强工业信号。公开 AUDIT-SID 不能复现线上收益，但可以诊断 cost、beam、ranking-alignment proxy。

Source: https://arxiv.org/abs/2605.14434

## Landscape Map

| 子方向 | 代表论文 | 主张 | 诊断缺口 |
|---|---|---|---|
| Recommendation-native tokenizer | ReSID, DIG | tokenizer 应服务 collaborative/ranking signal | 缺跨方法 predictability 和 ranking alignment 诊断 |
| Continual tokenizer update | DACT, SID staleness work | tokenizer 会 drift 并扰动已部署模型 | 缺统一 stability/plasticity stress test |
| Codebook / collision design | AdaSID, CARD, DIGER, CapsID | collision/utilization/quantization 重要 | 缺 benign collision 与 harmful collision 区分 |
| Industrial generative retrieval | CQ-SID, GenRec-style systems | SID 影响 latency、beam、ranking alignment | 缺公开 deployability proxy |
| Bottleneck analysis | AsymRec, CapsID | discrete ID 带来 input/output bottleneck | 缺 final Recall@K 之外的 decomposition |

## 结构性机会

1. 目前没有中立的 cross-method diagnostic standard。
2. Recall@K/NDCG 隐藏了机制来源。
3. collision 不能只看 occupancy，要看 recommendation harm。
4. drift/stability 在公开 benchmark 中被低估。
5. deployment cost 缺少标准 public proxy。
6. semantic-collaborative mismatch 是多篇论文共同暴露的问题。

## 公开数据可行性

| Dataset | 角色 | 优势 | 弱点 |
|---|---|---|---|
| Amazon Reviews / Amazon 2023 | 主 benchmark | metadata、category、long-tail、多域 | exposure 较弱 |
| MIND | text-heavy item benchmark | 新闻文本丰富、天然时间切分 | 与电商 catalog 行为不同 |
| H&M | catalog churn / seasonal stress | 活跃目录与季节变化明显 | SID baseline 需要适配 |
| Steam / Yelp / MovieLens | robustness check | metadata 和 user-item history 可用 | 工业 retrieval 贴合度较弱 |
| KuaiRec / KuaiRand | exposure-aware auxiliary | 有更强 exposure context | item semantic metadata 取决于具体使用方式 |

## 初步结论

AUDIT-SID 可行，但必须定位为：

> 面向 semantic-ID tokenizer 的 representation-to-deployment diagnostic suite。

不可定位为：

> 又一个 public SID leaderboard。
