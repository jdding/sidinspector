# Public OPE Preflight Experiment Tracker

| ID | Task | Status | Evidence / Output | Notes |
|---|---|---|---|---|
| P000 | Create public OPE branch | DONE | `codex/public-ope-preflight` | Empty repo initialized as a research branch. |
| P001 | Invoke idea-discovery skill | DONE | Codex meta logger best-effort call | Scope narrowed to public OPE preflight. |
| P002 | Create private GitHub repo and track branch | DONE | `git@github.com:jdding/lifecycle-ope-preflight.git`, `origin/codex/public-ope-preflight` | `gh` was unavailable; repo created through GitHub UI and pushed over SSH. |
| P010 | Draft research brief | DONE | `RESEARCH_BRIEF.md` | Defines two-stage public then production strategy. |
| P020 | Draft idea report | DONE | `idea-stage/IDEA_REPORT.md` | Ranks lifecycle-stratified OPE protocol first. |
| P030 | Draft experiment plan | DONE | `refine-logs/EXPERIMENT_PLAN.md` | Public-data run order and stop rules. |
| P040 | Dataset feasibility matrix | DONE | `docs/PUBLIC_DATASETS.md` | First-pass public dataset role and readiness labels drafted. |
| P050 | OBP estimator API smoke | TODO | TBD | No dataset download yet. |
| P060 | KuaiRand lifecycle-state feasibility | TODO | TBD | Needs schema inspection. |
| P070 | KuaiRec oracle stress-test design | TODO | TBD | Needs schema inspection. |
| P080 | MIND strict-OPE limitation note | TODO | TBD | Should not be used for strict IPS/DR claim without propensity. |

## Current Decision

Proceed with public research preflight first. Treat later production validation as a separate stage that requires logging-policy provenance, candidate sets, propensities or reconstructable randomization, and A/B or gray-release ground truth.
