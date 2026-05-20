# SIDInspector

SIDInspector is a mapping-first diagnostic resource for semantic-ID tokenizer
artifacts in generative recommendation. It validates normalized item-to-code
mappings and reports diagnostic probes over capacity utilization, full-code
aliasing, collaborative prefix alignment, head-to-tail allocation, and
structural cost, with optional hooks for refresh churn and generator traces.

The repository is the public reviewer artifact for the CIKM 2026 Resource Track
draft:

> SIDInspector: A Mapping-First Diagnostic Resource for Semantic-ID Tokenizers

## Reviewer Quickstart

Use the pinned tag when reviewing the artifact:

```bash
git clone --branch audit-sid-cikm-resource-v0.1 --depth 1 \
  https://github.com/jdding/sidinspector.git sidinspector
cd sidinspector
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests
MPLCONFIGDIR=/tmp/audit_sid_mpl \
  python3 tools/paper_figures/generate_audit_sid_pipeline.py
python3 tools/verify_paper_artifact.py
```

The final verifier line should be:

```text
SIDInspector/AUDIT-SID public artifact verification passed.
```

## Repository Layout

- `src/audit_sid/`: adapter contracts and D1-D5 diagnostic metrics.
- `methods/rqvae_minimal_reference/`: local residual-quantization reference
  adapter used to exercise an independent code path, not a published-method
  reproduction.
- `tools/`: clean-checkout verifier, figure generator, and bounded mechanism
  probe scripts.
- `tests/`: unit tests for metrics, churn, ranking-context probes, mechanism
  probes, and the reference adapter.
- `paper/`: ACM draft PDF/source and Figure 1.
- `paper_assets/tables/`: frozen CSV/Markdown/LaTeX evidence tables checked by
  the verifier.
- `docs/`: public evidence notes for method boundaries, controlled probes,
  ranking-context validation, and claim audits.

## Scope Boundary

SIDInspector audits exported tokenizer artifacts. It is not a new tokenizer, a
leaderboard, a faithful TIGER/GRID/ReSID reproduction, or a claim of downstream
ranking superiority. Larger local experiment caches are intentionally omitted;
the clean-checkout verifier checks the paper-facing frozen artifacts.

License: MIT.
