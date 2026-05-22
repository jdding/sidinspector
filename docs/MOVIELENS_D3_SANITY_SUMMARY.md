# SIDInspector MovieLens D3 Sanity Summary

Timestamp: 2026-05-20 18:18:54 CST

## Verdict

The existing MovieLens portability smoke is sufficient for a sanity D3 summary.
No rerun was needed, and no raw MovieLens archive was copied into the repository.

This result supports only non-Amazon schema/probe portability for SIDInspector's
mapping-level diagnostics. It is not a named SID tokenizer benchmark, not a
learned-tokenizer result, and not downstream Recall/NDCG validation.

Safe claim:

> SIDInspector's D1-D5/D3 metric pipeline can ingest a non-Amazon MovieLens
> schema and distinguish deterministic sanity SID assignments with complete
> item coverage.

## Artifact

- Local output:
  `_gate0_artifacts/movielens_portability_smoke/ml25m_1mratings_10kitems/`
- Script:
  `tools/autodl_audit_sid/run_movielens_portability_smoke.py`
- Metrics:
  `_gate0_artifacts/movielens_portability_smoke/ml25m_1mratings_10kitems/metrics/`
- SID assignments:
  `_gate0_artifacts/movielens_portability_smoke/ml25m_1mratings_10kitems/sanity/sid_assignments.parquet`

The external-disk precheck found MovieLens 20M CSV files under
`/Volumes/TU280Pro/Research/DataSet/ml-20m/`,
`/Volumes/TU280Pro/Research/Dataset/ml-20m/`, and
`/Volumes/TU280Pro/Research/dataset/ml-20m/`, but the existing target artifact
was already complete, so no external input was reread.

## Input Footprint

| Field | Value |
|---|---:|
| Dataset label | `MovieLens_25M_smoke` |
| Metadata items | 10,000 |
| Interaction items | 10,000 |
| Interaction rows after item filtering | 964,624 |
| Users | 6,747 |
| Primary genres | 19 |
| SID assignment rows | 30,000 |

Coverage report:

| Method | SID items | Metadata items | Interaction items | Missing metadata | Missing interactions |
|---|---:|---:|---:|---:|---:|
| category-prefix | 10,000 | 10,000 | 10,000 | 0 | 0 |
| mod-collision hash | 10,000 | 10,000 | 10,000 | 0 | 0 |
| popularity-balanced | 10,000 | 10,000 | 10,000 | 0 | 0 |

## Key D1-D5/D3 Numbers

| Method | D1 L1 unique | D2 full collision rate | D3 L1 weighted | D3 L1 category purity | D4 tail unique ratio | D5 unique SID | D5 duplicate SID rate | Prefix counts |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| category-prefix | 19 | 0.0000 | 0.2788 | 1.0000 | 1.0000 | 10,000 | 0.0000 | `19;19;19;10000` |
| popularity-balanced | 4 | 0.0350 | 0.7698 | 0.2693 | 0.9889 | 9,824 | 0.0176 | `4;1024;9824;9824` |
| mod-collision hash | 256 | 1.0000 | 0.0038 | 0.3045 | 0.0768 | 256 | 0.9744 | `256;256;256;256` |

D3 configuration: co-occurrence reference, top-k 20, 68 users used, 241,371
pair events, and 1,859 collaborative items.

## Interpretation

- The portability smoke has complete coverage for all three sanity methods,
  so the result is usable as a schema/probe sanity summary.
- The genre/category-prefix control is perfectly category-pure at level 0 and
  collision-free at full depth, but its D3 L1 weighted neighborhood alignment
  is moderate at 0.2788.
- The popularity-balanced control has the strongest D3 L1 weighted alignment
  at 0.7698 while keeping low full-SID duplication, but its level-0 category
  purity is low because it intentionally groups by popularity rather than genre.
- The mod-collision hash control is the negative sanity check: it has full-code
  collision rate 1.0000, only 256 unique full SIDs, duplicate SID rate 0.9744,
  and near-zero D3 L1 weighted alignment at 0.0038.

## Claim Boundary

This MovieLens summary can be cited as non-Amazon portability evidence for the
SIDInspector input schema and D1-D5/D3 probes. It must not be used to claim:

- MovieLens learned SID tokenizer quality.
- Named-method coverage beyond deterministic sanity assignments.
- Amazon-to-MovieLens transfer quality.
- D3 validity as Recall@K/NDCG or trained recommender performance.
- Any use of Huawei internal data, business logs, or proprietary implementation
  details.

## Validation

Lightweight validation completed on 2026-05-20:

```bash
python3 /Users/timber/aris-source/tools/axiomdesk_run.py \
  --project /Users/timber/Documents/Sec_phrase -- \
  python3 - <<'PY'
from pathlib import Path
import pandas as pd
base=Path('_gate0_artifacts/movielens_portability_smoke/ml25m_1mratings_10kitems')
metrics=base/'metrics'
required=['coverage_report.csv','d1_utilization.csv','d2_collision.csv','d3_alignment.csv','d4_head_tail.csv','d5a_deployment_cost.csv']
for name in required:
    pd.read_csv(metrics/name)
coverage=pd.read_csv(metrics/'coverage_report.csv')
assert (coverage['metadata_without_sid']==0).all()
assert (coverage['interaction_without_sid']==0).all()
pd.read_parquet(base/'input/item_metadata.parquet')
pd.read_parquet(base/'input/interactions.parquet')
pd.read_parquet(base/'sanity/sid_assignments.parquet')
PY
```

Observed validation summary: all six metric CSV files loaded, all three parquet
tables loaded, and `coverage_gap_total=0`.
