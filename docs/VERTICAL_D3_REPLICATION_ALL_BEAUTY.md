# SIDInspector B4 Vertical D3 Replication: All_Beauty

Timestamp: 2026-05-20 17:02:00 CST

## Verdict

The B4 vertical replication run completed on the port-21551 AutoDL instance and
was pulled back locally. It supports a **portable diagnostic inversion signal**:
on an All_Beauty 20k GRID export, a deterministic category-prefix control again
scores far above the learned/exported GRID row on D3 neighborhood alignment.

Seed43/44 follow-up panels were completed on the same no-GPU AutoDL instance on
2026-05-20 and pulled back locally. Across seed42/43/44, the GRID row stays in a
narrow D3 range (`0.0811--0.0898`), while the category-prefix control remains
`0.9684`. This strengthens the conclusion that the All_Beauty direction is not a
single-seed artifact.

This is **not** strong semantic-category replication, because the available
All_Beauty metadata only exposes a coarse `category` field. The result should be
used as a stressor/portability signal unless richer hierarchy metadata is added.

## Artifact

- Local result root:
  `_gate0_artifacts/vertical_replication/all_beauty_20k_grid_sanity_20260520/`
- Follow-up seed roots:
  `_gate0_artifacts/vertical_replication/all_beauty_20k_grid_sanity_seed43_20260520/`,
  `_gate0_artifacts/vertical_replication/all_beauty_20k_grid_sanity_seed44_20260520/`
- Script:
  `tools/autodl_audit_sid/run_vertical_d3_replication.py`
- Remote root:
  `/root/autodl-tmp/Sec_phrase/_gate0_artifacts/vertical_replication/all_beauty_20k_grid_sanity_20260520/`
- AutoDL connection:
  `ssh -p 21551 root@connect.westc.seetacloud.com`

## Results

### Seed42 Panel

| Dataset | Method | Unique SIDs | Duplicate SID rate | Full-code aliasing | D3 L1 weighted | D3 L1 mean | D4 tail | Prefix counts |
|---|---|---:|---:|---:|---:|---:|---:|---|
| All_Beauty | GRID RQ-KMeans 20k seed42 | 16,718 | 0.1641 | 0.2556 | 0.0811 | 0.1172 | 0.9231 | 128 / 7,126 / 16,718 |
| All_Beauty | category-prefix sanity | 20,000 | 0.0000 | 0.0000 | 0.9684 | 0.9823 | 1.0000 | 2 / 2 / 2 / 20,000 |
| All_Beauty | mod-collision hash sanity | 256 | 0.9872 | 1.0000 | 0.0046 | 0.0044 | 0.0384 | 256 / 256 / 256 / 256 |
| All_Beauty | popularity-balanced sanity | 1,024 | 0.9488 | 1.0000 | 0.2500 | 0.2479 | 0.1530 | 4 / 1,024 / 1,024 / 1,024 |

### GRID 3-Seed Stability

| Seed | GRID unique SIDs | GRID duplicate SID rate | GRID full-code aliasing | GRID D3 L1 weighted | GRID D4 tail | Category-prefix D3 |
|---:|---:|---:|---:|---:|---:|---:|
| 42 | 16,718 | 0.1641 | 0.2556 | 0.0811 | 0.9231 | 0.9684 |
| 43 | 16,951 | 0.1524 | 0.2379 | 0.0872 | 0.9210 | 0.9684 |
| 44 | 16,503 | 0.1748 | 0.2661 | 0.0898 | 0.8955 | 0.9684 |
| Mean | 16,724 | 0.1638 | 0.2532 | 0.0861 | 0.9132 | 0.9684 |

## Interpretation

- The category-prefix row is again much higher than GRID on D3 neighborhood
  alignment. Across GRID seeds 42/43/44, the GRID D3 range is
  `0.0811--0.0898`, while category-prefix is `0.9684`.
- The popularity-balanced row also beats GRID on D3 but has severe aliasing,
  which reinforces the paper's claim that D1/D2/D3/D4 measure different
  artifact properties.
- The GRID row has much lower aliasing than the Musical feature-text row, but
  D3 remains low; this helps separate capacity/collision pressure from
  collaborative-prefix alignment.
- The category-prefix control used a coarse fallback:
  `coarse_category_levels=true`, `level0_unique=2`,
  `used_category_columns=["category"]`. Do not write this as evidence that a
  rich category hierarchy dominates learned SID tokenizers.

## Paper Use

Safe wording:

> In a second All_Beauty vertical with coarser metadata, the same adapter
> contract again separates capacity, aliasing, popularity allocation, and D3
> neighborhood alignment. Across three GRID seeds, the category-prefix control
> remains directionally far above the GRID rows on D3, but because the category
> metadata is coarse, this remains a diagnostic stressor rather than a
> learned-tokenizer baseline.

Unsafe wording:

- Category-prefix is a better SID tokenizer.
- Learned SID tokenizers generally underperform categories across Amazon.
- This validates D3 against downstream Recall/NDCG.
