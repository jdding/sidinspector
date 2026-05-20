# rqvae_minimal_reference Implementation Notes

Status: local reference-adapter gate, not named-method reproduction.

## Purpose

`rqvae_minimal_reference` exists to test whether SIDInspector can ingest a third
independent SID-generation code path through the same mapping contract. It is
not a TIGER, GRID, ReSID, CARD, QuaSID, AdaSID, CapsID, or DIGER reproduction.
It must not be cited as a published tokenizer result.

## Algorithmic Scope

The implementation exports item-level SID codes using residual quantization:

1. load item embeddings and stable item ids;
2. optionally L2-normalize embedding rows;
3. fit a `MiniBatchKMeans` codebook at each level;
4. assign each item to the nearest codeword;
5. subtract the selected codeword to form the residual for the next level;
6. write `sid_assignments(item_id, method, dataset, sid_level_*)`;
7. run the shared SIDInspector D1-D5 validators and metrics.

The default smoke configuration uses widths `32,128,128`, seed `42`, and
`max_iter=20` for bounded local runs.

## What Is Deliberately Not Implemented

- no sequence generator training;
- no downstream Recall@K/NDCG training benchmark;
- no VAE decoder, reconstruction network, commitment loss, or EMA codebook
  update;
- no TIGER architectural choices beyond the broad residual-quantization idea;
- no GRID raw-text pipeline or official hyperparameter reproduction;
- no ReSID FAMAE/GAOQ training;
- no claim that the resulting codes match any published paper's artifact.

The label keeps `rqvae` only because the sprint decision used
`rqvae_minimal_reference` as the reference-adapter name. In paper prose, prefer
`RQ-VAE-min reference adapter` or `minimal residual-quantization reference
adapter` and keep the non-reproduction caveat attached.

## Gate Evidence

Local gates completed on 2026-05-20 without AutoDL/GPU:

- 512-item CPU smoke: passed, 512 items, 430 unique full SIDs, duplicate SID
  rate 0.1602.
- 2,000-item CPU gate: passed, 2,000 items, 1,634 unique full SIDs, duplicate
  SID rate 0.1830, D5 prefix counts `32;989;1634`.
- Full Musical CPU run: passed, 23,742 items, 17,247 unique full SIDs,
  duplicate SID rate 0.2736, D2 full-code aliasing rate 0.4401, D3-L1 0.0650,
  D4 tail unique-SID ratio 0.8831, and D5 prefix counts `32;2368;17247`.

The full output lives under:

`methods/rqvae_minimal_reference/outputs/cpu_full_23742_seed42/`

## Paper Admission Rule

This row can enter the paper only as reference-adapter evidence:

> A minimal residual-quantization reference adapter demonstrates that the same
> mapping contract accepts an independent SID-generation code path.

It cannot be used to claim third named-method coverage or faithful reproduction.
If a full-data run later collapses, treat it as a diagnostic observation only
after checking that the exporter, inputs, and metric pipeline are correct.
