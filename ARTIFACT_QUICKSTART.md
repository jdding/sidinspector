# Artifact Quickstart

Use Python 3.9+ on CPU (no GPU required). Run commands from the repository root, or install the unified `sidinspector` CLI with `python3 -m pip install -e .`.

The browser workbench ([`index.html`](index.html), served locally via `python3 -m http.server 8766`, or at `https://jdding.github.io/sidinspector/` once `v1.1.0` is published to GitHub Pages) executes the released Python scripts directly in your browser (pinned Pyodide `v314.0.7`, SHA-256 verified against `PACKAGE_MANIFEST.json`) with zero installation and also lets you audit your own CSV files client-side.

See [docs/RESOURCE_CAPABILITIES.md](docs/RESOURCE_CAPABILITIES.md) for what runs standalone from the release versus with upstream tokenizer exports.

## 1. Rebuild and verify CIKM '26 Tables 2 and 3

```sh
sidinspector verify-tables
# or without installing:
python3 tools/verify_reproducibility_matrix.py
```

Rebuilds `table2_musical_diagnostic.csv` and `table3_probe_calibration.csv` from `docs/reproducibility/sources/` into a temporary directory and asserts row-by-row equality against the frozen CIKM '26 snapshots.

## 2. Validate the complete release package

```sh
sidinspector validate
# or without installing:
python3 tools/validate_release.py
```

Verifies every SHA-256 entry in `PACKAGE_MANIFEST.json` and `CHECKSUMS.sha256`, confirms no non-package files are tracked, runs the toy diagnostic, reviewer quickstart, paper-table rebuild, and unit test suite. Expected final line: `PASS_SIDINSPECTOR_RELEASE_VALIDATION`.

## 3. Audit your own item-to-SID CSV in one command

```sh
sidinspector audit \
  --sid-csv examples/reviewer_quickstart_data/sid_codes.csv \
  --interactions-csv examples/reviewer_quickstart_data/interactions.csv \
  --metadata-csv examples/reviewer_quickstart_data/item_metadata.csv \
  --output-dir /tmp/sidinspector_audit
```

Writes `audit_summary.json` plus `d1_utilization.csv` through `d5a_deployment_cost.csv` and prints a concise terminal summary. Works with `item_id,sid_0,sid_1,...`, `item_id,sid_level_0,...`, or `item_id,sid`. See [docs/BRING_YOUR_OWN_DATA.md](docs/BRING_YOUR_OWN_DATA.md) for Parquet and LETTER/LC-Rec JSON indexes.

## 4. Run the full Parquet adapter + preflight + metrics pipeline

```sh
sidinspector quickstart
# or:
python3 examples/run_reviewer_quickstart.py
```

Exercises `examples/minimal_adapter.py`, `sidinspector.preflight`, and `sidinspector.metrics` on the bundled 12-item music slice, writing normalized Parquet tables and CSV diagnostics to `examples/reviewer_quickstart_output/`.

## 5. Launch the local interactive web workbench

```sh
sidinspector demo --port 8765
# or:
python3 tools/serve_demo.py --port 8765
```

Open <http://127.0.0.1:8765> and click **Run all diagnostic workflows** (or switch to the **Inspect Your Own CSV** tab). Every run verifies the SHA-256 manifest in an isolated temporary directory.
