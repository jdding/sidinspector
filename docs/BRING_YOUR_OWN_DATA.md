# Bring Your Own Mapping Data

SIDInspector audits any exported item-to-SID mapping without modifying or retraining your tokenizer.

## Option 1 · Zero-Install Browser Audit (CSV)

Serve [`index.html`](../index.html) locally (`python3 -m http.server 8766`, or open `https://jdding.github.io/sidinspector/` once `v1.1.0` is published to GitHub Pages) and switch to **Tab 4 · Inspect Your Own Mapping**. Paste CSV text or pick local `.csv` files; all validation and D1–D5 computations run inside Pyodide in your browser and nothing is uploaded. Note: if `interactions.csv` declares an explicit `split` column (`train`/`valid`/`test`), SIDInspector uses `train` rows only and fails closed when zero `train` rows are present.

## Option 2 · One-Command CLI CSV Audit

Prepare a mapping CSV with `item_id` and either `sid_0,sid_1,...`, `sid_level_0,sid_level_1,...`, or a delimited `sid` column:

```csv
item_id,sid_0,sid_1,sid_2
101,4,10,1
102,4,10,2
103,4,11,1
104,4,11,1
```

Optionally attach `interactions.csv` (`user_id,item_id,split`) for D3/D4 and `item_metadata.csv` (`item_id,category,title`) for level-0 category purity:

```sh
sidinspector audit \
  --sid-csv path/to/sid_codes.csv \
  --interactions-csv path/to/interactions.csv \
  --metadata-csv path/to/item_metadata.csv \
  --output-dir runs/my_tokenizer_audit
```

## Option 3 · Full Parquet Pipeline (Large Catalogs)

For large catalogs or multi-method Parquet comparisons, normalize first and run the pandas/pyarrow preflight and metrics modules:

```sh
python3 examples/minimal_adapter.py \
  --input-csv path/to/item_codes.csv \
  --output-dir runs/my_tokenizer \
  --method my_tokenizer \
  --dataset my_dataset

sidinspector preflight \
  --sid-assignments runs/my_tokenizer/sid_assignments.parquet \
  --item-metadata runs/my_tokenizer/item_metadata.parquet \
  --interactions runs/my_tokenizer/interactions.parquet \
  --run-metric-smoke

sidinspector metrics \
  --sid-assignments runs/my_tokenizer/sid_assignments.parquet \
  --item-metadata runs/my_tokenizer/item_metadata.parquet \
  --interactions runs/my_tokenizer/interactions.parquet \
  --output-dir runs/my_tokenizer/diagnostics
```

## Option 4 · LETTER / LC-Rec JSON Indexes

```sh
python3 -m sidinspector.adapters.letter \
  --index-json path/to/Instruments.index.json \
  --item-json path/to/Instruments.item.json \
  --inter-json path/to/Instruments.inter.json \
  --dataset-name Instruments \
  --method letter_official_rqvae \
  --output-dir runs/letter_instruments
```

Use `sidinspector.adapters.lcrec` with the same arguments for LC-Rec index exports, or see [docs/ADAPTER_TEMPLATE.md](ADAPTER_TEMPLATE.md) for writing a custom adapter.

## Option 5 · Compare Two Refresh Revisions (D6 Churn)

```sh
sidinspector churn \
  --old-sid runs/rev_old/sid_assignments.parquet \
  --new-sid runs/rev_new/sid_assignments.parquet \
  --output runs/d6_churn.csv
```
