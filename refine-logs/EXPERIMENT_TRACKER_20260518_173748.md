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
| A099B | External review absorption | DONE | `docs/EXTERNAL_REVIEW_ABSORPTION.md`, `docs/EXTERNAL_REVIEW_ABSORPTION_20260518_160032.md` | Resource-first sprint locked: strong finding is stretch, D5a required-light, toolkit interface required, Cluster B public-code screen added. |
| A099C | Public Cluster B code availability screen | DONE | `docs/METHOD_REPRESENTATIVENESS_AUDIT.md` | ReSID first, CARD fallback, DIGER backup; CapsID/AdaSID/AsymRec future-only unless code appears; DRIL removed as standalone candidate. |
| A099D | Toolkit interface skeleton | DONE | `src/audit_sid/interface.py` | Minimal schema contract for `sid_assignments`, `item_metadata`, `interactions`, and optional `generator_outputs`. |
| A100 | Gate 0 code/artifact feasibility | PENDING | TBD | Must pass by 2026-05-24 for CIKM 2026 submission. |
| A100A | Gate 0A method representativeness | PARTIAL | `docs/METHOD_REPRESENTATIVENESS_AUDIT.md` | Repo artifact-path evidence supports GRID/RQ-VAE + ReSID + sanity; actual export smoke still pending. |
| A101 | ReSID repo artifact audit | DONE | `docs/GATE0_REPO_AUDIT.md` | GAOQ writes `item_feature/item_code_mapping.parquet` with `item_id`, `codebook1_id`, `codebook2_id`, `codebook3_id`; T5 generator outputs not persisted by default. |
| A102 | GRID/RQ-VAE artifact audit | DONE | `docs/GATE0_REPO_AUDIT.md` | `rkmeans_inference_flat` uses `LocalPickleWriter` to persist item-keyed `cluster_ids`; TIGER candidate outputs optional. |
| A102A | CARD fallback artifact audit | DONE | `docs/GATE0_REPO_AUDIT.md` | `nu-rq-vae/generate_code.py` writes codes and parallel `_item_ids.npy`, but preprocessing/checkpoint path is too heavy for first probe. |
| A103 | Dataset schema audit | DONE | `docs/DATASET_SCHEMA_AUDIT.md` | ReSID `Musical_Instruments` schema passes: 23,742 items, complete train/valid/test join coverage, categorical features available. |
| A103A | Normalized adapter smoke | DONE | `docs/ADAPTER_SMOKE.md`, `src/audit_sid/adapters/resid.py`, `src/audit_sid/adapters/sanity.py` | ReSID item metadata/interactions normalized; sanity SID assignments generated for random/category/popularity baselines. |
| A103B | GRID output-format adapter smoke | DONE | `docs/GRID_ADAPTER_SMOKE.md`, `src/audit_sid/adapters/grid.py` | Synthetic `merged_predictions_tensor.pt` normalized into `sid_assignments`; no real GRID SID mapping exists locally yet. |
| A104 | D1-D5a metric implementation | PARTIAL | `docs/METRIC_SMOKE.md`, `src/audit_sid/metrics.py` | Mapping-first D1-D5a runner implemented and smoke-tested on sanity SID baselines; real ReSID/GRID tokenizer mapping still pending. |
| A104A | Real mapping preflight | BLOCKED | `docs/REAL_MAPPING_PREFLIGHT.md` | ReSID and GRID clones have export code but no pretrained/exported mapping artifacts. Gate 0 now requires bounded ReSID export, GRID artifact acquisition/generation, or CARD fallback. |
| A104B | ReSID run preflight | BLOCKED | `docs/RESID_RUN_PREFLIGHT.md` | Current Python env lacks `k_means_constrained`; ReSID configs also need bounded epochs/device and `leave_one_out` path alignment before launch. |
| A105 | MovieLens-1M portability smoke | DEFERRED | TBD | Half-day max only after Gate 0 is stable; no new tokenizer and no main-claim dependence. |

## Current Decision

Proceed only to Gate 0 feasibility:

> verify whether at least two public SID/tokenizer implementations can export item-to-SID mappings and generator outputs on one small public dataset.

Do not launch full experiments until Gate 0 and dataset support audit pass.

Venue direction: target CIKM 2026 Resource Track now, because it is the nearest track that explicitly accepts resource/protocol/software/evaluation-tool work. Abstract deadline is 2026-05-30 AoE and paper deadline is 2026-06-06 AoE. Gate 0 must pass by 2026-05-24; otherwise do not force a weak submission.

Frozen CIKM v0 scope: primary dataset is ReSID processed Amazon-2023 `Musical_Instruments`; backup dataset is Amazon 2014 Beauty/Sports. Must-run methods are RQ-VAE/TIGER-style SID, ReSID, and a sanity ID baseline. Must-have diagnostics are D1 utilization, D2 collision harm, D3 semantic-collaborative alignment, and D4 head-tail capacity allocation.

Correction: RQ-VAE/TIGER-style SID plus ReSID is only a preferred candidate pair, not automatically sufficient. Gate 0A must verify method representativeness. If the resulting comparison is shallow or does not cover a recent tokenizer innovation in a meaningful way, abandon CIKM 2026 rather than submitting a weak resource paper.

Cluster-first rule updated: must-run coverage is Cluster A canonical SID + Cluster B recent tokenizer/codebook innovation + sanity lower bound. Old Cluster B/C split is deprecated because it did not provide useful decision separation. The next artifact remains Gate 0A repo/artifact evidence, not a training launch.

External review absorption update: CIKM remains the active fast target, but the plan is now explicitly resource-first. Strong empirical finding is a stretch goal, not the paper's core claim. D5 is upgraded to D5a required-light using only SID mapping; generator-output cost remains optional D5b. Public code screening sets the local probing order to GRID/RQ-VAE for Cluster A, ReSID for Cluster B, CARD as fallback, DIGER only as backup; CapsID/AdaSID/AsymRec stay in Method Coverage Table unless runnable code appears.

Gate 0 repo audit update: repo-level artifact paths are feasible enough to continue. GRID/RQ-VAE is the Cluster A main candidate, ReSID/GAOQ is the Cluster B main candidate, and CARD is a valid but heavier fallback. This is not a full Gate 0 pass yet because no local SID assignment artifact has been generated; the next step is dataset schema probe plus bounded export smoke.

Dataset/adapters/metrics update: ReSID `Musical_Instruments` passes schema audit and has complete item-feature coverage for all split item IDs. Normalized `item_metadata`, `interactions`, and sanity `sid_assignments` were generated under ignored `_gate0_artifacts/`. The D1-D5a metric runner completes on sanity baselines and produces five CSV tables. GRID output-format normalization also passes on a synthetic `merged_predictions_tensor.pt`. Real mapping preflight found that both local repo clones lack pretrained/exported mapping artifacts. ReSID run preflight is currently blocked by missing `k_means_constrained` and config/path alignment. Gate 0 remains open and now requires bounded ReSID export setup, GRID artifact acquisition/generation, or CARD fallback.

Update: `docs/METHOD_REPRESENTATIVENESS_AUDIT.md` now exists as the Gate 0A framework. The next concrete artifact should fill the tables with real repo/artifact evidence.
