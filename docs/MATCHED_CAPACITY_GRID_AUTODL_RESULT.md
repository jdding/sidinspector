# AutoDL Matched-Capacity GRID Result

Time: 2026-05-20 16:43 CST

## Status

`COMPLETED_AUTODL_GPU`.

The user provided a new AutoDL instance:

```bash
ssh -p 21551 root@connect.westc.seetacloud.com
```

Read-only preflight found a private screen already running the planned B2
matched-capacity command:

- screen: `audit_sid_matched_grid_1600`
- remote root: `/root/autodl-tmp/audit-sid-matched-grid-20260520/repo`
- output: `_gate0_artifacts/grid_same_dataset_runs/matched_capacity_grid_32_1280_1280_seed42_20260520/grid_export`
- command: `run_grid_rqkmeans_direct_export.py --per-level-widths 32,1280,1280 --device cuda --seed 42`

No duplicate run was launched. The running process was monitored, completed
with exit code 0, and the result artifacts were pulled back locally.

## Local Evidence Path

```text
_gate0_artifacts/grid_same_dataset_runs/matched_capacity_grid_32_1280_1280_seed42_20260520/
```

Key files:

- `grid_export/grid_export_manifest.json`
- `grid_export/normalized/sid_assignments.parquet`
- `grid_export/metrics/coverage_report.csv`
- `grid_export/metrics/d1_utilization.csv`
- `grid_export/metrics/d2_collision.csv`
- `grid_export/metrics/d3_alignment.csv`
- `grid_export/metrics/d4_head_tail.csv`
- `grid_export/metrics/d5a_deployment_cost.csv`
- `remote_logs/run_matched_grid_1600.log`
- `remote_logs/audit_sid_matched_grid_1600.hardcopy`

## Configuration

| Field | Value |
|---|---|
| Dataset | `Musical_Instruments` |
| Items | 23,742 |
| Method label | `grid_official_rqkmeans_resid_feature_text_prefix_matched` |
| Widths | `32,1280,1280` |
| Steps per layer | 40 |
| Device | CUDA |
| Seed | 42 |
| Remote GPU | RTX 5090 |
| Run window | 2026-05-20 16:38:15--16:38:59 CST |

## Metrics

| Diagnostic | Value |
|---|---:|
| coverage metadata missing | 0 |
| coverage interaction missing | 0 |
| D1 unique level-0 codes | 32 |
| D1 unique level-1 codes | 1,280 |
| D1 unique level-2 codes | 1,278 |
| unique full SIDs | 9,874 |
| duplicate SID rate | 0.584113 |
| D2 full-code aliasing rate | 0.778452 |
| D3 L1 weighted co-occurrence prefix recall | 0.079595 |
| D4 head unique-SID ratio | 0.599899 |
| D4 mid unique-SID ratio | 0.639656 |
| D4 tail unique-SID ratio | 0.639064 |
| D5 prefix counts | `32;9300;9874` |

## Interpretation

The matched-capacity row addresses the R3 W2 critique directly. Giving the GRID
feature-text export a larger `32/1280/1280` budget materially changes the
artifact profile: unique full SIDs rise from 3,749 to 9,874 and D2 full-code
aliasing drops from about 0.9769 to 0.7785.

The critique is therefore real: part of the original GRID-vs-ReSID contrast was
capacity-sensitive. But the caveat is not eliminated. The matched-capacity row
still has substantial full-code aliasing and its D3 L1 neighborhood-alignment
score remains below ReSID and category-prefix controls. This supports the
narrow paper claim that SIDInspector exposes capacity-sensitive artifact profiles,
not a method ranking.

## Paper/Artifact Decision

- Safe to use as a compact worked-example row or artifact note.
- Do not describe it as faithful TIGER/GRID reproduction.
- Do not use it as downstream recommendation-quality evidence.
- Paper-facing label: `GRID ft-cap`.

