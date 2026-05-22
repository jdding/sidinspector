# Experiment Plan：AUDIT-SID for CIKM 2026 Resource

**生成时间**：2026-05-18 16:00:32 CST
**Status**：GATED；external review absorbed；Gate 0 之前不启动完整训练。
**Venue target**：CIKM 2026 Resource Track。
**Abstract deadline**：2026-05-30 AoE。
**Paper deadline**：2026-06-06 AoE。

**2026-05-19 15:36:33 CST update**：当前外部模拟评审已达 8.0/8.1。后续实验不应再扩新 metric，而应围绕 strong-accept lift：第三个真实 named tokenizer、同数据集 A/B panel、已有 GRID 三 seed 稳定性呈现、Fig. 1 重画。

**2026-05-19 16:26:26 CST closure update**：当前 CIKM Resource v0 实验包已闭环。第三 named tokenizer screen 给出 negative closure，Fig. 1 重画完成，同数据集 Musical panel 与 GRID Musical 三 seed 稳定性已纳入正文/artifact。剩余工作是 citation drift、真实 single-blind metadata、最终 copy-edit 和 claim audit；除非重新选定明确证据缺口，否则不再新增本地/GPU实验。

**2026-05-19 18:24:00 CST controller update**：controlled stressors/controllers
只作为诊断校准，不作为 named tokenizer 覆盖。v0 使用已有
`collision_collapse`、`semantic_only_grouping`、`popularity_capacity_skew`
三类控制行；唯一可考虑的本地增量是 `qualified_collision_probe`，且必须
留在 artifact 表中，不进入方法覆盖表。

**2026-05-19 19:01:39 CST controller revision**：18:24 版过于保守，已
修正为 method-inspired controller suite。三类 controller 都进入后续计划：
先做 `qualified_collision_probe`，再做 `capacity_budget_sweep`，最后做
`variable_depth_cost_probe`；第三类是否进入正文取决于结果是否能清楚补强
D5a 叙事。

**2026-05-19 19:01:39 CST controller execution update**：三类
method-inspired controllers 已本地完成。`qualified_collision_probe` 和
`capacity_budget_sweep` 结果清楚，适合作为 artifact-table/finding 支撑；
`variable_depth_cost_probe` 结果可作为 D5a 边界证据，是否进正文待论文
篇幅与叙事裁剪。

**2026-05-20 00:48:02 CST Round 4 paper-sync update**：Round 4 审计意见已
吸收到论文主体与验证脚本，但仍不等于“全部闭环”。Gate 3 口径必须写成
resource-scoped diagnostic separability，不能写原始 downstream Gate 3 passed。
Fig. 1 已变成 pipeline + diagnostic preview，Table 1 是 evidence-only/facet
coverage 表，Table 2 加入 sanity rows、GRID 三 seed 均值/方差、ReSID/category
prefix 的 structural-floor 标注与 same-capacity ablation future caveat，Table 3
是 controlled mechanism probe / diagnostic / baseline / under-probe 表，其中
variable-depth 行使用 max-depth 12,010 vs active 7,914，旧 Table 4 已删除，clean-checkout
verifier 只在 §5 用一句话承接。`tools/verify_paper_artifact.py` 已扩展覆盖
sanity rows、collision probe、capacity sweep、variable-depth probe；当前验证
状态是 paper compile、artifact verifier、unit tests 均通过。Matched-capacity
GRID ablation 尚未跑，保留为 future/caveat；除非重新选择明确 evidence gap，
不再启动本地/GPU实验。若正文继续变化，下一步是重新跑 external simulated
review，而不是扩实验。

**2026-05-20 01:09:23 CST framing decision update**：CIKM v0 明确走
diagnostic/interface resource（Type 4），不走 RecBole/BARS 式 coverage resource
（Type 1）。后续优先改 abstract、§2 adapter specification、§3 worked example
和 controlled mechanism probe 叙事；不要为了 method count 扩实验。自实现
artifact 可以作为 `AUDIT-SID reference implementation` 或 mechanism probe，
但不能冒充 CARD/AdaSID/CapsID 等 named reproduction。详见
`docs/RESOURCE_FRAMING_DECISION.md`。

