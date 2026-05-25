# SIDInspector Reviewer Artifact Manifest

Timestamp: 2026-05-20 19:32:36 CST

This manifest is the reviewer-facing public artifact index. It is intentionally
shorter than `MANIFEST.md`, which is the full ARIS provenance ledger.

## Frozen Artifact Entry

- Target venue/track: CIKM 2026 Resource Track
- Public artifact label: `sidinspector-9BB2`
- Anonymous review URL: `https://anonymous.4open.science/r/sidinspector-9BB2`
- License: MIT, see `LICENSE`

Some code paths use the legacy `audit_sid` module name. They are kept stable so
published verifier commands and generated artifacts remain reproducible; the
public resource name is SIDInspector.

## Public Verification Path

The clean-checkout verification path does not require ignored local caches such
as `_gate0_artifacts/`. Open the anonymous URL in a browser, use the page's
Download/ZIP entry, unzip the archive, then run:

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests
MPLCONFIGDIR=/tmp/sidinspector_mpl python3 tools/paper_figures/generate_audit_sid_pipeline.py
python3 tools/verify_paper_artifact.py
```

The verifier checks the published paper tables, figure, license, quickstart,
BibTeX file, the main Table 2 numeric claims, the auxiliary B4/B6/B7 vertical /
fixed-reranker / Sports numbers, the All_Beauty B6 replication, and the
RQ-min reference-adapter row now referenced in the paper.

## Public Files

| Path | Role | Clean-checkout status |
|---|---|---|
| `ARTIFACT_QUICKSTART.md` | reviewer command entry point | required |
| `LICENSE` | MIT license | required |
| `requirements.txt` | minimal local verification dependencies | required |
| `src/sidinspector/` | public import namespace for interface and metrics | import/test |
| `src/audit_sid/` | legacy-compatible implementation modules | import/test |
| `tests/` | metric and churn unit tests | runnable |
| `tools/verify_paper_artifact.py` | clean-checkout artifact verifier | runnable |
| `tools/paper_figures/generate_audit_sid_pipeline.py` | regenerates Fig. 1 | runnable |
| `examples/minimal_adapter.py` | minimal item-to-code adapter template | runnable |
| `tools/profile_diagnostics_runtime.py` | local D1-D5 runtime profiler | runnable with local artifacts |
| `tools/autodl_audit_sid/preflight_metric_inputs.py` | local preflight for future metric inputs | runnable |
| `tools/autodl_audit_sid/preflight_card_nurqvae.py` | local CPU preflight for CARD original `nu-rq-vae` source/import/export contract | runnable when the ignored CARD clone is present |
| `tools/autodl_audit_sid/run_d3_ranking_context.py` | bounded D3 prefix-candidate context probe | runnable with local artifacts |
| `tools/autodl_audit_sid/run_d3_ranking_validation.py` | B6 fixed-reranker D3 validation | runnable with local artifacts |
| `tools/autodl_audit_sid/run_rqvae_minimal_reference.py` | RQ-min reference-adapter gate runner | runnable with local artifacts |
| `tools/autodl_audit_sid/run_grid_rqkmeans_direct_export.py` | GRID/RQ-KMeans export path used for B2/B7 rows | runnable with local artifacts and GRID source |
| `tools/autodl_audit_sid/run_qualified_collision_probe.py` | D2 method-inspired mechanism probe | runnable |
| `tools/autodl_audit_sid/run_capacity_budget_sweep.py` | D1/D2/D4/D5 method-inspired mechanism probe | runnable |
| `tools/autodl_audit_sid/run_variable_depth_cost_probe.py` | D5 variable-depth mechanism probe | runnable |
| `docs/THIRD_METHOD_EVIDENCE_GATE.md` | admission rule for any third named tokenizer evidence | inspectable |
| `docs/METHOD_RELEASE_SCOUT.md` | official-release screen for QuaSID/AdaSID/CapsID/DIGER | inspectable |
| `docs/CARD_ORIGINAL_NURQVAE_EVIDENCE_GATE.md` | CARD original route failure report for v0 main evidence | inspectable |
| `docs/DIAGNOSTIC_PROBE_TAXONOMY.md` | D1-D7 diagnostic-probe naming and D6/D7 scope boundary | inspectable |
| `docs/CONTROLLED_STRESSOR_SELECTION.md` | method-inspired mechanism-probe policy and method-coverage boundary | inspectable |
| `docs/QUALIFIED_COLLISION_PROBE.md` | D2 mechanism-probe result | inspectable |
| `docs/CAPACITY_BUDGET_SWEEP.md` | capacity-budget mechanism-probe result | inspectable |
| `docs/VARIABLE_DEPTH_COST_PROBE.md` | variable-depth cost mechanism-probe result | inspectable |
| `docs/D3_RANKING_VALIDATION_MUSICAL.md` | B6 fixed-reranker D3 validation report | inspectable |
| `docs/D3_RANKING_VALIDATION_ALL_BEAUTY.md` | B6 All_Beauty temporal-LOO replication report | inspectable |
| `docs/RQVAE_MINIMAL_REFERENCE_GATE.md` | RQ-min reference-adapter gate report | inspectable |
| `docs/SPORTS_GRID_THIRD_VERTICAL.md` | B7 Sports GRID third-vertical report | inspectable |
| `docs/ADAPTER_TEMPLATE.md` | minimal adapter tutorial and evidence-role boundary | inspectable |
| `docs/PAPER_CONTROLLER_INTEGRATION.md` | paper-writing note for controlled mechanism-probe Table 3 and named-method boundary | inspectable |
| `paper/main.tex`, `paper/main.pdf` | current ACM draft and compiled PDF | inspectable |
| `paper_assets/tables/` | generated CSV/Markdown/LaTeX evidence tables | inspectable/verifiable |
| `paper_assets/tables/table16_runtime_profile.*` | local D1-D5 runtime profile for the Musical bundle | inspectable |
| `paper_assets/references/audit_sid_references.bib` | paper reference file | inspectable |
| `docs/PAPER_STRICT_CLAIM_AUDIT.md` | claim and numeric-audit trail | inspectable |

## Local-Cache Boundary

The full table builder `tools/autodl_audit_sid/build_paper_tables.py` rebuilds
tables from local experiment outputs under `_gate0_artifacts/`, which is
intentionally git-ignored because it contains larger run products and upstream
cache material. Reviewers should use `tools/verify_paper_artifact.py` for clean
checkout verification unless a separate full-artifact data bundle is provided.

## Evidence Roles

- `paper_assets/tables/table1_method_coverage.*`: method/facet coverage and
  claim boundary.
- `paper_assets/tables/table2_musical_diagnostic.*`: same-item Musical case
  study used in the PDF.
- `paper_assets/tables/table3_sanity_controls.*`: metric-sensitivity controls.
- `paper_assets/tables/table4_grid_scale.*`: GRID scale/stability evidence.
- `paper_assets/tables/table5_dact_d6_churn.*`: optional D6 churn evidence.
- `paper_assets/tables/table6_movielens_portability.*`: non-Amazon schema
  smoke evidence.
- `paper_assets/tables/table7_grid_musical_3seed.*`: same-item Musical
  GRID feature-text three-seed stability evidence.
- `paper_assets/tables/table8_qualified_collision_probe.*`: D2
  interaction-qualified aliasing mechanism probe.
- `paper_assets/tables/table9_capacity_budget_sweep.*`: capacity-budget
  mechanism probe across D1/D2/D4/D5.
- `paper_assets/tables/table10_variable_depth_cost_probe.*`: variable-depth
  D5 boundary mechanism probe, paper-optional.
- `paper_assets/tables/table11_d3_ranking_validation.*`: B6 Musical
  fixed-reranker validation table; paper wording must keep the Recall/NDCG
  values scoped to the fixed reranker, not a trained generator.
- `paper_assets/tables/table12_sports_grid_vertical.*`: B7 Sports GRID
  third-vertical portability table; this is a real GRID export row, not a third
  named tokenizer.
- `paper_assets/tables/table13_all_beauty_vertical_d3.*`: B4 All_Beauty
  vertical D3 replication table; category metadata is explicitly marked as a
  coarse fallback.
- `paper_assets/tables/table14_all_beauty_d3_ranking_validation.*`: B6
  All_Beauty fixed-reranker replication table; the split is constructed
  temporal leave-one-out because the local native interactions are splitless.
- `paper_assets/tables/table15_rqvae_minimal_reference.*`: RQ-min full-Musical
  reference-adapter table; this demonstrates an independent adapter path, not
  third named-method coverage.
- `paper_assets/tables/table16_runtime_profile.*`: local D1-D5 runtime profile
  over the Musical artifact bundle; it is operational guidance, not scale
  benchmarking.
- `docs/THIRD_METHOD_EVIDENCE_GATE.md`: do-not-self-implement boundary for a
  third named tokenizer row.
- `docs/METHOD_RELEASE_SCOUT.md`: negative release screen for current B2/B3
  candidates; it keeps QuaSID/AdaSID/CapsID/DIGER out of v0 main evidence.
- `docs/CARD_ORIGINAL_NURQVAE_EVIDENCE_GATE.md`: failure report showing why
  CARD original `nu-rq-vae` cannot enter v0 main evidence from the current
  public repo.
- `docs/CONTROLLED_STRESSOR_SELECTION.md`: policy for keeping method-inspired
  controlled mechanism probes separate from named-method evidence.
- `docs/PAPER_CONTROLLER_INTEGRATION.md`: writing note showing where the
  mechanism-probe results are used in the paper and where the claim boundary is
  preserved.

## Maintenance

New tokenizer adapters should emit the normalized `sid_assignments`,
`item_metadata`, `interactions`, and optional `generator_outputs` tables. New
diagnostics should be added as separate D modules only when they require new
input contracts; otherwise they should extend the existing generated-table
schema.
