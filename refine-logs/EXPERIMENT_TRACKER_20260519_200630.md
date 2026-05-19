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
| A100 | Gate 0 code/artifact feasibility | PASSED_ARTIFACT_FEASIBILITY | `docs/GATE0_DECISION.md`, `docs/GRID_CLUSTER_A_EXPORT_PREP.md`, `docs/RESID_REAL_MAPPING_SMOKE.md` | Real Cluster A and B export paths now exist: GRID official-module RQ-KMeans on 5,000 All_Beauty items and ReSID balanced GAOQ on 23,742 Musical_Instruments items. Both export joinable SID assignments and D1-D5a metrics. |
| A100A | Gate 0A method representativeness | CONDITIONAL_PASS_RESOURCE_DEMO | `docs/METHOD_REPRESENTATIVENESS_AUDIT.md`, `docs/GATE0A_EVIDENCE_MATRIX.md`, `docs/GATE0_DECISION.md` | Core Gate 0A is now closed only under conservative resource-demo framing: real GRID Cluster A on All_Beauty, real ReSID Cluster B on smaller Musical_Instruments, sanity lower bounds, and D1-D5a with D3v2. It is not a same-dataset leaderboard pass. |
| A101 | ReSID repo artifact audit | DONE | `docs/GATE0_REPO_AUDIT.md` | GAOQ writes `item_feature/item_code_mapping.parquet` with `item_id`, `codebook1_id`, `codebook2_id`, `codebook3_id`; T5 generator outputs not persisted by default. |
| A102 | GRID/RQ-VAE artifact audit | DONE | `docs/GATE0_REPO_AUDIT.md` | `rkmeans_inference_flat` uses `LocalPickleWriter` to persist item-keyed `cluster_ids`; TIGER candidate outputs optional. |
| A102A | CARD fallback artifact audit | DONE | `docs/GATE0_REPO_AUDIT.md` | `nu-rq-vae/generate_code.py` writes codes and parallel `_item_ids.npy`, but preprocessing/checkpoint path is too heavy for first probe. |
| A103 | Dataset schema audit | DONE | `docs/DATASET_SCHEMA_AUDIT.md` | ReSID `Musical_Instruments` schema passes: 23,742 items, complete train/valid/test join coverage, categorical features available. |
| A103A | Normalized adapter smoke | DONE | `docs/ADAPTER_SMOKE.md`, `src/audit_sid/adapters/resid.py`, `src/audit_sid/adapters/sanity.py` | ReSID item metadata/interactions normalized; sanity SID assignments generated for random/category/popularity baselines. |
| A103B | GRID output-format adapter smoke | DONE | `docs/GRID_ADAPTER_SMOKE.md`, `src/audit_sid/adapters/grid.py` | Synthetic `merged_predictions_tensor.pt` normalized into `sid_assignments`; no real GRID SID mapping exists locally yet. |
| A104 | D1-D5a metric implementation | DONE | `docs/METRIC_SMOKE.md`, `docs/RESID_REAL_MAPPING_SMOKE.md`, `src/audit_sid/metrics.py` | Mapping-first D1-D5a runner implemented and smoke-tested on sanity baselines plus real ReSID/GAOQ mapping. |
| A104A | Real mapping preflight | DONE | `docs/REAL_MAPPING_PREFLIGHT.md`, `docs/RESID_REAL_MAPPING_SMOKE.md` | Initial preflight found missing pretrained artifacts; bounded ReSID FAMAE -> GAOQ resolved the Cluster B real-mapping path. |
| A104B | ReSID run preflight | DONE | `docs/RESID_RUN_PREFLIGHT.md`, `docs/RESID_REAL_MAPPING_SMOKE.md` | Dependency/version and local DataLoader blockers were handled for a bounded local CPU export. |
| A104C | First code review fix pass | DONE | `docs/CODE_REVIEW_FIXES.md` | Fixed interaction semantics, dataset/method grouping, item-id validation, GRID unsafe ID default, ReSID codebook sorting, and sanity collision baseline naming. |
| A104D | First real ReSID mapping export | DONE | `docs/RESID_REAL_MAPPING_SMOKE.md` | Local CPU FAMAE 1 epoch -> GAOQ exported `item_code_mapping.parquet`; normalized `resid_gaoq` SID table has 23,742 rows and D1-D5a metrics. |
| A104E | AutoDL GPU experiment staging | READY | `docs/AUTODL_GPU_EXPERIMENT_PLAN.md`, `tools/autodl_audit_sid/run_resid_gate0_export.sh`, `tools/autodl_audit_sid/run_resid_matrix.sh` | Fixed target resource: 25 CPU cores, 90 GB RAM, 1 x RTX 5090. Scripts prepared for ReSID matrix; still need Cluster A path. |
| A104F | ReSID vs sanity case study | DONE | `docs/CASE_STUDY_RESID_VS_SANITY.md` | Combined real ReSID/GAOQ with sanity baselines; metrics runner now supports mixed SID depths across methods. |
| A104G | Second code review fix pass | DONE | `docs/CODE_REVIEW_FIXES_ROUND2.md` | Tightened D2 column semantics, partial-coverage fail-fast behavior, multi-dataset guard, and sanity metadata fallback. |
| A104H | Local RQ-KMeans proxy baseline | DONE | `docs/LOCAL_RQKMEANS_PROXY.md`, `src/audit_sid/baselines/rqkmeans.py` | Local feature-proxy residual kmeans baseline generated for toolkit development; not a replacement for GRID/CARD public implementation Gate 0. |
| A104I | Cluster A preflight and CARD fallback prep | READY | `docs/CLUSTER_A_PREFLIGHT.md`, `src/audit_sid/adapters/card.py`, `tools/autodl_audit_sid/run_card_rqvae_export.sh` | GRID remains preferred but heavy; CARD RQ-VAE feature-proxy fallback is now runnable on AutoDL once bundle is refreshed. |
| A104J | AutoDL handoff alignment | READY | `docs/AUTODL_READY_HANDOFF.md`, `tools/autodl_audit_sid/preflight_autodl.sh`, `tools/autodl_audit_sid/run_remote_audit_sid.sh`, `tools/autodl_audit_sid/run_autodl_gate0_queue.sh`, `tools/autodl_audit_sid/summarize_gate0_runs.py` | Aligned with `autodl-cloud-deploy`: `/root/autodl-tmp` active workspace, hardware/commit logging, `/root/autodl-fs` archive, script-owned automatic shutdown, local smoke passed. |
| A104K | AutoDL batched experiment matrix | QUICK_SMOKE_READY | `tools/autodl_audit_sid/gate0_experiment_matrix.tsv`, `docs/AUTODL_READINESS_REPORT.md` | Prepared 12 queued runs across quick/robust/sweep/quality; latest transfer bundle is `audit_sid_autodl_20260518_195614.tar.gz` with SHA256 `bb5031a8a812ad03472fbd02e34f21c8757a06e84591f577a1a27682da59d4f5`. Only `QUEUE_MODE=quick` is recommended now. |
| A104L | CARD source-integrity guard | FORMAL_GATE0_BLOCKED | `tools/autodl_audit_sid/check_card_source.py`, `tools/autodl_audit_sid/run_autodl_gate0_queue.sh` | Local CARD CPU smoke found missing `rqvae4/models/rq.py` and `rqvae4/models/vq.py`; quick writes CARD `SKIPPED.txt`, while robust/sweep/quality hard-stop unless CARD is repaired or `ALLOW_RESID_ONLY=1` is intentionally set. |
| A104M | AutoDL prelaunch code review | DONE | `docs/AUTODL_CODE_REVIEW.md`, `docs/AUTODL_CODE_REVIEW_20260518_195302.md` | Subagent-backed review fixed preflight hard failures, archive/shutdown safety, strict summary, CARD source gating, and readiness wording before any GPU launch. |
| A104N | Tokenizer dataset-category audit | DONE | `docs/TOKENIZER_DATASET_CATEGORY_AUDIT.md`, `docs/TOKENIZER_DATASET_CATEGORY_AUDIT_20260518_203431.md` | Musical-only is downgraded to development/quick-smoke evidence. Paper-facing Gate 0 should add at least one canonical vertical, preferably ReSID Amazon-2023 `Sports_and_Outdoors`, before robust/sweep/quality. |
| A104O | Canonical vertical dataset staging | DONE | `docs/CANONICAL_VERTICAL_SCHEMA_AUDIT.md`, `docs/CANONICAL_VERTICAL_SCHEMA_AUDIT_20260518_204859.md` | `Sports_and_Outdoors` and `Beauty_and_Personal_Care` ReSID processed parquet shards downloaded, moved to `/Volumes/TU280Pro/Research/DataSet/ReSID-dataset`, symlinked into `_gate0_repos/ReSID-dataset`, and schema-audited with zero missing item-feature joins. |
| A104P | ReSID canonical queue support | READY | `tools/autodl_audit_sid/run_resid_gate0_export.sh`, `tools/autodl_audit_sid/run_resid_matrix.sh`, `tools/autodl_audit_sid/gate0_experiment_matrix.tsv` | ReSID export is now dataset-aware. `QUEUE_MODE=canonical` runs `Sports_and_Outdoors` 1-epoch ReSID data-readiness smoke; Musical remains quick-smoke only. |
| A104Q | AutoDL no-GPU remote staging | TRANSFER_VERIFIED | `docs/AUTODL_REMOTE_STAGING.md`, `docs/AUTODL_REMOTE_STAGING_20260518_212037.md` | Remote `/root/autodl-tmp/Sec_phrase` has slim code bundle unpacked, ReSID Musical/Sports/Beauty processed datasets downloaded via `hf-mirror.com`, normalized artifacts generated, preflight reports `ASSETS_READY RUNNER_READY`, and full run is `FULL_REPRO_BLOCKED_NO_GPU`. |
| A104R | CARD source repair and CPU smoke | REMOTE_SMOKE_PASSED_NO_GPU | `docs/CARD_SOURCE_REPAIR.md`, `tools/autodl_audit_sid/repair_card_source.py`, `tools/autodl_audit_sid/check_card_source.py` | Missing `rqvae4/models/rq.py` and `rqvae4/models/vq.py` are now reconstructed from tracked templates; PyTorch 2.6 checkpoint loading is patched; local source/import/NURQVAE/tiny full-run CPU smoke pass, and remote no-GPU preflight now reports `CARD_SOURCE_READY`. |
| A104S | CARD canonical-vertical queue alignment | READY | `tools/autodl_audit_sid/run_card_rqvae_export.sh`, `tools/autodl_audit_sid/run_autodl_gate0_queue.sh`, `tools/autodl_audit_sid/gate0_experiment_matrix.tsv` | CARD queue entries now pass `DATASET_NAME=Sports_and_Outdoors` for canonical/robust/sweep/quality instead of silently falling back to Musical; launch should use this patch before GPU spend. |
| A104T | AutoDL GAOQ CPU stop-loss and parallel patch | PATCH_READY | `docs/AUTODL_GAOQ_STOPLOSS.md`, `tools/autodl_audit_sid/patch_resid_runtime.py`, `tools/autodl_audit_sid/run_resid_gate0_export.sh` | Remote robust queue did not finish: Sports FAMAE 1-epoch checkpoint exists, but GAOQ produced no mapping/metrics and `gate0_summary.csv` is 1 byte. GAOQ is CPU-only and `KMeansConstrained` defaulted to `n_jobs=1`; tracked runner now exposes `GAOQ_KMEANS_N_JOBS` and thread env while keeping `use_balancedkmeans=true` by default. |
| A104U | Gate 0 Sports diagnostic matrix | RECLASSIFIED_PIPELINE_EVIDENCE | `docs/GATE0_RESULTS.md`, `_gate0_artifacts/autodl_runs/gate0_summary_current.csv` | Re-audit found that this matrix does not close Gate 0. It remains useful pipeline evidence, but `card_rqvae_feature_proxy` and `resid_gaoq_unbalanced_proxy` cannot count as real Cluster A/B method exports under the spec. |
| A104V | Gate 0 verdict re-audit | DONE | `docs/GATE0_DECISION.md`, `docs/GATE0_DECISION_20260518_234958.md` | Corrected the project state: Gate 0 / 0A remain open; AutoDL CARD compact proxy follow-up is paused; next GPU spend should target a real Cluster A export or directly de-risk one. |
| A104W | GRID real Cluster A export path | LOCAL_5K_PASSED | `docs/GRID_CLUSTER_A_EXPORT_PREP.md`, `tools/autodl_audit_sid/prepare_amazon_text_grid_inputs.py`, `tools/autodl_audit_sid/run_grid_rqkmeans_direct_export.py`, `tools/autodl_audit_sid/run_grid_cluster_a_smoke.sh` | All_Beauty text -> MiniLM embeddings -> official GRID MiniBatchKMeans residual SID export now passes at 5,000 items with complete joins and D1-D5a metrics. This closes the Cluster A artifact-feasibility side of Gate 0, but not Gate 0A/paper readiness. |
| A104X | Gate 0 artifact-feasibility decision | DONE | `docs/GATE0_DECISION.md`, `docs/GATE0_DECISION_20260519_002827.md` | Gate 0 passed for artifact feasibility based on real GRID Cluster A and real ReSID Cluster B exports. At this point Gate 0A was still open; later rows A104AG/A104AO/A106 supersede that status with a conditional resource-demo pass. |
| A104Y | AutoDL Gate 0A staging | TRANSFER_VERIFIED | `docs/AUTODL_GATE0A_STAGING.md`, `tools/autodl_audit_sid/preflight_gate0a_grid.sh`, `tools/autodl_audit_sid/run_gate0a_grid_batch.sh` | No-GPU AutoDL staging is ready for the next GPU window: GRID clone, All_Beauty raw gzip files, MiniLM model, scripts, and imports are present remotely; `preflight_gate0a_grid.sh` reports READY. |
| A104Z | AutoDL Gate 0A clean GRID batch | DONE | `docs/AUTODL_GATE0A_GRID_RESULTS.md`, `_gate0_artifacts/grid_cluster_a_runs/audit_sid_gate0a_grid_20260519_0133_status.tsv` | Clean batch excluded CARD/proxy rows and completed real GRID/RQ-KMeans Cluster A strengthening: All_Beauty 20k seeds 42/43/44 plus 50k seed42, all exit 0 with D1-D5a metrics and zero metadata/interaction SID gaps. |
| A104AA | AutoDL Gate 0A ReSID canonical line | STOPPED_COMPUTE_BOTTLENECK | `docs/GATE0A_CLUSTER_B_PIVOT.md`; hardcopy `/root/autodl-tmp/Sec_phrase/_gate0_artifacts/autodl_runs/logs/audit_sid_gate0a_resid_sports_20260519_0148_20260519_025941.hardcopy` | Sports_and_Outdoors exact balanced GAOQ was preserved and stopped after >70 minutes with no mapping and no traceback. This is no longer the Gate 0A blocker; ReSID remains real Cluster B evidence only on the smaller Musical_Instruments balanced GAOQ export unless a more tractable path is chosen. |
| A104AB | AutoDL ReSID FAMAE-only extra checkpoints | DONE | remote screen `audit_sid_gate0a_resid_famae_extra_20260519_0208` | GPU-only checkpoint batch completed without starting a second GAOQ: Sports_and_Outdoors seed43, Beauty_and_Personal_Care seed42, and Beauty_and_Personal_Care seed43 all saved `best_model.pth`; both screen log stop flags confirm `STOP_AFTER_FAMAE=1`. |
| A104AC | AutoDL ReSID FAMAE-only seed44 backlog | DONE | remote screen `audit_sid_gate0a_resid_famae_seed44_20260519_0214` | Sports_and_Outdoors seed44 and Beauty_and_Personal_Care seed44 FAMAE-only both saved `best_model.pth`; the screen exited cleanly and no GAOQ was launched from this batch. |
| A104AD | ReSID GAOQ CPU optimization patch | REMOTE_SMOKE_PASSED_NOT_ADOPTED | `docs/AUTODL_GAOQ_OPTIMIZATION.md`, `tools/autodl_audit_sid/patch_resid_runtime.py`, `tools/autodl_audit_sid/run_resid_gate0_export.sh` | Remote synthetic tiny smoke passed, but optimized v2 still hit the level-1 exact `KMeansConstrained` bottleneck before level-2 parallelism could help. The v2 screen was preserved and stopped at `/root/autodl-tmp/Sec_phrase/_gate0_artifacts/autodl_runs/logs/audit_sid_gate0a_resid_sports_parallel_v2_20260519_0249_20260519_025941.hardcopy`. |
| A104AE | Cluster B route pivot | CLOSED_V0_CONSERVATIVE | `docs/GATE0A_CLUSTER_B_PIVOT.md`, `docs/B2_B3_METHOD_SCREEN.md`, `docs/EXPERIMENT_PLAN_CLOSURE_AUDIT.md` | Sports exact balanced GAOQ is not a v0 blocker. ReSID Musical remains the real bounded Cluster B evidence, and the current B2/B3 screen found no safe third named tokenizer for main evidence. |
| A104AF | D3 collaborative alignment upgrade | LOCAL_SMOKE_PASSED | `docs/D3_COLLABORATIVE_ALIGNMENT.md`, `src/audit_sid/metrics.py`, `tests/test_metrics.py` | `d3_alignment.csv` now uses item-item co-occurrence top-k neighbors as the collaborative reference and reports per-depth SID-prefix recall, while keeping category purity as auxiliary semantic metadata. Unit tests pass and local ReSID Musical + GRID All_Beauty 5k artifacts both emit D3v2 tables. |
| A104AG | Gate 0A evidence matrix | DONE | `docs/GATE0A_EVIDENCE_MATRIX.md`, `docs/GATE0A_EVIDENCE_MATRIX_20260519_031359.md`, `docs/METHOD_REPRESENTATIVENESS_AUDIT.md`, `docs/GATE0_DECISION.md` | Current verdict is `GATE0A_CORE_CONDITIONAL_PASS_RESOURCE_DEMO`: enough for a conservative toolkit/resource demo, not enough for a same-dataset method benchmark. ReSID Musical is the main B evidence; CARD remains controlled stressor/backlog. |
| A104AH | D3v2 case-study table | DONE | `docs/CASE_STUDY_RESID_VS_SANITY.md`, `docs/CASE_STUDY_RESID_VS_SANITY_20260519_031836.md`, `tools/autodl_audit_sid/summarize_case_study.py` | ReSID-vs-sanity Musical case study now has a compact paper-facing table from D2/D3v2/D4/D5a. The table supports a diagnostic tradeoff story without claiming downstream Recall/NDCG or same-dataset GRID-vs-ReSID superiority. |
| A104AI | CIKM resource paper plan | DONE | `docs/CIKM_RESOURCE_PAPER_PLAN.md`, `docs/CIKM_RESOURCE_PAPER_PLAN_20260519_032126.md` | Drafted claim-evidence matrix, safe abstract, 4-page structure, figure/table plan, and red-line wording for the conditional Gate 0A resource-demo route. |
| A104AJ | Citation scaffold | DONE | `docs/CITATION_SCAFFOLD.md`, `docs/CITATION_SCAFFOLD_20260519_032407.md` | Created a citation scaffold with source links and explicit no-BibTeX-from-memory rules. All citation metadata still needs verification before LaTeX. |
| A104AK | DACT optional D6 drift smoke | LOCAL_SMOKE_PASSED_OPTIONAL | `docs/DACT_DRIFT_SMOKE.md`, `_gate0_artifacts/dact_tools_smoke/d6_churn_0.6_to_0.7.csv`, `tools/autodl_audit_sid/compute_sid_churn.py` | DACT bundled Tools 0.6 -> 0.7 common-item SID churn is `2271/9610=0.236316`; 0.7 has only `3` full-collision groups / `6` items. Keep as optional drift/continual artifact evidence, not a replacement for Cluster B. |
| A104AL | AutoDL no-GPU delta sync | TRANSFER_VERIFIED_NO_GPU | `docs/AUTODL_NO_GPU_DELTA_SYNC.md`, remote `/root/autodl-tmp/Sec_phrase` | Synced docs/refine-logs/src/tools/tests plus DACT smoke artifacts to remote. Remote unit tests pass, D6 churn recomputes, preflight reports `ASSETS_READY RUNNER_READY`, and `torch.cuda.is_available=False`; no queue launched. |
| A104AM | AutoDL GPU quick smoke | DONE | `docs/AUTODL_GPU_QUICK_SMOKE.md`, `_gate0_artifacts/autodl_runs/gate0_summary_remote_quick_20260519_101555.csv` | GPU quick screen completed without auto-shutdown. ReSID Musical balanced GAOQ exported 23,742 SIDs with zero missing joins and zero full collisions; CARD Musical compact proxy exported 4,891 unique SIDs with 0.793994 duplicate rate. This is smoke/provenance evidence only; robust/sweep/quality remain blocked unless a new evidence gap is explicit. |
| A104AN | External audit handoff | DONE | `docs/AUDIT_SID_EXTERNAL_AUDIT_HANDOFF.md` | Subagent review found no blocker and fixed one paper-plan timestamp consistency issue. Handoff summarizes current verdict, evidence entry points, AutoDL state, verification commands, and remaining paper-draft work. |
| A104AO | GRID Musical same-dataset CPU row | DONE | `docs/GRID_MUSICAL_SAME_DATASET_CPU.md`, `_gate0_artifacts/grid_same_dataset_runs/musical_same_dataset_grid_vs_resid_summary_20260519_110722.csv` | Responds to third external audit's cross-dataset gap. Local CPU official GRID MiniBatchKMeans ran on ReSID Musical processed feature-text embeddings: 23,742 items, zero missing joins, unique SID 3,749, duplicate SID rate 0.842094, full collision rate 0.976876. Same dataset comparison to ReSID GAOQ is now available, but this is not a faithful raw-text TIGER/GRID reproduction. |
| A104AP | Third external audit response | DONE | `docs/THIRD_EXTERNAL_AUDIT_RESPONSE.md` | Accepted the cross-dataset critique, documented the local CPU GRID Musical response, and updated the CIKM paper plan to use same-item-universe wording with explicit feature-text caveat. |
| A104AQ | AutoDL no-GPU post-commit sync | TRANSFER_VERIFIED_NO_GPU_POST_COMMIT | `docs/AUTODL_NO_GPU_POST_COMMIT_SYNC.md`, remote `/root/autodl-tmp/Sec_phrase` | After commit `303e1fc`, synced docs/refine-logs/src/tools/tests plus manifest/findings to the no-GPU AutoDL instance. Remote conda Python unit tests pass: 6 tests OK. No training queue launched and old dead screens were left untouched. |
| A105 | MovieLens portability smoke | LOCAL_SMOKE_PASSED_NON_AMAZON_SCHEMA | `docs/MOVIELENS_PORTABILITY_SMOKE.md`, `tools/autodl_audit_sid/run_movielens_portability_smoke.py`, `_gate0_artifacts/movielens_portability_smoke/ml25m_1mratings_10kitems/metrics/coverage_report.csv` | Local CPU bounded MovieLens-25M smoke passed on first 1,000,000 ratings / 10,000 movie items with sanity SIDs only. It validates non-Amazon schema portability, not a main tokenizer benchmark. |
| A106 | Paper-facing metric scope absorption | DONE | `docs/CURRENT_STATE.md`, `docs/CIKM_EXPERIMENT_DESIGN.md`, `docs/CIKM_RESOURCE_PAPER_PLAN.md` | Accepted local paper-readiness docs and tightened D1-D6 scope: D1-D5a are main item-to-SID artifact diagnostics, D6 is optional, D2 is profile not causal harm, D5b/D7 require generator outputs, and full SID system quality is out of scope. |
| A107 | CIKM no-appendix paper tables and citation audit | DONE | `docs/CIKM_RESOURCE_FORMAT_AUDIT.md`, `docs/CITATION_AUDIT.md`, `tools/autodl_audit_sid/build_paper_tables.py`, `paper_assets/tables/table1_method_coverage.csv`, `paper_assets/tables/table2_musical_diagnostic.csv` | Official Resource page confirms 4 pages include appendices/acknowledgments; paper should be no-appendix. Generated paper-facing tables: Table 1 method coverage and Table 2 same-item Musical diagnostics for PDF, with Tables 3-6 for GitHub artifact. Citation metadata verified from primary pages. |
| A109 | Verified BibTeX generation | DONE | `docs/BIBTEX_AUDIT.md`, `paper_assets/references/audit_sid_references.bib` | Generated paper-ready BibTeX from verified arXiv/official pages and then expanded it with the reference-refresh must-cites. Keep one final citation drift check before submission, but final BibTeX is no longer an open blocker. |
| A110 | CIKM Resource paper draft | COMPILES_3P_DRAFT | `paper/main.tex`, `paper/main.pdf`, `paper/references.bib` | Created an ACM CIKM Resource draft with no appendix, Table 1 method coverage, Table 2 same-item Musical diagnostics, conservative limitations, and expanded reference framing. `latexmk -pdf` succeeds and `pdfinfo` reports 3 pages. |
| A111 | SID reference refresh | DONE | `docs/SID_REFERENCE_REFRESH.md`, `docs/SID_REFERENCE_REFRESH_20260519_125226.md` | Re-ran literature refresh against the AUDIT-SID spec. Current scaffold is too narrow: add identifier foundations, RecList-style diagnostic tooling, CoST/LETTER collaborative-tokenizer work, and recent 2026 SID papers including Snapchat SID, AdaSID, CapsID, AsymRec, and SID staleness before finalizing paper references. |
| A112 | SID cluster/diagnostic taxonomy refresh | DONE | `docs/SID_CLUSTER_DIAGNOSTIC_REFRESH.md`, `docs/SID_CLUSTER_DIAGNOSTIC_REFRESH_20260519_130606.md` | Updated paper-facing method taxonomy after the literature refresh: Cluster B is now B1-B4 facets, R0 reference-only foundations are separated from runnable methods, D5b is reframed as future D7 generator/retrieval behavior, and current v0 coverage is explicitly D1-D5a plus optional D6. |
| A113 | Paper figure/table strategy | DONE | `docs/PAPER_FIGURE_TABLE_STRATEGY.md`, `docs/PAPER_FIGURE_TABLE_STRATEGY_20260519_131103.md` | Planned a resource-paper figure/table layout from current outputs and CIKM/SIGIR/RecSys-style resource-paper patterns: add one interface/diagnostic-map figure, redesign Table 1 as a facet-aware coverage matrix, keep Table 2 as the only diagnostic case-study table, and move DACT/MovieLens/GRID-scale/sanity tables to the artifact repo. |
| A114 | Paper figure/table integration | COMPILES_3P_DRAFT | `paper/sections/2_toolkit.tex`, `paper/sections/3_resource_demo.tex`, `paper/main.pdf` | Added Fig. 1 artifact pipeline with D1-D7 map, replaced Table 1 with facet-aware A/B1-B4/C/D/control coverage, compressed Table 2 caption/columns, and recompiled. `pdfinfo` reports 3 pages; log has no undefined citations or LaTeX errors. No new experiment is required unless D7 `generator_outputs` become available. |
| A115 | Paper figure/table subagent review fixes | COMPILES_3P_DRAFT | `paper/sections/2_toolkit.tex`, `paper/sections/3_resource_demo.tex`, `paper/main.pdf` | Applied read-only reviewer fixes: B3 diagnostics now list D3/D5a/D7, Table 2 labels ReSID as bounded export, and the capacity sentence now refers to the tail-capacity column. Recompiled successfully to 3 pages. |
| A116 | Paper body expansion and figure/table upgrade | COMPILES_4P_BODY | `paper/main.tex`, `paper/figures/fig1_audit_sid_pipeline.pdf`, `tools/paper_figures/generate_audit_sid_pipeline.py`, `paper/sections/*.tex`, `paper/main.pdf` | Replaced the temporary LaTeX fbox figure with a generated vector PDF, rewrote Table 1 as a facet/evidence/boundary matrix, expanded Table 2 with item counts, added Table 3 for reviewer-facing artifact package, and expanded artifact contract / protocol / reviewer workflow / claim discipline. `paper/main.pdf` now compiles to 5 pages total with body text filling through page 4 and references/GenAI on page 5. |
| A117 | Strict paper claim audit | PASS | `docs/PAPER_STRICT_CLAIM_AUDIT.md`, `paper_assets/tables/table2_musical_diagnostic.csv` | Checked current numeric claims and scope claims. Table 2 and abstract numbers match the generated CSV; wording now avoids leaderboard, faithful TIGER/ReSID/CARD reproduction, real serving latency, generator-output D7, and online-impact claims. Remaining work is final citation drift check. |
| A118 | Paper plan/design sync after body expansion | DONE | `docs/CIKM_EXPERIMENT_DESIGN.md`, `docs/CIKM_RESOURCE_PAPER_PLAN.md` | Synchronized stale planning docs from the old one-figure/two-table/3-page draft to the current generated vector Fig. 1, Tables 1-3, reviewer workflow, claim discipline, and 4-page-body stance. |
| A119 | External 8/10 closure | DONE | `docs/EXTERNAL_SIM_REVIEW_ROUND2.md` | Two simulated external reviewers score the artifact 8.0/10 and 8.1/10 after pushed tag plus clean-checkout verification. No P0 blockers remain. |
| A120 | Strong-accept lift plan | CLOSED_FOR_V0 | `docs/CIKM_EXPERIMENT_DESIGN.md`, `docs/CIKM_RESOURCE_PAPER_PLAN.md`, `docs/EXPERIMENT_PLAN_CLOSURE_AUDIT.md` | Optional 8.5-target package was screened. The feasible v0 lifts are done; a third true named tokenizer remains future-only unless new runnable evidence appears. |
| A121 | Fig. 1 redesign | DONE | `docs/PAPER_FIGURE_TABLE_STRATEGY.md`, `tools/paper_figures/generate_audit_sid_pipeline.py`, `paper/figures/fig1_audit_sid_pipeline.pdf` | Fig. 1 is now an artifact-contract / diagnostics / evidence-maturity map with D5a vs D7 and main/control/backlog boundaries visible. |
| A122 | Same-dataset A/B panel upgrade | DONE_V0 | `paper_assets/tables/table2_musical_diagnostic.*`, `paper/sections/3_resource_demo.tex`, `docs/GRID_MUSICAL_3SEED_LOCAL.md` | Same-item Musical panel now uses GRID feature-text vs bounded ReSID plus GRID Musical three-seed stability wording. It remains a diagnostic panel, not faithful TIGER/GRID reproduction. |
| A123 | Third named tokenizer feasibility screen | SCREEN_DONE_NO_NEW_MAIN_METHOD | `docs/B2_B3_METHOD_SCREEN.md` | QuaSID/AdaSID/CapsID remain paper/motivation only in this screen; DIGER public repo is illustrative/reference and lacks data/checkpoints; CARD repaired path remains proxy/control. No third named tokenizer enters main evidence from this pass. |
| A124 | Method x diagnostic selection matrix | DONE | `docs/METHOD_DIAGNOSTIC_SELECTION_MATRIX.md` | Added a practical method-by-D1-D7 table for choosing new methods that can produce non-redundant diagnostic findings. Prioritizes B2 first, then B3, then B4. |
| A125 | GRID Musical three-seed local stability | LOCAL_3SEED_DONE | `docs/GRID_MUSICAL_3SEED_LOCAL.md`, `_gate0_artifacts/grid_same_dataset_runs/musical_grid_feature_text_3seed_summary_20260519_1600.csv` | Reused existing Musical feature-text embeddings and ran GRID/RQ-KMeans local CPU seeds 43/44 to join seed 42. All three seeds have zero metadata/interaction SID gaps; duplicate SID rate is 0.8327--0.8421 and full-collision rate is 0.9751--0.9769. This strengthens same-dataset artifact evidence but remains feature-text controlled GRID, not faithful raw-text TIGER/GRID. |
| A126 | Method-selection matrix refresh after screen | DONE | `docs/METHOD_DIAGNOSTIC_SELECTION_MATRIX.md`, `docs/METHOD_DIAGNOSTIC_SELECTION_MATRIX_20260519_155857.md` | Matrix now records the negative third-method screen and points the near-term lift toward same-dataset stability/finding sharpening rather than proxy method expansion. |
| A127 | Experiment plan closure audit | DONE | `docs/EXPERIMENT_PLAN_CLOSURE_AUDIT.md`, `docs/EXPERIMENT_PLAN_CLOSURE_AUDIT_20260519_162152.md` | Current CIKM Resource v0 experiment package is closed. Remaining work is citation drift, real single-blind metadata, copy editing, and final claim audit after text changes. |
| A128 | Results-based paper findings polish | DONE | `docs/PAPER_FINDINGS_POLISH.md`, `paper/main_20260519_170132.pdf` | Abstract, introduction, resource demo, and limitations now turn existing v0 evidence into explicit diagnostic findings while preserving non-leaderboard claim boundaries. |
| A129 | Additional experiment preflight code | DONE | `docs/ADDITIONAL_EXPERIMENT_PREFLIGHT_CODE.md`, `tools/autodl_audit_sid/preflight_metric_inputs.py`, `tests/test_preflight_metric_inputs.py` | Subagent-prepared local CPU preflight validates future `sid_assignments` / `item_metadata` / `interactions` inputs and can run bounded D1-D5a smoke summaries before any new method or GPU run. |
| A130 | Author artifact email drafts | DRAFTED_NOT_SENT | `docs/AUTHOR_ARTIFACT_EMAIL_DRAFTS.md` | Drafts for DIGER, QuaSID, AdaSID, and CapsID are signed `Timber Ding` and avoid mentioning AUDIT-SID/CIKM/research submission. Sending still requires confirmed recipient addresses plus Gmail/Outlook connector or SMTP route. |
| A131 | Method-inspired controller selection | DONE | `docs/CONTROLLED_STRESSOR_SELECTION.md` | Controllers are separated from named-method coverage. Planned order is `qualified_collision_probe` first, `capacity_budget_sweep` second, and `variable_depth_cost_probe` third; all three now have local results. |
| A132 | Qualified collision probe | LOCAL_CONTROLLER_DONE | `docs/QUALIFIED_COLLISION_PROBE.md`, `tools/autodl_audit_sid/run_qualified_collision_probe.py`, `paper_assets/tables/table8_qualified_collision_probe.csv` | D2b/D3 controller passed locally. GRID feature-text collided pairs have 3.86x co-occurrence lift over popularity-matched non-collision pairs; collision-heavy hash control has only 1.19x lift. |
| A133 | Capacity budget sweep | LOCAL_CONTROLLER_DONE | `docs/CAPACITY_BUDGET_SWEEP.md`, `tools/autodl_audit_sid/run_capacity_budget_sweep.py`, `paper_assets/tables/table9_capacity_budget_sweep.csv` | D1/D2/D4/D5a controller passed locally. Width-24 head-reserved policy preserves head unique ratio at 1.0 but leaves tail unique ratio at 0.028190, unlike rank-mod's more even allocation. |
| A134 | Variable depth cost probe | LOCAL_CONTROLLER_DONE_PAPER_OPTIONAL | `docs/VARIABLE_DEPTH_COST_PROBE.md`, `tools/autodl_audit_sid/run_variable_depth_cost_probe.py`, `paper_assets/tables/table10_variable_depth_cost_probe.csv` | D4/D5a boundary controller passed locally. Useful artifact evidence; include in PDF only if D5a needs an extra compact boundary example. |
| A135 | Paper controller integration | COMPILES_4P_BODY | `docs/PAPER_CONTROLLER_INTEGRATION.md`, `paper/main.pdf`, `paper/main_20260519_193420.pdf` | Section 3 now integrates qualified-collision, capacity-budget, and variable-depth controller findings as artifact stressors. They remain outside named-method coverage. `paper/main.pdf` compiles to 5 pages total with body through page 4 and references/GenAI on page 5. |
| A136 | Controlled-stressor table and prose polish | COMPILES_4P_BODY | `paper/main.pdf`, `paper/main_20260519_200630.pdf`, `docs/PAPER_CONTROLLER_INTEGRATION.md` | Added compact controlled-stressor Table 3, rewrote the abstract/resource-demo/limitations prose away from experiment-note style, preserved all numeric claims and claim boundaries, and kept the PDF at 5 pages total with body through page 4. |

