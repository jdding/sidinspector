# CARD Original NU-RQ-VAE Evidence Gate

Timestamp: 2026-05-19 17:47:29 CST

Purpose: decide whether CARD original `nu-rq-vae` can become a third named
tokenizer evidence row for AUDIT-SID v0.

## Verdict

CARD original `nu-rq-vae` does not pass the named-method evidence gate in the
current public/local state.

Status: **FAILED_FOR_V0_MAIN_EVIDENCE**.

The local runner can execute source/import/export-contract smoke tests only
because the local CARD clone contains compatibility repair files. The official
CARD tree at commit `b8ce0976af253a2056b11acc05617abcd9b1f0f9` is missing
quantizer modules required by the released NU-RQ-VAE wrapper. Therefore a
successful local export would not be attributable to official CARD without
author-provided source or artifacts.

## Blocking Evidence

### B1. Official source tree is incomplete for NU-RQ-VAE

After `git fetch origin`, local `HEAD` and `origin/main` are both:

```text
b8ce0976af253a2056b11acc05617abcd9b1f0f9
```

The official tree contains:

- `nu-rq-vae/models/nu_rqvae.py`
- `rqvae4/rq.py`

But it does not contain:

- `rqvae4/models/rq.py`
- `rqvae4/models/vq.py`
- `rqvae4/vq.py`

This is fatal for faithful execution because `nu-rq-vae/models/nu_rqvae.py`
imports:

```python
from rqvae4.models.rq import ResidualVectorQuantizer
```

and the released `rqvae4/rq.py` imports:

```python
from .vq import VectorQuantizer
```

The missing files define the residual/vector quantizer behavior. Filling them
with local templates is not a path-only repair; it changes the tokenizer's
core assignment semantics.

### B2. No official public artifacts are available

The official repo and local clone do not provide:

- trained NU-RQ-VAE checkpoint;
- ready `item_emb.parquet`;
- item-to-SID mapping;
- processed CARD visual semantic units;
- encoded SigLIP2 features.

The public paper page says code is available at the GitHub repository, but the
repository contents are not sufficient for direct reproduction of the
tokenizer artifact.

### B3. Local preflight is still useful, but not evidence

`tools/autodl_audit_sid/preflight_card_nurqvae.py` now reports:

```text
official_source_audit.status = local_repair_required
missing_from_official_tree = [
  "rqvae4/models/rq.py",
  "rqvae4/models/vq.py",
  "rqvae4/vq.py"
]
faithfulness.core_algorithm_patched = true
faithfulness.quantizer_replaced = true
next_step_ready = false
```

This is the correct interpretation:

- source/import/export plumbing can be tested;
- a tiny synthetic export can preserve item IDs;
- the result must not be used as faithful CARD named-method evidence.

## Decision

Do not add CARD to the main AUDIT-SID v0 evidence table.

Allowed uses:

- method coverage/backlog row;
- controlled stressor/proxy row with explicit label;
- future integration target if authors release missing quantizer source,
  checkpoints, processed CARD embeddings, or item-to-SID mappings.

Disallowed uses:

- "we audit CARD" as a main empirical result;
- "CARD original NU-RQ-VAE reproduction";
- any Table 2-style named comparison against GRID/ReSID.

## Revival Conditions

CARD can be reopened only if at least one condition holds:

1. authors release the missing `vq.py`/`rq.py` modules or a complete official
   source tree;
2. authors provide a trained tokenizer checkpoint plus the exact export command;
3. authors provide stable item-to-SID mappings for a public dataset;
4. the paper explicitly switches from named-method evidence to a controlled
   CARD-inspired stressor, with no attribution to official CARD performance.

## Current Action

Freeze CARD original as **failed for v0 main evidence** and return effort to
paper wording, release monitoring, or other official artifacts. Do not spend
GPU on CARD until the source/artifact gate changes.
