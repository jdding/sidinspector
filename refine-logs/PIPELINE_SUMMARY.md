# Pipeline Summary：AUDIT-SID

**生成时间**：2026-05-18 13:19:39 CST  
**Problem**：semantic-ID tokenizer/codebook evaluation for generative recommendation/retrieval  
**Final Verdict**：PROCEED WITH CAUTION TO FEASIBILITY GATE

## Final Deliverables

- Brief：`RESEARCH_BRIEF.md`
- Literature review：`idea-stage/LITERATURE_REVIEW.md`
- Idea report：`idea-stage/IDEA_REPORT.md`
- Novelty check：`refine-logs/NOVELTY_CHECK.md`
- Review summary：`refine-logs/REVIEW_SUMMARY.md`
- Proposal：`refine-logs/FINAL_PROPOSAL.md`
- Experiment plan：`refine-logs/EXPERIMENT_PLAN.md`
- Tracker：`refine-logs/EXPERIMENT_TRACKER.md`

## Contribution Snapshot

AUDIT-SID 应定位为 diagnostic methodology paper。核心 claim 是：semantic-ID tokenizer/codebook 的质量需要 representation-to-deployment diagnostics，而不能只看 final ranking metrics。

## Ranking After This Pipeline

1. **Internal-grounded method Top-1**：仍是 device-switch return recommendation with adaptive semantic evidence tokenization。
2. **Public-first methodology Top-1**：AUDIT-SID。
3. Ranking Experiment Agent 仍是独立 system/workflow 方向。

## Start Decision

暂不启动完整实验。下一步是 Gate 0：

> 验证至少两个 public SID/tokenizer implementation 能否在一个小公开数据集上导出 item-to-SID mappings 和 generator outputs。

如果 Gate 0 失败，应该早停，而不是把它硬做成弱 survey 或弱 benchmark。

## Frozen CIKM v0 Scope

- Dataset：ReSID processed Amazon-2023 `Musical_Instruments` first；Amazon 2014 Beauty/Sports backup。
- Methods：canonical RQ-VAE/TIGER-style SID + one representative recent tokenizer innovation, preferably ReSID if artifact export is meaningful, plus random/popularity/category sanity ID baseline。
- Diagnostics：D1 codebook utilization；D2 collision harm；D3 semantic-collaborative alignment；D4 head-tail capacity allocation。
- Optional：D5 deployment-cost proxy；D6 drift stability / DACT。
- Paper type：4-page CIKM 2026 Resource paper。

Method representativeness is a hard gate. If the runnable methods do not cover both canonical SID and recent tokenizer innovation, or if the analysis remains shallow, do not submit CIKM 2026.

## Venue Decision

目标不应按普通 recommender algorithm paper 选择。当前 venue plan：

- immediate target：CIKM 2026 Resource Track；
- abstract deadline：2026-05-30 AoE；
- paper deadline：2026-06-06 AoE；
- Gate 0 deadline：2026-05-24，必须确认至少两个 tokenizer implementation 可导出 item-to-SID mapping；
- later backup：SIGIR 2027 Resource/Reproducibility-style track，RecSys 2027 Resource/Reproducibility，CIKM 2027 Resource；
- WSDM 2027 main 只有在出现强 empirical finding 时成立。
