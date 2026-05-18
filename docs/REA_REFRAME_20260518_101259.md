# REA-Informed Reframe For LLM-Assisted RecOps

**Generated**: 2026-05-18 10:12:59 CST
**Purpose**: refine the LLM-assisted RecOps direction after reviewing Meta Ranking Engineer Agent (REA).

## Verdict

Meta REA changes the recommended scope. The first viable direction should not be an end-to-end RecOps copilot. It should be:

> Ranking Experiment Agent: a long-running, budgeted, human-approved ML engineering agent for ranking-model experiment planning, execution, failure handling, result analysis, and iteration.

This is closer to Meta REA and more immediately measurable than broad policy auditing, incident memory, and launch-decision automation.

## Interpretation Of REA

REA is not an online ranking or serving agent. It is an autonomous ML engineering agent for the ranking model development loop:

- generate hypotheses;
- create experiment plans;
- write configs or code changes;
- launch training;
- monitor failures;
- analyze metrics;
- continue iteration across multi-day workflows.

The key technical lesson is not "LLM writes code." The key lesson is:

> agentic ML experimentation needs persistent state, experiment memory, scheduler integration, hibernate-and-wake execution, failure runbooks, budget gates, and human approval.

## Corrected Scope

Earlier RecOps framing included diagnosis, policy audit, incident memory, and launch decision. That remains useful, but it is too broad for a first paper or first system.

The better sequencing is:

1. **Ranking Experiment Agent**: offline/nearline experiment automation.
2. **Metric Regression Investigator**: post-experiment diagnosis.
3. **Policy Change Auditor**: pre-launch risk review.
4. **Experiment-to-Decision Agent**: ship/rollback/extend recommendation.
5. **Incident Memory Agent**: historical case retrieval and postmortem support.

Only the first step should be treated as the immediate candidate.

## Proposed Architecture

```text
Ranking Experiment Agent
├── Planner
│   ├── Hypothesis Generator
│   ├── Historical Experiment RAG
│   ├── Research / Paper RAG
│   └── Budgeted Experiment Plan
├── Executor
│   ├── Config Writer
│   ├── Training Launcher
│   ├── Log Monitor
│   ├── Failure Debugger
│   └── Result Analyzer
├── Memory
│   ├── Experiment DB
│   ├── Failure Runbook
│   ├── Model / Dataset Registry
│   └── Prior Decisions
└── Governance
    ├── Permission Gate
    ├── GPU Budget Gate
    ├── CI / Config Validation Gate
    ├── Offline Metric Gate
    └── Human Approval Gate
```

## Minimum Viable Version

The first version should be config-only and human-approved:

1. Read ranking model configs, training logs, and metric tables.
2. Generate next-round experiment plans with explicit hypothesis and budget.
3. Write config diffs, not core model code.
4. Launch training through the existing scheduler.
5. Detect common failures: OOM, NaN, loss explosion, non-learning, infra failure.
6. Summarize each run into an experiment card.
7. Recommend continue / stop / combine / abandon.

Do not allow automatic production launch, direct trunk edits, or unbounded compute.

## Experiment Memory Schema

Minimum fields:

- experiment id;
- model family;
- dataset / traffic segment;
- config diff;
- code commit;
- training budget;
- launch time and completion status;
- offline metrics;
- guardrail metrics;
- cost;
- failure reason;
- human conclusion;
- follow-up decision;
- whether merged or deployed.

Without this structure, the agent will degrade into generic advice.

## Evaluation Tasks

### T1: Experiment Plan Quality

Given a model state, objective, budget, and historical cards, generate the next experiment plan.

Metrics:

- expert preference;
- valid-plan rate;
- budget compliance;
- duplicate-experiment avoidance;
- hypothesis specificity.

### T2: Config Generation Correctness

Given an approved plan, generate valid config diffs.

Metrics:

- config parse success;
- static validation pass rate;
- scheduler submission success;
- unintended-field-change rate.

### T3: Failure Diagnosis And Recovery

Given failed training logs, classify failure and propose recovery.

Metrics:

- failure classification accuracy;
- recovery success rate;
- time to diagnosis;
- false method-failure attribution rate.

### T4: Result Analysis And Next-Step Decision

Given completed runs and metrics, recommend continue / stop / combine / exploit.

Metrics:

- agreement with senior engineers;
- false continue rate;
- false stop rate;
- report factuality;
- metric-grounding completeness.

## Research Contribution Shape

A credible paper should not claim "LLM improves ranking." It should claim:

1. a recommender/ranking experiment automation task suite;
2. a persistent planner-executor architecture with memory and guardrails;
3. evidence that the system improves experiment throughput, failure recovery, and report quality under bounded compute;
4. an ablation showing that historical experiment memory and runbooks matter.

## Risks

- If the experiment DB is weak, the planner will produce generic suggestions.
- If metrics are not standardized, the agent will misread results.
- If budget gates are missing, the agent wastes compute.
- If failure runbooks are shallow, failures will be misclassified as method failures.
- If evaluation is only a demo, reviewers will call it engineering.

## Recommendation

If this direction is pursued, start with a feasibility audit:

1. Are there 50-200 historical ranking experiments that can be turned into experiment cards?
2. Is there a scheduler/API path for config-only training launch?
3. Are common failure logs accessible and labelable?
4. Can senior engineers label gold decisions for 30-50 cases?
5. Can the work be anonymized into a publishable benchmark or at least an industry-track case study?

If these are not true, postpone the direction.
