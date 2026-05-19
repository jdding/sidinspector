# Citation Audit

Timestamp: 2026-05-19 12:41:13 CST

Purpose: verify paper metadata from primary public pages before LaTeX writing.
This file is not final BibTeX.

## Verified Primary Sources

| Key | Verified source | Title | Authors / venue note | Paper role |
|---|---|---|---|---|
| `rajput2023tiger` | `https://arxiv.org/abs/2305.05065` | Recommender Systems with Generative Retrieval | Shashank Rajput et al.; arXiv says NeurIPS 2023 | motivates semantic-ID generative recommendation |
| `ju2025grid` | `https://arxiv.org/abs/2507.22224`; `https://github.com/snap-research/GRID` | Generative Recommendation with Semantic IDs: A Practitioner's Handbook | Clark Mingxuan Ju et al.; GRID GitHub public repo observed | canonical open framework / Cluster A artifact path |
| `liang2026resid` | `https://arxiv.org/abs/2602.02338`; `https://github.com/FuCongResearchSquad/ReSID` | Rethinking Generative Recommender Tokenizer: Recsys-Native Encoding and Semantic Quantization Beyond LLMs | Yu Liang et al.; ReSID GitHub and Hugging Face dataset linked from repo | Cluster B tokenizer/codebook motivation and artifact path |
| `fu2026diger` | `https://arxiv.org/abs/2601.19711`; `https://github.com/junchen-fu/DIGER` | Differentiable Semantic ID for Generative Recommendation | Junchen Fu et al.; arXiv says accepted by SIGIR 2026 | future/literature support for recommendation-aligned SIDs |
| `feng2026dact` | `https://arxiv.org/abs/2603.29705`; `https://github.com/HomesAmaranta/DACT` | Drift-Aware Continual Tokenization for Generative Recommendation | Yuebo Feng et al.; code availability stated on arXiv | optional D6 drift/churn motivation |
| `hu2026quasid` | `https://arxiv.org/abs/2603.00632` | Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale | Zheng Hu et al. | justifies D2b as future interaction-qualified collision harm |
| `penha2025jointsid` | `https://arxiv.org/abs/2508.10478` | Semantic IDs for Joint Generative Search and Recommendation | Gustavo Penha et al.; arXiv says RecSys 2025 LBR | future unified search-rec scope boundary |
| `wei2026card` | `https://arxiv.org/abs/2604.26427`; `https://github.com/HAI-UESTC/CARD` | CARD: Non-Uniform Quantization of Visual Semantic Unit for Generative Recommendation | Yibiao Wei et al.; code availability stated on arXiv | method coverage/backlog only; do not cite proxy as CARD result |
| `cikm2026resource` | `https://cikm2026.diag.uniroma1.it/resource-papers/` | CIKM 2026 Resource Papers submission page | official track page | confirms 4-page rule and supplementary-material boundary |

## Citation Use Rules

- Use TIGER/GRID/ReSID in the introduction and method-coverage narrative.
- Use DIGER/CARD/QuaSID/DACT/joint search-rec to motivate diagnostic gaps and
  future extensions, not as completed AUDIT-SID experimental evidence.
- Do not write BibTeX from memory. Generate final BibTeX only from verified
  arXiv/official pages.
- Recheck public code release status before final submission because repository
  availability can change.