## Current Decision

Proceed from Gate 0/Gate 0A into paper-readiness tightening:

> preserve the conservative resource-demo claim, build the same-item-universe
> Musical diagnostic table from D1-D5a/D3v2, keep ReSID-vs-sanity as secondary
> non-redundancy controls, and avoid leaderboard or faithful-CARD claims until
> new evidence appears.

Paper scope update: D1-D6 are an artifact-level audit suite, not a complete SID
system-quality benchmark. Main text should emphasize D1-D5a over `item -> SID`
artifacts; D6 stays optional. D2 is collision profile rather than causal harm,
and generator predictability/invalid generated paths remain future D5b/D7.

CIKM format update: Resource papers have only 4 pages including appendices and
acknowledgments, so AUDIT-SID must be written with no required appendix. The PDF
should contain only Table 1 method coverage and Table 2 same-item Musical
diagnostics; all extra run tables live in `paper_assets/tables/` and the GitHub
artifact.

Reference update: `docs/SID_REFERENCE_REFRESH.md` supersedes the older narrow
scaffold for paper planning. The paper should not tell a simple
`TIGER -> ReSID -> AUDIT-SID` story; it needs compact coverage of identifier
foundations, behavioral/diagnostic evaluation, collaborative tokenization,
collision qualification, industrial SID deployment, and drift/staleness.

