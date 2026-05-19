# AUDIT-SID Artifact Quickstart

This file is the reviewer-facing quickstart for the CIKM 2026 Resource draft.

## Resource URL

Review branch:

```text
https://github.com/jdding/lifecycle-ope-preflight/tree/codex/audit-sid-idea-discovery
```

License: MIT, see `LICENSE`.

## Local Verification

From the repository root:

```bash
python3 -m unittest tests/test_metrics.py tests/test_sid_churn.py
PYTHONPYCACHEPREFIX=/private/tmp/sec_phrase_pycache \
  python3 -m py_compile \
  tools/autodl_audit_sid/build_paper_tables.py \
  tools/paper_figures/generate_audit_sid_pipeline.py
MPLCONFIGDIR=/private/tmp/sec_phrase_mpl \
  python3 tools/paper_figures/generate_audit_sid_pipeline.py
python3 tools/autodl_audit_sid/build_paper_tables.py
```

Expected outputs:

- `paper/figures/fig1_audit_sid_pipeline.pdf`
- `paper_assets/tables/table1_method_coverage.csv`
- `paper_assets/tables/table2_musical_diagnostic.csv`
- `paper_assets/tables/table3_sanity_controls.csv`
- `paper_assets/tables/table4_grid_scale.csv`
- `paper_assets/tables/table5_dact_d6_churn.csv`
- `paper_assets/tables/table6_movielens_portability.csv`

## Paper-Facing Evidence

- Table 1 is the method/facet coverage matrix.
- Table 2 is the same-item Musical diagnostic profile.
- Table 3 is the reviewer action checklist.
- Auxiliary tables under `paper_assets/tables/` are artifact-repository
  evidence for sanity controls, GRID scale checks, D6 churn, and MovieLens
  portability. These are not numbered as main-paper tables.

## Boundary

The artifact audits item-to-SID tokenizer mappings. It does not claim a new
tokenizer, downstream ranking superiority, faithful full TIGER reproduction, or
industrial online-serving impact.
