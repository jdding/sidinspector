# Gate 0A Evidence Matrix

Timestamp: 2026-05-19 03:13:59 CST

## Verdict

`GATE0A_CORE_CONDITIONAL_PASS_RESOURCE_DEMO`

Gate 0A can be closed only under a conservative resource-demo framing:

- Cluster A: real GRID/RQ-KMeans official-module export on Amazon-2023
  `All_Beauty`;
- Cluster B: real ReSID/GAOQ export on ReSID processed Amazon-2023
  `Musical_Instruments`;
- Sanity lower bound: random/collision/category/popularity baselines on
  `Musical_Instruments`;
- D1-D5a available, with D3 upgraded to co-occurrence collaborative alignment.

Gate 0A is not a same-vertical comparative benchmark pass. `Sports_and_Outdoors`
exact balanced ReSID GAOQ was stopped for a CPU-bound `KMeansConstrained`
bottleneck, so any paper claim must avoid implying that ReSID was reproduced on
Sports or that GRID and ReSID were compared on the same category.

## Method Scores

| Method | Cluster | Evidence | Representativeness | Artifact | Diagnostics | Sprint cost | Decision |
|---|---|---|---:|---:|---:|---:|---|
| GRID official-module RQ-KMeans | A | All_Beauty 5k local + AutoDL 20k seeds 42/43/44 + 50k seed42 | 3.0 | 3.0 | 3.0 | 1.0 | main Cluster A evidence |
| ReSID balanced GAOQ | B | Musical_Instruments 23,742 items, real `item_code_mapping.parquet` export | 3.0 | 3.0 | 3.0 | 1.0 | main Cluster B smaller-dataset evidence |
| ReSID exact balanced GAOQ on Sports | B | FAMAE checkpoints exist; GAOQ stopped with no mapping | 3.0 | 1.0 | 0.0 | 0.0 | not a blocker; failure/provenance note only |
| CARD compact feature proxy | B/control | Sports compact e5 proxy metrics exist, but source repair is not faithful CARD Sinkhorn | 1.5 | 2.0 | 3.0 | 1.0 | controlled stressor only, not named CARD evidence |
| DIGER | B/D | public repo available, but release is not sprint-ready for full export | 2.0 | 1.0 | 1.0 | 0.0 | literature/backup only |
| Sanity baselines | sanity | Musical_Instruments same-dataset baselines | 2.0 | 3.0 | 3.0 | 1.0 | required lower bound |

## Same-Dataset Case-Study Evidence

The strongest currently honest case study is ReSID vs sanity baselines on
`Musical_Instruments`, not GRID vs ReSID.

Artifact:

```text
_gate0_artifacts/resid_real_runs/combined_resid_sanity/metrics_d3v2/
```

Key rows:

| Method | D2 full collision | D3 depth-1 mean collab-prefix recall | D3 category purity | D4 head SID unique ratio | D5 duplicate SID rate |
|---|---:|---:|---:|---:|---:|
| ReSID GAOQ | 0.0000 | 0.1535 | 0.5669 | 1.0000 | 0.0000 |
| category-prefix sanity | 0.0000 | 0.4470 | 0.6569 | 1.0000 | 0.0000 |
| mod-collision hash sanity | 1.0000 | 0.0037 | 0.0892 | 0.0324 | 0.9892 |
| popularity-balanced sanity | 0.0860 | 0.3026 | 0.0840 | 0.9639 | 0.0436 |

Interpretation:

- D2/D5 catch the pathological collision baseline.
- D3v2 shows that category-prefix IDs align better with co-occurrence
  neighborhoods than ReSID at depth 1, but this is a metadata taxonomy
  shortcut rather than a learned tokenizer claim.
- ReSID provides collision-free capacity allocation across head/mid/tail, while
  category-prefix provides stronger category/collaborative grouping.
- This is a useful resource-paper diagnostic tradeoff: AUDIT-SID can separate
  collision capacity, collaborative neighborhood alignment, and metadata
  grouping instead of collapsing them into Recall@K.

## Gate Interpretation

Pass if the paper says:

> We demonstrate AUDIT-SID on one canonical RQ semantic-ID exporter, one
> smaller public ReSID/GAOQ export, and controlled sanity tokenizers. The case
> study is diagnostic/toolkit-oriented, not a same-dataset leaderboard.

Fail if the paper says or implies:

- GRID and ReSID are compared as equivalent same-dataset methods;
- CARD compact feature proxy is faithful CARD;
- Sports ReSID balanced GAOQ completed;
- D3 is measured only by category purity.

## Next Local Work

1. Update `METHOD_REPRESENTATIVENESS_AUDIT.md` with the current scores.
2. Update `GATE0_DECISION.md` so Gate 0A is no longer described as blocked by
   D3 proxy, but remains constrained by cross-dataset method evidence.
3. Draft the case-study table from `combined_resid_sanity/metrics_d3v2`.
4. Keep CARD as a controlled stressor/backlog unless an upstream-complete CARD
   path appears.
