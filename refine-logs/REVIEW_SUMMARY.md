# Research Review Summary：AUDIT-SID

**生成时间**：2026-05-18 13:19:39 CST  
**Review mode**：按 `/research-review` 结构进行本地 critical review；本轮未启动 delegated reviewer。

## Mock Reviewer Verdict

**Score**：如果做成 diagnostic methodology，是 borderline positive；如果做成 leaderboard，是 weak reject。

这个 idea 时机很好。近期 semantic-ID 文献确实把 tokenizer/codebook 变成核心问题。但论文必须比“比较若干 SID 方法”更尖锐，需要产出可复用诊断、非显然发现和 actionable guidance。

## Strengths

- 方向时机强：近期论文连续暴露 tokenizer/codebook bottleneck。
- 与本项目 audit/evaluation brand 匹配。
- public-first 可行：Amazon、MIND、H&M、Steam 等可支持第一阶段。
- 即使发现 diagnostics 不稳定，也可能形成有价值的负结果。
- 后续可与内部 switch-back recommendation 的 semantic evidence token 连接。

## Weaknesses

- novelty 不是自动成立，因为很多 SID 方法论文已经报告 utilization、collision、quantization loss 或 cost。
- 公开数据无法支撑强工业部署 claim。
- 复现多个新 SID baseline 可能工程成本高。
- diagnostic metrics 之间可能高度相关，或无法解释最终表现。
- 如果问题不够尖锐，reviewer 会认为只是 benchmark engineering。

## Minimum Improvements Needed

1. 定义紧凑的 diagnostic taxonomy，避免 metric catalog。
2. 至少包含一个不太标准的诊断，如 **collision harm** 或 **ranking-alignment disagreement**。
3. 加入 stress regime：tail items、temporal split、catalog churn、beam/cost pressure。
4. 给出 result-to-claim matrix，明确正负结果都能支持什么 claim。
5. 先用 open baseline 和可导出的 SID assignments，不要一上来承诺所有新方法。

## Key Objections

**Objection**：这不是 method paper。  
**Response**：是的，应定位为 methodology / diagnostic evaluation。贡献是公开 protocol 和关于 tokenizer properties 的经验发现。

**Objection**：DIG 已经指出 ranking 和 generation 是 tokenizer-alignment 问题。  
**Response**：DIG 是方法论文；AUDIT-SID 要将 ranking alignment 作为跨 tokenizer / dataset / regime 的诊断。

**Objection**：DACT 已经研究 drift。  
**Response**：DACT 是 continual tokenizer 方法；AUDIT-SID 把 drift stability 纳入统一 audit suite。

## Scope Reduction

v1 不要覆盖所有 SID paper。建议从：

- 一个 RQ-VAE/TIGER-style baseline；
- 一个 recommendation-native tokenizer，如 ReSID；
- 一个 continual/drift-oriented tokenizer，如果 code 可用，否则用 controlled tokenizer-refresh simulation。

数据从两个开始：

- Amazon category subset；
- MIND 或 H&M。

## Final Recommendation

进入 feasibility gate。第一步不是训练，而是证明至少两个 tokenizer family 能在一个公开数据集上导出诊断所需 artifact。
