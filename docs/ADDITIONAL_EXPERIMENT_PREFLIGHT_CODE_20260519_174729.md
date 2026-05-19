# Additional Experiment Preflight Code

Timestamp: 2026-05-19 17:47:29 CST

Purpose: record the subagent-prepared local CPU code path for future additional
AUDIT-SID experiments.

## Added Code

- `tools/autodl_audit_sid/preflight_metric_inputs.py`
- `tests/test_preflight_metric_inputs.py`
- `tools/autodl_audit_sid/preflight_card_nurqvae.py`
- `tests/test_preflight_card_nurqvae.py`

The script validates the AUDIT-SID metric input contract before a future
method/artifact is allowed into D1-D5a diagnostics:

- `sid_assignments`;
- `item_metadata`;
- `interactions`.

It supports `parquet`, `csv`, `json`, `jsonl`, and `ndjson` inputs. It checks
required columns, empty tables, join coverage, and optionally runs a bounded
D1-D5a metric smoke summary.

## Intended Use

This is a pre-experiment gate, not a new result table. Use it before adding a
third named tokenizer or any new local/GPU experiment:

```bash
python3 tools/autodl_audit_sid/preflight_metric_inputs.py \
  --sid-assignments path/to/sid_assignments.parquet \
  --item-metadata path/to/item_metadata.parquet \
  --interactions path/to/interactions.parquet \
  --run-metric-smoke \
  --output-json _gate0_artifacts/local_preflight_summary.json
```

For the CARD original `nu-rq-vae` route, use:

```bash
python3 tools/autodl_audit_sid/preflight_card_nurqvae.py \
  --card-dir _gate0_repos/CARD \
  --run-synthetic-export \
  --work-dir _gate0_artifacts/card_nurqvae_preflight \
  --output-json _gate0_artifacts/card_nurqvae_preflight/preflight_card_nurqvae.json
```

## Boundaries

- Does not launch GPU or AutoDL jobs.
- Does not make new paper claims.
- The CARD preflight checks source/import/export contracts only. It now also
  flags that the official CARD tree is missing required quantizer modules, so
  local compatibility repair is not faithful named-method evidence.
- Reads full input tables before bounded metric smoke; for very large parquet
  files, a future version should add metadata/sampling-only preflight.

## Verification

Worker verification:

- `python3 -m unittest tests/test_preflight_metric_inputs.py`: 3 tests OK.
- `python3 -m unittest discover -s tests`: 9 tests OK.
- `python3 -m py_compile tools/autodl_audit_sid/preflight_metric_inputs.py`:
  OK.

CARD original route worker verification:

- `python3 -m unittest tests/test_preflight_card_nurqvae.py`: 3 tests OK.
- `python3 -m unittest discover -s tests`: 12 tests OK.
- `python3 tools/autodl_audit_sid/preflight_card_nurqvae.py --card-dir
  _gate0_repos/CARD`: source/import/export contract passed locally.
- Synthetic export on CPU preserved `ItemID` and emitted a `(6, 2)` code
  matrix. The official-source audit reports `local_repair_required`, so this is
  still preflight evidence, not paper evidence.
