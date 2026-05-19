# AUDIT-SID Figure And Table Strategy

Timestamp: 2026-05-19 15:36:33 CST

Scope: decide which figures and tables should appear in the 4-page CIKM
Resource paper, and how they should be integrated into the current draft.

Inputs:

- current compiled draft: `paper/main.tex`, `paper/main.pdf`;
- current table assets: `paper_assets/tables/`;
- format constraint: `docs/CIKM_RESOURCE_FORMAT_AUDIT.md`;
- taxonomy refresh: `docs/SID_CLUSTER_DIAGNOSTIC_REFRESH.md`;
- reference refresh: `docs/SID_REFERENCE_REFRESH.md`;
- external resource/toolkit paper patterns from CIKM/SIGIR/RecSys-style
  artifacts and calls.

## Bottom Line

Use **one generated vector figure and three tables** in the body.

| Slot | Artifact | PDF role | Status |
|---|---|---|---|
| Fig. 1 | AUDIT-SID artifact contract + diagnostic map | explains what the toolkit is | integrated in §2 |
| Table 1 | method/facet coverage matrix | proves resource scope and honesty | redesigned in §2 |
| Table 2 | same-item Musical diagnostic case study | proves diagnostics produce useful signals | compacted in §3 |
| Table 3 | reviewer-facing artifact package | proves resource usability and provenance surface | added in §4 |

Do **not** put DACT churn, MovieLens portability, GRID scale, or sanity-control
result tables in the PDF. They should remain artifact-repository evidence
referenced from §4. Table 3 is not a result table; it is an artifact package
checklist for reviewers.

Implementation status as of 2026-05-19 14:20:21 CST: Fig. 1 is generated from
`tools/paper_figures/generate_audit_sid_pipeline.py` and explicitly tied to
comparable audit artifacts. Table 1 is a facet/status/boundary matrix. Table 2
is the same-item Musical diagnostic table with metric directionality and D5a
prefix counts. Table 3 is now a reviewer action checklist rather than a generic
component list. `latexmk` compiles `paper/main.pdf` to 5 pages total, with the
body filling through page 4 and references/GenAI disclosure on page 5.

Revision note as of 2026-05-19 15:36:33 CST: Fig. 1 should be reconsidered
before the next serious draft review. The current linear pipeline is correct
but visually low-signal. A stronger figure should explain the artifact
contract, diagnostic facets, and evidence maturity boundaries in one glance.

This matches resource-paper expectations: the paper must be self-contained, but
resource details can live online if the core value proposition is visible in
the main body.

## External Pattern Scan

### What Resource/Toolkit Papers Usually Show

Across resource/toolkit papers such as RecBole, Elliot, RecList-style
diagnostic tooling, and dataset/resource papers, the repeated pattern is:

1. **System/interface figure**: what enters the resource, what it normalizes,
   and what it outputs.
2. **Capability/coverage table**: which tasks, datasets, models, or modules are
   covered, and what is not covered.
3. **One concrete demo table/plot**: a small example proving the resource is
   operational, not just conceptual.
4. **Availability/provenance paragraph**: where code, data, commands, and logs
   live.

AUDIT-SID should follow this structure. It should not spend the main PDF on a
leaderboard-style method comparison because the current claim is toolkit value,
not model superiority.

### Relevant Venue Constraints

CIKM Resource paper rules make the PDF extremely tight: four pages include
appendices and acknowledgments, while references and GenAI disclosure are
unlimited. Therefore:

- the PDF needs the interface, coverage, and one diagnostic case;
- reproducibility details go to GitHub;
- no core evidence should be appendix-only.

SIGIR-style resource guidance similarly emphasizes novelty, availability,
reproducibility, documentation, and a clear real-world use case. This reinforces
the same design: one interface figure plus one coverage table plus one usage
case.

## Current Assets Inventory

| Existing asset | Best use |
|---|---|
| `paper_assets/tables/table1_method_coverage.*` | redesign into Table 1 in PDF |
| `paper_assets/tables/table2_musical_diagnostic.*` | keep as Table 2 in PDF, with D5a prefix counts and directionality |
| `paper_assets/tables/table3_sanity_controls.*` | artifact repo; mention as metric sensitivity controls |
| `paper_assets/tables/table4_grid_scale.*` | artifact repo; mention as scale/stability evidence |
| `paper_assets/tables/table5_dact_d6_churn.*` | artifact repo; mention as optional D6 extension |
| `paper_assets/tables/table6_movielens_portability.*` | artifact repo; mention as non-Amazon schema smoke |
| `docs/SID_CLUSTER_DIAGNOSTIC_REFRESH.md` | update Table 1 to B1-B4 facets and D1-D7 taxonomy |
| `paper/figures/fig1_audit_sid_pipeline.pdf` | generated vector Fig. 1 used in the PDF |
| `paper/main.pdf` | currently 5 pages total; body fills through page 4 |

