# Tokenizer Dataset Category Audit

**Time**: 2026-05-18 20:34:31 CST
**Question**: whether the current `Musical_Instruments`-only AUDIT-SID case study can withstand reviewer scrutiny.
**Decision**: `Musical_Instruments` is acceptable for local toolkit development and quick smoke, but it is weak as the only paper-facing dataset. Before spending AutoDL on formal Gate 0 evidence, add at least one canonical public vertical aligned with prior SID/tokenizer papers.

## Current AUDIT-SID Dataset State

| Role | Dataset | Status | Reviewer risk |
|---|---|---|---|
| Local development / smoke | ReSID processed Amazon-2023 `Musical_Instruments` | Downloaded, schema-audited, normalized, ReSID GAOQ mapping exported locally | Safe as smoke; weak as sole paper evidence because it is not the common SID/generative-rec benchmark triad |
| Planned backup | Amazon 2014 `Beauty` / `Sports` | Mentioned in spec only; no schema audit or mapping export yet | Cannot be presented as evidence |
| Portability smoke | MovieLens-1M | Deferred | Useful for toolkit generality, but does not solve tokenizer-paper vertical alignment by itself |

## What Candidate Tokenizer Papers/Repos Use

| Method / artifact family | Dataset verticals used or supported | Evidence | Implication for AUDIT-SID |
|---|---|---|---|
| TIGER / canonical RQ-VAE SID | Amazon 2014 `Beauty`, `Sports and Outdoors`, `Toys and Games` | NeurIPS paper dataset section reports these three categories and their stats | This is the strongest canonical benchmark target; `Musical_Instruments` alone does not align with TIGER's public evaluation norm |
| GRID / canonical SID framework | P5-style Amazon data: `beauty`, `sports`, `toys` | GRID README quick-start says available data includes beauty, sports, toys | If GRID remains Cluster A, we should prefer one of these categories |
| GenRec model zoo / modern GR benchmark | Amazon 2014 `Beauty`, `Sports`, `Toys`, plus `Home` in its current README | README states Amazon 2014 5-core protocol and reports Beauty/Sports/Toys/Home | Confirms Beauty/Sports/Toys are the community default, not Musical |
| ReSID | Processed Amazon-2023 categories include `Musical_Instruments`, `Sports_and_Outdoors`, `Toys_and_Games`, `Beauty_and_Personal_Care`, `Video_Games`, and others | ReSID repo example uses Musical; HF dataset tree lists multiple categories; run script has code sizes for 10 categories | ReSID can support a canonical vertical; using only Musical is a convenience choice, not a defensible final choice |
| CARD | Amazon Reviews 2014; local repo defaults/examples include `Beauty` and `Food` paths | CARD README says Amazon Reviews 2014; code defaults mention Beauty/Food | If CARD becomes fallback, Amazon 2014 Beauty is the most natural target |
| CapsID / recent variable-length SID | Reported on Amazon `Beauty`, `Sports`, `Toys`, plus industrial catalog | Web review summary reports Beauty/Sports/Toys | Supports the claim that recent tokenizer papers still use the standard triad |
| DIGER | Public abstract says multiple public datasets; secondary summary shows Amazon Beauty in analysis figure | Source evidence is weaker than TIGER/ReSID/GRID/CARD | Keep as Method Coverage Table / backup only until artifact and dataset details are verified |

## Risk Assessment

`Musical_Instruments` is not objectively unusable: our local audit shows 23,742 items, complete item-feature join coverage, sequential interactions, and category metadata. The problem is reviewer perception and comparability:

- it is a ReSID example category, not the common cross-paper SID benchmark;
- it is currently the only downloaded and audited dataset;
- if the paper claims general toolkit value from one convenience category, the reviewer can fairly ask why Beauty/Sports/Toys were not used;
- because AUDIT-SID is a resource paper, dataset choice is part of artifact credibility.

## Revised Recommendation

Use `Musical_Instruments` only as the **development smoke dataset**. For paper-facing Gate 0, add one of:

1. **Recommended single add-on**: ReSID processed Amazon-2023 `Sports_and_Outdoors`.
   - It is a canonical vertical name shared with TIGER/GRID/GenRec/CapsID.
   - It is larger/more defensible than Beauty/Toys in many Amazon-2014 protocols.
   - ReSID already has category-specific code-size settings.

2. **If compute/time allows**: add both `Beauty_and_Personal_Care` and `Sports_and_Outdoors`.
   - This gives one standard short-sequence category and one larger category.
   - It directly addresses the "single Amazon category" attack without adding a new tokenizer.

3. **If CARD becomes the actual Cluster A/B fallback**: prioritize Amazon 2014 `Beauty`.
   - CARD repo and many generative-rec baselines are naturally aligned with Amazon 2014 Beauty.
   - Do not claim this unless we complete schema audit and mapping export.

## Launch Gate Update

Do not treat the current Musical-only AutoDL quick run as paper evidence. It remains useful for:

- verifying remote Python/CUDA/dependency path;
- verifying ReSID export and D1-D5a summary on GPU;
- catching packaging bugs before larger categories.

Before `robust`, `sweep`, or paper-facing Gate 0:

- download and schema-audit at least `Sports_and_Outdoors` from `PIIR/ReSID-dataset`;
- normalize its `item_metadata` and `interactions`;
- add it to the AutoDL queue as a canonical vertical run;
- report Musical separately as `development/smoke`, not as the sole case study.

## Sources Checked

- Local: `docs/DATASET_SCHEMA_AUDIT.md`, `docs/AUDIT_SID_CIKM_EXECUTION_SPEC.md`, `refine-logs/EXPERIMENT_TRACKER.md`.
- Local repos: `_gate0_repos/ReSID`, `_gate0_repos/GRID`, `_gate0_repos/CARD`.
- Web: TIGER NeurIPS paper, GRID README, GenRec README, ReSID Hugging Face dataset tree, CapsID review summary, DIGER paper summary.
