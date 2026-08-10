# SIDInspector

**Mapping-first diagnostics for Semantic-ID tokenizer artifacts.**

[Paper](https://arxiv.org/abs/2606.10375) |
[CIKM 2026 Resource Track](https://cikm2026.diag.uniroma1.it/resource-papers/) |
[Release v1.0](https://github.com/jdding/sidinspector/tree/sidinspector-cikm2026-resource-v1.0) |
[Reproducibility matrix](docs/REPRODUCIBILITY_MATRIX.md) |
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
and writes D1-D5 reports to:

```text
examples/reviewer_quickstart_output/preflight_summary.json
examples/reviewer_quickstart_output/diagnostics/d1_utilization.csv
examples/reviewer_quickstart_output/diagnostics/d2_collision.csv
examples/reviewer_quickstart_output/diagnostics/d3_alignment.csv
examples/reviewer_quickstart_output/diagnostics/d4_head_tail.csv
examples/reviewer_quickstart_output/diagnostics/d5a_deployment_cost.csv
```

This is a usability example. The paper-table reproduction path is described
separately below.

## What SIDInspector Checks

| Probe | Signal | Typical next check |
| --- | --- | --- |
| D1 utilization | Per-level code use, entropy, and imbalance | Compare active codes with the intended codebook budget. |
| D2 aliasing | Full-code and prefix collision profiles | Inspect duplicate groups and capacity settings. |
| D3 neighborhood alignment | SID-prefix recovery of interaction co-occurrence neighborhoods | Compare with same-dataset controls and candidate exposure. |
| D4 popularity allocation | Head/mid/tail allocation of unique SIDs | Check whether tail items are compressed disproportionately. |
| D5 structural cost | SID depth, unique full IDs, and active prefix counts | Inspect fan-out and depth before choosing a decoding stack. |
| D6 churn (optional) | Refresh-to-refresh SID and prefix stability | Trace changed items and affected prefixes across snapshots. |

The core workflow consumes three normalized tables:

- `sid_assignments`: one item per row with its full SID and per-level codes;
- `item_metadata`: item keys plus optional category, title, brand, or text;
- `interactions`: user-item events plus optional split and timestamp fields.

See [Diagnostics](docs/DIAGNOSTICS.md) for metric definitions and
[Probe interpretation](docs/PROBE_INTERPRETATION.md) for risks and follow-up
checks. D7 is an optional generator-trace input hook, not an empirical result in
the CIKM 2026 resource paper.

## Inspect Your Own Mapping

For a tokenizer that already exports one row per item:

```csv
item_id,sid_0,sid_1,sid_2
1,12,3,91
2,12,8,17
```

normalize it with the minimal adapter:

```bash
python3 examples/minimal_adapter.py \
  --input-csv path/to/item_codes.csv \
  --output-dir runs/my_tokenizer \
  --method my_tokenizer \
  --dataset my_dataset
```

Then validate the joins and run D1-D5:

```bash
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

The [adapter template](docs/ADAPTER_TEMPLATE.md) defines the normalized
contract. Official LETTER and LC-Rec item-index paths are documented in
[Validated adapters](docs/VALIDATED_ADAPTERS.md). A method is listed there only
after an official item-code artifact passes preflight and D1-D5.

## Reproduce The Paper Tables

The release includes compact metric summaries and run manifests for Tables 2
and 3. From a clean checkout:

```bash
python3 tools/build_paper_tables.py \
  --output-dir /tmp/sidinspector_paper_tables
python3 tools/verify_reproducibility_matrix.py
```

The verifier rebuilds both table CSVs from 16 released source summaries and
checks every reported row. The
[reproducibility matrix](docs/REPRODUCIBILITY_MATRIX.md) distinguishes this
clean-checkout path from evidence that relies on upstream public artifacts or
saved experiment manifests. It does not retrain upstream tokenizers or
regenerate omitted training caches.

To run the complete release gate, including package import, the toy workflow,
the reviewer quickstart, table reconstruction, and unit tests:

```bash
python3 tools/verify_package.py
```

## Optional Analyses

Refresh-to-refresh churn:

```bash
python3 -m sidinspector.churn --help
```

Fixed-reranker candidate-exposure probe:

```bash
python3 -m sidinspector.downstream_probe \
  --manifest path/to/probe_manifest.csv \
  --output-dir path/to/probe_output
```

The downstream probe reports candidate exposure under a fixed protocol. It is
not a trained-generator evaluation and does not establish final ranking
quality.

## Evidence Boundaries

- SIDInspector is an inspector for exported mappings, not a new tokenizer or a
  tokenizer leaderboard.
- D2 reports aliasing; it does not prove causal harm to recommendation quality.
- D3 is dataset-dependent and should be interpreted with same-dataset controls.
- D5 reports structural pressure, not measured serving latency.
- Controlled and reference adapters test diagnostic mechanisms or interface
  portability; they are not additional named-method coverage.
- The reproducibility matrix is the source of truth for runnable, reconstructed,
  and snapshot-backed evidence.

## Repository Guide

| Path | Purpose |
| --- | --- |
| `src/sidinspector/` | Adapter contract, validator, D1-D6 metrics, and optional probe code. |
| `examples/` | Toy workflow, reviewer quickstart, and minimal adapter. |
| `docs/` | Diagnostic definitions, adapter guidance, interpretation, and evidence matrix. |
| `docs/reproducibility/` | Compact paper evidence and table-source manifests. |
| `tools/` | Package, table, and reproducibility verifiers. |
| `tests/` | Unit tests for metrics, adapters, validation, churn, and the downstream probe. |

## Citation

Until ACM publishes the final DOI and page range, use the following accepted,
forthcoming citation. The entry will be refreshed when the official proceedings
metadata becomes available.

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

The repository also provides [`CITATION.cff`](CITATION.cff), which enables
GitHub's **Cite this repository** interface. The current preprint is
[arXiv:2606.10375](https://arxiv.org/abs/2606.10375).

## Development

```bash
python3 -m pip install -e .
python3 -m unittest discover -s tests
python3 tools/verify_package.py
python3 tools/verify_reproducibility_matrix.py
```

SIDInspector is released under the [MIT License](LICENSE).
