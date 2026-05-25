# SIDInspector Diagnostics

SIDInspector audits item-to-SID mapping artifacts. It does not train a
tokenizer and does not replace downstream Recall/NDCG evaluation.

## Required Tables

- `sid_assignments`: `item_id`, `sid`, `method`, `dataset`, and one or more
  `sid_level_<k>` columns.
- `item_metadata`: `item_id`; optional `dataset`, `category`, `title`, `brand`,
  and `text`.
- `interactions`: `user_id`, `item_id`; optional `dataset`, `timestamp`, and
  `split`.

## D1-D5 Reports

- D1 utilization: per-level unique-code counts, entropy, Gini, and max code.
- D2 aliasing: full-code and prefix collision counts/rates.
- D3 neighborhood alignment: prefix recall against item co-occurrence
  neighborhoods, with optional category-purity context when `category` exists.
- D4 popularity allocation: SID capacity allocation over head/mid/tail buckets.
- D5 structural cost: SID depth, unique full SIDs, duplicate rate, and active
  prefix counts.

## Optional D6 Churn

Use `python3 -m sidinspector.churn` with two `sid_assignments.parquet` files to
measure refresh-to-refresh SID churn and prefix collision changes.
