# AUDIT-SID / SIDInspector Resource Framing Decision

Timestamp: 2026-05-20 02:17:10 CST

## Decision

SIDInspector is the paper-facing name for the AUDIT-SID project. CIKM v0 should
be framed as a **diagnostic / interface resource** (Type 4), not as a coverage
resource in the RecBole/BARS sense (Type 1).

This is a scope decision for the 2026-05-30 / 2026-06-06 submission window, not
a permanent rejection of coverage-resource work.

## Why Not Type 1 For CIKM v0

A Type 1 resource paper asks reviewers to judge breadth: many reproduced
methods, common datasets, comparable training protocols, and long-term
maintenance. SIDInspector currently has two true public SID export paths plus
sanity rows and controlled probes. Forcing a Type 1 frame would make the paper
look under-covered and would invite questions about missing TIGER/CARD/AdaSID/
CapsID/DIGER reproductions.

The current evidence does not support a RecBole-style claim. It supports a
different claim: a normalized item-to-SID artifact contract plus diagnostics can
make SID tokenizer failure modes inspectable before downstream generator
training.

## Type 4 Thesis

The paper should make the following contribution first-class:

> SIDInspector is a mapping-first diagnostic framework for SID tokenizer artifacts:
> any method that can emit `sid_assignments` plus joinable metadata/interactions
> can be adapted, validated, and inspected through D1-D5 diagnostics.

Under this frame:

- GRID and ReSID are **worked examples / public export paths**, not the center
  of the contribution.
- sanity rows and controlled mechanism probes are **first-class diagnostic
  validation evidence**, not degraded method substitutes.
- Table 1 should emphasize evidence roles, adapter status, supported
  diagnostics, and caveats rather than method-count coverage.
- Table 2 should be a worked example showing what the framework surfaces.
- Table 3 should be called controlled mechanism probes, because its role is to
  test diagnostic sensitivity to known failure mechanisms.

## Self-Implemented Tokenizers And Probes

Self-implemented artifacts are allowed only when their evidence role is named
correctly.

Allowed:

- `AUDIT-SID reference implementation of a minimal RQ tokenizer`;
- controlled mechanism probes for collision qualification, capacity budgeting,
  variable depth, or other diagnostic mechanisms;
- sanity tokenizers that calibrate metric behavior.

Not allowed:

- calling a local implementation "CARD", "AdaSID", "CapsID", or another named
  recent method unless it faithfully follows the released method and documents
  all deviations;
- using self-implemented artifacts to claim reproduced ranking performance;
- treating probes as named-method coverage.

Every reference implementation or probe must ship an implementation note that
states which paper/mechanism it follows, what is simplified, what inputs it
uses, and which claims it can and cannot support.

## Immediate Paper Changes

The next writing pass should prioritize framing, not new experiments:

1. Abstract: replace method-comparison emphasis with the missing artifact
   inspection interface and use two public exports plus controlled mechanism
   probes to demonstrate adapter and diagnostic behavior.
2. Section 2: add an Adapter Specification paragraph or compact table covering
   required adapter outputs, validator gates, and extension workflow.
3. Section 4: rename from a generic demonstration/finding frame toward
   "Worked Example" language.
4. Table 3: rename controlled stressors to controlled mechanism probes and
   explain that probes validate diagnostic sensitivity.
5. Table 1: make evidence role and supported diagnostics more central than
   method coverage breadth.

## Optional Future Type 1 Path

After CIKM v0, SIDInspector/AUDIT-SID can evolve toward a coverage resource if the project
adds:

- at least 5--8 faithful named-method adapters or author-provided mappings;
- a stable adapter registry and contribution guide;
- common dataset cards and protocol cards;
- clean reproduction boundaries for each method;
- CI checks that run validators and a bounded metric smoke for every adapter.

That is a larger resource-platform project. It should not be mixed into the
current CIKM v0 claim.
