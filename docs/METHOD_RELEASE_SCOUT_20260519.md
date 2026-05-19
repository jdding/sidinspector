# AUDIT-SID Method Release Scout

Timestamp: 2026-05-19 17:27:18 CST

Scope: official/primary-source release search for a possible third named
tokenizer artifact. Non-official reproductions and local reimplementations are
not accepted as named evidence.

## Verdict

None of QuaSID, AdaSID, CapsID, or DIGER is ready to enter AUDIT-SID v0 main
evidence today.

- QuaSID, AdaSID, and CapsID: paper-only from the primary-source screen. No
  official code, SID export, processed dataset, checkpoint, supplement, Zenodo,
  OpenReview artifact, or Hugging Face model/dataset was found.
- DIGER: official GitHub exists, but it is explicitly an illustrative/reference
  implementation. It requires external processed data, semantic embeddings, and
  a pre-trained RQ-VAE checkpoint; the README says runnable code plus processed
  data/checkpoints are planned before SIGIR 2026. It has no GitHub releases and
  no tags as of this scout.

Recommendation: keep all four out of v0 main evidence. DIGER is worth a GitHub
issue because the official repo already exists and has open issues enabled.
QuaSID/AdaSID/CapsID are worth short author emails only if the paper needs a
future-release statement or permission to cite artifact unavailability.

## Release Matrix

| method | primary source checked | official code/artifact status | SID export availability | dataset/checkpoint availability | AUDIT-SID fit (D1-D5a/D7) | risk | next action |
|---|---|---|---|---|---|---|---|
| QuaSID | arXiv page/PDF/TeX for `2603.00632`; exact-title web/GitHub/HF/OpenReview/Zenodo searches | No official repo or artifact found. arXiv page exposes only paper/PDF/HTML/TeX plus generic code-discovery widgets, not an author release. | None found. | None found. Paper reports public and industrial data, but no official processed assets/checkpoints were located. | Strong conceptual fit for D2 collision qualification; possible D1/D3/D4 if item-to-SID mappings ever appear; no D7. | High: industrial-scale paper, no public artifact, no export contract. | Do not use as v0 evidence. Cite only as D2/D2b motivation. Email authors if a third B2 method becomes necessary. |
| AdaSID | arXiv page/PDF/TeX for `2604.23522`; exact-title web/GitHub/HF/OpenReview/Zenodo searches | No official repo or artifact found. arXiv page has no code link in the paper metadata. | None found. | None found. Public benchmark results are described, but no processed data/checkpoint release was found. | Strong D1/D2/D4 fit; possible D3 if collaborative alignment artifacts are exposed; no current D7. | High: likely industrial/proprietary components; no official export. | Do not use as v0 evidence. Keep as adaptive collision/capacity coverage. Email only for release roadmap or SID mappings. |
| CapsID | arXiv page/PDF/TeX for `2605.05096`; exact-title web/GitHub/HF/OpenReview/Zenodo searches | No official repo or artifact found. arXiv page has no author code link. | None found. | None found. Paper claims Amazon Beauty/Sports/Toys plus proprietary catalog, but no checkpoint/dataset artifacts were located. | Strong D4/D5a fit because variable-length SID and soft routing affect capacity/cost; D1/D2 possible; D7 only if generation traces appear. | High: very recent paper; variable-length/soft SID may need custom adapter even after release. | Do not use as v0 evidence. Keep as B2/B4 motivation. Email authors if variable-length SID export would materially improve the paper. |
| DIGER | arXiv `2601.19711` v3; official GitHub `junchen-fu/DIGER`; `git ls-remote` heads/tags | Official repo exists, but README says current release is illustrative/reference, not full end-to-end. No GitHub releases; `git ls-remote` found only `main` and no tags. | Not directly available. Current code can train from user-supplied data/checkpoints but does not publish ready item-to-SID mappings. | Not available in repo. README says processed data, embeddings, configs, and pre-trained RQ-VAE checkpoints are planned before SIGIR 2026. | Best B3/D3/D7 future target because it aligns SID learning with recommendation loss; current mapping-only D1-D5a could run only after full assets or a faithful export. | Medium-high: official but incomplete; using it now would blur reference code with reproducible artifact. | File a polite GitHub issue asking for item-to-SID export format, processed public assets, and checkpoint ETA. Recheck near SIGIR 2026. |

