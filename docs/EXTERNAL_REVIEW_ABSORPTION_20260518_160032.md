# External Review Absorption: AUDIT-SID CIKM Sprint

**生成时间**：2026-05-18 16:00:32 CST
**状态**：absorbed into current plan/spec materials
**目标**：把外部 AI/同行评审意见转成 CIKM 2026 Resource sprint 的硬规则、降级策略和 next actions。

## 结论

继续走 CIKM 2026 Resource Track，但只走 **速战速决的 resource-first v0**：

- 主贡献是 AUDIT-SID toolkit、输入接口、diagnostic taxonomy、Method Coverage Table；
- case study 只需证明 diagnostics 非冗余、可解释、有行动价值；
- 强 empirical finding 是 stretch goal，不再作为论文成立的前提；
- 不为了拉长周期而补很多新 tokenizer；
- 2026-05-24 前 Gate 0 / 0A 不过，停止 CIKM 2026，不硬投。

## 已吸收的评审意见

| Review concern | Absorbed decision | Files updated |
|---|---|---|
| 当前 spec 更像 research paper plan，不像 resource paper plan | 改成 resource-first：toolkit/interface/coverage table 是主线；finding 降为 stretch | `docs/PROJECT_SPEC.md`, `docs/AUDIT_SID_CIKM_EXECUTION_SPEC.md`, `refine-logs/EXPERIMENT_PLAN.md` |
| 时间表物理极限过高 | 保留 CIKM，但把 2026-05-24 作为 hard no-go；不扩展新 tokenizer | `refine-logs/EXPERIMENT_TRACKER.md`, `START_HERE_AUDIT_SID.md` |
| Cluster B 候选真实可得性不确定 | 当天完成 public availability screen；ReSID first, CARD fallback, DIGER backup；CapsID/AdaSID/AsymRec future-only unless code appears | `docs/METHOD_REPRESENTATIVENESS_AUDIT.md` |
| D1 utilization 太 commodity | D1 只做基础表；case study 必须来自 D2/D3/D4/D5a 至少一个 | `docs/PROJECT_SPEC.md`, `refine-logs/EXPERIMENT_PLAN.md` |
| D2 collision harm 太宽 | Gate 2 要求 D2 区分 full SID collision、prefix collision，并用 popularity/category matched pair 控制混杂 | next implementation note |
| D3 collaborative reference 易变成“像不像 SASRec” | D3 必须至少支持 co-occurrence reference；SASRec embedding kNN 只能作为 optional second reference | next implementation note |
| D4 容易复述 popularity | D4 要控制 popularity bucket 后比较 tokenizer capacity behavior | next implementation note |
| D5 deployment cost 对 resource 价值高 | D5a 升级为 required-light：SID length、trie branching、duplicate/ambiguous SID rate；D5b generator outputs optional | `docs/PROJECT_SPEC.md`, `docs/AUDIT_SID_CIKM_EXECUTION_SPEC.md` |
| 单 Amazon dataset 易被 reviewer 攻击 | MovieLens-1M 作为 half-day portability smoke only after Gate 0 stable；不引入新 tokenizer | `docs/PROJECT_SPEC.md`, `refine-logs/EXPERIMENT_PLAN.md` |
| Toolkit-as-artifact 写得太少 | 新增 `src/audit_sid/interface.py` skeleton 和 schema contract | `src/audit_sid/interface.py`, `docs/PROJECT_SPEC.md` |
| “B artifact only D1” 太弱 | Gate 0A 改为 Cluster B 必须支撑至少两个核心诊断 | `docs/METHOD_REPRESENTATIVENESS_AUDIT.md` |
| Gate 2 稳定性未量化 | single-artifact metrics 必须 deterministic；重新训练 tokenizer 时报告 2-3 seeds 或明确 single-artifact limitation | `refine-logs/EXPERIMENT_PLAN.md` |

## Public Availability Screen

本节是 2026-05-19 local repo audit 的优先级依据，不等于真正 Gate 0 通过。

| Candidate | Status on public web | Sprint decision | Source |
|---|---|---|---|
| ReSID | Official GitHub exists; README links arXiv and Hugging Face dataset; one-command pipeline on `Musical_Instruments` | Cluster B first probe | https://github.com/FuCongResearchSquad/ReSID |
| ReSID dataset | Hugging Face dataset includes 10 Amazon-2023 categories, user sequences, structured item features, train/valid/test | Primary dataset probe | https://huggingface.co/datasets/PIIR/ReSID-dataset |
| GRID | Public GitHub; README shows semantic ID learning/generation and TIGER inference with RQ-KMeans/RQ-VAE/RVQ | Cluster A first probe | https://github.com/snap-research/GRID |
| CARD | Public GitHub; README shows Amazon 2014 preprocessing, `nu-rq-vae/main.py`, and `generate_code.py` | Cluster B fallback if ReSID weak | https://github.com/HAI-UESTC/CARD |
| DIGER | Public GitHub exists, but README says current release is illustrative/reference and full runnable assets are planned later | Backup only | https://github.com/junchen-fu/DIGER |
| CapsID | arXiv paper exists; quick public screen did not find runnable code | Method Coverage Table / future support | https://arxiv.org/abs/2605.05096 |
| AdaSID | arXiv paper exists; quick public screen did not find confirmed public code | Method Coverage Table / future support | https://arxiv.org/abs/2604.23522 |
| AsymRec | arXiv page says code will be released | Method Coverage Table / future support | https://arxiv.org/abs/2605.14512 |
| DACT | Public GitHub with tokenizer train/tokenize scripts | Optional D6 only, after A+B stable | https://github.com/HomesAmaranta/DACT |

## Revised Gate Policy

Gate 0 / 0A passes only if all are true:

1. one Cluster A method and one Cluster B method export joinable `item-to-SID` assignments;
2. Cluster B supports at least two of D1-D5a, not D1 alone;
3. primary dataset can join SID mapping, metadata, interactions, and popularity;
4. toolkit adapters can convert outputs to the fixed interface schema;
5. D1-D5a can run without downstream model training;
6. no proprietary/internal data or implementation detail is used.

Stop CIKM 2026 if:

- ReSID and CARD both fail as exportable Cluster B artifacts;
- only GRID/RQ-VAE + sanity baseline remains;
- diagnostic output is only utilization/collision counts with no case study;
- local probing consumes more than the 2026-05-24 gate budget.

## Next Actions

1. Run local Gate 0 repo audit in this order: GRID/RQ-VAE, ReSID, then CARD only if needed.
2. Convert any exported mapping into `src/audit_sid/interface.py` schema.
3. Freeze dataset schema on ReSID `Musical_Instruments`; only consider MovieLens-1M after Gate 0 is stable.
4. Implement D1-D5a as mapping-first metrics.
5. Write `docs/GATE0_DECISION.md` by 2026-05-24 with explicit go/no-go.
