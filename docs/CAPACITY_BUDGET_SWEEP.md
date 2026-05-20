# Capacity Budget Sweep

Timestamp: 2026-05-19 19:01:39 CST

Status: **LOCAL_CONTROLLER_DONE**.

Role: second method-inspired controller in
`docs/CONTROLLED_STRESSOR_SELECTION.md`. It probes whether D1/D2/D4/D5a react
coherently when the same item universe is compressed under controlled
fixed-depth codebook budgets. It is inspired by adaptive-capacity and
capacity-pressure concerns, but it is not an implementation of AdaSID, CARD,
or any other named tokenizer.

## Command

```bash
python3 tools/autodl_audit_sid/run_capacity_budget_sweep.py \
  --item-metadata _gate0_artifacts/resid_musical_normalized/item_metadata.parquet \
  --interactions _gate0_artifacts/resid_musical_normalized/interactions.parquet \
  --output-dir _gate0_artifacts/controllers/capacity_budget_sweep_20260519_1901 \
  --dataset-name Musical_Instruments \
  --widths 8,12,16,24,32,48 \
  --depth 3 \
  --policies rank_mod,head_reserved
```

Tracked public summary:

- `paper_assets/tables/table9_capacity_budget_sweep.csv`;
- `paper_assets/tables/table9_capacity_budget_sweep.md`.

Ignored local details:

- `_gate0_artifacts/controllers/capacity_budget_sweep_20260519_1901/sid_assignments.parquet`;
- `_gate0_artifacts/controllers/capacity_budget_sweep_20260519_1901/d1_utilization.csv`;
- `_gate0_artifacts/controllers/capacity_budget_sweep_20260519_1901/d2_collision.csv`;
- `_gate0_artifacts/controllers/capacity_budget_sweep_20260519_1901/d4_head_tail.csv`;
- `_gate0_artifacts/controllers/capacity_budget_sweep_20260519_1901/d5a_deployment_cost.csv`;
- `_gate0_artifacts/controllers/capacity_budget_sweep_20260519_1901/capacity_budget_manifest.json`.

## Key Results

| Policy | Width | Capacity | Duplicate SID rate | Full collision rate | Head / mid / tail unique ratio | Prefix counts |
|---|---:|---:|---:|---:|---|---|
| `rank_mod` | 8 | 512 | 0.978435 | 1.000000 | 0.064827 / 0.064827 / 0.064435 | `8;64;512` |
| `rank_mod` | 24 | 13,824 | 0.417741 | 0.835481 | 0.860091 / 0.865409 / 0.853511 | `24;576;13824` |
| `rank_mod` | 32 | 32,768 | 0.000000 | 0.000000 | 1.000000 / 1.000000 / 1.000000 | `24;742;23742` |
| `head_reserved` | 8 | 512 | 0.978435 | 0.978772 | 0.064827 / 0.001013 / 0.001007 | `8;64;512` |
| `head_reserved` | 24 | 13,824 | 0.417741 | 0.418752 | 1.000000 / 0.724994 / 0.028190 | `24;576;13824` |
| `head_reserved` | 32 | 32,768 | 0.000000 | 0.000000 | 1.000000 / 1.000000 / 1.000000 | `24;742;23742` |

## Interpretation

The sweep gives a clean D1/D2/D4/D5a stressor.

- Capacity below the item count creates predictable collision pressure:
  width `8` and `16` produce high duplicate SID rates under both policies.
- Allocation policy matters even at the same nominal capacity. At width `24`,
  `rank_mod` distributes unique capacity relatively evenly across
  head/mid/tail buckets, while `head_reserved` preserves head items but leaves
  tail unique ratio at only `0.028190`.
- D5a prefix counts expose a separate cost surface. Width `32` and `48` both
  remove full collisions, but their prefix counts differ (`24;742;23742` vs
  `11;495;23742`) because realized prefix usage is shaped by the assignment
  policy and item universe, not just nominal capacity.

Safe paper claim:

> A capacity controller shows that D1/D2/D4/D5a separate nominal capacity,
> collision pressure, head-tail allocation, and prefix-cost structure.

Do not claim:

- AdaSID or CARD reproduction;
- adaptive capacity performance;
- downstream recommendation gains.

## Next Step

Proceed to `variable_depth_cost_probe`, the third method-inspired controller.
It should be run locally, but included in the four-page paper only if it gives
a clean D5a boundary result.
