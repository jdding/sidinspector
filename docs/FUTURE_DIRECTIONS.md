# Future Direction Notes

**Generated**: 2026-05-18 01:53:42 CST
**Purpose**: record post-closeout directions so they do not remain only in chat.

## 1. TOIS 5+1 Journal Synthesis

**Status**: highest-confidence next academic workstream, but should wait for AC outcomes.

**Target**: TOIS.

**Reasoning**:

- The existing 5+1 portfolio already has a coherent arc: temporal staleness, semantic/attribute support, support-not-deployment, source-protected net utility, and multi-proxy audit.
- TOIS is more suitable than a short-method venue because the value is topic-level synthesis, problem formulation, method family comparison, and evaluation methodology.
- This should be an independent branch, not a continuation of the OPE or lifecycle-transition exploration branches.

**Provisional title frame**:

> Dormant-Return Recommendation: From Temporal Staleness to Deployable Support Conversion

**Start condition**:

- Wait for multiple 5+1 AC/review outcomes.
- Then decide whether the journal article is a synthesis/extension, a long version, or a reframed survey-plus-methodology paper.

## 2. Device-Switch Return Recommendation

**Status**: Top-1 new method direction when TOIS synthesis is excluded from ranking; internal-data-first, not public-only.

**Scenario**:

Users leave the Huawei ecosystem, switch to another device/ecosystem, and later return to Huawei. This is not ordinary cold-start and not ordinary dormant-return. It is a re-entry problem after ecosystem switching.

**Academic framing**:

> Return-to-platform recommendation after device/ecosystem switching.

**Why it may have academic value**:

- **Stale identity evidence**: old Huawei-side behavior may be partially valid but cannot be trusted wholesale.
- **Ecosystem transition**: device and ecosystem changes alter app usage, content preference, service intent, and purchase context.
- **Restart policy**: the recommender must decide whether to use old preferences, safe popular content, device-context priors, or early-session probing.
- **Industrial uniqueness**: public datasets rarely contain reliable "switch out and switch back" traces, while Huawei Terminal Cloud may observe this pattern in production.

**Possible research question**:

> How should a recommender restart personalization for users returning after device/ecosystem switching when historical platform evidence is stale but not empty?

**Method possibilities**:

- evidence validity estimation for old platform behavior;
- device/context-conditioned restart policy;
- early-session probing under retention risk;
- old-vs-current preference conflict diagnostics.
- adaptive semantic evidence tokenization: use the current `semantic ID / tokenizer / codebook` trend as a representation tool for re-entry evidence, rather than entering the generic SID race directly.

**Key risk**:

This direction requires internal data, compliance review, and a publishable abstraction of device-switch state. Without that, it will collapse into cold-start or dormant-return variants.

**Updated ranking note, excluding TOIS**:

After the 2026-05-18 paper-watch trend validation, this becomes the recommended Top-1 new direction:

> Device-switch return recommendation with adaptive semantic evidence tokenization.

The reason is that it combines a real external trend (`semantic ID / tokenizer / codebook`) with a rare internal scenario where this project has a defensible edge. The trend should be used to strengthen the switch-back recommendation problem, not to start a generic generative-retrieval paper.

## 3. LLM-Assisted Recommendation System Operations

**Status**: promising separate topic, but the first viable version should be narrowed from end-to-end RecOps to a Ranking Experiment Agent.

**Where the idea came from**:

This idea did not come from dormant-return mechanics. It came from combining three facts:

1. The user works on recommendation system architecture in industry, so the strongest unique asset may be production workflow, not only ranking models.
2. LLM4Rec is crowded with direct-ranker, conversational recommender, and recommender-agent papers. Many are weak because they show demos or benchmark gains without production workflow grounding.
3. Recommendation teams spend large effort on experiment diagnosis, policy-change review, metric regression analysis, launch decisions, and incident memory. These are high-value RecOps tasks where LLMs can help without pretending to be the recommender model.

The initial proposed angle was:

> LLM-assisted RecOps: using LLM agents to improve recommendation experiment operations, diagnosis, policy auditing, and launch decisions.

After reviewing Meta's Ranking Engineer Agent (REA), the better first paper/workstream should be narrower:

> Ranking Experiment Agent: a long-running, budgeted, human-approved ML engineering agent for ranking-model experiment planning, execution, failure handling, result analysis, and iteration.

This is not an online serving agent and not a recommender ranker. It lives in the offline/nearline model-development loop.

### REA-Informed Reframe

