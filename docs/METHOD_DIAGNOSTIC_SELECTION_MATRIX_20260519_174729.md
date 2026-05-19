# Method x Diagnostic Selection Matrix

Timestamp: 2026-05-19 17:47:29 CST

Purpose: provide a working table for selecting additional SID/tokenizer
methods that can produce credible diagnostic findings for AUDIT-SID. This file
is the practical screening table that sits between the paper-facing taxonomy in
`docs/SID_CLUSTER_DIAGNOSTIC_REFRESH.md` and the historical Gate 0A scoring in
`docs/METHOD_REPRESENTATIVENESS_AUDIT.md`.

## Why This Exists

The current CIKM Resource draft is externally reviewed at 8.0--8.1/10. To move
toward a stronger review, the most important missing ingredient is not another
diagnostic definition; it is more evidence material from true named tokenizer
artifacts. A method is valuable for the next sprint only if it can light up at
least one under-supported diagnostic facet and produce a non-redundant finding.

## Legend

Diagnostic cells:

- `R`: runnable/currently supported by a real artifact or a direct export path.
- `P`: proxy or controlled stressor only; useful for debugging, unsafe as
  named-method evidence.
- `S`: screen needed; plausible from the method design, but artifact status is
  not yet verified in this repo.
- `G`: requires generator outputs or beam/candidate traces.
- `T`: temporal snapshots required.
- `L`: literature motivation only for the current sprint.
- `-`: not a useful fit.

Priority:

- `MAIN`: already used as current v0 evidence.
- `HIGH`: first candidates for a third named method.
- `MED`: useful if a cheap export appears.
- `LOW`: keep in method coverage only unless code/artifacts improve.
- `CONTROL`: sanity or stress-test material, not named-method evidence.

## Selection Matrix

| Method / line | Facet | Current artifact state | D1 util | D2 collision | D3 collab align | D4 head-tail | D5a prefix cost | D6 drift | D7 generator/retrieval | Finding material | Priority | Next action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GRID / RQ-KMeans | A canonical SID | real exports: All_Beauty 5k/20k/50k; Musical feature-text controlled row now has seeds 42/43/44 | R | R | R | R | R | - | G | capacity/collision pressure; seed stability; same-item contrast vs ReSID | MAIN | surface Musical 3-seed stability and keep feature-text caveat explicit |
| ReSID / GAOQ | B1 + B2 | real Musical GAOQ mapping; Sports GAOQ stopped at CPU bottleneck | R | R | R | R | R | - | G | collision-free capacity vs weaker collab-prefix alignment; B1 runnable anchor | MAIN | do not reopen Sports unless a bounded GAOQ path is proven |
| CARD faithful path | B2 capacity/collision | failed for v0 main evidence: official CARD tree is missing required quantizer modules; local preflight depends on compatibility repair | L | L | L | L | L | - | G | non-uniform quantization would be valuable only with author-complete artifact | LOW | do not run; reopen only if authors release complete source/checkpoint/mapping |
| QuaSID | B2 collision qualification | paper verified; no official runnable artifact found in current screen | L | L | L | L | L | - | - | strongest fit for D2b interaction-qualified collision harm | LOW | cite/motivate D2b; do not run until code or artifacts appear |
| AdaSID | B2 adaptive capacity | paper verified; no official runnable artifact found in current screen | L | L | L | L | L | - | - | adaptive capacity/collision should produce clear D1/D2/D4 contrast | LOW | cite/motivate adaptive collision/capacity; do not run until code or artifacts appear |
| CapsID | B2 + B4 variable/soft SID | paper verified; no official runnable artifact found in current screen | L | L | L | L | L | - | G | variable/soft routing could make D4/D5a visibly different | LOW | coverage/motivation only for CIKM v0 |
| DIGER | B3 ranking/differentiable | public repo says current release is illustrative/reference and lacks data/checkpoints | L | L | L | L | L | - | G | ranking-aligned SID is the best bridge to D3/D7 if outputs exist | LOW | reject for v0 main evidence; revisit only after full release |
| AsymRec | B4 bottleneck/interface | code promised/unverified in current audit | S | S | S | S | S | - | G | input/output bottleneck and SID length pressure are good D5a/D7 material | MED | screen public availability; keep as coverage context otherwise |
| LC-Rec | B1 / A-to-B bridge | not locally audited for export | S | S | S | S | S | - | G | collaborative semantics can test D3 vs semantic category alignment | MED | screen for direct SID mapping artifact and dataset compatibility |
| CoST | B1 collaborative tokenization | literature only in current local state | L | L | S | L | L | - | - | motivates D3; likely useful if code exposes tokens | LOW | method coverage unless repo/artifact is easy |
| LETTER | B1 + B2 | literature only in current local state | L | S | S | S | L | - | - | collaborative regularization plus diversity can motivate D1/D3/D4 | LOW | method coverage unless runnable release is verified |
| DiscRec | B1 disentanglement | literature only in current local state | L | L | S | L | L | - | - | semantic/collaborative disentanglement motivates D3 | LOW | method coverage only for CIKM sprint |
| DACT | C drift/staleness | local Tools 0.6 -> 0.7 churn smoke passed | R | R | R | R | R | R/T | - | D6 churn and rare full-collision groups; optional extension | MED | keep as optional resource evidence, not Cluster B replacement |
| SID staleness / refresh papers | C | literature/current local code unverified | L | L | L | L | L | T | - | motivates D6 and catalog-refresh limits | LOW | cite/coverage only unless artifacts appear |
| Joint search-rec SID | D / B3 | literature/current local code unverified | S | S | S | S | S | - | G | strongest long-term D7 target for search-rec unification | LOW | coverage context; do not block CIKM v0 |
| Snapchat / industrial SID | D deployment | literature/industrial surface only | L | L | L | L | L | T | G | motivates D5a/D6/D7 boundaries | LOW | cite as motivation, not reproducible method evidence |
| Category-prefix sanity | control | implemented on Musical and MovieLens smoke | R | R | R | R | R | - | - | shows semantic/category grouping can overstate D3 without being a tokenizer | CONTROL | keep in artifact tables and finding text |
| Mod-collision hash sanity | control | implemented on Musical and MovieLens smoke | R | R | R | R | R | - | - | exposes collision collapse and D5a ambiguity | CONTROL | keep as negative control |
| Popularity-balanced sanity | control | implemented on Musical and MovieLens smoke | R | R | R | R | R | - | - | shows prefix-depth collapse and popularity/collab confounding | CONTROL | keep as calibration row |

