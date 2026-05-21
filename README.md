# SIDInspector

SIDInspector is a mapping-first diagnostic resource for semantic-ID tokenizer
artifacts in generative recommendation. It validates normalized item-to-code
mappings and reports diagnostic probes over capacity utilization, full-code
aliasing, collaborative prefix alignment, head-to-tail allocation, and
structural cost, with optional hooks for refresh churn and generator traces.

The repository is the reviewer artifact for the CIKM 2026 Resource Track draft:

> SIDInspector: A Mapping-First Diagnostic Resource for Semantic-ID Tokenizers

The submitted manuscript PDF is handled through the submission system. This
artifact intentionally ships code, frozen evidence tables, and provenance notes,
but not the manuscript source, compiled PDF, or figure-generation scripts.

## Reviewer Quickstart

Use the anonymous review URL when reviewing the artifact:

```bash
git clone https://anonymous.4open.science/r/sidinspector-9BB2 sidinspector
cd sidinspector
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests
python3 tools/verify_paper_artifact.py
```

Environment and runtime:

- Python: tested with Python 3.9.6 on macOS.
- Dependencies: install exactly from `requirements.txt` (`pandas`, `numpy`,
  `pyarrow`, `scikit-learn`, and `torch`).
- Hardware: no GPU is required for this reviewer verification path. SID
  tokenizer training/export may use GPU in normal research or production
  settings; the clean-checkout verifier audits frozen mappings and tables.
- Expected runtime: typically under two minutes after dependencies are
  installed. The unit tests may skip optional checks when ignored upstream
  clones or local experiment caches are absent.

The verifier should finish with:

```text
SIDInspector/AUDIT-SID reviewer artifact verification passed.
```

## Repository Layout

- `src/audit_sid/`: adapter contracts and D1-D5 diagnostic metrics.
- `methods/rqvae_minimal_reference/`: local residual-quantization reference
  adapter used to exercise an independent code path, not a published-method
  reproduction.
- `tools/`: clean-checkout verifier and bounded mechanism-probe scripts.
- `tests/`: unit tests for metrics, churn, ranking-context probes, mechanism
  probes, and the reference adapter.
- `paper_assets/tables/`: frozen CSV/Markdown/LaTeX evidence tables checked by
  the verifier.
- `docs/`: public evidence notes for method boundaries, controlled probes,
  ranking-context validation, and claim audits.

## Scope Boundary

SIDInspector audits exported tokenizer artifacts. It is not a new tokenizer, a
leaderboard, a faithful TIGER/GRID/ReSID reproduction, or a claim of downstream
ranking superiority. Larger local experiment caches are intentionally omitted;
the clean-checkout verifier checks the submitted-paper-facing frozen artifacts
without requiring manuscript sources.

License: MIT.