Meta REA is important because it validates the workflow shape:

- planner/executor split;
- hypothesis generation from historical experiment knowledge and research knowledge;
- human-approved compute budgets;
- multi-day hibernate-and-wake execution;
- automated training launch, failure debugging, metric analysis, and iteration.

The lesson is not "let an LLM invent models." The lesson is:

> autonomous ML engineering only becomes credible when it is wrapped in state machines, experiment memory, scheduler integration, failure runbooks, budget gates, and human approval.

Therefore the first Huawei-style version should target **ranking experiment automation**, not full RecOps decision automation.

**What not to do**:

- Do not build an LLM ranker.
- Do not write another generic "LLM for recommendation" survey/application.
- Do not make a chatbot demo that recommends items.
- Do not claim model-quality improvements without production-style operational tasks.

**Concrete idea candidates**:

### A0. Ranking Experiment Agent

Input: current ranking model config, experiment objective, historical experiment cards, available compute budget, training platform constraints, and evaluation protocol.

Output: a budgeted experiment plan, generated config diffs, launched training jobs, monitored failures, analyzed metrics, and a structured next-step recommendation.

Required modules:

- Planner: hypothesis generator, historical experiment retrieval, research/paper retrieval, budgeted plan.
- Executor: config writer, training launcher, log monitor, failure debugger, result analyzer.
- Memory: experiment DB, failure runbook, model/dataset registry, previous decisions.
- Governance: permission gate, GPU budget gate, CI/config validation gate, offline metric gate, human approval gate.

Minimum viable version:

1. Read configs, logs, and metric tables.
2. Generate a next-round experiment plan.
3. Write config only; do not edit core model code.
4. Launch training through the existing scheduler.
5. Detect OOM, NaN, loss explosion, non-learning, and infra failure.
6. Summarize results into experiment cards.
7. Recommend continue / stop / combine / abandon.

Measurable tasks:

- valid-plan rate under budget;
- config correctness;
- failed-run recovery rate;
- experiment report accuracy;
- manual engineer time saved;
- improvement in successful experiment throughput.

This is now the recommended entry point before broader RecOps.

### A. Metric Regression Investigator

Input: A/B results, metric deltas, bucket analysis, strategy diff, traffic configuration, and known historical incidents.

Output: ranked root-cause hypotheses, required SQL/log checks, and a decision tree for confirmation.

Measurable tasks:

- root-cause recall@K;
- diagnosis time reduction;
- false-hypothesis rate;
- agreement with senior engineer postmortems.

### B. Recommendation Policy Change Auditor

Input: policy diff, launch config, affected modules, offline metrics, bucket risks.

Output: pre-launch risk report, affected user/source segments, missing guardrails, rollback triggers.

Measurable tasks:

- risky-change detection accuracy;
- missed guardrail rate;
- reviewer agreement;
- reduction in launch-review time.

### C. Experiment-to-Decision Agent

Input: offline metrics, online A/B metrics, confidence intervals, guardrail metrics, known business constraints.

Output: structured decision: ship, rollback, extend test, split by segment, or request follow-up experiment.

Measurable tasks:

- decision consistency with expert panel;
- calibration of uncertainty;
- number of avoidable follow-up experiments reduced;
- false ship / false rollback rate.

### D. RecSys Incident Memory Agent

Input: historical experiments, incidents, postmortems, strategy changes, metric anomalies.

Output: similar prior cases, likely causes, relevant dashboards/logs, and tested fixes.

Measurable tasks:

- retrieval accuracy for relevant incidents;
- time-to-first-useful-cause;
- postmortem coverage;
- engineer acceptance rate.

**Likely paper positioning**:

- Not "LLM improves recommendation ranking."
- Instead: "LLM agents for recommendation system operations."
- Stronger if framed as an evaluation benchmark plus agent workflow on real or anonymized production-style incidents.

**Main risk**:

Reviewers may call it engineering unless the task suite, metrics, and baselines are rigorous. The paper needs a clear benchmark or logged workflow evaluation, not just a system description.

## Recommendation After Closeout

Do not start experiments in this repo.

Recommended sequencing:

1. Close and archive current exploratory branches.
2. Prepare a separate TOIS synthesis branch when review/AC information is available.
3. Separately assess internal data feasibility for device-switch return recommendation; when excluding TOIS, this is the current Top-1 new method direction.
4. If exploring LLM-assisted RecOps, start with a Ranking Experiment Agent task definition and experiment-memory schema, not an e2e operations copilot.
