# Changelog

All notable resource updates to SIDInspector are documented here. The published CIKM '26 paper snapshots (`docs/reproducibility/table2_musical_diagnostic.csv` and `table3_probe_calibration.csv`) remain frozen across all `1.x` releases.

## [1.1.0] - 2026-11-24

### Added
- **Zero-install browser workbench** (`index.html`, `demo/`, `.nojekyll`) running real released Python scripts inside a pinned Pyodide (`v314.0.7`) Web Worker with SHA-256 verification against `PACKAGE_MANIFEST.json`, including:
  - Live D1–D5 mapping diagnostics and interactive depth-1 prefix / full-code alias inspector.
  - Live mechanism sensitivity (collision injection & 25% refresh churn) and in-browser CIKM Table 3 verification.
  - Live in-browser CIKM Table 2 rebuild & verification plus LETTER/LC-Rec/All_Beauty/Sports portability views.
  - **100% client-side Bring-Your-Own-CSV inspector** with interactive CIKM Table 1 triage cards.
- **Local HTTP web demo** (`tools/serve_demo.py`, `demo/local.html`, `sidinspector demo`) with loopback binding, CSP nonces, Host/Origin checks, and isolated temporary-directory execution.
- **Unified `sidinspector` CLI** (`src/sidinspector/cli.py`) exposing `audit`, `quickstart`, `preflight`, `metrics`, `churn`, `probe`, `verify-tables`, `validate`, and `demo`.
- **Standard-library pure-Python diagnostic core** (`src/sidinspector/pure_diagnostics.py`) verified against `sidinspector.metrics` and `sidinspector.churn` for exact numerical parity.
- **Release integrity artifacts**: `PACKAGE_MANIFEST.json`, `CHECKSUMS.sha256`, `RELEASE_STATUS.json`, `tools/build_release_manifest.py`, and `tools/validate_release.py`.
- **Resource governance & onboarding docs**: `ARTIFACT_QUICKSTART.md`, `MAINTENANCE.md`, `EXPECTED_OUTPUTS.md`, `docs/BRING_YOUR_OWN_DATA.md`, `docs/RESOURCE_CAPABILITIES.md`, `docs/LOCAL_DEMO.md`, `docs/RELATION_TO_SIDSCOPE_AND_SIDDUET.md`, and GitHub issue templates.

### Changed
- Updated `README.md` and `CITATION.cff` with the final published CIKM '26 ACM DOI (`10.1145/3799682.3840174`), ISBN (`979-8-4007-2539-5/2026/11`), and Rome, Italy proceedings citation.
- Preserved all `v1.0.0` CLI module paths, Parquet schemas, adapters, and CIKM '26 paper snapshots unchanged.

## [1.0.0] - 2026-08-10 (`sidinspector-cikm2026-resource-v1.0`)

- Initial public resource release accompanying the CIKM 2026 Resource Track paper.
- Mapping-first adapter contract (`sid_assignments`, `item_metadata`, `interactions`), validation preflight, D1–D5 probes, optional D6 churn, fixed-reranker exposure probe, LETTER/LC-Rec/GRID/ReSID/CARD/DACT adapters, and deterministic Table 2 & Table 3 rebuilders.
