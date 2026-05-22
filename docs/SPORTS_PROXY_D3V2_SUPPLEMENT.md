# SIDInspector Sports Proxy/Control D3v2 Supplement

Timestamp: 2026-05-20 17:40:00 CST

## Verdict

The Sports_and_Outdoors proxy/control D3v2 supplement completed on the port-21551
AutoDL instance and was pulled back locally. It is useful as artifact
supplement evidence for directional portability of the D3 gap, but it must not
enter the main named-method evidence table.

Reason: the rows are explicitly proxy rows:

- ReSID row is `resid_unbalanced_proxy_seed42`, not faithful balanced GAOQ.
- CARD row is `card_feature_proxy_seed42`, not faithful CARD/NU-RQ-VAE.

## Artifact

- Remote root:
  `/root/autodl-tmp/Sec_phrase/_gate0_artifacts/vertical_replication/sports_proxy_d3v2_20260520/`
- Local root:
  `_gate0_artifacts/vertical_replication/sports_proxy_d3v2_20260520/`
- ReSID proxy summary:
  `_gate0_artifacts/vertical_replication/sports_proxy_d3v2_20260520/resid_unbalanced_proxy/vertical_d3_summary.csv`
- CARD proxy summary:
  `_gate0_artifacts/vertical_replication/sports_proxy_d3v2_20260520/card_feature_proxy/vertical_d3_summary.csv`

The run used `--d3-max-pair-events 300000 --d3-max-user-items 100` on 151,411
Sports items and 2,924,461 interactions.

## Key Metrics

| Row | Unique SIDs | Duplicate SID rate | Full-code aliasing | D3 L1 weighted | D3 L1 mean | D4 tail |
|---|---:|---:|---:|---:|---:|---:|
| ReSID unbalanced proxy | 151,411 | 0.0000 | 0.0000 | 0.1075 | 0.1185 | 1.0000 |
| CARD feature proxy | 18,298 | 0.8792 | 0.9637 | 0.0514 | 0.0565 | 0.2531 |
| category-prefix control | 151,411 | 0.0000 | 0.0000 | 0.4827 | 0.4839 | 1.0000 |
| popularity-balanced control | 115,424 | 0.2377 | 0.4349 | 0.4811 | 0.4488 | 0.7995 |
| mod-collision hash | 256 | 0.9983 | 1.0000 | 0.0039 | 0.0040 | 0.0050 |

The category control uses real hierarchy columns:
`category_l1`, `category_l2`, `category_l3`; `coarse_category_levels=false`.

## Interpretation

- Directionally, Sports matches the Musical/All_Beauty pattern: category-derived
  and popularity-balanced controls recover substantially more co-occurrence
  prefix neighbors than the learned/proxy rows.
- The result strengthens the diagnostic portability story, not named-method
  coverage. It should be described as a proxy/control supplement.
- The ReSID proxy has perfect full-code uniqueness but much lower D3 than the
  category-prefix and popularity controls, again separating collision-free
  capacity from neighborhood alignment.
- The CARD feature proxy shows high aliasing and low D3, making it useful only
  as a stressor/proxy row.

## Safe Wording

> A Sports proxy/control supplement shows the same directional D3 gap under
> bounded co-occurrence probing, but because both learned rows are proxy exports,
> we keep it in the artifact supplement rather than the main evidence table.

Unsafe wording:

- Sports validates ReSID or CARD as faithful named-method evidence.
- The supplement is a SID leaderboard.
- D3 is downstream Recall/NDCG validation.

