# AUDIT-SID Artifact Quickstart

Timestamp: 2026-05-19 17:32:36 CST

This file is the reviewer-facing quickstart for the CIKM 2026 Resource draft.

## Resource URL

Pinned review tag:

```text
https://github.com/jdding/lifecycle-ope-preflight/tree/audit-sid-cikm-resource-v0.1
```

Review branch:

```text
https://github.com/jdding/lifecycle-ope-preflight/tree/codex/audit-sid-idea-discovery
```

License: MIT, see `LICENSE`.

Tested local environment: Python 3.9 on macOS. The clean-checkout verifier uses
only the dependencies in `requirements.txt` plus the Python standard library.

## Clean-Checkout Verification

The default reviewer path verifies the public package without ignored local
experiment caches such as `_gate0_artifacts/`.

```bash
git clone --branch audit-sid-cikm-resource-v0.1 --depth 1 \
  https://github.com/jdding/lifecycle-ope-preflight.git audit-sid
cd audit-sid
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests
MPLCONFIGDIR=/tmp/audit_sid_mpl \
  python3 tools/paper_figures/generate_audit_sid_pipeline.py
python3 tools/verify_paper_artifact.py
```

Expected final line:

```text
AUDIT-SID public artifact verification passed.
```

Typical runtime on a laptop is under one minute after dependencies are
installed.

## Local Full-Artifact Rebuild

This path is for authors or reviewers who also have the ignored local
experiment outputs under `_gate0_artifacts/`. It rebuilds the paper tables from
run artifacts rather than checking the published CSVs.

```bash
PYTHONPYCACHEPREFIX=/private/tmp/sec_phrase_pycache \
  python3 -m py_compile \
  tools/autodl_audit_sid/build_paper_tables.py \
  tools/autodl_audit_sid/preflight_metric_inputs.py \
  tools/autodl_audit_sid/preflight_card_nurqvae.py \
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

## Troubleshooting

- If `build_paper_tables.py` cannot find `_gate0_artifacts/`, use the
  clean-checkout verification path above. The full rebuild path depends on
  local experiment caches that are not committed to git.
- If matplotlib cannot write its cache, set `MPLCONFIGDIR=/tmp/audit_sid_mpl`.
- If Python bytecode cache writes are blocked, set
  `PYTHONPYCACHEPREFIX=/tmp/audit_sid_pycache`.
- `tests/test_preflight_card_nurqvae.py` skips automatically when the ignored
  upstream CARD clone is absent. When `_gate0_repos/CARD` is present, it checks
  only the original source/import/export contract; it does not make CARD a
  paper evidence row.
