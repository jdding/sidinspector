# AUDIT-SID Reviewer Artifact Manifest

Timestamp: 2026-05-19 17:32:36 CST

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
| `docs/THIRD_METHOD_EVIDENCE_GATE.md` | admission rule for any third named tokenizer evidence | inspectable |
| `docs/METHOD_RELEASE_SCOUT.md` | official-release screen for QuaSID/AdaSID/CapsID/DIGER | inspectable |
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
- `docs/THIRD_METHOD_EVIDENCE_GATE.md`: do-not-self-implement boundary for a
  third named tokenizer row.
- `docs/METHOD_RELEASE_SCOUT.md`: negative release screen for current B2/B3
  candidates; it keeps QuaSID/AdaSID/CapsID/DIGER out of v0 main evidence.

## Maintenance

New tokenizer adapters should emit the normalized `sid_assignments`,
`item_metadata`, `interactions`, and optional `generator_outputs` tables. New
diagnostics should be added as separate D modules only when they require new
input contracts; otherwise they should extend the existing generated-table
schema.
