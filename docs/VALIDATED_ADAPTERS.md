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

## Adapter-Ready But Not Faithful Evidence Yet

### CARD

- Source: official CARD repository.
- Artifact shape expected by SIDInspector: generated `.npy` code array plus
  explicit item ids.
- SIDInspector entry point: `python3 -m sidinspector.adapters.card`.
- Validation status: the adapter path and D1-D5 pass on a CARD-compatible local
  smoke artifact. The official repository currently provides a full
  raw-data-to-code pipeline rather than a ready item-code mapping/checkpoint
  bundle in the cloned repository, so this should not be described as faithful
  CARD evidence until an official generated-code artifact is produced and
  joined.

Example:

```bash
python3 -m sidinspector.adapters.card \
  --codes-path path/to/card_codes.npy \
  --item-ids path/to/card_codes_item_ids.npy \
  --dataset-name CARD_Beauty \
  --method card_nurqvae \
  --output-dir runs/card_beauty
```

If no explicit item-id file is available, the adapter requires
`--unsafe-assume-dense-item-ids` before using row order as item identity.