**2026-05-20 01:34:54 CST terminology update**：当前 paper-facing 术语统一为
diagnostic probes：D1 utilization、D2 aliasing、D3 neighborhood alignment、D4
popularity allocation、D5 structural cost。D6 temporal churn 已有 DACT 本地
refresh-pair smoke，保留为 optional extension evidence；D7 generation traces
需要真实 `generator_outputs`/beam logs，CIKM v0 不做 synthetic D7 实验。详见
`docs/DIAGNOSTIC_PROBE_TAXONOMY.md`。

**2026-05-20 02:17:10 CST title/abstract update**：paper-facing name 改为
`SIDInspector`，标题为 `SIDInspector: A Mapping-First Diagnostic Resource for
Semantic-ID Tokenizers`。不做 repo/global rename：AUDIT-SID 继续作为内部项目名
和历史 artifact/provenance 名。Abstract 改为从缺失 artifact inspection
interface 开场，并保留 23,742、3,749、0.9769、0.9751--0.9769 等 numeric
anchors。

**2026-05-20 16:14:52 CST 17-day lift update**：接受更进取的冲 8/10 路线，
不再把当前状态视为纯 conservative closure。新的 active plan 是
`docs/CIKM_17_DAY_8PT_LIFT_PLAN.md`：B1 把 category-prefix D3 inversion 升级为
主 finding；B2 跑/记录 matched-capacity GRID；B3 仅在 B1/B2 稳定后尝试
D3-vs-ranking context；B4 先做 vertical replication preflight，只有真实 joinable
rows 才进主证据；B5 reference implementation/third method 是 stretch。原则是
更乐观地跑，但只 claim survives-the-gate evidence。

## Purpose

这个 plan 用来把 AUDIT-SID 收敛成 CIKM 2026 Resource Track 可提交版本。核心产物是开源 diagnostic toolkit + stable artifact interface + 小规模 public case study。强 empirical finding 是 stretch goal，不再压过 resource-first 定位。

资源类型冻结：当前版本是 diagnostic / interface resource。GRID/ReSID 是
worked examples，controlled mechanism probes 是诊断敏感性证据；Type 1 覆盖型
resource 是后续平台化路线，不是当前 sprint 的目标。

## CIKM v0 冻结配置

| Component | Decision | Rationale |
|---|---|---|
| Primary dataset | ReSID processed Amazon-2023 `Musical_Instruments` | ReSID 官方 processed dataset + 示例 category，降低数据处理成本 |
| Backup dataset | Amazon 2014 Beauty/Sports | GenRec 支持；如果 ReSID dataset 与 RQ-VAE pipeline 不易对齐时兜底 |
| Preferred method 1 | RQ-VAE / TIGER-style SID | classical semantic-ID baseline |
| Preferred method 2 | ReSID | candidate recent tokenizer innovation, not automatically sufficient |
| Sanity baseline | Random / popularity-balanced / category-prefix ID | 确认 diagnostics 有基本区分度 |
| Alternative recent method | CARD first; DIGER backup; CapsID / AdaSID / AsymRec only if code appears | avoid shallow RQ-VAE + ReSID-only comparison without chasing many new tokenizers |
| Optional extension | DACT / CQ-SID-inspired artifact if cheap | drift or retrieval-facing extension; local DACT artifact smoke passed, but it is not a replacement for the Cluster B main line |
| Must-have diagnostics | D1-D5 | utilization, aliasing, neighborhood alignment, popularity allocation, structural cost |
| Optional diagnostics | D6-D7 | D6 temporal churn already has a DACT refresh-pair smoke; D7 generation traces require real `generator_outputs`/beam logs |
| Portability smoke | MovieLens-1M/25M bounded smoke, half-day max | local-first; only validates non-Amazon toolkit schema; no new tokenizer |

