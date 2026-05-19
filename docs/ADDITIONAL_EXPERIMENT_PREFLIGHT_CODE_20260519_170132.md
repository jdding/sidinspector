# Additional Experiment Preflight Code

Timestamp: 2026-05-19 17:01:32 CST

Purpose: record the subagent-prepared local CPU code path for future additional
AUDIT-SID experiments.

## Added Code

- `tools/autodl_audit_sid/preflight_metric_inputs.py`
- `tests/test_preflight_metric_inputs.py`

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

## Boundaries

- Does not launch GPU or AutoDL jobs.
- Does not make new paper claims.
- Reads full input tables before bounded metric smoke; for very large parquet
  files, a future version should add metadata/sampling-only preflight.

## Verification

Worker verification:

- `python3 -m unittest tests/test_preflight_metric_inputs.py`: 3 tests OK.
- `python3 -m unittest discover -s tests`: 9 tests OK.
- `python3 -m py_compile tools/autodl_audit_sid/preflight_metric_inputs.py`:
  OK.
