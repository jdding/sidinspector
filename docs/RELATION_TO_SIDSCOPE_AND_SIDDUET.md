# Relationship to SIDScope and SIDDuet

SIDInspector, SIDScope, and SIDDuet form a coherent three-resource Semantic-ID diagnostic family, each addressing a distinct research and engineering boundary:

| Dimension | **SIDInspector** (CIKM '26) | **SIDScope** (TOIS under review) | **SIDDuet** (Search & Rec) |
| --- | --- | --- | --- |
| **Inspected object** | Single-task `item_id -> SID` mapping (+ optional metadata/interactions/refresh) | Reusable SID interface spanning mappings, prefix exposure controls, trained generator traces (D7), and refresh handoffs (D6) | Shared SID mapping joined with paired **search vs. recommendation** task observations `(S_i, R_i)` |
| **Core probes** | D1 utilization, D2 aliasing, D3 neighborhood alignment, D4 popularity allocation, D5 structural cost, optional D6 churn | D1–D5 + `A_b` vs global singleton `S_b`, fixed-budget permutation controls, D7 resolver comparison, D6 4-gate handoff | Per-group allocation JSD, disjoint task leaders, band-matched & exact-total count-matched references, temporal pooling |
| **Governance / packaging** | Mapping-first contract, preflight gate, SHA-256 manifest, CLI + Pyodide workbench | C0–C5 & G0–G5 conformance, Adapter SDK 1.0, 46 JSON schemas, immutable EvidenceBundles, CLI + Pyodide workbench | Paired-observation contracts, RoleMapRecord schema, SHA-256 manifest, CLI + Pyodide workbench |
| **When to start here** | Fast pre-training audit of any exported item-to-SID table | Rigorous consumer evaluation, beam resolution, refresh handoff, or adapter conformance | Auditing shared SIDs deployed across both search and recommendation |

## Compatibility

- SIDScope preserves the `sidinspector` Python import path for backward compatibility while adding the curated `sidscope` facade and CLI.
- All three resources ship standalone CPU verifiers, SHA-256 release manifests, and zero-install Pyodide browser workbenches.