## Source Notes

- QuaSID arXiv primary source: `https://arxiv.org/abs/2603.00632`. Submitted
  2026-02-28; metadata provides PDF/HTML/TeX, but no author code link. The
  abstract defines Qualification-Aware Semantic ID Learning and reports public
  plus Kuaishou online results.
- AdaSID arXiv primary source: `https://arxiv.org/abs/2604.23522`. Submitted
  2026-04-26; metadata provides PDF/HTML/TeX, but no author code link. The
  abstract describes adaptive overlap regulation and public plus Kuaishou
  results.
- CapsID arXiv primary source: `https://arxiv.org/abs/2605.05096`. Submitted
  2026-05-06; metadata provides PDF/HTML/TeX, but no author code link. The
  abstract describes soft-routed variable-length SIDs and SemanticBPE.
- DIGER arXiv primary source: `https://arxiv.org/abs/2601.19711`. v3 was
  revised 2026-04-14, accepted by SIGIR 2026, and links to the GitHub repo.
- DIGER official repo: `https://github.com/junchen-fu/DIGER`. README states the
  current repository is illustrative/reference and plans runnable code, configs,
  processed data, embeddings, and pre-trained RQ-VAE checkpoints before SIGIR
  2026. The GitHub page reports no releases.
- Local read-only check: `git ls-remote --heads --tags
  https://github.com/junchen-fu/DIGER.git` returned only `refs/heads/main`;
  `git ls-remote --tags` returned no tags.

## Main-Evidence Decision

Current v0 main evidence should remain restricted to methods with actual
joinable item-to-SID mappings and diagnostic-ready artifacts. None of these
four passes the minimum gate:

1. true named method artifact;
2. stable item IDs and item-to-SID export;
3. metadata/interactions joinability;
4. at least D1-D5a mapping diagnostics or uniquely important D7 traces;
5. finding not already covered by GRID/ReSID/controls.

DIGER is the only near-term candidate because it has an official repo and a
public release roadmap. QuaSID/AdaSID/CapsID are method-coverage and motivation
only until an official artifact appears.

## Suggested GitHub Issue For DIGER

Title: Request for reproducible SID export assets for AUDIT-style diagnostics

Body:

```text
Hi, thanks for releasing the DIGER reference implementation.

I am working on an artifact-level diagnostic toolkit for semantic-ID tokenizers
in generative recommendation. For DIGER, the most useful reproducibility assets
would be:

1. processed public datasets / semantic embedding files used in the paper;
2. the pre-trained RQ-VAE checkpoints expected by RQVAE_INIT / rqvae_path;
3. a deterministic item_id -> SID export script or saved mapping for Beauty,
   Instruments, or Yelp;
4. any generator outputs or beam traces, if available, for decoding diagnostics.

The README says a fuller release is planned before SIGIR 2026. Is there an
expected timeline or preferred export format for these assets?

Thanks.
```

## Suggested Author Email For QuaSID/AdaSID/CapsID

Subject: Question about official Semantic ID artifacts for [METHOD]

```text
Dear authors,

I am preparing an artifact-level diagnostic study of semantic-ID tokenizers for
generative recommendation. I am only using official releases as named evidence.

Could you let me know whether you plan to release any of the following for
[METHOD]?

1. official code;
2. processed public benchmark data or item embeddings;
3. pretrained tokenizer/checkpoint files;
4. item_id -> SID mappings or an export script;
5. generator outputs / beam traces, if available.

Even a short release-roadmap answer would help us decide whether to keep the
method as future coverage or include it in a reproducible artifact screen.

Best regards,
```