## 未来主 claim

Semantic-ID tokenizer 不能只靠 final Recall@K/NDCG 判断；可复用 diagnostics 能揭示 aliasing risk、neighborhood-alignment mismatch、popularity allocation problem 和 structural-cost pressure。CIKM v0 的 claim 是 toolkit/resource claim，不是新 tokenizer 或大规模 benchmark claim。

## Gate 0：Code And Artifact Feasibility

**Question**：是否能从至少两个公开 tokenizer/recommender implementation 中导出 SID assignments 和 generator outputs？

Tasks：

1. 查找 RQ-VAE/TIGER-style baseline、ReSID、CARD fallback、DIGER backup 或兼容实现；CapsID/AdaSID/AsymRec 只做 public availability check；DACT 只作为 optional extension。
2. 确认每个实现是否能导出：
   - item-to-SID mapping；
   - codebook assignments by level；
   - trained generator scores 或 generated candidates；
   - evaluation predictions。
3. 只做 smoke-level check，不启动完整训练。

Pass condition：

- 至少两个 tokenizer family 能在一个小公开数据集上导出 SID assignments。
- 这两个 family 必须覆盖 **canonical baseline** 和 **recent tokenizer innovation**，不能只是两个同类 quantization 变体。
- 至少一个 D2/D3/D4/D5 diagnostic result 能支撑非冗余 case study，而不是浅层 utilization 表格。

Fail condition：

- 只有一个实现可用，或所有方法都无法导出诊断所需 artifact。
- 只能形成 RQ-VAE + sanity baseline 的弱对比。
- ReSID 或其他 recent method 无法导出可解释 tokenizer artifact。

## Gate 0A：Method Representativeness

**Question**：选中的方法是否足以让社区相信 AUDIT-SID 的诊断资源有价值？

Required layers：

| Layer | Required? | Candidate |
|---|---|---|
| Canonical semantic-ID baseline | yes | RQ-VAE / TIGER / GenRec / GRID-style SID |
| Recent tokenizer/codebook innovation | yes | ReSID / CARD / DIGER; CapsID / AdaSID / AsymRec only if code appears |
| Drift/retrieval extension | no | DACT / CQ-SID-inspired artifact |
| Sanity lower bound | yes | random / popularity-balanced / category-prefix ID |

Pass condition：

- 写出一张 method coverage table；
- 至少一个 recent method 的技术点能对应到 D1-D5 中的诊断轴；
- 诊断结果能解释一个 community-relevant failure mode，如 harmful collision、tail capacity collapse、semantic-collaborative mismatch 或 SID-trie cost pressure。
- 最终 must-run 组合必须覆盖 `Cluster A + Cluster B + sanity lower bound`。

Fail condition：

- 只是“两个 repo 跑通”；
- 只是“ReSID 指标高于 RQ-VAE”；
- 只是 utilization/collision 的浅表统计，没有 case study。
- 只能覆盖 Cluster A，或 Cluster B 方法 artifact 不可解释。

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
2. aliasing profile；
3. neighborhood alignment；
4. popularity allocation；
5. structural cost；
6. temporal churn optional；
7. generation traces optional。

Pass condition：

- D1-D5 能在一个数据集和两个 tokenizer variants 上输出稳定、可解释结果。
- 每个 metric 必须对应一个明确问题：D1 容量利用，D2 aliasing profile，D3 neighborhood alignment，D4 popularity allocation，D5 structural cost。
- “稳定”在 CIKM sprint 中定义为：同一 artifact 重跑指标完全一致；若重新训练 tokenizer，则至少报告 2-3 个 seed 或明确标注 single-artifact case study，不能声称 seed-stable superiority。

## Gate 3：Small Empirical Correlation Check

Bounded study：

- 一个 dataset；
- 两个 tokenizer families；
- 一个 generator backbone；
- 可行时 2-3 seeds；
- 比较 diagnostics 与 Recall@K/NDCG、tail Recall、invalid generation、beam/candidate cost。

