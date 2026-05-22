# R3 Simulated Review Absorption Plan

Timestamp: 2026-05-20 17:03:00 CST

Target: CIKM 2026 Resource Track paper
`SIDInspector: A Mapping-First Diagnostic Resource for Semantic-ID Tokenizers`.

## Verdict

R3's 5/10 review is credible. The score is lower than prior simulated reviews
because it applies a stricter Resource Track standard to evidence breadth and
methodological isolation. We should treat it as an action list, not as an
outlier to dismiss.

The top three risks are:

1. thin named-method coverage;
2. architecturally biased GRID-vs-ReSID worked example;
3. D3 external grounding / interpretation risk.

## Action Matrix

| R3 item | Severity | Decision | Owner status | Closure target |
|---|---|---|---|---|
| W1 named-method coverage thin | high | accept as structural weakness; do not add proxy named methods | open/future | improve wording now; only add true method if official artifact appears |
| W2 worked example capacity mismatch | high | addressed with matched-capacity GRID ablation | completed AutoDL GPU | keep caveat; ask next review whether severity drops from high |
| W3 D3 lacks downstream validation | medium-high | soften D3 as triage/warning signal; optional downstream correlation is future unless cheap | writing patch done; experiment future | no unsupported "gate" wording |
| W4 synthetic-only probes | medium | state mechanism probes calibrate separability, not real-world utility | writing patch done | keep probes outside named-method evidence |
| W5 single-dataset core | medium | keep Musical as core; mention DACT/MovieLens as portability only | partially closed | no generality overclaim |
| W6 adapter spec prose-only | low-medium | add compact schema specification in §2 | writing patch done | compile check |
| W7 D6/D7 overexposed | low | D6 as optional extension with numeric repository smoke; D7 as hook only | writing patch done | compile check |
| W8 Figure 1 small panels | low | hold unless next review repeats; current PDF page budget tight | deferred | optional figure redesign |

## Writing Fixes Already Applied

- Added a compact adapter schema in §2:
  `item_id, method, dataset, sid_0...sid_L -> D1...D5`, with interactions,
  paired mappings, and generator traces activating D3/D4, D6, and D7.
- Replaced "pre-training gate" wording with "pre-training triage step" and
  explicitly says diagnostics are not replacement objectives for Recall@K/NDCG.
- Elevated the category-prefix D3 inversion as a finding: the non-learned
  category-prefix row has higher D3-L1 than ReSID and GRID, which supports D3
  as a warning signal rather than a standalone quality score.
- Added the existing DACT D6 smoke number in §4: 23.6% common-item code churn.

## Experiment Gate: Matched-Capacity GRID

Purpose: address R3 W2 directly.

Question:

> If GRID is given ReSID-like prefix capacity, does the high aliasing pressure
> remain, or does it largely disappear?

Completed run:

- dataset: ReSID processed `Musical_Instruments`;
- input: existing processed feature-text embeddings;
- method: official GRID MiniBatchKMeans exporter;
- widths: `32,1280,1280`;
- seed: 42;
- output root:
  `_gate0_artifacts/grid_same_dataset_runs/matched_capacity_grid_32_1280_1280_seed42_20260520/`;
- result:
  - unique full SIDs: 9,874;
  - D2 full-code aliasing: 0.7785;
  - D3 L1 co-occurrence prefix recall: 0.0796;
  - D4 tail unique-SID ratio: 0.6391;
  - D5 prefixes: `32/9300/9874`.

Interpretation: the ablation directly weakens the old capacity-confound attack.
Capacity expansion materially reduces GRID aliasing, but it does not eliminate
it. This row must remain a prefix-capacity ablation of the same feature-text
path, not a ReSID-matched reproduction and not a method-ranking claim.

## Non-Goals

- Do not self-implement QuaSID/AdaSID/CapsID/DIGER as named evidence.
- Do not claim D3 is validated against Recall/NDCG without an actual downstream
  correlation run.
- Do not turn mechanism probes into method coverage.

## Next Review Preparation

Before the next simulated review:

1. compile and verify the current writing patches;
2. keep `docs/MATCHED_CAPACITY_GRID_GATE.md` as the current W2 status;
3. keep Table 2's `GRID ft-cap` row and dagger/caveat wording conservative;
4. rerun strict claim audit focused on W1/W2/W3 wording;
5. run an external R3-delta review to test whether W2 is now partially or
   mostly resolved and whether W1/W3 remain score ceilings.
