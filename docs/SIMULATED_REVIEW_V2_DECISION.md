# Simulated Review v2 Decision

Timestamp: 2026-05-20 21:23:32 CST

## Verdict

The sixth-round simulated review is accepted as the current decision input. It
raises the paper from the earlier 5/10 risk zone to roughly 7/10 because the
draft now has a real diagnostic finding:

> Addressability is not behavioral prefix alignment.

The project should continue the 8/10 attempt, but the next work should remain
gated. The goal is not to add rows for their own sake; it is to close the
reviewer attacks that remain after the D3 inversion, matched-capacity GRID, and
Musical fixed-reranker evidence.

## Accepted Actions

1. **W2 wording fix: All_Beauty coarse category.**
   The All_Beauty D3 value of 0.968 is unusually high and must be interpreted
   explicitly. It is not evidence that category identifiers are universally
   better tokenizers. It is evidence that D3 can expose when a dataset's coarse
   taxonomy is strongly aligned with user co-occurrence. The cross-vertical
   difference between Musical and All_Beauty is itself a diagnostic signal.

2. **B6-Beauty replication.**
   Repeat the B6 fixed-reranker ranking-context protocol on All_Beauty if the
   local artifacts and splits make it feasible. The paper target is to reduce
   the small-n weakness in the Musical-only Spearman analysis. If the protocol
   is blocked or too proxy-like, freeze the gap rather than forcing the claim.

3. **Figure 1 upgrade.**
   The figure should become a finding preview, not only a pipeline diagram. The
   bottom panels should highlight D3 inversion, capacity ablation, ranking
   context, and portability/aliasing support.

4. **`rqvae_minimal_reference` gated adapter.**
   A third implementation path is worth doing only as a reference adapter, not
   as a named-method reproduction. The label is `rqvae_minimal_reference`.
   Required gates are:
   - implementation notes that state what is and is not reproduced;
   - local 512/2k smoke before any full run;
   - export validator pass;
   - D1-D5 metrics;
   - no TIGER/GRID/ReSID/CARD naming in the row.

## Rejected / Constrained Actions

- Do not claim that `rqvae_minimal_reference` solves the "only two published
  methods" weakness. It can show a third independent adapter/code path, but it
  is still not a third published tokenizer artifact.
- Do not write RQ-VAE collapse as a useful finding unless implementation
  sanity checks rule out an engineering bug.
- Do not start AutoDL GPU work until local smoke and GPU-worthiness evidence
  pass. If GPU is needed, ask the user before launch.

## Ownership Split

- Main agent: paper wording, plan/tracker/manifest updates, Figure 1
  integration, claim boundaries.
- B6-Beauty worker: All_Beauty ranking-context feasibility and bounded run.
- RQ-VAE worker: `rqvae_minimal_reference` gated local implementation/smoke.

## Paper Impact

If W2 wording, B6-Beauty, Figure 1, and `rqvae_minimal_reference` all pass their
gates, the paper can credibly move from the current 7.0 region toward a 7.5--8.0
attempt. If B6-Beauty or RQ-VAE fails, the paper should keep the current
resource-interface framing and avoid compensating with weak coverage claims.
