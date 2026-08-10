# SIDInspector

**Mapping-first diagnostics for Semantic-ID tokenizer artifacts.**

[Paper](https://arxiv.org/abs/2606.10375) |
[CIKM 2026 Resource Track](https://cikm2026.diag.uniroma1.it/resource-papers/) |
[Citation](#citation) |
[Release v1.0](https://github.com/jdding/sidinspector/tree/sidinspector-cikm2026-resource-v1.0) |
[MIT license](LICENSE)

SIDInspector inspects an exported `item_id -> SID` mapping before a downstream
generative recommender is trained or evaluated. It validates the mapping
contract and reports utilization, aliasing, behavioral neighborhood alignment,
popularity allocation, and structural pressure. It does not train a tokenizer
or replace downstream Recall/NDCG evaluation.

> **Paper status:** accepted to the Resource Track of the 35th ACM
> International Conference on Information and Knowledge Management (CIKM
> 2026). The ACM proceedings DOI and page range are not yet available. The
> public artifact release is `sidinspector-cikm2026-resource-v1.0` (Python
> package version `1.0.0`).

## Citation

Until ACM publishes the final DOI and page range, use this accepted,
forthcoming citation:

```bibtex
@inproceedings{ding2026sidinspector,
  author    = {Jiandong Ding and Heng Chang and Huijie Qin and Tianying Liu},
  title     = {{SIDInspector}: A Mapping-First Diagnostic Resource for
               Semantic-ID Tokenizers},
  booktitle = {Proceedings of the 35th ACM International Conference on
               Information and Knowledge Management},
  year      = {2026},
  note      = {Accepted to the CIKM 2026 Resource Track; forthcoming},
  url       = {https://arxiv.org/abs/2606.10375}
}
```

[`CITATION.cff`](CITATION.cff) provides the same preferred citation through
GitHub's **Cite this repository** interface.

## Quickstart

The bundled workflow is CPU-only and supports Python 3.9+.

```bash
git clone https://github.com/jdding/sidinspector.git
cd sidinspector
git checkout sidinspector-cikm2026-resource-v1.0
python3 -m pip install -e .
python3 examples/run_reviewer_quickstart.py
```

The quickstart normalizes a small music-like SID export, validates its joins,
and writes `preflight_summary.json` plus D1-D5 CSV reports under
`examples/reviewer_quickstart_output/`.

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

SIDInspector is released under the [MIT License](LICENSE).