Pass condition：

- 至少一个 diagnostic 揭示非冗余差异，或比 aggregate metrics 更早暴露 downstream failure mode / cost pressure。
- 强 surprising finding 只作为 stretch goal；resource paper 只需证明 toolkit 能稳定暴露 reviewer 可理解的 artifact-level failure mode。

## Gate 4：Paper Viability Decision

只有 Gate 3 产生以下任一结果，才进入完整实验：

- diagnostic metric 能跨 tokenizer 预测 downstream performance；
- diagnostic metric 暴露 final Recall@K 相近时隐藏的 failure；
- diagnostics 之间的冲突揭示 regime split，如 head vs tail 或 static vs temporal。
- toolkit interface + Method Coverage Table 足够完整，且 case study 不是 D1-only shallow table。

停止条件：

- diagnostics 只是 final metrics 的平凡复述；
- 可用方法/数据过于脆弱；
- 工作变成维护成本很高但 scientific claim 很弱的 benchmark。

## Strong-Accept Lift Package：8.5 Target

当前版本的接受力主要来自 toolkit/resource value；分数上限来自 method
coverage breadth。下面是可选补强包，不是当前 CIKM external-8 gate 的
blocker。

Closure note: as of 2026-05-19 16:26 CST, this package has been executed as far
as the current public/local evidence allows. L1 is closed negative for v0
because no third named tokenizer has a low-risk faithful export path; L2/L3/L5
are closed with the same-item Musical panel, GRID Musical three-seed stability,
and redesigned Fig. 1. L4 remains a writing task, not a new experiment task.

| Block | Priority | Goal | Minimum success | Stop condition |
|---|---|---|---|---|
| L1 third named tokenizer | HIGH if feasible | 增加一个 B2/B3 真实 named tokenizer artifact | joinable `sid_assignments` + D1/D2/D3/D4/D5 或明确子集 | 只能 proxy/probe 时不进主证据 |
| L2 same-dataset A/B panel | HIGH | 把 Musical 同 item universe 从两行表升级成更强 case panel | GRID feature-text + ReSID + sanity calibration；若 L1 成功则加第三方法 | 不能暗示 faithful TIGER/GRID 或 downstream superiority |
| L3 stability/vertical evidence | MEDIUM | 用已有 3 seed / portability 证明资源不是 toy only | GRID All_Beauty 20k seeds 42/43/44 duplicate-rate range 0.1524--0.1748；MovieLens 只作 schema smoke | ReSID 只有 FAMAE checkpoint、没有 GAOQ mapping 时不算 seed evidence |
| L4 finding sharpening | HIGH | 把 finding 写成 diagnostic insight | 每条 finding 有表/图锚点和 limitation | 只形成“某方法更好”的 leaderboard 叙事 |
| L5 Fig. 1 redesign | HIGH | 提升 resource-paper 10 秒可读性 | artifact contract + D1-D5/D6/D7 boundary + evidence maturity | 变成装饰性流程图 |

Candidate findings:

1. Collision-free capacity and collaborative-prefix alignment are not the same
   objective.
2. Same-item GRID feature-text vs ReSID exposes capacity/collision pressure
   that final Recall/NDCG alone would not localize.
3. Prefix-depth diagnostics matter: a method/control can look reasonable at
   depth 1 while collapsing at deeper prefix recall.

Run order:

1. Redraw Fig. 1 from the current evidence contract; this is local and cheap.
2. Use `docs/METHOD_DIAGNOSTIC_SELECTION_MATRIX.md` to screen B2/B3 candidate
   repos for a real item-to-SID export; stop if only proxy evidence is
   available.
3. If a third real method is found, run local bounded export first; use AutoDL
   only after source/import/adapter smoke passes.
4. Upgrade Table 2 or add an artifact-panel table only after the method evidence
   is real and joinable.
5. Run a new strict claim audit before any external re-review.

## Controlled Mechanism Probe Policy

Status: selected, executed, and paper-integrated in
`docs/PAPER_CONTROLLER_INTEGRATION.md`.

