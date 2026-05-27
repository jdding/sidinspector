# Validated Adapter Status

SIDInspector counts a named-method adapter as validated only when an official
method source provides or can produce item-level SID codes that join to item
metadata or interactions, and the normalized tables pass preflight plus D1-D5.

## Validated Official Artifacts

### LETTER

- Source: official LETTER repository.
- Artifact shape: JSON item-index mapping plus item metadata and interactions.
- SIDInspector entry point: `python3 -m sidinspector.adapters.letter`.
- Validation status: preflight and D1-D5 pass on official Instruments artifact.

### LC-Rec

- Source: official LC-Rec repository and its linked Google Drive datasets.
- Artifact shape: JSON item-index mapping plus item metadata and interactions.
- SIDInspector entry point: `python3 -m sidinspector.adapters.lcrec`.
- Validation status: preflight and D1-D5 pass on official Instruments artifact.

Example:

```bash
python3 -m sidinspector.adapters.lcrec \
  --index-json path/to/Instruments.index.json \
  --item-json path/to/Instruments.item.json \
  --inter-json path/to/Instruments.inter.json \
  --dataset-name LCRec_Instruments \
  --output-dir runs/lcrec_instruments

python3 -m sidinspector.preflight \
  --sid-assignments runs/lcrec_instruments/sid_assignments.parquet \
  --item-metadata runs/lcrec_instruments/item_metadata.parquet \
  --interactions runs/lcrec_instruments/interactions.parquet \
  --run-metric-smoke

python3 -m sidinspector.metrics \
  --sid-assignments runs/lcrec_instruments/sid_assignments.parquet \
  --item-metadata runs/lcrec_instruments/item_metadata.parquet \
  --interactions runs/lcrec_instruments/interactions.parquet \
  --output-dir runs/lcrec_instruments/diagnostics
```

## Local-Only Adapter Checks

Some method-specific code paths are useful engineering checks but are not
listed here until an official item-code artifact passes the validation
standard above. These local-only records are kept out of the public validated
adapter catalog so they are not mistaken for named-method evidence.
