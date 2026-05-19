# AUDIT-SID Reviewer Artifact Manifest

Timestamp: 2026-05-19 20:06:30 CST

This manifest is the reviewer-facing public artifact index. It is intentionally
shorter than `MANIFEST.md`, which is the full ARIS provenance ledger.

## Frozen Artifact Entry

- Target venue/track: CIKM 2026 Resource Track
- Review tag: `audit-sid-cikm-resource-v0.1`
- Review branch: `codex/audit-sid-idea-discovery`
- Repository: `https://github.com/jdding/lifecycle-ope-preflight`
- License: MIT, see `LICENSE`

## Public Verification Path

The clean-checkout verification path does not require ignored local caches such
as `_gate0_artifacts/`.

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests
MPLCONFIGDIR=/tmp/audit_sid_mpl python3 tools/paper_figures/generate_audit_sid_pipeline.py
python3 tools/verify_paper_artifact.py
```

The verifier checks the published paper tables, figure, license, quickstart,
BibTeX file, and the exact Table 2 numeric claims used in the paper.

## Public Files

| Path | Role | Clean-checkout status |
|---|---|---|
| `ARTIFACT_QUICKSTART.md` | reviewer command entry point | required |
| `LICENSE` | MIT license | required |
| `requirements.txt` | minimal local verification dependencies | required |
| `src/audit_sid/` | mapping-first interface, adapters, metrics | import/test |
| `tests/` | metric and churn unit tests | runnable |
| `tools/verify_paper_artifact.py` | clean-checkout artifact verifier | runnable |
| `tools/paper_figures/generate_audit_sid_pipeline.py` | regenerates Fig. 1 | runnable |
| `tools/autodl_audit_sid/preflight_metric_inputs.py` | local preflight for future metric inputs | runnable |
| `tools/autodl_audit_sid/preflight_card_nurqvae.py` | local CPU preflight for CARD original `nu-rq-vae` source/import/export contract | runnable when the ignored CARD clone is present |
| `tools/autodl_audit_sid/run_qualified_collision_probe.py` | D2b method-inspired controller | runnable |
| `tools/autodl_audit_sid/run_capacity_budget_sweep.py` | D1/D2/D4/D5a method-inspired controller | runnable |
| `tools/autodl_audit_sid/run_variable_depth_cost_probe.py` | D4/D5a variable-depth controller | runnable |
| `docs/THIRD_METHOD_EVIDENCE_GATE.md` | admission rule for any third named tokenizer evidence | inspectable |
| `docs/METHOD_RELEASE_SCOUT.md` | official-release screen for QuaSID/AdaSID/CapsID/DIGER | inspectable |
| `docs/CARD_ORIGINAL_NURQVAE_EVIDENCE_GATE.md` | CARD original route failure report for v0 main evidence | inspectable |
| `docs/CONTROLLED_STRESSOR_SELECTION.md` | method-inspired controller policy and method-coverage boundary | inspectable |
| `docs/QUALIFIED_COLLISION_PROBE.md` | D2b controller result | inspectable |
| `docs/CAPACITY_BUDGET_SWEEP.md` | capacity-budget controller result | inspectable |
| `docs/VARIABLE_DEPTH_COST_PROBE.md` | variable-depth cost controller result | inspectable |
| `docs/PAPER_CONTROLLER_INTEGRATION.md` | paper-writing note for controlled-stressor Table 3 and named-method boundary | inspectable |
| `paper/main.tex`, `paper/main.pdf` | current ACM draft and compiled PDF | inspectable |
| `paper_assets/tables/` | generated CSV/Markdown/LaTeX evidence tables | inspectable/verifiable |
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
- `paper_assets/tables/table8_qualified_collision_probe.*`: D2b
  interaction-qualified collision controller.
- `paper_assets/tables/table9_capacity_budget_sweep.*`: capacity-budget
  controller across D1/D2/D4/D5a.
- `paper_assets/tables/table10_variable_depth_cost_probe.*`: variable-depth
  D4/D5a boundary controller, paper-optional.
- `docs/THIRD_METHOD_EVIDENCE_GATE.md`: do-not-self-implement boundary for a
  third named tokenizer row.
- `docs/METHOD_RELEASE_SCOUT.md`: negative release screen for current B2/B3
  candidates; it keeps QuaSID/AdaSID/CapsID/DIGER out of v0 main evidence.
- `docs/CARD_ORIGINAL_NURQVAE_EVIDENCE_GATE.md`: failure report showing why
  CARD original `nu-rq-vae` cannot enter v0 main evidence from the current
  public repo.
- `docs/CONTROLLED_STRESSOR_SELECTION.md`: policy for keeping method-inspired
  controllers separate from named-method evidence.
- `docs/PAPER_CONTROLLER_INTEGRATION.md`: writing note showing where the
  controller results are used in the paper and where the claim boundary is
  preserved.

## Maintenance

New tokenizer adapters should emit the normalized `sid_assignments`,
`item_metadata`, `interactions`, and optional `generator_outputs` tables. New
diagnostics should be added as separate D modules only when they require new
input contracts; otherwise they should extend the existing generated-table
schema.
