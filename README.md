# SIDInspector

This branch contains SIDInspector, a public-facing diagnostic resource for
semantic-ID tokenizer mappings and codebooks in generative
recommendation/retrieval. Some internal module and script paths retain the
legacy `audit_sid` name for compatibility with earlier experiment artifacts.

## Start Here

1. `ARTIFACT_QUICKSTART.md`
2. `docs/CURRENT_STATE.md`
3. `docs/CIKM_EXPERIMENT_DESIGN.md`
4. `docs/DOCUMENT_INDEX.md`
5. `docs/ARCHIVE_INDEX.md`
6. `docs/ARTIFACTS_INDEX.md`
7. `docs/PROJECT_SPEC.md`
8. `docs/GATE0_DECISION.md`
9. `docs/GATE0A_EVIDENCE_MATRIX.md`
10. `docs/GRID_MUSICAL_SAME_DATASET_CPU.md`
11. `docs/CIKM_RESOURCE_PAPER_PLAN.md`
12. `refine-logs/EXPERIMENT_TRACKER.md`
13. `refine-logs/EXPERIMENT_PLAN.md`

## Current Thesis

SIDInspector is the current public-first methodology candidate. It should be
framed as mapping-first diagnostics for semantic-ID tokenizers/codebooks, not
as another SID generation algorithm or a simple leaderboard.

## Current Gate

Gate 0 artifact feasibility is **passed**:

- Cluster A: GRID official-module RQ-KMeans exports joinable SID mappings with D1-D5 diagnostic probes.
- Cluster B: bounded ReSID/GAOQ exports 23,742 joinable `Musical_Instruments` SIDs with D1-D5 diagnostic probes.
- Sanity baselines exist for metric sensitivity.

Gate 0A core is **conditionally passed for a conservative resource-demo framing**:

- It is enough for a toolkit/resource demo with method coverage and a
  same-item-universe GRID Musical feature-text vs ReSID Musical diagnostic
  table.
- It is not enough for a same-dataset GRID-vs-ReSID leaderboard or a claim that ReSID Sports balanced GAOQ completed.
- D3 is no longer category-purity-only; `d3_alignment.csv` now includes co-occurrence collaborative top-k prefix recall.

## Frozen CIKM v0 Scope

- Dataset: `Musical_Instruments` now supports the main same-item-universe
  diagnostic row. `Sports_and_Outdoors` remains preferred for future
  canonical-vertical strengthening, but exact balanced ReSID GAOQ is not
  currently tractable enough to block Gate 0A.
- Methods: canonical RQ-VAE/TIGER-style SID, one representative recent tokenizer innovation such as ReSID if artifact export is meaningful, and random/popularity/category sanity ID baseline.
- Diagnostics: D1-D5 artifact diagnostics over `item -> SID` mappings:
  utilization, aliasing profile, neighborhood alignment, popularity allocation,
  and structural-cost proxy.
- Optional only: D6 drift/churn and future generator-output D7.
- Paper stance: resource-first. Strong empirical finding is a stretch goal, not the core CIKM claim.

## Venue Target

Short-term target: CIKM 2026 Resource Track.

Key dates:

- Abstract: 2026-05-30 AoE
- Paper: 2026-06-06 AoE

Gate 0 has passed, and Gate 0A has a conditional resource-demo pass. If the paper needs a stronger same-dataset method comparison, do not force a weak CIKM submission. Longer-term backups are SIGIR 2027 Resource/Reproducibility-style track, RecSys 2027 Resource/Reproducibility, and CIKM 2027 Resource.

Method representativeness is part of Gate 0. A shallow RQ-VAE + ReSID comparison is not enough for submission.

The must-run method coverage is cluster-based: canonical SID baseline + representative recent tokenizer/codebook innovation from Cluster B + sanity lower bound.

Current public-code priority: keep the paper-ready tables, terminology, and
artifact verifier aligned. CARD compact feature proxy is a controlled
mechanism-probe/backlog path only and should not be counted as faithful
named-method evidence.

## Reviewer Artifact Environment

Reviewer-facing verification uses the anonymous artifact URL:

```text
https://anonymous.4open.science/r/sidinspector-9BB2
```

The clean-checkout reviewer verification path does not require GPU access and
has been tested with Python 3.9.6 on macOS. Open the anonymous URL in a browser,
use the page's Download/ZIP entry, unzip the archive, then run the local
verification commands from the extracted directory. Do not rely on command-line
access to `anonymous.4open.science`; Cloudflare may block non-browser clients.
SID tokenizer training/export may use GPU in normal research or production
settings; this verifier audits frozen mappings and tables. Install the
dependencies from `requirements.txt`, run the
unit tests, and then run the verifier:

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests
python3 tools/verify_paper_artifact.py
```

Expected final verifier line:

```text
SIDInspector reviewer artifact verification passed.
```

Typical runtime is under two minutes after dependencies are installed. Optional
tests may skip when ignored upstream clones or local experiment caches are not
present.

For new tokenizer exports, start from `examples/minimal_adapter.py`; it
normalizes `item_id, sid_0, ..., sid_L` into `sid_assignments.parquet`. Runtime
notes for the public Musical bundle are in
`paper_assets/tables/table16_runtime_profile.md`.

## Boundary

This branch is public-stage only. Do not commit Huawei internal data, business logs, or proprietary implementation details.
