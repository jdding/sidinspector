# SIDInspector

**Mapping-first diagnostics for Semantic-ID tokenizer artifacts (CIKM '26 Resource Track).**

[Live Browser Demo](https://jdding.github.io/sidinspector/) |
[Paper (ACM DOI)](https://doi.org/10.1145/3799682.3840174) |
[Preprint (arXiv)](https://arxiv.org/abs/2606.10375) |
[SIDScope (TOIS Extension)](https://github.com/jdding/SIDscope) |
[MIT License](LICENSE)

SIDInspector (`v1.1.0`) is an open-source diagnostic toolkit and reproducibility package for inspecting exported `item_id -> SID` tokenizer artifacts **before** training or evaluating a downstream generative recommender. Without retraining a tokenizer, SIDInspector validates the item-code contract and runs three core diagnostic workflows:

| Workflow | Core question | Entry point |
| --- | --- | --- |
| **1. Mapping Audit (D1–D5)** | Are all items mapped, how concentrated is codebook usage, which leaves collide, do prefixes recover co-occurrence neighbors, and is tail capacity compressed? | `sidinspector audit` · [Diagnostics](docs/DIAGNOSTICS.md) |
| **2. Mechanism & Churn Probes (D2/D4/D5/D6)** | Do diagnostics react to qualified aliasing, head-reserved capacity, variable depth, and refresh-to-refresh mapping churn? | `sidinspector churn` · [Probe guide](docs/PROBE_INTERPRETATION.md) |
| **3. Exposure & CIKM '26 Benchmark Replay** | How do released mappings compare on a fixed item universe, and does prefix alignment track candidate exposure? | `sidinspector verify-tables` · `sidinspector probe` |

See [what this release supports](docs/RESOURCE_CAPABILITIES.md) for package-only, browser-only, and own-data workflows, and [how SIDInspector relates to SIDScope and SIDDuet](docs/RELATION_TO_SIDSCOPE_AND_SIDDUET.md).

## Try it online (zero install)

Open the [live browser workbench](https://jdding.github.io/sidinspector/) to run SIDInspector directly in your browser using a pinned standard-library Pyodide runtime (`v314.0.7`):

- **Tab 1 · Mapping Audit (D1–D5):** Executes real Python D1–D5 diagnostics on the bundled music-like fixture with an interactive depth-1 prefix and full-code alias inspector.
- **Tab 2 · Mechanism Controls & D6 Churn:** Demonstrates live collision injection and 25% refresh churn on the fixture, and runs `tools/build_paper_tables.py` live to verify CIKM Table 3.
- **Tab 3 · Published CIKM '26 Benchmark:** Rebuilds and row-checks CIKM Table 2 across all seven same-item Musical profiles (23,742 items) plus LETTER/LC-Rec, All_Beauty, Sports, and fixed-reranker snapshots.
- **Tab 4 · Inspect Your Own Mapping (BYO CSV):** Paste or pick a local `item_id,sid_0,sid_1,...` CSV (plus optional interactions and metadata) to run preflight, D1–D5, and Table 1 triage cards **100% client-side** — nothing leaves your browser.

All executed scripts and source tables are SHA-256 verified against `PACKAGE_MANIFEST.json` before execution.

## Install and Quickstart

The entire toolkit is CPU-only (Python 3.9+). Pure-CSV audits (`sidinspector audit`), table verification, and the local web demo run with the Python standard library; Parquet adapters and the full pandas/pyarrow pipeline install via `pip install -e .`.

```sh
git clone https://github.com/jdding/sidinspector.git
cd sidinspector
python3 -m pip install -e .

# 1. Rebuild & verify CIKM '26 Tables 2 & 3 from compact sources
sidinspector verify-tables

# 2. Run SHA-256 manifest integrity check, quickstart, and test suite
sidinspector validate

# 3. Audit a CSV mapping directly (no manual normalization needed)
sidinspector audit \
  --sid-csv examples/reviewer_quickstart_data/sid_codes.csv \
  --interactions-csv examples/reviewer_quickstart_data/interactions.csv \
  --metadata-csv examples/reviewer_quickstart_data/item_metadata.csv \
  --output-dir /tmp/sidinspector_audit

# 4. Launch the local browser workbench
sidinspector demo --port 8765
```

All v1.0 CIKM camera-ready commands (`examples/run_reviewer_quickstart.py`, `python3 -m sidinspector.preflight`, `python3 -m sidinspector.metrics`, `tools/verify_package.py`) remain fully supported for backward compatibility. See [ARTIFACT_QUICKSTART.md](ARTIFACT_QUICKSTART.md) and [docs/BRING_YOUR_OWN_DATA.md](docs/BRING_YOUR_OWN_DATA.md).

## Measured CPU Runtime and Memory

Single-machine CPU benchmarks (macOS arm64, no GPU required; measured in `v1.1.0`):

| Workload | Scale | Wall time | Peak RSS |
| --- | --- | ---: | ---: |
| `sidinspector verify-tables` | CIKM Tables 2 & 3 + reproducibility matrix | 0.08 s | 15 MiB |
| `sidinspector audit` (quickstart CSV) | 12 items, D1–D5 pure-Python CSV | 0.05 s | 16 MiB |
| `sidinspector audit` (synthetic 20k CSV) | 20,000 items, 50,000 interactions, D1–D5 | 0.54 s | 124 MiB |
| `sidinspector validate` | SHA-256 manifest + package smoke + unit tests | 3.75 s | 99 MiB |

## Relationship to SIDScope and SIDDuet

SIDInspector is the published **CIKM '26** mapping-first foundation of a three-resource Semantic-ID diagnostic family:

| Resource | Primary Question | Scope & Status |
| --- | --- | --- |
| **SIDInspector** (this repo) | Is an exported `item_id -> SID` mapping structurally healthy (D1–D5) and stable across refreshes (D6) before generator training? | Published at **CIKM '26 Resource Track** (`10.1145/3799682.3840174`). Frozen paper evidence (`v1.0.0`); actively maintained resource (`v1.1.0+`). |
| **[SIDScope](https://github.com/jdding/SIDscope)** | How do mapping differences affect fixed-budget prefix retrieval, trained-beam D7 path-to-item resolution, and refresh generator handoff, with C0–C5/G0–G5 conformance and immutable EvidenceBundles? | Substantial journal extension (**TOIS** under review). Compatible `sidinspector` import namespace; expanded `sidscope` SDK & CLI. |
| **[SIDDuet](https://github.com/jdding/SIDDuet)** | When search and recommendation share one SID space, do co-coded items diverge in task allocation, and should task counts be pooled or kept separate? | Companion dual-task resource (**search vs. recommendation** paired observation contract). |

See [docs/RELATION_TO_SIDSCOPE_AND_SIDDUET.md](docs/RELATION_TO_SIDSCOPE_AND_SIDDUET.md) for the detailed boundary matrix.

## Artifact and Provenance Coverage

| Evidence | Verified scope |
| --- | --- |
| Same-item Musical benchmark (Table 2) | 23,742 items: GRID-style FT (`64/64/64`), GRID-style capacity (`32/1280/1280`), RQ-min ref, ReSID/GAOQ, plus 3 deterministic controls |
| Paired mechanism controls (Table 3) | D2 qualified aliasing (`1.19x -> 3.86x`), D1/D4 head-reserved capacity (`1.000 -> 0.028`), D5 realized depth (`12,010 -> 7,914`) |
| Official item-index portability | Released `LETTER` & `LC-Rec` Instruments artifacts (9,922 items; 9,897 unique SIDs) |
| Cross-dataset & exposure extensions | `All_Beauty 20k`, `Sports 20k`, 5,000-user fixed-reranker probes (Musical & All_Beauty), MovieLens schema, DACT D6 churn |

## Scope, License, and Maintenance

- **Scope:** SIDInspector inspects exported mappings, not downstream ranking quality. D2 characterizes aliasing without claiming causal harm; D3 is dataset-dependent and requires same-dataset controls; D5 reports structural pressure, not serving latency.
- **License:** [MIT License](LICENSE). Upstream tokenizer checkpoints and large caches are never redistributed; see [docs/REPRODUCIBILITY_MATRIX.md](docs/REPRODUCIBILITY_MATRIX.md).
- **Maintenance:** The CIKM '26 paper numbers (`docs/reproducibility/table2_musical_diagnostic.csv` and `table3_probe_calibration.csv`) are frozen. Ongoing releases (`v1.1+`) maintain CLI ergonomics, adapters, bug fixes, and the browser workbench; see [MAINTENANCE.md](MAINTENANCE.md) and [CHANGELOG.md](CHANGELOG.md).

## Citation

```bibtex
@inproceedings{ding2026sidinspector,
  author    = {Jiandong Ding and Heng Chang and Huijie Qin and Tianying Liu},
  title     = {{SIDInspector}: A Mapping-First Diagnostic Resource for Semantic-ID Tokenizers},
  booktitle = {Proceedings of the 35th ACM International Conference on Information and Knowledge Management (CIKM '26)},
  year      = {2026},
  month     = nov,
  location  = {Rome, Italy},
  pages     = {1--5},
  publisher = {Association for Computing Machinery},
  address   = {New York, NY, USA},
  isbn      = {979-8-4007-2539-5/2026/11},
  doi       = {10.1145/3799682.3840174},
  url       = {https://doi.org/10.1145/3799682.3840174}
}
```

[`CITATION.cff`](CITATION.cff) provides the same preferred citation through GitHub's **Cite this repository** button.