## Fig. 1 Redesign Brief

Figure ID: Fig. 1.

Claim supported: AUDIT-SID is a reusable artifact-audit contract for SID
tokenizers, not a new tokenizer and not a leaderboard.

Reader takeaway in 10 seconds: reviewers should understand which files a new
tokenizer must export, which diagnostics run from mappings alone, and why D6/D7
require additional temporal or generator-output artifacts.

Evidence role: system/interface figure with claim-boundary annotation.

Data source: schema contract from `src/audit_sid/interface.py`, current
diagnostic taxonomy in `docs/SID_CLUSTER_DIAGNOSTIC_REFRESH.md`, and evidence
status from Table 1.

Unit of analysis: artifact fields and diagnostics, not model architecture.

Statistics: none.

Visual grammar: compact three-band evidence map:

1. **Artifact contract band**: required inputs
   `sid_assignments`, `item_metadata`, `interactions`, plus optional
   `generator_outputs` and temporal snapshots.
2. **Diagnostic band**: D1 utilization, D2 collisions, D3 collaborative
   alignment, D4 head-tail capacity, D5a prefix/trie structure; optional D6
   churn; future D7 generator behavior.
3. **Evidence maturity band**: main named exports, controls, resource-only
   tables, future/backlog methods.

Caption claim:

> AUDIT-SID separates the artifact contract from diagnostic coverage and
> evidence maturity: v0 computes D1-D5a from item-to-SID mappings, optionally
> computes D6 from temporal snapshots, and reserves D7 for artifacts with
> generator outputs.

Review risk:

- Do not imply D7 is implemented for current named methods.
- Do not imply CARD/DIGER/QuaSID are reproduced if they are only taxonomy rows.
- Do not let the figure become a decorative architecture diagram.

Implementation target:

- Replace `tools/paper_figures/generate_audit_sid_pipeline.py` with a
  publication-style vector figure using restrained colors and direct labels.
- Generate deterministic PDF metadata as in the current script.
- Preserve a source-data/figure brief entry in `MANIFEST.md`.

## Recommended PDF Layout

### §1 Introduction

No figure or table.

Use prose to set the problem and cite the wider method space. The reader should
not hit a table before understanding that AUDIT-SID is an artifact-audit
resource.

### §2 Toolkit and Diagnostics

Add **Fig. 1** near the top of §2, before the D1-D5a paragraphs.

Recommended caption:

> AUDIT-SID normalizes heterogeneous tokenizer exports into a mapping-first
> artifact contract, then computes D1-D5a mapping diagnostics, optional D6
> churn, and future D7 generator/retrieval diagnostics when generated outputs
> are available.

Recommended content:

```
Tokenizer repos / SID exports
        |
        v
sid_assignments + item_metadata + interactions + optional generator_outputs
        |
        v
adapter validation + join checks + provenance manifest
        |
        v
D1 utilization | D2 collisions | D3 collab alignment | D4 head-tail
D5a structure cost | D6 churn optional | D7 generator behavior future
        |
        v
CSV/Markdown/LaTeX audit tables + failure-case slices
```

Design:

- single-column figure if using text-heavy diagram;
- two-column figure only if drawn as compact vector blocks;
- avoid decorative architecture art;
- emphasize the schema and output contract, not a machine-learning model.

Implementation options:

1. safest: LaTeX `figure` with compact `tabularx` or `fbox` blocks;
2. better visual: generate `paper/figures/fig1_audit_sid_pipeline.pdf` as a
   vector diagram;
3. avoid TikZ unless we want template/dependency churn.

### §2 or §3 Boundary

Place **Table 1** after the D1-D7 scope explanation. It should be a coverage
matrix, not a list of random methods.

Current Table 1 is useful but too coarse because it has one large "B" bucket.
Redesign it using the refreshed taxonomy:

| Row | Facet | Artifact status | v0 role | Diagnostics | Caveat |
|---|---|---|---|---|---|
| A canonical SID | GRID/RQ-KMeans | runnable export | main A | D1-D5a | Musical row uses feature text |
| B1 collaborative/predictability | ReSID/GAOQ | runnable export | main B | D1-D5a/D3 | bounded Musical export |
| B2 collision/utilization | CARD/QuaSID/AdaSID/CapsID | literature/backlog | motivates D1/D2/D4 | D1/D2/D4 | not run as named evidence |
| B3 ranking/differentiable | DIGER/joint search-rec | literature/backlog | motivates D3/D7 | D3/D7 | no generator outputs |
| C drift/staleness | DACT | optional smoke | optional D6 | D6 | not main B |
| Controls/portability | sanity + MovieLens smoke | runnable controls | metric sanity | D1-D5a | not named SID methods |

