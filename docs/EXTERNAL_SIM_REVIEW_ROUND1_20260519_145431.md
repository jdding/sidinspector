# AUDIT-SID External Simulated Review Round 1

Timestamp: 2026-05-19 14:54:31 CST

Target venue/track: CIKM 2026 Resource Track.

External target: 8.0 / 10.

## Reviewers

- Reviewer A: Resource/artifact availability, reproducibility, documentation,
  maintenance, and clean-checkout utility.
- Reviewer B: SID/recommender technical evidence, method representativeness,
  D1--D5a interpretability, and overclaim risk.

## Initial Scores

| Reviewer | Initial score | Main blockers |
|---|---:|---|
| Resource/artifact | 7.2 | missing real tag/release, uncommitted artifact files, clean checkout could not rebuild tables, single-blind metadata |
| SID/recommender | 7.4 | artifact URL/commands absent from paper, D3/D5a definitions too compressed, method breadth still conservative |

## Fixes Applied

- Added `requirements.txt`.
- Added `ARTIFACT_MANIFEST.md` as a reviewer-facing public artifact manifest,
  separate from the full ARIS `MANIFEST.md` ledger.
- Added `tools/verify_paper_artifact.py`, a clean-checkout verifier that checks
  public files and exact Table 2 numeric claims without requiring ignored
  `_gate0_artifacts/` caches.
- Reworked `ARTIFACT_QUICKSTART.md` around a pinned review tag
  `audit-sid-cikm-resource-v0.1`, clone/install/test/figure/verifier commands,
  expected output, runtime, and troubleshooting.
- Updated Section 4 and Table 3 so reviewers run tests plus the public verifier
  from a clean checkout; full metric rebuilds are explicitly optional and
  require local experiment caches.
- Expanded D2/D3/D5a definitions in the paper: D2 is item fraction sharing a
  full SID, D3 is top-20 co-occurrence prefix recovery, and D5a is prefix/fanout
  structure rather than latency.
- Tightened Table 2 caption/labels and Table 1 header to reduce benchmark or
  named-method misreading.
- Recompiled with no overfull boxes, undefined citations, or LaTeX errors.

## Re-review Scores

| Reviewer | Re-review score | Status |
|---|---:|---|
| Resource/artifact | 7.7 local; 8.0 after commit/tag/push/clean clone | P0 reduced to publication freeze and author metadata |
| SID/recommender | 7.7 local; 8.0--8.1 after commit/tag/push/clean clone | Technical and claim-boundary issues no longer block 8 |

## Remaining External 8.0 Gate

1. Commit and push the current artifact files.
2. Create and push the `audit-sid-cikm-resource-v0.1` tag.
3. Run a clean checkout from that tag and execute the quickstart verifier.
4. Replace anonymous local-draft author metadata before final CIKM submission.

The first three items are engineering/release tasks and do not require new
experiments. The fourth requires the real author/affiliation block and should
not be invented in the local draft.

## Current Judgment

No new experiment is required to reach external 8/10. The technical paper is
now a conservative Resource Track artifact paper. The remaining score gap is
release/package availability, plus final single-blind metadata.