Cluster taxonomy update: use `docs/SID_CLUSTER_DIAGNOSTIC_REFRESH.md` for
paper-facing method grouping. Cluster B is no longer one homogeneous bucket; it
has B1 collaborative/predictability, B2 collision/capacity, B3
ranking/differentiable/retrieval, and B4 bottleneck/interface facets. Current
evidence implements D1-D5a plus optional D6; D7 requires `generator_outputs`.

Figure/table update: use `docs/PAPER_FIGURE_TABLE_STRATEGY.md` for the next
paper edit. The PDF should have one Fig. 1 interface/diagnostic map, a
facet-aware Table 1 coverage matrix, and the same-item Musical Table 2. Extra
diagnostic tables remain artifact-repo evidence, not PDF evidence.

Figure/table integration update: Fig. 1 and the redesigned Table 1/Table 2 are
now in the compiled draft. The current draft compiles to 5 pages total, with
the core body filling through page 4 and references/GenAI disclosure on page 5.
The active blocker is final submission hygiene rather than page budget or new
experiments.

Paper body/figure update: the current draft now uses a generated vector Fig. 1,
three body tables, and expanded resource-paper text. `paper/main.pdf` compiles
to 5 pages total, with the core body filling through page 4 and references plus
GenAI disclosure on page 5. `docs/PAPER_STRICT_CLAIM_AUDIT.md` is the current
claim audit and reports PASS with conservative wording retained.

