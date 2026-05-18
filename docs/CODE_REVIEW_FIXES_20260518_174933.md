# Code Review Fixes

**生成时间**：2026-05-18 17:49:33 CST
**状态**：first sub-agent code review findings partially fixed and smoke-tested

## Review Source

A read-only sub-agent reviewed:

- `src/audit_sid/interface.py`
- `src/audit_sid/adapters/resid.py`
- `src/audit_sid/adapters/sanity.py`
- `src/audit_sid/adapters/grid.py`
- `src/audit_sid/metrics.py`

The review flagged three correctness blockers: interaction semantics, dataset grouping, and item-id coverage validation.

## Fixes Applied

| Finding | Fix |
|---|---|
| ReSID adapter treated `history + target` as events and reused target timestamp for history items | `normalize_interactions()` now emits target-only events for train/valid/test |
| Metrics grouped only by `method` | Metrics now group by `dataset, method` when `dataset` exists |
| No item-id uniqueness/coverage validation | `validate_inputs()` checks duplicate SID rows, duplicate metadata items, null SID/code fields, metadata coverage, and writes `coverage_report.csv` |
| D2 fixed prefix depth at 2 | D2 collision profile now emits prefix depths 1..L |
| GRID `.pt/.npy` adapter silently guessed dense item ids | GRID adapter now requires `--item-ids` unless `--unsafe-assume-dense-zero-indexed` is explicit |
| ReSID codebook columns relied on parquet order | ReSID GAOQ mapping adapter now parses `codebookN_id` with regex and sorts by numeric level |
| `sanity_random_hash` name was misleading because it intentionally created only 256 full SIDs | Renamed to `sanity_mod_collision_hash` |

## Verification

Commands passed:

```bash
PYTHONPATH=src PYTHONPYCACHEPREFIX=/private/tmp/audit_sid_pycache \
python3 -m py_compile \
  src/audit_sid/interface.py \
  src/audit_sid/__init__.py \
  src/audit_sid/adapters/__init__.py \
  src/audit_sid/adapters/resid.py \
  src/audit_sid/adapters/sanity.py \
  src/audit_sid/adapters/grid.py \
  src/audit_sid/metrics.py

PYTHONPATH=src PYTHONPYCACHEPREFIX=/private/tmp/audit_sid_pycache \
python3 -m audit_sid.adapters.resid \
  --dataset-root _gate0_repos/ReSID-dataset/Musical_Instruments/leave_one_out/dataset \
  --output-dir _gate0_artifacts/resid_musical_normalized \
  --dataset-name Musical_Instruments

PYTHONPATH=src PYTHONPYCACHEPREFIX=/private/tmp/audit_sid_pycache \
python3 -m audit_sid.adapters.sanity \
  --item-metadata _gate0_artifacts/resid_musical_normalized/item_metadata.parquet \
  --interactions _gate0_artifacts/resid_musical_normalized/interactions.parquet \
  --output-dir _gate0_artifacts/sanity_musical \
  --dataset-name Musical_Instruments

PYTHONPATH=src PYTHONPYCACHEPREFIX=/private/tmp/audit_sid_pycache \
python3 -m audit_sid.metrics \
  --sid-assignments _gate0_artifacts/sanity_musical/sid_assignments.parquet \
  --item-metadata _gate0_artifacts/resid_musical_normalized/item_metadata.parquet \
  --interactions _gate0_artifacts/resid_musical_normalized/interactions.parquet \
  --output-dir _gate0_artifacts/sanity_musical/metrics
```

## Updated Smoke Facts

| Artifact | Rows | Notes |
|---|---:|---|
| `item_metadata.parquet` | 23,742 | unchanged |
| `interactions.parquet` | 433,164 | target-only events: train 318,612; valid 57,296; test 57,256 |
| `sid_assignments.parquet` | 71,226 | three sanity methods, renamed collision baseline included |

Coverage report:

| Dataset | Method | SID items | Metadata items | Interaction items | Metadata without SID | Interaction without SID |
|---|---|---:|---:|---:|---:|---:|
| `Musical_Instruments` | `sanity_category_prefix` | 23,742 | 23,742 | 23,736 | 0 | 0 |
| `Musical_Instruments` | `sanity_mod_collision_hash` | 23,742 | 23,742 | 23,736 | 0 | 0 |
| `Musical_Instruments` | `sanity_popularity_balanced` | 23,742 | 23,742 | 23,736 | 0 | 0 |

## Remaining Review Debt

D2 is still a collision profile, not a fully matched counterfactual harm estimate. It should be described conservatively until generator outcomes or a controlled proxy are added.
