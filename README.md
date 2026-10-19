# SIDInspector

[![arXiv](https://img.shields.io/badge/arXiv-2606.10375-b31b1b.svg)](https://arxiv.org/abs/2606.10375)
[![DOI](https://img.shields.io/badge/DOI-10.1145%2F3799682.3840174-blue)](https://doi.org/10.1145/3799682.3840174)
[![CIKM 2026](https://img.shields.io/badge/CIKM-2026-0B3D91.svg)](https://cikm2026.diag.uniroma1.it/resource-papers/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB.svg)](https://www.python.org/downloads/)

SIDInspector inspects an exported item-to-semantic-ID mapping for people working on semantic IDs and generative recommendation, before a downstream generator is trained or evaluated.

[Paper](https://arxiv.org/abs/2606.10375) |
[DOI](https://doi.org/10.1145/3799682.3840174) |
[Project page](https://jdding.github.io/sidinspector) |
[CIKM 2026 Resource Track](https://cikm2026.diag.uniroma1.it/resource-papers/) |
[Release v1.0](https://github.com/jdding/sidinspector/tree/sidinspector-cikm2026-resource-v1.0)

![SIDInspector workflow. Adapters turn GRID-style, ReSID/GAOQ, LETTER, and LC-Rec exports into one item-to-code table. A validation gate checks schema, joins, and provenance. The probe engine then writes D1–D5 reports, with optional D6 churn and a D7 trace hook.](assets/sidinspector_workflow.png)

*Workflow figure from Ding et al., CIKM 2026 ([arXiv:2606.10375](https://arxiv.org/abs/2606.10375)), included under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Adapters normalize GRID-style, ReSID/GAOQ, LETTER, and LC-Rec exports into one item-to-code contract. Validation precedes the D1–D5 reports; paired mappings enable D6 churn, and D7 stays a trace-input hook.*

Published in the Resource Track of CIKM 2026. The main conference is 9–11 November 2026 in Rome; the proceedings front matter dates the event 7–11 November 2026. The public artifact is tag `sidinspector-cikm2026-resource-v1.0` (Python package `1.0.0`). Install from a local checkout. This package is not published on PyPI.

## Quickstart

The bundled workflow is CPU-only and supports Python 3.9+.

```bash
git clone https://github.com/jdding/sidinspector.git
cd sidinspector
git checkout sidinspector-cikm2026-resource-v1.0
python3 -m pip install -e .
python3 examples/run_reviewer_quickstart.py
```

The quickstart normalizes a small music-like SID export shipped in this repository, validates its joins, and writes `preflight_summary.json` plus D1–D5 CSV reports under `examples/reviewer_quickstart_output/`. It is a usability check, not a reproduction of the paper tables.

The same demo is in [`examples/quickstart.ipynb`](examples/quickstart.ipynb). After that file is on the default branch, Colab can open it from [`main`](https://colab.research.google.com/github/jdding/sidinspector/blob/main/examples/quickstart.ipynb).

## Key findings

On one Musical Instruments catalog of 23,742 items, full-code aliasing and neighborhood alignment move apart. A larger GRID-style budget lowers aliasing, and the ReSID/GAOQ export is alias-free, while level-1 neighborhood alignment stays below a deterministic category-prefix control.

| Artifact | Unique SIDs | D2 full-code aliasing | D3 level-1 neighborhood alignment |
| --- | ---: | ---: | ---: |
| GRID-style feature-text (seed 42, widths 64/64/64) | 3,749 | 0.977 | 0.055 |
| GRID-style capacity (budget 32/1280/1280) | 9,874 | 0.779 | 0.080 |
| ReSID/GAOQ | 23,742 | 0.000 | 0.154 |
| Category-prefix control | 23,742 | 0.000 | 0.447 |

These figures are copied from Table 2 of the CIKM 2026 paper. The same rows, before that table's printed rounding, are in [`docs/reproducibility/table2_musical_diagnostic.csv`](docs/reproducibility/table2_musical_diagnostic.csv). GRID-style feature-text is a controlled export through a released residual k-means module, not an end-to-end GRID reproduction. The category-prefix row is a deterministic control for the D3 scale, not a learned tokenizer. These measurements describe the mappings. They are not recommendation-quality results.

On the same 23,742 items, the RQ-min reference row in that table has 17,247 unique SIDs, D2 0.440, and D3 0.065. On a separate Instruments index of 9,922 items, the released LETTER and LC-Rec mappings each have 9,897 unique full SIDs, with D3 level-1 alignment 0.109 for LETTER and 0.052 for LC-Rec.

## Diagnostics

| Probe | Signal | Typical next check |
| --- | --- | --- |
| D1 utilization | Per-level code use, entropy, and imbalance | Compare active codes with the intended budget. |
| D2 aliasing | Full-code and prefix collisions | Inspect duplicate groups and capacity settings. |
| D3 neighborhood alignment | Prefix recovery of co-occurrence neighborhoods | Compare same-dataset controls and candidate exposure. |
| D4 popularity allocation | Head/mid/tail allocation of unique SIDs | Check whether tail items are disproportionately compressed. |
| D5 structural cost | SID depth, unique IDs, and active prefixes | Inspect fan-out and depth before choosing a decoding stack. |
| D6 churn (optional) | Refresh-to-refresh mapping stability | Trace changed items and affected prefixes. |

The core workflow consumes `sid_assignments`, `item_metadata`, and
`interactions` tables. D7 is an optional generator-trace input hook, not an
empirical result in the CIKM 2026 resource paper.

## Inspect Your Own Mapping

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

## Scope

- SIDInspector is an inspector for exported mappings, not a tokenizer
  leaderboard.
- D2 reports aliasing but does not prove causal recommendation harm.
- D3 is dataset-dependent and should be interpreted with same-dataset controls.
- D5 reports structural pressure, not measured serving latency.
- The fixed-reranker probe concerns candidate exposure, not trained-generator
  quality.

Run the complete package, quickstart, table, and test gate with:

```bash
python3 tools/verify_package.py
```

SIDInspector is released under the [MIT License](LICENSE). The workflow figure
above is reproduced from the paper and remains under CC BY 4.0.

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
  address   = {Rome, Italy},
  publisher = {ACM},
  doi       = {10.1145/3799682.3840174},
  url       = {https://doi.org/10.1145/3799682.3840174},
  isbn      = {979-8-4007-2539-5},
  numpages  = {5}
}
```

The ACM reference format records this article as 5 pages. It does not print a
start–end page range. [`CITATION.cff`](CITATION.cff) provides the same
preferred citation through GitHub's **Cite this repository** interface.
