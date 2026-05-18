# AUDIT-SID Idea-Discovery Tracker

| ID | Task | Status | Evidence / Output | Notes |
|---|---|---|---|---|
| A000 | Create AUDIT-SID branch | DONE | `codex/audit-sid-idea-discovery` | New investigation branch separated from closed OPE/lifecycle branches. |
| A001 | Invoke `/idea-discovery` protocol | DONE | Codex meta logger best-effort call | Topic: `audit-sid-diagnostic-framework-public-first`. |
| A002 | Run memory preflight | DONE | `status=checked`, no prior failures found | No negative run memory specific to AUDIT-SID. |
| A010 | Write research brief | DONE | `RESEARCH_BRIEF.md`, `RESEARCH_BRIEF_20260518_131939.md` | Public-first diagnostic framing, no Huawei internal data. |
| A020 | Run literature survey | DONE | `idea-stage/LITERATURE_REVIEW.md`, `idea-stage/LITERATURE_REVIEW_20260518_131939.md` | Main signal: tokenizer/codebook is now a method bottleneck; diagnostic gap exists. |
| A030 | Generate and rank ideas | DONE | `idea-stage/IDEA_REPORT.md`, `idea-stage/IDEA_REPORT_20260518_131939.md` | Top idea: AUDIT-SID diagnostic suite; pure leaderboard abandoned. |
| A040 | Strict novelty check | DONE | `refine-logs/NOVELTY_CHECK.md`, `refine-logs/NOVELTY_CHECK_20260518_131939.md` | Verdict: 7/10, proceed with caution. |
| A050 | Critical review | DONE | `refine-logs/REVIEW_SUMMARY.md`, `refine-logs/REVIEW_SUMMARY_20260518_131939.md` | Main risk: reviewer sees it as benchmark engineering unless diagnostic claims are sharp. |
| A060 | Refine proposal | DONE | `refine-logs/FINAL_PROPOSAL.md`, `refine-logs/FINAL_PROPOSAL_20260518_131939.md` | Final thesis: representation-to-deployment diagnostics for SID tokenizers. |
| A070 | Draft gated experiment plan | DONE | `refine-logs/EXPERIMENT_PLAN.md`, `refine-logs/EXPERIMENT_PLAN_20260518_131939.md` | Gate 0 is code/artifact feasibility, not training. |
| A080 | Pipeline summary | DONE | `refine-logs/PIPELINE_SUMMARY.md`, `refine-logs/PIPELINE_SUMMARY_20260518_131939.md` | AUDIT-SID is public-first Top-1 methodology line. |

## Current Decision

Proceed only to Gate 0 feasibility:

> verify whether at least two public SID/tokenizer implementations can export item-to-SID mappings and generator outputs on one small public dataset.

Do not launch full experiments until Gate 0 and dataset support audit pass.
