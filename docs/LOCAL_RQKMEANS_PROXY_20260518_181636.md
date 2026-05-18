# Local RQ-KMeans Feature-Proxy Baseline

**生成时间**：2026-05-18 18:16:36 CST
**状态**：local canonical-style proxy baseline generated for toolkit development

## Purpose

This baseline supports local AUDIT-SID toolkit development while GRID/CARD public implementation export remains unresolved.

It is a residual MiniBatchKMeans baseline over normalized ReSID item metadata features:

- `store_id`;
- `category_l1`;
- `category_l2`;
- `category_l3`.

It is not a substitute for a public GRID/TIGER-style implementation in Gate 0.

## Command

```bash
PYTHONPATH=src PYTHONPYCACHEPREFIX=/private/tmp/audit_sid_pycache \
python3 -m audit_sid.baselines.rqkmeans \
  --item-metadata _gate0_artifacts/resid_real_runs/normalized_resid_gaoq_1epoch/item_metadata.parquet \
  --output-dir _gate0_artifacts/local_rqkmeans_feature_proxy \
  --dataset-name Musical_Instruments \
  --widths 32,40,19
```

## Output

| Artifact | Rows | Notes |
|---|---:|---|
| `_gate0_artifacts/local_rqkmeans_feature_proxy/sid_assignments.parquet` | 23,742 | `local_rqkmeans_feature_proxy`, 3 SID levels |

## Diagnostic Summary

Compared in `_gate0_artifacts/resid_real_runs/combined_resid_sanity_rqproxy/metrics/`.

| Method | SID length | Unique SID | Duplicate SID rate | Prefix counts | Level-0 category purity |
|---|---:|---:|---:|---|---:|
| `local_rqkmeans_feature_proxy` | 3 | 2,229 | 0.9061 | `32;730;2229` | 0.3816 |
| `resid_gaoq` | 3 | 23,742 | 0.0000 | `32;1280;23742` | 0.5669 |

## Interpretation

The proxy is useful as a stressor: with the same nominal width/depth as ReSID, it leaves substantial full-SID collisions. This helps validate that D2/D5a can distinguish a weak canonical-style quantizer from ReSID/GAOQ.

Do not claim this as GRID/TIGER reproducibility. The remaining Gate 0 public-implementation blocker is still Cluster A: GRID/RQ-VAE/RKMeans or CARD must export a real mapping.

## Notes

Scikit-learn emitted local numerical warnings during MiniBatchKMeans initialization, but the command completed and produced a valid SID table. Treat this baseline as a proxy only.
