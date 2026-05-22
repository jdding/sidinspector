# SIDInspector B5 Release Recheck

Timestamp: 2026-05-20 18:25:00 CST

## Verdict

B5 remains **NO-GO for implementation**. The release recheck did not find a new
official item-to-SID mapping, checkpoint package, or processed public artifact
that can enter the SIDInspector v0 main evidence table as a third named method.

This confirms the current plan: do not spend the sprint implementing a
paper-inspired third named tokenizer. Keep B5 as a lightweight release-watch
task only.

## Checks

| Method | Current status | Main-evidence decision |
|---|---|---|
| DIGER | Official GitHub exists, but `git ls-remote --heads --tags https://github.com/junchen-fu/DIGER.git` still returns only `refs/heads/main` and no tags/releases in the local check. Prior author reply says datasets and RQ-VAE checkpoint are planned before SIGIR conference on July 20. | Not ready for v0 main evidence. Recheck near the promised release window. |
| QuaSID | Web/arXiv-style search still shows paper-level availability, not an official item-to-SID artifact. | Motivation/related work only. |
| AdaSID | Web/arXiv-style search still shows paper-level availability, not an official item-to-SID artifact. | Motivation/related work only. |
| CapsID | arXiv/aggregator pages expose the paper and request-code surfaces, but no official runnable SID export package was found in this recheck. | Motivation/related work only. |
| CARD | Existing local route remains proxy/control or incomplete `nu-rq-vae` repair; no new author-complete source/checkpoint/mapping was found in this recheck. | Do not promote current CARD rows to named-method evidence. |

## Claim Boundary

Safe wording:

> Additional named SID/tokenizer methods are tracked as future adapters, but v0
> only includes named rows when an official or author-provided artifact exposes
> stable item-to-SID mappings that pass the SIDInspector adapter contract.

Unsafe wording:

- B5 closes method coverage.
- DIGER/CapsID/QuaSID/AdaSID/CARD are audited as v0 named methods.
- A local reference implementation can substitute for an official named-method
  artifact.

## Next Recheck Trigger

- DIGER public release near SIGIR 2026 / July 20.
- Author replies with public item-to-SID mappings or checkpoint/export package.
- Official GitHub/Hugging Face/Zenodo artifact appears for QuaSID, AdaSID,
  CapsID, or CARD.
