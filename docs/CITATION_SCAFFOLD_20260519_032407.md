# Citation Scaffold

Timestamp: 2026-05-19 03:24:07 CST

Purpose: keep paper-writing citations auditable without inventing BibTeX from
memory. This is a scaffold, not final references.

## Core Citations To Verify Before LaTeX

| Topic | Candidate source | Current use | Status |
|---|---|---|---|
| Semantic-ID generative recommendation baseline | TIGER paper: `https://arxiv.org/abs/2305.05065` | motivates SID tokenizers and generative retrieval | verify title/authors/venue before BibTeX |
| ReSID / GAOQ | GitHub: `https://github.com/FuCongResearchSquad/ReSID`; arXiv: `https://arxiv.org/abs/2602.02338`; dataset: `https://huggingface.co/datasets/PIIR/ReSID-dataset` | Cluster B recent tokenizer/codebook innovation | verify paper metadata and code/data license |
| GRID / RQ-KMeans semantic ID exporter | arXiv: `https://arxiv.org/abs/2507.22224`; GitHub: `https://github.com/snap-research/GRID` | Cluster A canonical RQ-style exporter | verify paper metadata and exact module name |
| CARD / NU-RQ-VAE | GitHub: `https://github.com/HAI-UESTC/CARD` | method coverage/backlog, not main evidence | verify paper metadata; do not cite proxy as faithful CARD |
| DIGER | arXiv/paper page: `https://arxiv.org/abs/2601.19711`; GitHub observed in prior audit as `https://github.com/junchen-fu/DIGER` | future/literature support for ranking-aligned SID | verify release status close to submission |
| CapsID / AdaSID / AsymRec | paper pages / code pages if public | method coverage table only | verify code availability close to submission |

## Working Citation Roles

Intro:

- TIGER-style semantic-ID generation: explain why SID tokenizers matter.
- ReSID/CARD/DIGER/CapsID/AdaSID/AsymRec: show recent tokenizer/codebook
  innovation pressure.

Toolkit section:

- GRID/ReSID/CARD GitHub docs: justify artifact paths and adapter coverage.
- Do not over-cite code repositories as scientific claims; use them for
  artifact availability only.

Case study:

- ReSID processed Amazon-2023 dataset.
- Amazon public review data lineage where needed.

Limitations:

- Cite ReSID/CARD/DIGER only for method motivation, while stating that the
  current AUDIT-SID evidence is bounded and not full reproduction.

## Red Lines

- Do not generate BibTeX from memory.
- Do not cite CARD compact feature proxy as CARD result.
- Do not cite DIGER/CapsID/AdaSID/AsymRec as runnable evidence until code status
  is rechecked.
- Recheck all current-public-code statements before submission because public
  releases may change.
