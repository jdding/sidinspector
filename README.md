# SIDInspector

SIDInspector is a small Python toolkit for auditing semantic-ID tokenizer
exports before training or evaluating a downstream generative recommender. It
does not train a tokenizer. It checks an existing `item_id -> SID` mapping plus
item metadata and interactions.

## What It Reports

- D1 utilization: per-level code usage, entropy, and imbalance.
- D2 aliasing: full-code and prefix collision profile.
- D3 neighborhood alignment: whether SID prefixes recover interaction
  co-occurrence neighborhoods.
- D4 popularity allocation: head/mid/tail capacity allocation.
- D5 structural cost: SID length, unique full IDs, and active prefix counts.
- D6 churn: optional refresh-to-refresh SID stability.

## Install

```bash
python3 -m pip install -e .
```

This installs the `sidinspector` package from the repository's `src/` layout.

## Run The Bundled Smoke Example

```bash
python3 examples/run_toy_diagnostic.py
```

Expected final line:

```text
Wrote SIDInspector toy diagnostic outputs to .../examples/toy_output
```

The example writes normalized parquet inputs and D1-D5 CSV reports under
`examples/toy_output/`.

## Reviewer Quickstart

The reviewer quickstart uses a small music-like export slice and exercises the
same command path a new adapter user would run: adapter normalization,
preflight validation, and D1-D5 CSV generation.

```bash
python3 examples/run_reviewer_quickstart.py
```

Expected outputs:

```text
examples/reviewer_quickstart_output/preflight_summary.json
examples/reviewer_quickstart_output/diagnostics/d1_utilization.csv
examples/reviewer_quickstart_output/diagnostics/d2_collision.csv
examples/reviewer_quickstart_output/diagnostics/d3_alignment.csv
examples/reviewer_quickstart_output/diagnostics/d4_head_tail.csv
examples/reviewer_quickstart_output/diagnostics/d5a_deployment_cost.csv
```

This quickstart is a usability example, not a reproduction of the paper tables.

## Use Your Own Tokenizer Export

If your tokenizer already exports one row per item:

```csv
item_id,sid_0,sid_1,sid_2
1,12,3,91
2,12,8,17
```

normalize it:

```bash
python3 examples/minimal_adapter.py \
  --input-csv path/to/item_codes.csv \
  --output-dir runs/my_tokenizer \
  --method my_tokenizer \
  --dataset my_dataset
```

Prepare `item_metadata.parquet` and `interactions.parquet`, then run:

```bash
python3 -m sidinspector.preflight \
  --sid-assignments runs/my_tokenizer/sid_assignments.parquet \
  --item-metadata runs/my_tokenizer/item_metadata.parquet \
  --interactions runs/my_tokenizer/interactions.parquet \
  --run-metric-smoke

python3 -m sidinspector.metrics \
  --sid-assignments runs/my_tokenizer/sid_assignments.parquet \
  --item-metadata runs/my_tokenizer/item_metadata.parquet \
  --interactions runs/my_tokenizer/interactions.parquet \
  --output-dir runs/my_tokenizer/diagnostics
```

See `docs/ADAPTER_TEMPLATE.md` for the required table contract.

## Development Checks

```bash
python3 -m pip install -e .
python3 -m unittest discover -s tests
python3 tools/verify_package.py
```

`tools/verify_package.py` checks package importability, the toy diagnostic, the
reviewer quickstart, and unit tests from a clean checkout.
