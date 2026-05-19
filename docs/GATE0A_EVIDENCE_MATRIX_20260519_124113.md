# Gate 0A Evidence Matrix

Timestamp: 2026-05-19 12:41:13 CST

## Verdict

`GATE0A_CORE_CONDITIONAL_PASS_RESOURCE_DEMO`

Gate 0A can be closed only under a conservative resource-demo framing:

- Cluster A: real GRID/RQ-KMeans official-module export on Amazon-2023
  `All_Beauty`;
- Cluster B: real ReSID/GAOQ export on ReSID processed Amazon-2023
  `Musical_Instruments`;
- Sanity lower bound: random/collision/category/popularity baselines on
  `Musical_Instruments`;
- D1-D5a available, with D3 upgraded to co-occurrence collaborative alignment;
- one same-item-universe Musical diagnostic row is now available for the main
  case-study table.

Gate 0A is not a same-vertical comparative benchmark pass. `Sports_and_Outdoors`
exact balanced ReSID GAOQ was stopped for a CPU-bound `KMeansConstrained`
bottleneck, so any paper claim must avoid implying that ReSID was reproduced on
Sports or that GRID and ReSID were compared on the same category.

Update: the later GRID Musical feature-text run adds a controlled same-item
diagnostic row, but it is not a faithful raw-text TIGER/GRID reproduction and
does not make the work a method leaderboard.

## Method Scores

| Method | Cluster | Evidence | Representativeness | Artifact | Diagnostics | Sprint cost | Decision |
|---|---|---|---:|---:|---:|---:|---|
| GRID official-module RQ-KMeans | A | All_Beauty 5k local + AutoDL 20k seeds 42/43/44 + 50k seed42 + Musical feature-text controlled row | 3.0 | 3.0 | 3.0 | 1.0 | main Cluster A evidence and same-item diagnostic row |
| ReSID balanced GAOQ | B | Musical_Instruments 23,742 items, real `item_code_mapping.parquet` export | 3.0 | 3.0 | 3.0 | 1.0 | main Cluster B smaller-dataset evidence |
| ReSID exact balanced GAOQ on Sports | B | FAMAE checkpoints exist; GAOQ stopped with no mapping | 3.0 | 1.0 | 0.0 | 0.0 | not a blocker; failure/provenance note only |
| CARD compact feature proxy | B/control | Sports compact e5 proxy metrics exist, but source repair is not faithful CARD Sinkhorn | 1.5 | 2.0 | 3.0 | 1.0 | controlled stressor only, not named CARD evidence |
| DIGER | B/D | public repo available, but release is not sprint-ready for full export | 2.0 | 1.0 | 1.0 | 0.0 | literature/backup only |
| Sanity baselines | sanity | Musical_Instruments same-dataset baselines | 2.0 | 3.0 | 3.0 | 1.0 | required lower bound |

## Same-Item-Universe Case-Study Evidence

The strongest currently honest main case study is GRID feature-text vs ReSID
GAOQ on the same ReSID `Musical_Instruments` item universe.

Artifact:

```text
paper_assets/tables/table2_musical_diagnostic.*
```

Key rows:

| System | Items | Unique SID | Duplicate SID rate | Full collision rate | D3 L1 weighted recall | D4 head/mid/tail |
|---|---:|---:|---:|---:|---:|---|
| GRID feature-text | 23742 | 3749 | 0.8421 | 0.9769 | 0.0552 | 0.3530 / 0.3590 / 0.3695 |
| ReSID GAOQ | 23742 | 23742 | 0.0000 | 0.0000 | 0.1535 | 1.0000 / 1.0000 / 1.0000 |

Interpretation:

- D2/D5a expose the collision/capacity pressure of the controlled GRID
  feature-text row.
- D3v2 and D4 show that the two artifacts have different collaborative-prefix
  and head-tail capacity profiles on the same item universe.
- This supports a resource-paper diagnostic tradeoff story, not downstream
  recommender superiority.

Secondary controls:

```text
paper_assets/tables/table3_sanity_controls.*
```

Use the ReSID/sanity controls to show metric non-redundancy if there is space
in the paper, or keep them in the artifact repository.

## Gate Interpretation

Pass if the paper says:

> We demonstrate AUDIT-SID on one canonical RQ semantic-ID exporter, one
> smaller public ReSID/GAOQ export, and controlled sanity tokenizers. The main
> case study is a same-item-universe diagnostic contrast, not a leaderboard.

Fail if the paper says or implies:

- GRID feature-text and ReSID are compared as equivalent faithful same-dataset
  methods;
- CARD compact feature proxy is faithful CARD;
- Sports ReSID balanced GAOQ completed;
- D3 is measured only by category purity.

## Next Local Work

1. Fit Table 1 and Table 2 into the 4-page CIKM Resource body.
2. Generate final BibTeX from `docs/CITATION_AUDIT.md`.
3. Keep CARD as a controlled stressor/backlog unless an upstream-complete CARD
   path appears.
