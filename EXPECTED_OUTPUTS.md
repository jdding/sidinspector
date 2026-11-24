# Expected Outputs

| Command | Primary output | Expected verdict / check |
| --- | --- | --- |
| `sidinspector verify-tables` | Rebuilt CIKM Table 2 (7 rows) & Table 3 (3 rows) | Exact row-by-row match with frozen snapshots; exits `0` |
| `sidinspector validate` | SHA-256 manifest audit + package smoke + `pytest` | Final line: `PASS_SIDINSPECTOR_RELEASE_VALIDATION` |
| `sidinspector audit --sid-csv examples/reviewer_quickstart_data/sid_codes.csv --interactions-csv examples/reviewer_quickstart_data/interactions.csv --metadata-csv examples/reviewer_quickstart_data/item_metadata.csv` | Terminal D1–D5 summary (optional JSON & CSVs) | `Items: 12 \| Depth: 3 \| Unique SIDs: 11 \| D2 full aliasing: 0.1667` |
| `sidinspector quickstart` | `examples/reviewer_quickstart_output/` | `preflight_summary.json` + `d1`–`d5a` CSVs |
| `sidinspector demo --port 8765` | `DEMO_READY http://127.0.0.1:8765` | `/health` returns `status=ready`; browser run completes all workflows |
