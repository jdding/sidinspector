# Gate 0 Results

Timestamp: 2026-05-18 23:33:31 CST

## Verdict

Gate 0 is closed with a usable Sports-and-Outdoors diagnostic matrix.

This is a feasibility pass, not a paper-quality final experiment. The matrix now has:

- Cluster A proxy: `card_rqvae_feature_proxy` on `Sports_and_Outdoors`
- Cluster B proxy: `resid_gaoq_unbalanced_proxy` on `Sports_and_Outdoors`
- Sanity controls: category-prefix, mod-collision hash, popularity-balanced
- Metrics: coverage, D1 utilization, D2 collision, D3 category-alignment proxy, D4 head-tail, D5a trie/deployment proxy

The formal balanced ReSID/GAOQ Sports run remains too expensive for the sprint path and was stopped after the proxy matrix closed.

## Remote Provenance

- Host: `ssh -p 10197 root@connect.westc.seetacloud.com`
- Remote workspace: `/root/autodl-tmp/Sec_phrase`
- Summary: `_gate0_artifacts/autodl_runs/gate0_summary_current.csv`
- Latest code commit used during this round: `4352625`

## Summary Table

| Method | Coverage | Unique SID | Duplicate SID Rate | Full Collision Rate | Prefix Counts | Level-0 Category Purity |
|---|---:|---:|---:|---:|---|---:|
| `resid_gaoq_unbalanced_proxy` | 151411 / 151411 | 151411 | 0.0000 | 0.0000 | `128;16384;151411` | 0.7794 |
| `card_rqvae_feature_proxy` | 151411 / 151411 | 18298 | 0.8792 | 0.9637 | `128;4516;18298` | 0.4445 |
| `sanity_category_prefix` | 151411 / 151411 | 151411 | 0.0000 | 0.0000 | `200;279;713;151411` | 0.9191 |
| `sanity_mod_collision_hash` | 151411 / 151411 | 256 | 0.9983 | 1.0000 | `256;256;256;256` | 0.0581 |
| `sanity_popularity_balanced` | 151411 / 151411 | 115424 | 0.2377 | 0.4348 | `4;1024;115424;115424` | 0.0531 |

## Interpretation

The toolkit now distinguishes method behavior on the canonical Sports vertical:

- ReSID unbalanced proxy gives collision-free depth-3 SIDs and high category purity.
- CARD compact feature-proxy exposes severe collision/capacity pressure under the current compact feature setup.
- Sanity baselines bracket the metrics: category-prefix is semantically pure, mod-collision is intentionally collapsed, and popularity-balanced has moderate collisions.

## Caveats

- `resid_gaoq_unbalanced_proxy` is not the faithful balanced ReSID/GAOQ export. It is a sprint-safe proxy because balanced GAOQ remained CPU-heavy on Sports.
- `card_rqvae_feature_proxy` is a repaired/compact feature-proxy path, not a claim of full upstream CARD reproduction.
- These results are sufficient for Gate 0 artifact feasibility and diagnostic sensitivity, but not yet sufficient for final CIKM paper claims.

## Next

1. Use this matrix for the resource-paper case-study skeleton.
2. If time permits, rerun CARD compact with a less collision-heavy configuration or 20 epochs.
3. Keep balanced ReSID/GAOQ as optional follow-up only if it can be made materially faster.
