# Maintenance Policy

SIDInspector is maintained as an active open-source diagnostic resource accompanying the published CIKM 2026 Resource Track paper ([DOI: 10.1145/3799682.3840174](https://doi.org/10.1145/3799682.3840174)).

## What Stays Frozen vs. What Evolves

- **Frozen published evidence:** `docs/reproducibility/table2_musical_diagnostic.csv`, `docs/reproducibility/table3_probe_calibration.csv`, and their compact source summaries under `docs/reproducibility/sources/` reproduce the published CIKM 2026 paper verbatim and are never silently overwritten.
- **Actively maintained `1.x` line:** CLI ergonomics, bug fixes, Python version compatibility, new tokenizer format adapters, documentation clarity, and the browser/local diagnostic workbenches evolve through semantic minor/patch releases (`1.1.x`, `1.2.x`, ...).
- **Substantial architectural extensions:** Consumer-facing fixed-budget retrieval controls, trained-beam D7 resolution accounting, C0–C5 / G0–G5 conformance governance, and immutable EvidenceBundles live in the companion journal extension **[SIDScope](https://github.com/jdding/SIDscope)**.

## Compatibility Commitments

- All `v1.0.0` Python imports (`sidinspector.metrics`, `sidinspector.preflight`, `sidinspector.churn`, `sidinspector.downstream_probe`, `sidinspector.adapters.*`) and Parquet schemas remain backward compatible within `1.x`.
- Any metric definition change that alters numerical output would require a new metric column or major version, never a silent overwrite of D1–D5 semantics.

## Release Checklist

Before tagging any `1.x` release:
1. Run `python3 tools/build_release_manifest.py` to refresh `PACKAGE_MANIFEST.json` and `CHECKSUMS.sha256`.
2. Run `python3 tools/validate_release.py` and confirm `PASS_SIDINSPECTOR_RELEASE_VALIDATION`.
3. Verify the local web demo (`sidinspector demo`) and the static Pyodide workbench against a local HTTP server.
4. Keep upstream checkpoints, raw datasets, and unpublished manuscripts excluded from the public repository.

## Issue and Adapter Intake

- Use `.github/ISSUE_TEMPLATE/bug_report.md` for defects or reproducibility mismatches.
- Use `.github/ISSUE_TEMPLATE/adapter_request.md` to propose a new tokenizer export format adapter.
