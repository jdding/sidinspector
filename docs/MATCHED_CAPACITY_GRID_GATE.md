# Matched-Capacity GRID Gate

Timestamp: 2026-05-20 15:39:08 CST

Purpose: respond to R3's high-severity concern that the main GRID-vs-ReSID
worked example confounds method design with codebook capacity.

## Gate Question

If the GRID feature-text exporter is given a ReSID-like prefix capacity
(`32,1280,1280`), does the high aliasing pressure remain, or does it largely
disappear?

This is a prefix-capacity ablation, not a ReSID reproduction and not a faithful
raw-text TIGER/GRID run.

## Attempted Local Run

Command class:

```bash
PYTHONPATH=src python3 tools/autodl_audit_sid/run_grid_rqkmeans_direct_export.py \
  --grid-dir _gate0_repos/GRID \
  --embeddings _gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/input/item_embeddings.pt \
  --item-ids _gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/input/item_ids.npy \
  --item-metadata _gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/input/item_metadata.parquet \
  --interactions _gate0_artifacts/grid_same_dataset_runs/grid_official_rqkmeans_Musical_Instruments_resid_feature_text_cpu_max23742_20260519_110722/input/interactions.parquet \
  --output-dir _gate0_artifacts/grid_same_dataset_runs/matched_capacity_grid_32_1280_1280_seed42_20260520_153908/grid_export \
  --dataset-name Musical_Instruments \
  --method grid_official_rqkmeans_resid_feature_text_prefix_matched \
  --per-level-widths 32,1280,1280 \
  --batch-size 4096 \
  --steps-per-layer 40 \
  --init-buffer-size 4096 \
  --device cpu \
  --seed 42
```

## Result

Status: `COMPLETED_AUTODL_GPU`.

The local CPU attempt was stopped under `BLOCKED_LOCAL_CPU_STOPLOSS`, then the
same bounded gate was run on AutoDL port 21551 in private screen
`audit_sid_matched_grid_1600`.

Remote execution summary:

- Host: `ssh -p 21551 root@connect.westc.seetacloud.com`
- GPU: RTX 5090, CUDA available.
- Start/end: 2026-05-20 16:38:15--16:38:59 CST.
- Stop-loss check: passed; GPU SM was 97--99% with about 20.8GB allocated.
- Exit: `RUN_EXIT=0`.
- Local result root:
  `_gate0_artifacts/grid_same_dataset_runs/matched_capacity_grid_32_1280_1280_seed42_20260520/grid_export/`

Core metrics:

| Metric | Value |
|---|---:|
| Items | 23,742 |
| Per-level widths | 32 / 1280 / 1280 |
| Unique per-level codes | 32 / 1280 / 1278 |
| Unique full SIDs | 9,874 |
| D2 full-code aliasing rate | 0.778452 |
| D3 L1 co-occurrence prefix recall | 0.079539 |
| D4 tail unique-SID ratio | 0.639064 |
| D5 prefix counts | 32 / 9300 / 9874 |

## Interpretation

R3's capacity critique is partially validated and partially bounded. Increasing
GRID's prefix capacity materially reduces aliasing: unique full SIDs rise from
the original GRID row's about 3.9k to 9,874, and D2 full-code aliasing falls
from about 0.976 to 0.778. However, aliasing does not disappear and the row does
not approach the structurally item-unique ReSID/category-prefix rows.

The paper can now replace the earlier "future work" caveat with a concrete
matched-capacity row. The claim remains conservative: the ablation clarifies
capacity sensitivity; it is not a method ranking, a faithful TIGER/GRID run, or
a ReSID reproduction.

## Next Feasible Paths

1. Keep the matched-capacity row in Table 2 only with the feature-text /
   prefix-capacity-ablation label.
2. Rebuild the PDF and rerun the artifact verifier after any table updates.
3. If a later clean release package is cut, either include this result package
   in the artifact or cite it as local AutoDL provenance rather than public
   reproducibility evidence.
