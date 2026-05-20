# SIDInspector Citation Audit

Timestamp: 2026-05-21 01:58:00 CST

Scope: active CIKM 2026 Resource Track paper sources:

- `paper/main.tex`
- `paper/sections/1_introduction.tex`
- `paper/sections/2_resource_scope.tex`
- `paper/sections/3_diagnostics.tex`
- `paper/sections/4_demonstration.tex`
- `paper/sections/5_availability_limits.tex`
- `paper/references.bib`

## Verdict

PASS after metadata fixes.

The reference set is now appropriate for the current SIDInspector resource
framing. It covers the 2023 learned-ID / TIGER foundation, 2024--2025
collaborative and learnable tokenizer work, and the 2026 wave on ReSID,
collision qualification, adaptive collision handling, differentiable SID,
variable/asymmetric SID interfaces, drift/staleness, and industrial/search
deployment surfaces.

## Counts

| Item | Count | Note |
|---|---:|---|
| BibTeX entries in `paper/references.bib` | 27 | all active after this pass |
| Unique cite keys in active paper source | 27 | no uncited bib entries remain |
| Missing cited keys | 0 | all cited keys exist in the bib |
| 2024--2026 references | 20 | main recent-SID coverage |
| 2025--2026 references | 16 | recent method-space coverage |
| Older retained anchors | 7 | 2021--2023 foundations/toolkit precedents |

## Metadata Fixes Applied

| Key | Problem found | Fix |
|---|---|---|
| `hua2023indexids` | author list/order drifted from arXiv record | corrected to Wenyue Hua, Shuyuan Xu, Yingqiang Ge, Yongfeng Zhang |
| `singh2023bettersemanticids` | wrong author set from an unrelated/incorrect record | corrected to Anima Singh et al. from arXiv |
| `zhu2024cost` | title/authors did not match arXiv:2404.14774 | corrected to CoST: Contrastive Quantization based Semantic Tokenization for Generative Recommendation, Jieming Zhu et al. |
| `wang2024letter` | title/authors did not match arXiv:2405.07314 | corrected to Learnable Item Tokenization for Generative Recommendation, Wenjie Wang et al. |
| `ju2026snapchatsid` | title shortened and author list belonged to a different/older scaffold | corrected to the full Snapchat title and Clark Mingxuan Ju et al. author list |
| `chia2022reclist` | author list drifted to unrelated recommender-system authors | corrected to Patrick John Chia, Jacopo Tagliabue, Federico Bianchi, Chloe He, Brian Ko; added pages 99--104 and ACM DOI metadata |
| `rajput2023tiger` | NeurIPS entry lacked pages/volume metadata under `ACM-Reference-Format` | added NeurIPS 36, pages 10299--10315, publisher/address, and proceedings URL |
| `fu2026diger` | accepted future SIGIR entry had no final proceedings pages | represented as arXiv:2601.19711 with accepted-by-SIGIR note until final proceedings metadata appears |
| `penha2025jointsid` | RecSys late-breaking entry had no final proceedings pages in the active bib | represented as arXiv:2508.10478 with accepted-by-RecSys-LBR note |
| `anelli2021elliot` | ACM entry lacked publisher/address/series fields | added ACM publisher/address and SIGIR '21 series metadata |

The same fixes were applied to both:

- `paper/references.bib`
- `paper_assets/references/audit_sid_references.bib`

## Recent-Coverage Assessment

| Literature role | Current coverage | Verdict |
|---|---|---|
| Foundation / learned identifiers | How to Index Item IDs, TIGER, Better Generalization with Semantic IDs | sufficient; keep older anchors |
| Resource / evaluation tooling precedent | RecList, Elliot | sufficient; do not replace only because older |
| 2024 collaborative / learnable tokenizers | LC-Rec, CoST, LETTER, ETEGRec | sufficient |
| 2025 method-space broadening | GRID, DiscRec, joint search-rec SID | sufficient after activating DiscRec citation |
| 2026 tokenizer/codebook methods | ReSID, DIGER, CARD, QuaSID, AdaSID, CapsID, AsymRec, ACERec, Text-as-Vision | strong coverage |
| 2026 drift/deployment/search surfaces | DACT, SID staleness, SID-Coord, Snapchat SID | strong coverage |

## Old References: Keep Or Replace?

Do not replace the older references mechanically.

- `anelli2021elliot` and `chia2022reclist` are not SID-tokenizer papers, but
  they justify resource/evaluation-tool framing. They should remain.
- `rajput2023tiger`, `hua2023indexids`, and `singh2023bettersemanticids` are
  older than the newest tokenizer wave, but they are foundation papers for
  learned IDs, generative retrieval, and ranking/industrial SID use. They
  should remain.
- The recent-method coverage is now carried by the 2024--2026 citations rather
  than by replacing these anchors.

## Citation Context Audit

| Paper section | Citation role | Verdict |
|---|---|---|
| Introduction | TIGER establishes generative retrieval with SID sequences; recent papers motivate artifact inspection | supported |
| Resource Scope | RecList/Elliot support diagnostic and reproducible-evaluation framing beyond aggregate metrics | supported |
| Diagnostic Design | recent methods motivate collaborative alignment, collision qualification, variable/asymmetric interfaces, drift, and deployment surfaces | supported after adding DiscRec and AsymRec |
| Availability / Limits | CARD, survey, joint search-rec, Better Generalization, SID-Coord, Snapchat SID support limits and future coverage | supported |

## Sources Spot-Checked In This Pass

Primary public pages used in this pass include:

- arXiv:2305.06569, How to Index Item IDs for Recommendation Foundation Models
- arXiv:2306.08121, Better Generalization with Semantic IDs
- arXiv:2404.14774, CoST
- arXiv:2405.07314, LETTER
- arXiv:2506.15576, DiscRec
- arXiv:2507.22224, GRID
- arXiv:2601.19711, DIGER
- arXiv:2602.02338, ReSID
- arXiv:2602.13573, ACERec / Long SID
- arXiv:2603.00632, QuaSID
- arXiv:2604.03949, Snapchat SID
- arXiv:2604.10471, SID-Coord
- arXiv:2604.13273, SID staleness
- arXiv:2604.23522, AdaSID
- arXiv:2605.05096, CapsID
- arXiv:2605.14512, AsymRec
- IR Anthology / DBLP page for RecList, confirming WWW Companion 2022 authors,
  pages 99--104, and DOI 10.1145/3487553.3524215
- NeurIPS Proceedings page for TIGER/generative retrieval, confirming title,
  authors, and NeurIPS 2023 venue; page range cross-checked against proceedings
  metadata

## Remaining Watch Items

1. Recheck accepted-venue metadata immediately before final submission, because
   several 2026 papers are fresh arXiv / accepted-manuscript records.
2. Do not add more references only for count. The current 27 active entries are
   enough for a four-page Resource paper.
3. If page pressure appears, prune prose before pruning references; references
   are not the current page-budget bottleneck.