Do not launch full experiments until the next evidence gap is explicit. AutoDL
Sports exact GAOQ is no longer the blocker. The current paper draft uses the
four-page body budget, so the next blockers are final citation drift check,
real single-blind metadata, and final claim audit after text changes rather
than new GPU work.

DACT local smoke is now available as optional D6 drift evidence only: it can
support a small continual-tokenization extension, but it must not change the
main paper route or replace ReSID/CARD/DIGER Cluster B decisions.

Remote no-GPU state was transfer-verified as of 2026-05-19 09:56 CST. After
GPU power-on, `REQUIRE_CUDA=1` preflight passed at 2026-05-19 10:15 CST and a
bounded `QUEUE_MODE=quick` screen completed at 2026-05-19 10:21 CST. Do not
escalate to robust/sweep/quality after this pass; it is smoke/provenance
evidence only.

Post-commit no-GPU sync is transfer-verified as of 2026-05-19 11:49 CST:
commit `303e1fc` surfaces are staged under `/root/autodl-tmp/Sec_phrase`, and
remote conda Python unit tests pass. This is staging only, not a new GPU run.

Local-first experiment policy update: run all remaining feasible experiments
locally first. AutoDL/GPU should only be used when a specific local blocker is
documented. The MovieLens portability smoke followed this rule and completed
locally.

