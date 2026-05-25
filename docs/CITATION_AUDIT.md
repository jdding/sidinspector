# SIDInspector Citation Audit

Timestamp: 2026-05-21 12:23:46 CST

Scope: final high-risk metadata polish plus an ICML 2026 official-list scan for
missing SID/tokenizer references in the CIKM 2026 Resource Track paper source
used to generate the submitted PDF snapshot. The public reviewer artifact keeps
the compiled PDF and verified BibTeX asset, but not the TeX source tree.

## Verdict

PASS after proceedings-record upgrades and one ICML 2026 SID/tokenizer addition.

The active paper cites 28 unique keys, all 28 exist in the verified BibTeX
asset, and there are no uncited bib entries in the active bibliography. The final pass
focused on high-risk SID/resource references: RecList, TIGER, GRID, ReSID, DACT,
QuaSID/AdaSID/CARD/CapsID/AsymRec, Snapchat SID, SID-Coord, recently accepted
ACM records, and ICML 2026 SID/tokenizer candidates.

## Fixes Applied

| Key | Change |
|---|---|
| `hua2023indexids` | Upgraded from arXiv `@misc` to the official SIGIR-AP 2023 ACM proceedings record with DOI `10.1145/3624918.3625339`. |
| `wang2024letter` | Upgraded from arXiv `@misc` to the official CIKM 2024 ACM proceedings record with DOI `10.1145/3627673.3679569`. |
| `liu2024elit` | Upgraded from arXiv `@misc` to the official SIGIR 2025 ACM proceedings record with DOI `10.1145/3726302.3729989`. |
| `zhang2026hgrec` | Added from the official ICML 2026 poster record because it directly concerns hyperbolic RQ-VAE, generative recommendation, differential-length codebooks, codebook utilization, and collision rates. |
| `baikalov2026staleness` | Kept as arXiv because the DOI is not yet resolved by Crossref; added accepted-by-SIGIR-2026 note from arXiv. |
| `li2026sidcoord` | Kept as arXiv because the related DOI is not yet resolved by Crossref; added accepted-by-SIGIR-2026 note from arXiv. |
| `ju2026snapchatsid` | Added SIGIR 2026 Industry Track acceptance note from arXiv. |

The same BibTeX content is now synchronized in:

- `paper_assets/references/audit_sid_references.bib`

## ICML 2026 Scan Result

Official ICML 2026 sources checked:

- `https://icml.cc/virtual/2026/papers.html`
- `https://icml.cc/Downloads/2026`
- `https://icml.cc/virtual/2026/poster/65614`
- `https://icml.cc/virtual/2026/poster/63723`

Strong relevant addition:

- `Hyperbolic RQ-VAE enhanced Generative Recommendation with Differential-Length Codebook Strategy` (ICML 2026 poster 65614). Official abstract states that the method enhances residual quantization in hyperbolic space, uses a differential-length codebook strategy, and reports lower collision rates, more uniform codebook usage, and less training time. This supports the D5 structural-cost discussion and is now cited there.

Screened but not added:

- `SynGR: Unleashing the Potential of Cross-Modal Synergy for Generative Recommendation` is about cross-modal synergy in generative recommendation and item identifiers, but the official abstract does not make a SID tokenizer/codebook artifact claim. It is not strong enough for the current four-page SIDInspector paper.
- Other ICML 2026 recommendation papers found by title search are broader recommender/generative-rec work, not SID/tokenizer artifact diagnostics.

## Spot-Checked Sources

Primary source checks included ACM/Crossref metadata for RecList, SIGIR-AP
2023, CIKM 2024, and SIGIR 2025 records; NeurIPS proceedings for TIGER; ICML
2026 official poster/list pages for HG-Rec and SynGR; and arXiv pages for
ReSID, DACT, QuaSID, AdaSID, CARD, CapsID, AsymRec, ACERec, SID staleness,
SID-Coord, Snapchat SID, GRID, DIGER, DiscRec, LETTER, CoST, and related
SID/tokenizer work.

## Compile / Verification

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`: passed.
- Output PDF: 5 pages; page 5 contains GenAI Usage Disclosure and references.
- Remaining LaTeX warnings: local `acmart` unused `natbib=true` option and
  `balance` second-column warning only.
- `python3 tools/verify_paper_artifact.py`: passed.

## Remaining Watch Items

1. Do not add more citations for count; the active 28-entry bibliography is
   enough for a four-page Resource paper.
2. If submitting after a long delay, recheck the 2026 arXiv accepted-paper
   entries and ICML 2026 papers whose official DOI/PMLR metadata were not yet
   resolvable.
3. The anonymous artifact URL should still be tested manually in a browser;
   command-line `curl` can hit a Cloudflare challenge and is not a reliable
   reviewer-experience test.
