# Resource Capabilities and Evidence Boundaries

| Workflow | Runs from release alone? | Runs in browser (Pyodide)? | Requires external inputs? |
| --- | --- | --- | --- |
| Quickstart D1–D5 on bundled 12-item music slice | Yes | Yes | No |
| CIKM '26 Table 2 & Table 3 deterministic rebuild & row check | Yes | Yes | No |
| Mechanism sensitivity demo (collision injection & 25% D6 churn) | Yes | Yes | No |
| SHA-256 manifest & package integrity validation | Yes | Yes | No |
| Bring-your-own CSV mapping audit (D1–D5 + Table 1 triage) | Yes (user CSV) | Yes (client-side only) | User CSV |
| Large-scale Parquet D1–D6 + fixed-reranker exposure probe | Yes (user Parquet) | No (local CPU CLI) | User or upstream exports |
| Upstream tokenizer retraining (GRID, ReSID, LETTER, LC-Rec) | No | No | Upstream repos & datasets |

## Provenance Boundary

- Compact summaries under `docs/reproducibility/sources/` deterministically reconstruct CIKM Tables 2 and 3.
- Upstream checkpoints, raw Amazon/MovieLens datasets, and large caches remain at their original sources and are excluded from this repository.