Venue direction: target CIKM 2026 Resource Track now, because it is the nearest track that explicitly accepts resource/protocol/software/evaluation-tool work. Abstract deadline is 2026-05-30 AoE and paper deadline is 2026-06-06 AoE. Gate 0 must pass by 2026-05-24; otherwise do not force a weak submission.

Frozen CIKM v0 scope: primary dataset is ReSID processed Amazon-2023 `Musical_Instruments`; backup dataset is Amazon 2014 Beauty/Sports. Must-run methods are RQ-VAE/TIGER-style SID, ReSID, and a sanity ID baseline. Must-have diagnostics are D1 utilization, D2 collision harm, D3 semantic-collaborative alignment, and D4 head-tail capacity allocation.

Correction: RQ-VAE/TIGER-style SID plus ReSID is only a preferred candidate pair, not automatically sufficient. Gate 0A must verify method representativeness. If the resulting comparison is shallow or does not cover a recent tokenizer innovation in a meaningful way, abandon CIKM 2026 rather than submitting a weak resource paper.

Cluster-first rule updated: must-run coverage is Cluster A canonical SID + Cluster B recent tokenizer/codebook innovation + sanity lower bound. Old Cluster B/C split is deprecated because it did not provide useful decision separation. The next artifact remains Gate 0A repo/artifact evidence, not a training launch.