Controlled mechanism probes are not a replacement for a third official named
tokenizer. Their job is narrower: check whether AUDIT-SID diagnostic probes
react to known method-family failure modes under controlled inputs. They are
inspired by collision qualification, adaptive capacity, and long/variable SID
concerns in the literature, but they are not implementations of unreleased
named methods.

Mechanism-probe run order:

| Order | Probe | Method-family concern | Diagnostics | Output | Paper decision |
|---:|---|---|---|---|---|
| 1 | `qualified_collision_probe` | collision qualification / harmful conflict | D2b, D3 | `docs/QUALIFIED_COLLISION_PROBE.md`, `paper_assets/tables/table8_qualified_collision_probe.csv` | high priority; strong artifact-table/finding support |
| 2 | `capacity_budget_sweep` | adaptive capacity / capacity pressure | D1, D2, D4, D5 | `docs/CAPACITY_BUDGET_SWEEP.md`, `paper_assets/tables/table9_capacity_budget_sweep.csv` | high priority; strong artifact-table/finding support |
| 3 | `variable_depth_cost_probe` | variable/long SID interface cost | D4, D5, D7-boundary | `docs/VARIABLE_DEPTH_COST_PROBE.md`, `paper_assets/tables/table10_variable_depth_cost_probe.csv` | used as compact D5 boundary evidence, not D7 coverage |

2026-05-19 19:34 CST writing update:

- All three mechanism-probe results are now integrated into
  `paper/sections/4_demonstration.tex` as controlled mechanism evidence.
- `docs/PAPER_CONTROLLER_INTEGRATION.md` records the claim boundary:
  mechanism-probe rows support diagnostic interpretation but do not add
  named-method coverage.
- No additional local or GPU experiment is required from the mechanism-probe suite
  before the next paper claim audit.

Existing generic calibration rows remain useful but secondary:

- `sanity_mod_collision_hash`;
- `sanity_category_prefix`;
- `sanity_popularity_balanced`.

They should be kept as sanity/calibration rows and not presented as the
controlled mechanism probe suite.

2026-05-19 15:58 CST execution update:

- B2/B3 screen completed in `docs/B2_B3_METHOD_SCREEN.md`. No third named
  tokenizer is safe for main evidence from the current public/local state:
  QuaSID/AdaSID/CapsID are paper/motivation only, DIGER is incomplete for
  artifact export, and CARD is proxy/control unless the original `nu-rq-vae`
  path is repaired and reviewed.
- Same-dataset lift continued locally instead of waiting for GPU:
  `docs/GRID_MUSICAL_3SEED_LOCAL.md` adds GRID Musical feature-text seeds
  42/43/44. All three seeds have complete joins; duplicate SID rate is
  0.8327--0.8421 and full-collision rate is 0.9751--0.9769.
- Next paper-facing action should use this as stability support for the
  same-item Musical panel, not as a stronger method-superiority claim.

## Optional D6：DACT Drift Artifact Smoke

Status: `LOCAL_SMOKE_PASSED_OPTIONAL_D6`。

Evidence:

- report: `docs/DACT_DRIFT_SMOKE.md`；
- artifacts: `_gate0_artifacts/dact_tools_smoke/`；
- tool: `tools/autodl_audit_sid/compute_sid_churn.py`；
- smoke runner: `tools/autodl_audit_sid/run_dact_artifact_smoke.py`。

Current result:

- DACT bundled `Tools` 0.6 -> 0.7 common-item SID churn is
  `2271 / 9610 = 0.236316` at every prefix depth.
- 0.7 has `3` full-collision groups / `6` full-collision items, duplicate SID
  rate `0.000303`.
- 0.7 adds `275` new item rows relative to the 0.6 code array under the
  normalized integer item-id convention.

Interpretation:

- This is useful optional drift/continual-tokenization artifact evidence.
- It should be used only as an optional D6 demonstration if the paper has room.
- It does not replace the main B route: ReSID remains the current named recent
  tokenizer/codebook evidence, and CARD/DIGER remain fallback/backlog.

