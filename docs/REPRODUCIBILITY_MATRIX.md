# Resource Reproducibility Matrix

This document connects the paper evidence to the released SIDInspector
resource. It is intentionally stricter than the quickstart: the quickstart
shows that the package runs, while this matrix shows where each paper-facing
evidence block comes from and whether a reviewer can regenerate it from the
release repository, an upstream public artifact, or a saved local manifest.

The machine-readable version is `docs/reproducibility_matrix.csv`. Compact
evidence snapshots are tracked under `docs/reproducibility/`.

## Status Labels

- `fully runnable from release repo`: all inputs are included in the public
  repository and the command can be run directly after installation.
- `adapter released; upstream artifact required`: SIDInspector code is
  released, but the method's official item-index artifact must be downloaded
  from the upstream method release.
- `tracked evidence snapshot`: the paper value is preserved in a tracked CSV,
  while large/raw experiment artifacts are not shipped in the release repo.
- `raw local artifacts not shipped`: large generated artifacts, downloaded
  datasets, or local experiment caches are intentionally omitted from the
  reviewer package.

## Matrix

| Paper evidence | Source artifact | Command | Output | Runtime | Release status |
|---|---|---|---|---|---|
| Release package verifier | tracked package files, examples, docs, tests | `python3 tools/verify_package.py` | package import, toy diagnostic, reviewer quickstart, unit tests | CPU seconds to minutes | fully runnable from release repo |
| Reviewer quickstart | `examples/reviewer_quickstart_data/*.csv` | `python3 examples/run_reviewer_quickstart.py --output-dir /tmp/sidinspector_quickstart` | `/tmp/sidinspector_quickstart/{preflight_summary.json,diagnostics/*.csv}` | CPU seconds | fully runnable from release repo; usability example, not paper-table reproduction |
| Toy diagnostic | `examples/sample_data/*.csv` | `python3 examples/run_toy_diagnostic.py --output-dir /tmp/sidinspector_toy` | `/tmp/sidinspector_toy/*.csv` and normalized parquet files | CPU seconds | fully runnable from release repo |
| Table 1 evidence catalog | `docs/reproducibility/table1_evidence_catalog.csv`; `docs/VALIDATED_ADAPTERS.md` | `python3 tools/verify_reproducibility_matrix.py` | matrix and evidence snapshots validated | CPU seconds | tracked evidence snapshot |
| Table 2 Musical diagnostic profile | `docs/reproducibility/table2_musical_diagnostic.csv`; `docs/reproducibility/rqmin_reference_snapshot.csv`; local `_gate0_artifacts` paths listed per row | `python3 -m sidinspector.metrics --sid-assignments <normalized/sid_assignments.parquet> --item-metadata <item_metadata.parquet> --interactions <interactions.parquet> --output-dir <metrics_dir>` | `d1_utilization.csv`, `d2_collision.csv`, `d3_alignment.csv`, `d4_head_tail.csv`, `d5a_deployment_cost.csv` | CPU minutes from normalized artifacts | tracked evidence snapshot; raw local artifacts not shipped |
| Table 3 mechanism probes | `docs/reproducibility/table3_probe_calibration.csv`; local `_gate0_artifacts/controllers/*` summary CSVs | `python3 tools/verify_reproducibility_matrix.py` | probe snapshot validated | CPU seconds | tracked evidence snapshot; controller raw artifacts not shipped |
| LETTER official adapter row | official LETTER item-index JSON artifact; `docs/reproducibility/official_adapter_metrics_snapshot.csv` | `python3 -m sidinspector.adapters.letter ... && python3 -m sidinspector.preflight ... && python3 -m sidinspector.metrics ...` | `sid_assignments.parquet`, preflight JSON, D1-D5 CSVs | CPU minutes after downloading upstream artifact | adapter released; upstream artifact required |
| LC-Rec official adapter row | official LC-Rec Instruments JSON artifact; `docs/reproducibility/official_adapter_metrics_snapshot.csv` | `python3 -m sidinspector.adapters.lcrec ... && python3 -m sidinspector.preflight ... && python3 -m sidinspector.metrics ...` | `sid_assignments.parquet`, preflight JSON, D1-D5 CSVs | CPU minutes after downloading upstream artifact | adapter released; upstream artifact required |
| D3/ranking and portability checks | `docs/reproducibility/extension_checks_snapshot.csv`; local `_gate0_artifacts` vertical/downstream/churn paths | `python3 -m sidinspector.downstream_probe --manifest <manifest.csv> --output-dir <probe_output>`; `python3 -m sidinspector.churn --old-sid <old.parquet> --new-sid <new.parquet> --output <d6.csv>` | `downstream_probe_summary.csv`, `downstream_probe_correlations.csv`, `d6_churn*.csv` | CPU minutes for bounded probes | tracked evidence snapshot; raw local artifacts not shipped |

## Paper Table Snapshots

The following tracked snapshots preserve the exact numbers used by the paper
without shipping large local artifacts:

- `docs/reproducibility/table1_evidence_catalog.csv`
- `docs/reproducibility/table2_musical_diagnostic.csv`
- `docs/reproducibility/table3_probe_calibration.csv`
- `docs/reproducibility/official_adapter_metrics_snapshot.csv`
- `docs/reproducibility/extension_checks_snapshot.csv`
- `docs/reproducibility/rqmin_reference_snapshot.csv`

The `source_evidence` column records the local raw artifact path used during
paper construction when that artifact is not included in the release repo. Rows
with `raw local artifacts not shipped` should be read as traceable evidence
snapshots, not as a claim that a fresh reviewer checkout contains the full
training/evaluation cache.

## Verification

Run:

```bash
python3 tools/verify_reproducibility_matrix.py
```

This checks that the matrix and tracked evidence snapshots are present,
well-formed, and internally consistent. For a full package smoke test, run:

```bash
python3 tools/verify_package.py
```

The package verifier runs import checks, the toy diagnostic, the reviewer
quickstart, unit tests, and the reproducibility-matrix check.