External review absorption update: CIKM remains the active fast target, but the plan is now explicitly resource-first. Strong empirical finding is a stretch goal, not the paper's core claim. D5 is upgraded to D5a required-light using only SID mapping; generator-output cost remains optional D5b. Public code screening sets the local probing order to GRID/RQ-VAE for Cluster A, ReSID for Cluster B, CARD as fallback, DIGER only as backup; CapsID/AdaSID/AsymRec stay in Method Coverage Table unless runnable code appears.

Gate 0 repo audit update: repo-level artifact paths are feasible enough to continue. GRID/RQ-VAE is the Cluster A main candidate, ReSID/GAOQ is the Cluster B main candidate, and CARD is a valid but heavier fallback. This is not a full Gate 0 pass yet because no local SID assignment artifact has been generated; the next step is dataset schema probe plus bounded export smoke.

Dataset/adapters/metrics update: ReSID `Musical_Instruments` passes schema audit and has complete item-feature coverage for all split item IDs. Normalized `item_metadata`, target-only `interactions`, and sanity `sid_assignments` were generated under ignored `_gate0_artifacts/`. The D1-D5a metric runner completes on sanity baselines, validates item coverage, groups by dataset/method, and produces six CSV tables including `coverage_report.csv`. GRID output-format normalization also passes on a synthetic `merged_predictions_tensor.pt` with an explicit unsafe dense-ID flag. Local ReSID FAMAE 1 epoch -> balanced GAOQ now produces the first real `resid_gaoq` SID mapping: 23,742 rows, zero duplicate full SIDs, prefix counts `32;1280;23742`. CARD output normalization and AutoDL fallback runner are prepared but no longer needed for Gate 0. The Sports matrix with proxy rows remains only pipeline evidence. The GRID path passes on All_Beauty with official GRID MiniBatchKMeans classes and has a same-item-universe Musical controlled feature-text row against ReSID. Gate 0 is passed for artifact feasibility, and Gate 0A has a conditional pass for conservative resource-demo framing. D3 has been upgraded from category-only proxy to co-occurrence collaborative alignment on local artifacts. Remaining work is paper-readiness: LaTeX fitting, final citation drift check, and strict caveat wording.