This table should answer reviewer questions in one glance:

- Do you cover both canonical and recent SID work?
- Which parts are runnable evidence?
- Which parts are only literature motivation?
- What diagnostics are covered?
- What is explicitly not claimed?

### §3 Resource Demo And Case Study

Keep **Table 2** as the only diagnostic result table in the PDF.

Current compact version:

| System | Unique | D2 coll. | D3 rec. | D4 tail | D5a prefixes |
|---|---:|---:|---:|---|---|

Keep both rows:

- GRID feature-text: 3,749 unique, 0.9769 full collision, 0.0552 D3-L1, tail
  cap. 0.3695.
- ReSID GAOQ: 23,742 unique, 0 full collision, 0.1535 D3-L1, tail cap. 1.0000.

Caption must be conservative:

> Same-item Musical diagnostic case study. The table compares artifact
> profiles, not downstream recommender quality. GRID feature-text uses ReSID
> processed feature text and is not a faithful raw-text TIGER reproduction.

Do not add an extra ReSID-vs-sanity table in the PDF. Mention it in text:

> Sanity controls and additional scale/portability tables are included in the
> artifact repository.

### §4 Resource Availability And Limitations

Keep **Table 3** as a reviewer action checklist, not a generic package table.
It should map actions to checked claims:

- quickstart/license -> MIT license and local verification commands;
- tests/table builders -> D1-D5a and optional D6 executability;
- generated CSVs -> numeric claims in Tables 1--2;
- manifest/claim audit -> runnable vs controlled vs optional evidence labels;
- auxiliary CSVs -> sanity, scale, churn, and MovieLens portability evidence.

## What Not To Include In The PDF

| Candidate | Decision | Reason |
|---|---|---|
| DACT D6 churn table | artifact repo only | optional extension; not core Gate 0A |
| MovieLens portability table | artifact repo only | validates schema portability, not SID method quality |
| GRID 20k/50k scale table | artifact repo only | useful provenance but not central story |
| ReSID vs sanity full table | artifact repo only | can be described in one sentence |
| CARD proxy table | do not include as method result | too easy to misread as faithful CARD |
| Full D1-D7 definition table | avoid in PDF | consumes space; Fig. 1 + prose is enough |

## Strong-Accept Figure/Table Upgrades

These upgrades are optional for the current 8.0/8.1 external-review state but
would help push the paper toward a stronger review:

1. Upgrade Fig. 1 using the redesign brief above.
2. Consider turning Table 2 into a compact same-item A/B diagnostic panel if a
   third real named method is added.
3. Add one resource-table pointer sentence for GRID 20k three-seed stability:
   duplicate SID rate 0.1524--0.1748 across seeds 42/43/44.
4. Keep ReSID/sanity, GRID scale, DACT churn, and MovieLens portability out of
   the PDF unless they directly support a sentence in §4.

## Concrete Draft Edits Needed

1. Fig. 1 is integrated in `paper/sections/2_toolkit.tex`.
2. Table 1 has been replaced with a facet-aware status/boundary matrix.
3. Table 2 has readable labels, directionality in the caption, and D5a prefix
   counts.
4. §2 states that v0 implements D1-D5a, D6 is optional, and D7 requires
   `generator_outputs`.
5. §4 includes a reviewer action checklist plus explicit CARD, GRID
   feature-text, D2, D3, D5a, and D6 caveats.

## Expected Page Budget

Current compiled draft is 5 pages total: body through page 4, references and
GenAI disclosure on page 5. The main body is within the intended four-page
Resource Track budget if references/disclosure remain unlimited.

- Table 1 stays full-width but compact;
- Table 2 stays single-column;
- §1 prose is not expanded further;
- DACT/MovieLens/GRID scale tables stay out of the PDF.

If the body spills beyond page 4, the first cuts should be:

1. compress §1 related-work paragraph;
2. move D7 discussion to one sentence;
3. reduce Table 1 caveat text;
4. remove the artifact checklist sentence.

Do not cut Table 2. It is the one concrete diagnostic case study.

## Current Recommendation

Proceed with a **resource-paper layout**:

- Fig. 1: "what AUDIT-SID is";
- Table 1: "what method/facet space it covers and what is runnable";
- Table 2: "what the diagnostics reveal on one real same-item case";
- Table 3: "what reviewers can run or inspect and which claims it checks".

This is stronger than adding more result tables. It aligns the paper with
resource-track review criteria and reduces the risk that reviewers interpret
the work as an underpowered SID benchmark.
