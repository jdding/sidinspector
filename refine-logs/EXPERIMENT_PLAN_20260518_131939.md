# Experiment Plan：AUDIT-SID for CIKM 2026 Resource

**生成时间**：2026-05-18 13:19:39 CST  
**Status**：GATED；Gate 0 之前不启动完整训练。  
**Venue target**：CIKM 2026 Resource Track。  
**Abstract deadline**：2026-05-30 AoE。  
**Paper deadline**：2026-06-06 AoE。

## Purpose

这个 plan 用来把 AUDIT-SID 收敛成 CIKM 2026 Resource Track 可提交版本。核心产物是开源 diagnostic toolkit + 小规模 public case study。

## CIKM v0 冻结配置

| Component | Decision | Rationale |
|---|---|---|
| Primary dataset | ReSID processed Amazon-2023 `Musical_Instruments` | ReSID 官方 processed dataset + 示例 category，降低数据处理成本 |
| Backup dataset | Amazon 2014 Beauty/Sports | GenRec 支持；如果 ReSID dataset 与 RQ-VAE pipeline 不易对齐时兜底 |
| Must-run method 1 | RQ-VAE / TIGER-style SID | classical semantic-ID baseline |
| Must-run method 2 | ReSID | recommendation-native tokenizer with official code |
| Sanity baseline | Random / popularity-balanced / category-prefix ID | 确认 diagnostics 有基本区分度 |
| Optional method | DACT | 仅在 2026-05-24 前可导出 updated SID mapping 时纳入 |
| Must-have diagnostics | D1-D4 | utilization, collision harm, semantic-collaborative alignment, head-tail capacity |
| Optional diagnostics | D5-D6 | deployment-cost proxy, drift stability |

## 未来主 claim

Semantic-ID tokenizer 不能只靠 final Recall@K/NDCG 判断；可复用 diagnostics 能揭示 collision harm、ranking-alignment mismatch、head-tail capacity problem、drift instability 和 deployment-cost pressure。

## Gate 0：Code And Artifact Feasibility

**Question**：是否能从至少两个公开 tokenizer/recommender implementation 中导出 SID assignments 和 generator outputs？

Tasks：

1. 查找 RQ-VAE/TIGER-style baseline、ReSID、DACT、CapsID 或兼容实现。
2. 确认每个实现是否能导出：
   - item-to-SID mapping；
   - codebook assignments by level；
   - trained generator scores 或 generated candidates；
   - evaluation predictions。
3. 只做 smoke-level check，不启动完整训练。

Pass condition：

- 至少两个 tokenizer family 能在一个小公开数据集上导出 SID assignments。

Fail condition：

- 只有一个实现可用，或所有方法都无法导出诊断所需 artifact。

## Gate 1：Dataset Support Audit

**Question**：哪些公开数据支持足够多诊断轴？

Candidate datasets：

- Primary: ReSID processed Amazon-2023 `Musical_Instruments`。
- Backup: Amazon 2014 Beauty/Sports。
- Cut for CIKM v0: MIND, H&M, KuaiRec/KuaiRand。

Pass condition：

- CIKM v0 至少一个 primary dataset 支持 metadata、sequential interactions、item popularity buckets，并能与 SID mapping join。
- 如果 backup dataset 也可用，作为 robustness，不作为 CIKM go/no-go 必要条件。

## Gate 2：Diagnostic Metric Implementation

按 CIKM v0 优先级实现：

1. codebook utilization；
2. collision harm；
3. semantic-collaborative alignment；
4. head-tail capacity allocation；
5. deployment-cost proxy optional；
6. drift stability optional。

Pass condition：

- 至少四个 metrics 能在一个数据集和两个 tokenizer variants 上输出稳定、可解释结果。

## Gate 3：Small Empirical Correlation Check

Bounded study：

- 一个 dataset；
- 两个 tokenizer families；
- 一个 generator backbone；
- 可行时 2-3 seeds；
- 比较 diagnostics 与 Recall@K/NDCG、tail Recall、invalid generation、beam/candidate cost。

Pass condition：

- 至少一个 diagnostic 揭示非显然差异，或比 aggregate metrics 更早暴露 downstream failure mode。

## Gate 4：Paper Viability Decision

只有 Gate 3 产生以下任一结果，才进入完整实验：

- diagnostic metric 能跨 tokenizer 预测 downstream performance；
- diagnostic metric 暴露 final Recall@K 相近时隐藏的 failure；
- diagnostics 之间的冲突揭示 regime split，如 head vs tail 或 static vs temporal。

停止条件：

- diagnostics 只是 final metrics 的平凡复述；
- 可用方法/数据过于脆弱；
- 工作变成维护成本很高但 scientific claim 很弱的 benchmark。

## CIKM v0 Package If Gates Pass

Datasets：

- ReSID processed Amazon-2023 `Musical_Instruments`；
- Amazon 2014 Beauty/Sports optional backup only。

Methods：

- RQ-VAE/TIGER-style baseline；
- ReSID；
- Random / popularity-balanced / category-prefix ID sanity baseline；
- DACT optional only if artifact extraction is easy。

Ablations：

- no semantic metadata；
- no collaborative signal；
- fixed vs adaptive codebook size；
- static vs temporal tokenizer；
- head/tail bucket analysis；
- beam size sweep。

CIKM outputs：

- diagnostic tables；
- failure-case visualizations；
- toolkit README and examples；
- result-to-claim matrix。

## Post-CIKM Expansion Candidates

只有 CIKM 版本投出或 Gate 0 证明 artifact path 稳定后，再考虑：

- MIND / H&M / KuaiRec 扩展；
- DACT drift stability；
- deployment-cost proxy with generated candidates；
- WSDM/SIGIR main-track empirical finding version。

## CIKM 19-Day Milestones

| Date | Milestone | Output | Decision |
|---|---|---|---|
| 2026-05-19 | ReSID + GenRec/RQ-VAE repo audit | `docs/GATE0_REPO_AUDIT.md` | continue only if mappings exportable |
| 2026-05-20 | dataset schema audit | `docs/DATASET_SCHEMA_AUDIT.md` | freeze primary dataset |
| 2026-05-21 | first SID mapping export | artifact sample | freeze input schema |
| 2026-05-22 | second SID mapping export | artifact sample | Gate 0 likely pass |
| 2026-05-23 | D1-D4 metrics v0 | diagnostic table | decide if finding exists |
| 2026-05-24 | formal Gate 0 | `docs/GATE0_DECISION.md` | go/no-go for CIKM |
| 2026-05-28 | paper tables/figures | diagnostic case study | submit-ready evidence |
| 2026-05-30 | CIKM abstract | EasyChair abstract | must submit |
| 2026-06-06 | CIKM resource paper | 4-page paper + artifact | final submission |
