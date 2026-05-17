# Public OPE Preflight Experiment Tracker

| ID | Task | Status | Evidence / Output | Notes |
|---|---|---|---|---|
| P000 | Create public OPE branch | DONE | `codex/public-ope-preflight` | Empty repo initialized as a research branch. |
| P001 | Invoke idea-discovery skill | DONE | Codex meta logger best-effort call | Scope narrowed to public OPE preflight. |
| P002 | Create private GitHub repo and track branch | DONE | `git@github.com:jdding/lifecycle-ope-preflight.git`, `origin/codex/public-ope-preflight` | `gh` was unavailable; repo created through GitHub UI and pushed over SSH. |
| P003 | Align project outputs with ARIS skill protocol | DONE | `AGENTS.md`, `MANIFEST.md`, `findings.md`, second-level timestamped artifacts | Fixed initial lightweight formatting drift after user correction. |
| P010 | Draft research brief | DONE | `RESEARCH_BRIEF.md` | Defines two-stage public then production strategy. |
| P020 | Draft idea report | DONE | `idea-stage/IDEA_REPORT.md` | Ranks lifecycle-stratified OPE protocol first. |
| P021 | Expand public-data idea report | DONE | `idea-stage/IDEA_REPORT_20260517_222854.md` | Generated 10 concrete ideas and selected top 3 novelty-check candidates: lifecycle credibility protocol, lifecycle-conservative policy selection, lifecycle-targeted exploration budget. |
| P021A | Reconstruct literature review | DONE | `idea-stage/LITERATURE_REVIEW.md`, `idea-stage/LITERATURE_REVIEW_20260517_223308.md` | Restored missing `/research-lit` evidence chain before relying on downstream plans. |
| P022 | Strict novelty check for top 3 ideas | DONE | `refine-logs/NOVELTY_CHECK.md`, `refine-logs/NOVELTY_CHECK_20260517_224105.md` | Verdict: Idea 1 PROCEED as protocol/resource only; Idea 2 CAUTION as group-constrained LCB selection risk; Idea 3 CAUTION as simulator/logging-design module. |
| P023 | Align idea report after novelty gate | DONE | `idea-stage/IDEA_REPORT.md` | Added post-novelty decision, then superseded resource-only direction with method-first rethink. |
| P030 | Draft experiment plan | GATED | `refine-logs/EXPERIMENT_PLAN.md`, `refine-logs/EXPERIMENT_PLAN_20260517_225333.md` | Rewritten as method-first feasibility preflight; final claim-driven plan waits for Gate A schema audit and method-support check. |
| P031 | Delete misleading early plan snapshots | DONE | removed early idea/plan/tracker snapshots and protocol-only plan snapshot | Avoids carrying pre-literature/pre-novelty or resource-first artifacts into later work. |
| P032 | Rethink direction after resource-only concern | DONE | `refine-logs/METHOD_DIRECTION_RETHINK.md`, `refine-logs/METHOD_DIRECTION_RETHINK_20260517_225333.md` | Pivot recommendation: lifecycle-adaptive shrinkage DR as method route; protocol becomes diagnostic layer. |
| P033 | Reassess dormant/lifecycle topic from research wiki | DONE | `refine-logs/DORMANT_TOPIC_REASSESSMENT.md`, `refine-logs/DORMANT_TOPIC_REASSESSMENT_20260518_005053.md` | Verdict: do not continue OPE as mainline; prioritize preference evidence validity / lifecycle transition decision problem if workspace is upgraded. |
| P040 | Dataset feasibility matrix | DONE | `docs/PUBLIC_DATASETS.md` | First-pass public dataset role and readiness labels drafted. |
| P050 | OBP estimator API smoke | PAUSED | TBD | Paused until user decides whether to upgrade away from OPE mainline. |
| P060 | KuaiRand lifecycle-state feasibility | PAUSED | TBD | Paused until reassessment review; may be reused for lifecycle-transition idea discovery. |
| P070 | KuaiRec oracle stress-test design | PAUSED | TBD | Paused until reassessment review; may be reused for deployable-support stress tests. |
| P080 | MIND strict-OPE limitation note | PAUSED | TBD | Keep limitation, but do not advance OPE-specific work now. |

## Current Decision

Pause the OPE preflight as the mainline. The wiki-grounded reassessment says the better next problem is not public OPE, but preference evidence validity / lifecycle transition decision under stale, sparse, and conflicting evidence.

Before any dataset gate or experiment, review `refine-logs/DORMANT_TOPIC_REASSESSMENT.md` and decide whether to upgrade the workspace into a dormant/lifecycle reassessment branch. If yes, the next artifact should be a new idea report focused on preference evidence validity, lifecycle transition decision policy, and deployable support conversion beyond CASP.
