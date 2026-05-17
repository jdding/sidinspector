# Idea Report Post-Novelty Addendum

**Direction**: lifecycle-stratified off-policy evaluation under sparse support in sequential recommendation
**Generated**: 2026-05-17 22:45:46 CST
**Base report**: `idea-stage/IDEA_REPORT.md`
**Novelty report**: `refine-logs/NOVELTY_CHECK.md`
**Language**: zh

## 结论

重新按 `/research-lit -> /idea-creator -> /novelty-check` 跑完后，当前 top-3 ideas 都不能按“新 OPE estimator / 新 OPE method”来写。最稳妥路线是：

1. **主线**：Lifecycle-State Credibility Protocol for OPE，作为 public-data protocol/resource contribution。
2. **辅助模块**：Lifecycle-Targeted Exploration Budget Simulator，作为 logging-design simulator 和后续内部业务落地桥梁。
3. **基线规则**：Lifecycle-Conservative Policy Selection，只作为 conservative decision-rule baseline，不作为主创新点。

## Novelty Gate

| Idea | Novelty | Decision | Reviewer Risk |
|---|---:|---|---|
| Lifecycle-State Credibility Protocol for OPE | 5/10 | PROCEED | 容易被认为是 DataCOPE/OBP-style OPE readiness 加 subgroup diagnostics。 |
| Lifecycle-Conservative Policy Selection | 3/10 | CAUTION | 容易被认为是 group-constrained lower-confidence policy selection。 |
| Lifecycle-Targeted Exploration Budget Simulator | 4/10 | CAUTION | 容易被认为是 simulation-only support/uncertainty allocation heuristic。 |

## 对实验计划的影响

早期 `refine-logs/EXPERIMENT_PLAN.md` 不能作为正式 claim-driven plan 使用。后续只能先做 gate-level feasibility：

- OBP：验证 estimator API、propensity、confidence interval、ground-truth-style sanity check。
- KuaiRand：验证 random-exposure subset、policy/scenario metadata、pre-exposure lifecycle-state 可计算性。
- KuaiRec：验证 oracle stress test 能否构造 aggregate-vs-state reversal。
- MIND：保留为 D0/D1 impression-scale diagnostic，不做 strict IPS/DR claim。

只有当 schema feasibility 证明公开数据能支撑 lifecycle-state credibility protocol 后，才重写正式 experiment plan。
