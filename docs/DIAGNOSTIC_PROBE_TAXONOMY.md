# AUDIT-SID Diagnostic Probe Taxonomy

Timestamp: 2026-05-20 01:34:54 CST

## Decision

Use **diagnostic probe** for the D-numbered metric families and **controlled
mechanism probe** for synthetic or method-inspired input rows that calibrate a
diagnostic. Avoid `stressor` and `controller` in paper-facing prose except when
referring to historical file names.

## D1-D7 Names

| ID | Paper name | Input required | Current v0 status | Notes |
|---|---|---|---|---|
| D1 | Utilization | `sid_assignments` | main evidence | code usage, prefix counts, imbalance, dead/underused codes |
| D2 | Aliasing | `sid_assignments`; optional interactions for qualification | main evidence plus mechanism probe | full/prefix SID collisions; not causal downstream harm |
| D3 | Neighborhood alignment | `sid_assignments` + interactions; metadata optional | main evidence | co-occurrence prefix recall; category purity is auxiliary |
| D4 | Popularity allocation | `sid_assignments` + interactions or popularity buckets | main evidence | head/mid/tail capacity and prefix allocation |
| D5 | Structural cost | `sid_assignments` | main evidence | SID length, prefix fan-out, duplicate codes, trie-like expansion; not serving latency |
| D6 | Temporal churn | paired `sid_assignments` snapshots | optional extension evidence | DACT Tools smoke already demonstrates reusable refresh-pair churn |
| D7 | Generation traces | `generator_outputs`, beam traces, or candidate logs | interface hook only | invalid paths, duplicate generated candidates, next-token entropy; not current evidence |

## D6 Decision

D6 is worth keeping now because it is already implemented and has a local DACT
Tools smoke result: common-item churn from Tools 0.6 to 0.7 is 23.6%, and the
0.7 artifact has only rare full-code collisions. This is useful resource
evidence because it shows the adapter contract can audit refresh-pair artifacts.

D6 should **not** move into the main paper table. It is not a replacement for
the GRID/ReSID worked example, and churn does not prove ranking harm or benefit.
The paper should mention D6 as an extension capability and keep the full churn
table in the artifact package.

## D7 Decision

D7 should not be implemented for the current v0 unless a real method artifact
exports generator candidates, beam traces, or per-step scores. A synthetic D7
toy would demonstrate only that the parser can read a file, not that AUDIT-SID
audits a real SID generator. For CIKM v0, D7 stays as an interface hook and
future adapter target.

## Legacy Names

Some existing scripts and CSV files still use `d5a` in filenames or column
groups, for example `d5a_deployment_cost.csv`. Keep those paths stable for
reproducibility. Paper-facing prose should call the same metric family **D5
structural cost**.

## Safe Paper Wording

> AUDIT-SID implements five mapping-level diagnostic probes: D1 utilization,
> D2 aliasing, D3 neighborhood alignment, D4 popularity allocation, and D5
> structural cost. D6 temporal churn is available when paired tokenizer
> snapshots exist, and D7 generation traces are reserved for artifacts that
> expose generated candidates or beam logs.

Avoid:

- "D1-D7 are implemented in v0."
- "D6 is a main method result."
- "D7 is evaluated by synthetic generator outputs."
- "D5 measures serving latency."