Update: `docs/METHOD_REPRESENTATIVENESS_AUDIT.md` now exists as the Gate 0A framework. The next concrete artifact should fill the tables with real repo/artifact evidence.

Internal review update: two local review rounds are completed for the CIKM 2026
Resource Track target. Round 1 scored the draft at 7.1/10 and drove
license/quickstart, abstract-scope, artifact-table, and resource-utility fixes.
Round 2 scores the current paper at 8.0/10 after Fig. 1, Table 1, Table 2,
Table 3, and GenAI-disclosure revisions. External simulated review has not yet
been run; the next review must keep the target fixed to CIKM 2026 Resource
Track and judge artifact utility, claim discipline, reproducibility, coverage,
and page budget.

External simulated review target update: external review also uses an 8.0/10
target, not a weak-accept bar. Two read-only simulated reviewers are assigned:
one resource/artifact reviewer and one SID/recommender reviewer. Absorb only
edits that improve external 8/10 credibility without strengthening claims
beyond current artifact evidence.

External review Round 1 update: reviewers scored the draft 7.2 and 7.4 before
packaging fixes. After adding `requirements.txt`, `ARTIFACT_MANIFEST.md`,
`tools/verify_paper_artifact.py`, pinned-tag quickstart commands, D2/D3/D5a
definitions, and clean-checkout wording in Section 4/Table 3, both reviewers
rescored local state at 7.7 and stated 8.0 is reachable after commit/tag/push
and clean-checkout verification. No new experiment is required for external
8/10; the remaining non-engineering blocker is real single-blind author
metadata for final submission.

