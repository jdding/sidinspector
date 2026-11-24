# SIDInspector

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB.svg)](https://www.python.org/downloads/)

SIDInspector checks exported item-to-semantic-ID mappings before you train or
evaluate a downstream generator. Use it to find collisions, check which
prefixes preserve item neighborhoods, and see how unique codes are distributed
across popular and rare items.

[ACM paper](https://doi.org/10.1145/3799682.3840174) |
[arXiv preprint](https://arxiv.org/abs/2606.10375) |
[Project page](https://jdding.github.io/sidinspector) |
[CIKM 2026 Resource Track](https://cikm2026.diag.uniroma1.it/resource-papers/) |
[Release v1.0.1](https://github.com/jdding/sidinspector/tree/sidinspector-cikm2026-resource-v1.0.1)

## Quickstart

The CPU demo requires Python 3.9 or later. Use the CIKM 2026 Resource Track
artifact tagged `sidinspector-cikm2026-resource-v1.0.1` (package version `1.0.0`).
Install it from a checkout; the package is not on PyPI.

```bash
git clone https://github.com/jdding/sidinspector.git
cd sidinspector
git checkout sidinspector-cikm2026-resource-v1.0.1
python3 -m pip install -e .
python3 examples/run_reviewer_quickstart.py
```

The demo normalizes a bundled music-like export, checks its joins, and writes
`preflight_summary.json` and D1–D5 CSV reports to
`examples/reviewer_quickstart_output/`. The [notebook](examples/quickstart.ipynb)
runs the same demo from an installed checkout. This checks that the workflow
runs. For the paper tables and their evidence, see the
[reproducibility matrix](docs/REPRODUCIBILITY_MATRIX.md).

## v1.1 workbench

The v1.1 candidate adds an interactive browser workbench and the
`sidinspector` CLI. From this checkout, run
`python3 -m http.server 8766 --bind 127.0.0.1` and open
<http://127.0.0.1:8766>. The workbench loads Pyodide and checks its scripts
and data against the release manifest. It runs D1–D6 examples, verifies
CIKM Tables 2 and 3, and processes your CSV files in the browser.
The project page linked above hosts the paper.

To use the CLI from this checkout, install it with a recent version of pip:

```bash
python3 -m pip install -e .
sidinspector verify-tables
sidinspector validate
sidinspector demo --port 8765
```

See the [artifact quickstart](ARTIFACT_QUICKSTART.md) for an end-to-end run,
the [CSV guide](docs/BRING_YOUR_OWN_DATA.md) for `sidinspector audit`, and the
[release notes](CHANGELOG.md) for the relationship to
[SIDScope](docs/RELATION_TO_SIDSCOPE_AND_SIDDUET.md).

| CPU workload (macOS arm64) | Wall time | Peak RSS |
| --- | ---: | ---: |
| Verify CIKM Tables 2 and 3 and the reproducibility matrix | 0.08 s | 15 MiB |
| Audit a bundled CSV with 12 items | 0.05 s | 16 MiB |
| Audit a synthetic CSV with 20,000 items and 50,000 interactions | 0.54 s | 124 MiB |
| Validate the release package and run tests | 3.75 s | 99 MiB |

## Key findings

On the same catalog of 23,742 Musical Instruments items, a larger GRID-style
budget reduced aliasing and ReSID/GAOQ had no full-code collisions. The
category-prefix control scored highest on neighborhood alignment (D3).

| Artifact | Unique SIDs | D2 full-code aliasing | D3 level-1 neighborhood alignment |
| --- | ---: | ---: | ---: |
| GRID-style feature-text (seed 42, widths 64/64/64) | 3,749 | 0.977 | 0.055 |
| GRID-style capacity (budget 32/1280/1280) | 9,874 | 0.779 | 0.080 |
| ReSID/GAOQ | 23,742 | 0.000 | 0.154 |
| Category-prefix control | 23,742 | 0.000 | 0.447 |

The [unrounded Table 2 values](docs/reproducibility/table2_musical_diagnostic.csv)
are included in the repo. The GRID-style feature-text row is a controlled
export from a released residual k-means module; it does not reproduce GRID end
to end. The deterministic category-prefix row calibrates D3. Recommendation
quality requires downstream evaluation.

On the same catalog, the RQ-min reference has 17,247 unique SIDs (D2: 0.440;
D3: 0.065). On a separate Instruments index of 9,922 items, LETTER and LC-Rec
each have 9,897 unique full SIDs, with D3 of 0.109 and 0.052, respectively.

## Diagnostics

![SIDInspector workflow. Adapters turn GRID-style, ReSID/GAOQ, LETTER, and LC-Rec exports into one item-to-code table. A validation gate checks schema, joins, and provenance. The probe engine then writes D1–D5 reports, with optional D6 churn and a D7 trace hook.](assets/sidinspector_workflow.png)

*Workflow figure from Ding et al., CIKM 2026 ([arXiv:2606.10375](https://arxiv.org/abs/2606.10375)), reproduced under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

| Probe | Signal | Typical next check |
| --- | --- | --- |
| D1 utilization | Per-level code use, entropy, and imbalance | Compare active codes with the intended budget. |
| D2 aliasing | Full-code and prefix collisions | Inspect duplicate groups and capacity settings. |
| D3 neighborhood alignment | Prefix recovery of co-occurrence neighborhoods | Compare same-dataset controls and candidate exposure. |
| D4 popularity allocation | Head/mid/tail allocation of unique SIDs | Check whether tail items are disproportionately compressed. |
| D5 structural cost | SID depth, unique IDs, and active prefixes | Inspect fan-out and depth before choosing a decoding stack. |
| D6 churn (optional) | Refresh-to-refresh mapping stability | Trace changed items and affected prefixes. |

The workflow validates `sid_assignments`, `item_metadata`, and `interactions`
before running the probes. D7 accepts optional generator traces; the CIKM paper
does not report D7 results.

## Inspect your own mapping

For an export with one row per item:

```csv
item_id,sid_0,sid_1,sid_2
1,12,3,91
2,12,8,17
```

normalize and inspect it:

```bash
python3 examples/minimal_adapter.py \
  --input-csv path/to/item_codes.csv \
  --output-dir runs/my_tokenizer \
  --method my_tokenizer \
  --dataset my_dataset

python3 -m sidinspector.preflight \
  --sid-assignments runs/my_tokenizer/sid_assignments.parquet \
  --item-metadata runs/my_tokenizer/item_metadata.parquet \
  --interactions runs/my_tokenizer/interactions.parquet \
  --run-metric-smoke

python3 -m sidinspector.metrics \
  --sid-assignments runs/my_tokenizer/sid_assignments.parquet \
  --item-metadata runs/my_tokenizer/item_metadata.parquet \
  --interactions runs/my_tokenizer/interactions.parquet \
  --output-dir runs/my_tokenizer/diagnostics
```

See the [adapter template](docs/ADAPTER_TEMPLATE.md),
[validated adapters](docs/VALIDATED_ADAPTERS.md), and
[probe interpretation guide](docs/PROBE_INTERPRETATION.md) for the full
contract and supported official artifact paths.

## Interpreting the results

- D2 measures code sharing. It cannot establish causal harm to recommendations.
- D3 depends on the dataset. Compare against controls on the same catalog.
- D5 describes structure. Measure serving latency separately.
- The fixed-reranker probe measures candidate exposure. Assess trained
  generator quality downstream.

Run the package, quickstart, table, and test checks with:

```bash
python3 tools/verify_package.py
```

The software is released under the [MIT License](LICENSE).

## Citation

```bibtex
@inproceedings{ding2026sidinspector,
  author    = {Jiandong Ding and Heng Chang and Huijie Qin and Tianying Liu},
  title     = {{SIDInspector}: A Mapping-First Diagnostic Resource for
               Semantic-ID Tokenizers},
  booktitle = {Proceedings of the 35th ACM International Conference on
               Information and Knowledge Management},
  series    = {CIKM '26},
  year      = {2026},
  address   = {New York, NY, USA},
  location  = {Rome, Italy},
  publisher = {ACM},
  doi       = {10.1145/3799682.3840174},
  url       = {https://doi.org/10.1145/3799682.3840174},
  isbn      = {979-8-4007-2539-5},
  pages     = {8890--8894},
  numpages  = {5}
}
```

GitHub's **Cite this repository** uses the same reference from
[`CITATION.cff`](CITATION.cff). The proceedings cover 7–11 November 2026 in
Rome, including the main conference on 9–11 November.
