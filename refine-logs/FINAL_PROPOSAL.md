# Final Proposal：AUDIT-SID

**生成时间**：2026-05-18 13:19:39 CST  
**Verdict**：READY FOR FEASIBILITY GATE，暂不进入完整实验。

## Problem Anchor

Semantic-ID generative recommenders 越来越依赖 tokenizer/codebook 设计，但现有评估主要报告 Recall@K/NDCG 和方法内部 ablation。这会掩盖改进来源：semantic grouping、collaborative alignment、collision harm、token predictability、tail capacity、decoding cost、drift stability。

## Final Method Thesis

AUDIT-SID 是一个 public diagnostic suite，用 representation、ranking、stability、deployment-proxy 四类视角审计 semantic-ID tokenizers，并检验哪些 diagnostics 能解释下游 generative recommendation/retrieval 行为。

## Dominant Contribution

主贡献不是新 tokenizer，而是：

> 可复用的 semantic-ID tokenizer/codebook 诊断协议，以及关于哪些内部性质能或不能预测下游质量的经验发现。

## Core Diagnostic Metrics

### D1. Codebook Utilization

- dead-code rate；
- per-level code usage entropy；
- prefix occupancy；
- branch imbalance；
- effective vocabulary size。

### D2. Collision Harm

衡量共享相同或相近 SID prefix 的 item，是否在用户行为上本应被区分。

### D3. Semantic-Collaborative Alignment

比较 metadata/text/image embedding neighborhood、collaborative co-occurrence neighborhood、SID-prefix neighborhood 的一致性。

### D4. Token Predictability

衡量 generator 预测 SID sequence 的难度：

- correct SID sequence rank；
- prefix-level next-token likelihood；
- invalid-token rate；
- beam search 下的 prefix ambiguity。

### D5. Head-Tail Capacity Allocation

衡量表达容量是否被 head item 占据，tail item 是否获得足够可区分且可预测的 code。

### D6. Drift Stability

在 temporal split 或 simulated catalog update 下衡量：

- SID churn rate；
- popularity bucket 下的 prefix churn；
- retained-generator compatibility；
- tokenizer refresh 后的 downstream degradation。

### D7. Deployment-Cost Proxy

- average SID length；
- fixed recall 所需 beam size；
- candidate duplication rate；
- invalid candidate rate；
- trie branching factor / prefix fan-out。

## Claims Matrix

| Possible result | Allowed claim | Not allowed |
|---|---|---|
| diagnostics 强预测 downstream quality | AUDIT-SID 找到可靠 tokenizer quality signals | universal production deployment claim |
| diagnostics 只在部分 regime 有效 | SID evaluation 是 regime-dependent | single global tokenizer score |
| diagnostics 无法预测 final Recall@K | 常见内部指标不可靠，downstream training 可能主导 | AUDIT-SID 能排序所有方法 |
| collision harm 解释 tail degradation | collision 必须行为化衡量 | all collisions are bad |
| drift metrics 暴露 tokenizer churn | static public SID evaluation 不完整 | DACT-style 方法总是更好 |

## Explicitly Rejected Complexity

- 不以新 tokenizer 为主贡献。
- 不从公开数据声称工业部署有效。
- v1 不复现所有近期 SID paper。
- 除非数据必须，不引入大型 LLM 或复杂 multimodal encoder 依赖。

## Target Venue Shape

可能匹配：

- SIGIR / CIKM / WSDM resource、benchmark、evaluation-oriented track；
- 结果强时可冲 RecSys main 或 industry-adjacent evaluation paper；
- 只有在证据成熟后再考虑 journal。

## Go / No-Go Condition

只有满足以下条件才进入完整实验：

1. 至少两个 tokenizer family 能在公开数据上运行或重建；
2. 能导出 SID assignments 和 generator outputs；
3. 至少四个 diagnostic axes 可稳定计算；
4. 至少一个 diagnostic 结果不是 final Recall@K 的平凡复述。
