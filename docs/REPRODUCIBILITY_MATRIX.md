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
- `rebuildable paper table`: released metric summaries and manifests are direct
  inputs to a deterministic table-generation command. Upstream tokenizer
  training is not rerun.
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
| Table 2 Musical diagnostic profile | `docs/reproducibility/sources/`; `docs/reproducibility/table2_musical_diagnostic.csv` | `python3 tools/build_paper_tables.py --output-dir /tmp/sidinspector_paper_tables` | `/tmp/sidinspector_paper_tables/table2_musical_diagnostic.csv` | CPU seconds | rebuildable paper table from released metric summaries and manifests |
| Table 3 mechanism probes | `docs/reproducibility/sources/`; `docs/reproducibility/table3_probe_calibration.csv` | `python3 tools/build_paper_tables.py --output-dir /tmp/sidinspector_paper_tables` | `/tmp/sidinspector_paper_tables/table3_probe_calibration.csv` | CPU seconds | rebuildable paper table from released controller summaries |
| LETTER official adapter row | official LETTER item-index JSON artifact; `docs/reproducibility/official_adapter_metrics_snapshot.csv` | `python3 -m sidinspector.adapters.letter ... && python3 -m sidinspector.preflight ... && python3 -m sidinspector.metrics ...` | `sid_assignments.parquet`, preflight JSON, D1-D5 CSVs | CPU minutes after downloading upstream artifact | adapter released; upstream artifact required |
| LC-Rec official adapter row | official LC-Rec Instruments JSON artifact; `docs/reproducibility/official_adapter_metrics_snapshot.csv` | `python3 -m sidinspector.adapters.lcrec ... && python3 -m sidinspector.preflight ... && python3 -m sidinspector.metrics ...` | `sid_assignments.parquet`, preflight JSON, D1-D5 CSVs | CPU minutes after downloading upstream artifact | adapter released; upstream artifact required |
| D3/ranking and portability checks | `docs/reproducibility/extension_checks_snapshot.csv`; local `_gate0_artifacts` vertical/downstream/churn paths | `python3 -m sidinspector.downstream_probe --manifest <manifest.csv> --output-dir <probe_output>`; `python3 -m sidinspector.churn --old-sid <old.parquet> --new-sid <new.parquet> --output <d6.csv>` | `downstream_probe_summary.csv`, `downstream_probe_correlations.csv`, `d6_churn*.csv` | CPU minutes for bounded probes | tracked evidence snapshot; raw local artifacts not shipped |

## Paper Table Snapshots

The following tracked snapshots preserve the exact numbers used by the paper:

- `docs/reproducibility/table1_evidence_catalog.csv`
- `docs/reproducibility/table2_musical_diagnostic.csv`
- `docs/reproducibility/table3_probe_calibration.csv`
- `docs/reproducibility/official_adapter_metrics_snapshot.csv`
- `docs/reproducibility/extension_checks_snapshot.csv`
- `docs/reproducibility/rqmin_reference_snapshot.csv`

For Tables 2 and 3, `source_evidence` points to released inputs under
`docs/reproducibility/sources/`. These inputs are compact metric summaries and
run manifests, not tokenizer checkpoints or training caches. The builder makes
every reported table cell obtainable from a clean checkout while preserving
the boundary between table reconstruction and upstream tokenizer retraining.

Other rows may still be snapshot-only or require an upstream official artifact;
their `release_status` states that boundary explicitly.

## Verification

Run:

```bash
python3 tools/build_paper_tables.py --output-dir /tmp/sidinspector_paper_tables
python3 tools/verify_reproducibility_matrix.py
```

This checks that the matrix and tracked evidence snapshots are present,
well-formed, and internally consistent, then reconstructs Tables 2 and 3 and
compares every row with the tracked snapshots. For a full package smoke test,
run:

```bash
python3 tools/verify_package.py
```

The package verifier runs import checks, the toy diagnostic, the reviewer
quickstart, unit tests, and the reproducibility-matrix check.
