# DACT Drift Artifact Smoke

Timestamp: 2026-05-19 09:35:06 CST

## Verdict

`LOCAL_SMOKE_PASSED_OPTIONAL_D6`

DACT is useful as optional drift / continual-tokenization artifact evidence for
AUDIT-SID, but it does not replace the Cluster B main line. The current CIKM v0
resource-demo claim remains GRID/ReSID/sanity first; DACT only adds a cheap D6
churn example if page budget and citation verification allow it.

## Source

| Field | Value |
|---|---|
| Repo | `_gate0_repos/DACT` |
| Commit | `c7b4d755dead38f30e876236bad32010ad82082d` |
| Dataset | DACT bundled `Tools` |
| Artifacts | `Tools_0.6_cf.npy`, `Tools_0.7_dact.npy`, `train_0.6.parquet`, `train_0.7.parquet` |
| Output | `_gate0_artifacts/dact_tools_smoke/` |

Command:

```bash
PYTHONPATH=src python3 tools/autodl_audit_sid/run_dact_artifact_smoke.py --output-dir _gate0_artifacts/dact_tools_smoke
```

## Results

| Artifact | Items | Interaction rows used | Unique full SIDs | Full collision groups | Full collision items | Duplicate SID rate |
|---|---:|---:|---:|---:|---:|---:|
| `dact_cf_0.6` | 9,610 | 51,570 | 9,610 | 0 | 0 | 0.000000 |
| `dact_0.7` | 9,885 | 10,818 | 9,882 | 3 | 6 | 0.000303 |

D6 churn from 0.6 to 0.7:

| Prefix depth | Old items | New items | Common items | New-only items | Changed common items | Churn rate on common items |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 9,610 | 9,885 | 9,610 | 275 | 2,271 | 0.236316 |
| 2 | 9,610 | 9,885 | 9,610 | 275 | 2,271 | 0.236316 |
| 3 | 9,610 | 9,885 | 9,610 | 275 | 2,271 | 0.236316 |
| 4 | 9,610 | 9,885 | 9,610 | 275 | 2,271 | 0.236316 |

Interpretation:

- The shared 0.6 -> 0.7 item set has about `23.6%` SID churn.
- Churn is identical at every prefix depth because changed items differ at the
  first SID level.
- The 0.7 artifact has extremely rare full collisions: `6 / 9,885` items.
- This is a useful D6 example for continual-tokenization artifact inspection,
  not evidence that DACT should replace ReSID/CARD/DIGER as the Cluster B
  paper-facing method.

## Code Surfaces

| File | Purpose |
|---|---|
| `src/audit_sid/adapters/dact.py` | normalizes public DACT `.npy` code arrays into `sid_assignments.parquet` |
| `tools/autodl_audit_sid/run_dact_artifact_smoke.py` | runs DACT artifact smoke and D1-D5a metrics |
| `tools/autodl_audit_sid/compute_sid_churn.py` | reusable D6 churn table for two `sid_assignments` files |
| `tests/test_sid_churn.py` | unit coverage for D6 common-item denominator and collision columns |

## Red Lines

Do not claim:

- DACT replaces the current Cluster B evidence route.
- AUDIT-SID has completed same-dataset GRID/ReSID/DACT comparison.
- D6 churn alone proves downstream ranking benefit or harm.

Safe wording:

> As an optional extension, AUDIT-SID can also inspect continual-tokenization
> artifacts. On bundled DACT Tools snapshots, the 0.6 -> 0.7 common-item SID
> churn is 23.6%, while the 0.7 artifact has only rare full collisions. We use
> this as drift-diagnostic evidence, not as a main-method comparison.