## Portability Smoke：MovieLens

Status: `LOCAL_SMOKE_PASSED_NON_AMAZON_SCHEMA`。

Evidence:

- report: `docs/MOVIELENS_PORTABILITY_SMOKE.md`；
- runner: `tools/autodl_audit_sid/run_movielens_portability_smoke.py`；
- artifacts: `_gate0_artifacts/movielens_portability_smoke/ml25m_1mratings_10kitems/`。

Current result:

- Local MovieLens-25M bounded slice: first `1,000,000` ratings rows and `10,000`
  movie items.
- Sanity baselines have complete joins: `metadata_without_sid=0`,
  `interaction_without_sid=0` for all three sanity methods.
- D1-D5 and D3 run unchanged on movie title/genre metadata and ratings
  interactions.

Interpretation:

- This validates the toolkit input contract beyond Amazon schemas.
- It must not become a main tokenizer benchmark or recommender-quality claim.
- AutoDL/GPU is not needed for this portability check.

## CIKM v0 Package If Gates Pass

Datasets：

- ReSID processed Amazon-2023 `Musical_Instruments`；
- Amazon 2014 Beauty/Sports optional backup only。
- MovieLens-1M optional portability smoke only if Gate 0 is already stable。

Methods：

- RQ-VAE/TIGER-style baseline；
- ReSID or another recent tokenizer innovation that passes Gate 0A；
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
- Method Coverage Table；
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
| 2026-05-18 | public code availability screen + review absorption | `docs/EXTERNAL_REVIEW_ABSORPTION.md` | sprint priorities frozen |
| 2026-05-19 | ReSID + GRID/RQ-VAE repo audit; CARD fallback only if needed | `docs/GATE0_REPO_AUDIT.md` | continue only if mappings exportable |
| 2026-05-19 | method representativeness audit | `docs/METHOD_REPRESENTATIVENESS_AUDIT.md` | continue only if methods cover canonical + recent tokenizer innovation |
| 2026-05-19 | toolkit interface skeleton | `src/audit_sid/interface.py` | adapters must target this schema |
| 2026-05-20 | dataset schema audit | `docs/DATASET_SCHEMA_AUDIT.md` | freeze primary dataset |
| 2026-05-21 | first SID mapping export | artifact sample | freeze input schema |
| 2026-05-22 | second SID mapping export | artifact sample | Gate 0 likely pass |
| 2026-05-23 | D1-D5 metrics v0 | diagnostic table | decide if case study exists |
| 2026-05-24 | formal Gate 0 | `docs/GATE0_DECISION.md` | go/no-go for CIKM |
| 2026-05-28 | paper tables/figures | diagnostic case study | submit-ready evidence |
| 2026-05-30 | CIKM abstract | EasyChair abstract | must submit |
| 2026-06-06 | CIKM resource paper | 4-page paper + artifact | final submission |

## Current Submission-Hygiene Status (2026-05-20 13:36 CST)

- Experiments are closed for the conservative CIKM Resource v0 framing unless a
  new explicit evidence gap is selected.
- Paper-facing terminology is now `SIDInspector` with D1-D5 diagnostic probes:
  utilization, aliasing, neighborhood alignment, popularity allocation, and
  structural cost. D6 remains optional temporal churn evidence; D7 remains a
  generator-trace hook.
- Legacy code and CSV names are preserved for provenance compatibility rather
  than renamed in place.
- Latest verification: Fig. 1 regeneration, paper table rebuild, public
  verifier, 16 unit tests, `git diff --check`, and `paper/main.pdf` compile
  all pass.
- Remaining non-experiment work: real single-blind author metadata, citation
  drift check, and final strict claim audit after any later paper edits.
- Naming is now `SIDInspector` for active paper-facing files; AUDIT-SID remains
  the repository/provenance name. Final artifact URL/tag freeze is pending the
  next submission-ready commit.
