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

## Venue Decision

目标不应按普通 recommender algorithm paper 选择。当前 venue plan：

- 2026-06-15 左右：arXiv + GitHub v0；
- 主目标：SIGIR 2027 Resource/Reproducibility-style track；
- 自然备选：RecSys 2027 Resource/Reproducibility，CIKM 2027 Resource；
- 条件性目标：WSDM 2027 main track，只有在有强 empirical finding 时成立；
- 短期曝光：RecSys 2026 workshop/demo/R&P，如时间和 artifact 质量允许。
