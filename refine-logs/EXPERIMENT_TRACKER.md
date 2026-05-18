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
| A090 | Venue plan | DONE | `docs/AUDIT_SID_VENUE_PLAN.md`, `docs/AUDIT_SID_VENUE_PLAN_20260518_133645.md` | Immediate target changed to CIKM 2026 Resource Track; abstract May 30, paper Jun 6. |
| A095 | CIKM execution spec | DONE | `docs/AUDIT_SID_CIKM_EXECUTION_SPEC.md`, `docs/AUDIT_SID_CIKM_EXECUTION_SPEC_20260518_135256.md` | Freezes dataset/method/diagnostic scope for 4-page resource paper. |
| A096 | Method representativeness correction | DONE | `docs/AUDIT_SID_CIKM_EXECUTION_SPEC.md`, `refine-logs/EXPERIMENT_PLAN.md` | RQ-VAE + ReSID are no longer treated as automatically sufficient; Gate 0A added. |
| A097 | SID method cluster audit | DONE | `docs/SID_METHOD_CLUSTER_AUDIT.md`, `docs/SID_METHOD_CLUSTER_AUDIT_20260518_144128.md` | Initial cluster audit added. Superseded by A099 because old B/C boundary was not useful. |
| A098 | Method representativeness audit framework | DONE | `docs/METHOD_REPRESENTATIVENESS_AUDIT.md`, `docs/METHOD_REPRESENTATIVENESS_AUDIT_20260518_145445.md` | Adds cluster x diagnostic mapping, method x diagnostic feasibility template, and Gate 0A scoring. |
| A099 | Merge weak B/C method clusters | DONE | `docs/SID_METHOD_CLUSTER_AUDIT.md`, `docs/METHOD_REPRESENTATIVENESS_AUDIT.md` | Old B/C split collapsed into Cluster B recent tokenizer/codebook innovation with B1/B2/B3 facets. Must-run is now Cluster A + Cluster B + sanity lower bound. |
| A099A | Unified project spec | DONE | `docs/PROJECT_SPEC.md`, `docs/PROJECT_SPEC_20260518_151326.md` | Consolidates project thesis, non-goals, method coverage, artifact interface, diagnostics, gates, and timeline. |
| A100 | Gate 0 code/artifact feasibility | PENDING | TBD | Must pass by 2026-05-24 for CIKM 2026 submission. |
| A100A | Gate 0A method representativeness | PENDING | TBD | Must show canonical baseline + recent tokenizer innovation + sanity baseline; otherwise no CIKM submission. |
| A101 | ReSID repo artifact audit | TODO | TBD | Confirm item-to-SID export path and processed Amazon-2023 dataset usability. |
| A102 | GenRec/RQ-VAE artifact audit | TODO | TBD | Confirm RQ-VAE/TIGER-style item-to-SID export path. |
| A103 | Dataset schema audit | TODO | TBD | Primary: ReSID processed Amazon-2023 Musical_Instruments; backup: Amazon 2014 Beauty/Sports. |
| A104 | D1-D4 metric implementation | TODO | TBD | Utilization, collision harm, semantic-collaborative alignment, head-tail capacity. |

## Current Decision

Proceed only to Gate 0 feasibility:

> verify whether at least two public SID/tokenizer implementations can export item-to-SID mappings and generator outputs on one small public dataset.

Do not launch full experiments until Gate 0 and dataset support audit pass.

Venue direction: target CIKM 2026 Resource Track now, because it is the nearest track that explicitly accepts resource/protocol/software/evaluation-tool work. Abstract deadline is 2026-05-30 AoE and paper deadline is 2026-06-06 AoE. Gate 0 must pass by 2026-05-24; otherwise do not force a weak submission.

Frozen CIKM v0 scope: primary dataset is ReSID processed Amazon-2023 `Musical_Instruments`; backup dataset is Amazon 2014 Beauty/Sports. Must-run methods are RQ-VAE/TIGER-style SID, ReSID, and a sanity ID baseline. Must-have diagnostics are D1 utilization, D2 collision harm, D3 semantic-collaborative alignment, and D4 head-tail capacity allocation.

Correction: RQ-VAE/TIGER-style SID plus ReSID is only a preferred candidate pair, not automatically sufficient. Gate 0A must verify method representativeness. If the resulting comparison is shallow or does not cover a recent tokenizer innovation in a meaningful way, abandon CIKM 2026 rather than submitting a weak resource paper.

Cluster-first rule updated: must-run coverage is Cluster A canonical SID + Cluster B recent tokenizer/codebook innovation + sanity lower bound. Old Cluster B/C split is deprecated because it did not provide useful decision separation. The next artifact remains Gate 0A repo/artifact evidence, not a training launch.

Update: `docs/METHOD_REPRESENTATIVENESS_AUDIT.md` now exists as the Gate 0A framework. The next concrete artifact should fill the tables with real repo/artifact evidence.