External review Round 2 closure: branch `codex/audit-sid-idea-discovery` and
tag `audit-sid-cikm-resource-v0.1` are pushed to GitHub at commit `d24dfec`.
A fresh tag clone under `/private/tmp/audit_sid_clean_verify_20260519_1512`
passed 6 unit tests, regenerated Fig. 1, passed
`tools/verify_paper_artifact.py`, and stayed clean after `git status --short`.
The two simulated external reviewers now score the CIKM 2026 Resource artifact
at 8.0/10 and 8.1/10 with no P0 blockers. Remaining work is submission
hygiene, real single-blind metadata, citation drift recheck, and optional
evidence breadth strengthening.

Strong-accept lift update: optional next work is now explicitly scoped. To move
beyond the current 8.0/8.1 external-review state, prioritize a third true named
B2/B3 tokenizer artifact, a stronger same-dataset A/B diagnostic panel, a
concise use of existing GRID 20k three-seed stability evidence, and a Fig. 1
redesign. Do not add new D metrics before these evidence-width issues are
handled.

Method-selection update: `docs/METHOD_DIAGNOSTIC_SELECTION_MATRIX.md` is now
the working screen for new methods. It records each candidate method/facet
against D1-D7, artifact state, expected finding material, priority, and next
action. Current screening order is B2 collision/capacity first
(`QuaSID`/`AdaSID`/faithful `CARD`), then B3 ranking/retrieval (`DIGER`/joint
search-rec SID), then B4 bottleneck/interface (`CapsID`/`AsymRec`).

Third-method screen update: the 2026-05-19 B2/B3 screen did not find a
low-risk third named tokenizer for main evidence. QuaSID/AdaSID/CapsID are
paper/motivation only for now, DIGER is incomplete for artifact export, and
CARD remains proxy/control unless the original `nu-rq-vae` path is repaired
and reviewed. Local effort shifted to same-dataset stability instead: GRID
Musical feature-text now has seeds 42/43/44 with complete joins and stable high
collision pressure.

Experiment closure update: `docs/EXPERIMENT_PLAN_CLOSURE_AUDIT.md` closes the
current CIKM 2026 Resource v0 experiment package. Gate 0, conditional Gate 0A,
D1-D5a/D3v2 implementation, same-item Musical contrast, GRID Musical
three-seed stability, third-method screen, Fig. 1 redesign, public verifier,
unit tests, and paper compile are all closed for v0. Remaining work is
submission hygiene and final writing/review discipline, not additional local or
GPU experiments unless a new evidence gap is explicitly selected.

Paper polish update: `docs/PAPER_FINDINGS_POLISH.md` records the first
results-based writing pass after v0 closure. The draft now states three
artifact-level findings in Section 3: stable collision pressure in the
controlled GRID Musical row, separation between collision-free capacity and
collaborative-prefix alignment, and separation between tail capacity and
prefix/fan-out structure. These are still diagnostic claims, not downstream
ranking claims.

Additional-experiment code update: `tools/autodl_audit_sid/preflight_metric_inputs.py`
is now the local gate for future method/artifact additions. It validates table
contracts and join coverage before metric execution, with an optional bounded
D1-D5a smoke summary. This supports future 8.5-lift work without reopening GPU
experiments or admitting proxy artifacts directly into paper evidence.

Third-method evidence gate update: self-implemented paper-inspired tokenizers
are excluded from named-method evidence by default. A third method must have an
official or author-provided anchor, stable item-to-SID export, AUDIT-SID joins,
at least three useful diagnostics, and a fidelity note before entering the main
case study. `docs/THIRD_METHOD_EVIDENCE_GATE.md` is the current rule.

Official-release scout update: QuaSID, AdaSID, and CapsID remain paper-only in
the current screen, and DIGER's official repo is still illustrative/reference
without processed data/checkpoints or a ready item-to-SID export. None enters
AUDIT-SID v0 main evidence; see `docs/METHOD_RELEASE_SCOUT.md`.

CARD original preflight update: `tools/autodl_audit_sid/preflight_card_nurqvae.py`
passes local source/import/export-contract checks for CARD's original
`nu-rq-vae` path, including a tiny CPU synthetic export that preserves item
IDs. This removes the import-path blocker but is not evidence for faithful CARD
yet; the next gate is real CARD input/checkpoint/export plus AUDIT-SID joins.

CARD original v0 failure update: after fetching the official CARD repo, local
`HEAD` and `origin/main` are both `b8ce0976`. The official tree is missing
`rqvae4/models/rq.py`, `rqvae4/models/vq.py`, and `rqvae4/vq.py`, although
`nu-rq-vae/models/nu_rqvae.py` imports `rqvae4.models.rq`. The preflight now
reports `local_repair_required`, `core_algorithm_patched=true`,
`quantizer_replaced=true`, and `next_step_ready=false`. CARD original is closed
as `FAILED_FOR_V0_MAIN_EVIDENCE` unless authors provide complete source,
checkpoints, processed embeddings, or item-to-SID mappings.

Author-contact update: `docs/AUTHOR_ARTIFACT_EMAIL_DRAFTS.md` contains
ready-to-send drafts for DIGER, QuaSID, AdaSID, and CapsID, signed as Timber
Ding. They have not been sent from this Codex session because there is no
email connector/SMTP route and recipient addresses still need confirmation
from official author/project pages.

Controller-selection revision: `docs/CONTROLLED_STRESSOR_SELECTION.md` now
uses a method-inspired controller suite, not only generic sanity calibration.
The agreed order is: first `qualified_collision_probe` for D2b/D3, second
`capacity_budget_sweep` for D1/D2/D4/D5a, and third
`variable_depth_cost_probe` for D4/D5a/D7-boundary. All three remain outside
named-method coverage; the variable-depth result is optional for the paper
depending on whether it strengthens the D5a narrative cleanly.

Controller-execution update: all three method-inspired controllers have local
results. `qualified_collision_probe` supports the distinction between raw
collision volume and interaction-qualified collision risk. `capacity_budget_sweep`
supports the distinction between nominal capacity, collision pressure,
head-tail allocation, and prefix-cost structure. `variable_depth_cost_probe`
supports the D5a active-prefix boundary but should remain artifact-repo
evidence unless the paper needs a compact variable-depth example.

Paper-controller integration update: `docs/PAPER_CONTROLLER_INTEGRATION.md`
records the writing pass that folds all three controller results into the draft
as stressor evidence. The draft now uses qualified collision for D2b,
capacity-budget pressure for D1/D2/D4/D5a, and variable-depth active-prefix
structure for D5a boundary wording, while keeping these rows out of named
tokenizer coverage.

Paper-style polish update: the controller evidence is now a real main-text
controlled-stressor table rather than only prose. The abstract, introduction,
resource demo, and limitations were tightened toward a CIKM/SIGIR-style
resource-paper narrative: artifact problem, reusable interface, compact
evidence, and explicit boundary.
