# Third Method Evidence Gate

Timestamp: 2026-05-19 17:26:26 CST

Purpose: define when a third SID/tokenizer method can enter the AUDIT-SID main
evidence table. This is a guard against repeating the earlier proxy-vs-method
mistake.

## Default Rule

Do not count a self-implemented paper-inspired method as named-method evidence.
It can be a controlled stressor, but it cannot be written as "we audit Method
X" unless the artifact is anchored in an official release or author-provided
artifact.

## Main-Evidence Admission Criteria

A third method can enter the main paper only if all conditions hold:

1. **Official anchor**: official repo, official released artifact, author
   artifact, or a repair of the authors' released implementation.
2. **Minimal semantic edits**: any local patch is limited to import paths,
   environment compatibility, path resolution, or output normalization. No
   replacement of the tokenizer objective, quantizer, routing rule, or
   assignment semantics.
3. **Export contract**: produces stable item-to-SID mappings with item IDs and
   per-level code columns.
4. **Joinability**: passes AUDIT-SID `sid_assignments`, `item_metadata`, and
   `interactions` coverage checks with zero or explicitly justified gaps.
5. **Diagnostic support**: supports at least three of D1/D2/D3v2/D4/D5a, or a
   uniquely valuable D7/generator-output artifact.
6. **Non-redundant finding**: adds a finding not already provided by
   GRID/ReSID/sanity/DACT/MovieLens evidence.
7. **Fidelity note**: documents what was official, what was patched, and which
   original method components remain unmodified.

If any condition fails, keep the method in Table 1 as coverage/backlog or as a
controlled stressor. Do not add it to the main diagnostic case study.

## CARD Original `nu-rq-vae` Route

CARD is no longer a realistic v0 candidate from the current public repository.
The original `nu-rq-vae` path is export-shaped, but the official tree is missing
the quantizer modules required by the wrapper. Local compatibility repairs
therefore replace missing assignment semantics and cannot be counted as
path-only repair.

Minimum revival gate:

- author-complete source tree, including the missing quantizer modules; or
- author checkpoint / processed CARD embeddings / item-to-SID mappings;
- explicit evidence that any local patch is path/runtime-only and does not
  replace quantizer or visual-semantic-unit semantics.

## DIGER / QuaSID / AdaSID / CapsID Route

These methods can enter main evidence only through official release or
author-provided artifacts. A paper-inspired local implementation is not enough.

Current primary-source notes from 2026-05-19:

- DIGER arXiv v3 states that code is released, but the GitHub README says the
  current repository is an illustrative/reference implementation and that
  runnable configs, processed data, embeddings, and pre-trained RQ-VAE
  checkpoints are planned before SIGIR 2026.
- QuaSID/AdaSID/CapsID arXiv pages expose paper text and source/PDF links; no
  official runnable artifact was confirmed in the current screen.

## Issue / Email Request Template

Subject: Request for item-to-SID artifacts for AUDIT-SID diagnostic resource

Hello [Author],

We are building AUDIT-SID, a resource paper/toolkit for artifact-level
diagnostics of Semantic-ID tokenizers. We would like to include [METHOD] as a
named method only if we can use an official or author-provided artifact.

Would you be willing to share either:

1. item-to-SID mappings with stable item IDs for one public dataset;
2. the trained tokenizer checkpoint plus the exact export command; or
3. the processed data/checkpoint package needed to reproduce the mapping?

We will not claim downstream superiority or modify the method objective. The
audit only reports mapping diagnostics such as code utilization, full/prefix
collisions, co-occurrence prefix alignment, head-tail capacity, and prefix
fan-out. We will clearly cite and label the artifact provenance.

Thanks.