## Current Coverage Gaps

| Gap | Why it matters | Best method facets to fill | Current best candidates |
|---|---|---|---|
| True B2 evidence | current B2 is mostly proxy/literature; D2/D4 findings need real collision-aware methods | collision/utilization/capacity | no immediate runnable candidate after 2026-05-19 screen; future QuaSID/AdaSID/CapsID/faithful CARD |
| True B3/D7 evidence | current D7 is only an interface hook; generator behavior would make D5a/D7 boundary concrete | ranking/retrieval/generator-output | DIGER, joint search-rec SID, AsymRec |
| Same-dataset A/B breadth | current same-item table has GRID feature-text and ReSID only | any real named method with Musical-compatible export | faithful CARD if exportable; otherwise a B2/B3 method with portable metadata join |
| Seed stability for B methods | GRID has 3-seed evidence; ReSID does not have complete multi-seed mappings | B1/B2 with cheap mapping export | ReSID only if GAOQ bottleneck is solved; otherwise a cheaper B2 method |

## Recommended Screening Order

1. **B2 first**: the first screen found QuaSID/AdaSID/CapsID to be paper-only
   for the current sprint. CARD original `nu-rq-vae` now fails the v0
   named-evidence gate because the official repository lacks the quantizer
   modules needed by the released wrapper. Do not run or add it unless authors
   release complete source/checkpoints/mappings.
2. **B3 second**: DIGER is rejected for v0 evidence because the public repo is
   an illustrative/reference release without data/checkpoints. Screen joint
   search-rec SID only if it exposes
   item-to-SID mappings; otherwise they become D7 motivation rather than
   current evidence.
3. **B4 third**: screen CapsID/AsymRec if code is actually public; they are
   useful for D4/D5a/D7 but likely costlier.
4. Keep controls as calibration rows, never as method coverage.

## Decision Rule For Adding A Method To Main Evidence

A new method can enter the main paper only if all are true:

1. It is a true named method artifact, not a proxy or stressor.
2. It exports item-to-SID mappings with stable item IDs.
3. It joins to metadata and interactions with zero or explainable gaps.
4. It supports at least three of D1/D2/D3/D4/D5a, or two diagnostics plus a
   uniquely important facet such as D7 generator outputs.
5. It creates a finding not already shown by GRID/ReSID/sanity controls.

If any condition fails, keep the method in Table 1 as coverage/backlog and do
not use it as paper evidence.

## Finding Hypotheses To Test

| Hypothesis | Needed methods | Diagnostics | Current status |
|---|---|---|---|
| Collision-free capacity and collaborative alignment are different objectives | ReSID + category/popularity controls; optional B1 method | D2, D3, D4 | already visible, can be sharpened |
| Collision-aware methods reduce harmful ambiguity without merely increasing SID length | true B2 method + GRID/ReSID | D1, D2, D4, D5a | needs third named B2 artifact |
| Ranking/retrieval-aligned tokenizers produce different D3/D7 profiles from mapping-only quantizers | true B3 method + generator outputs if available | D3, D5a, D7 | future unless DIGER/joint SID export is usable |
| Variable/asymmetric SIDs shift cost from capacity to decoding/interface complexity | B4 method + GRID/ReSID | D4, D5a, D7 | future unless CapsID/AsymRec becomes runnable |
| Drift-aware tokenizers trade churn for collision stability under refresh | DACT or staleness artifacts | D1, D2, D4, D6 | optional DACT smoke exists |

## Notes For Paper Use

- This matrix is for internal screening and resource-repo transparency. The
  PDF should keep Table 1 compact.
- Before running any new method, refresh public release status; several rows
  are based on local audit snapshots and may be stale.
- Do not broaden claims before evidence exists. A method marked `S` or `L` can
  motivate a diagnostic, but it cannot support an empirical finding.
