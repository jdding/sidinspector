# RQ-VAE Minimal Reference Gate

生成时间：2026-05-20 21:31:24

状态：PASSED
方法标签：`rqvae_minimal_reference`

## 边界

这是本地 residual-quantization reference exporter；不包含 VAE/generator 训练，也不冒充 TIGER、GRID、ReSID 或 CARD。

## 产物

- gate JSON: `methods/rqvae_minimal_reference/outputs/cpu_full_23742_seed42/audit_result.json`
- output dir: `methods/rqvae_minimal_reference/outputs/cpu_full_23742_seed42`
- sid_assignments: `methods/rqvae_minimal_reference/outputs/cpu_full_23742_seed42/normalized/sid_assignments.parquet`
- metrics: `methods/rqvae_minimal_reference/outputs/cpu_full_23742_seed42/metrics`

## 结论

- items: `23742`
- GPU-worthy: `True`
- condition: Run GPU/full-data only after 2k CPU smoke passes and duplicate_sid_rate < 0.5.

## Full-run summary

- unique full SIDs: `17247`
- duplicate SID rate: `0.2736`
- D2 full-code aliasing: `0.4401`
- D3-L1: `0.0650`
- D4 tail unique-SID ratio: `0.8831`
- D5 prefixes: `32;2368;17247`
