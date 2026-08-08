# Adapter Template

SIDInspector adapters are thin export layers. They do not retrain or reproduce a
tokenizer; they normalize an existing item-to-code export into the mapping
contract consumed by D1-D5.

## Minimal Input

For a tokenizer that already provides item-level codes, prepare a CSV with one
row per item:

```text
item_id,sid_0,sid_1,sid_2
101,4,18,7
102,4,21,9
103,8,2,13
```

Run:

```bash
python3 examples/minimal_adapter.py \
  --input-csv path/to/item_codes.csv \
  --output-dir runs/my_tokenizer/normalized \
  --method my_tokenizer \
  --dataset my_dataset
```

The output is:

```text
runs/my_tokenizer/normalized/sid_assignments.parquet
```

with columns:

```text
item_id, sid_level_0, ..., sid_level_L, sid, method, dataset
```

This table is enough for D1, D2, and D5 once item coverage can be checked. D3 and
D4 additionally need interaction histories; metadata enables category and
semantic slices. Paired refresh mappings activate D6, and generator traces
activate D7.

## Optional Side Tables

- `item_metadata`: one row per `item_id`; category or other semantic fields are
  optional and enable metadata slices.
- `interactions`: `user_id`, `item_id`, and optional `split`; train events
  enable D3 co-occurrence neighborhoods and D4 popularity buckets.
- Refresh pair: old and new normalized SID tables with the same item keys for D6.
- Generator outputs: trace rows supplied by an external generator for D7.

The adapter does not implement a metric. It emits normalized tables and
provenance; the shared validator and probe engine do the rest.

## Integration Checklist

1. Export one stable `item_id` and one discrete value per SID level.
2. Run `examples/minimal_adapter.py` or write an equivalent thin normalizer.
3. Record method, dataset, upstream source, and checkpoint or artifact version.
4. Run `python3 -m sidinspector.preflight ... --run-metric-smoke`.
5. Resolve duplicate keys, missing mappings, inconsistent depths, and failed
   side-table joins before reporting metrics.
6. Run D1-D5 and compare the result with the intended codebook budget and
   same-dataset controls.

For a tokenizer that already exposes item-level codes, integration is a schema
normalization task. Checkpoint-only releases require method-specific export
logic upstream and should not be listed as validated named-method coverage
until item-level codes pass preflight.

## Contract Boundary

- A named tokenizer row counts as method evidence only when the item-level export
  comes from that public method path and passes SIDInspector validation.
- A local reference adapter or controlled mechanism probe can test the interface
  or a diagnostic mechanism, but it is not named-method coverage.
- If an upstream repository exposes only checkpoints or intermediate features,
  the adapter should record that provenance and avoid claiming faithful support
  until a validated item-to-code export is available.
