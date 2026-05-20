# Variable Depth Cost Probe

Timestamp: 2026-05-19 19:01:39 CST

Status: **LOCAL_CONTROLLER_DONE; PAPER_OPTIONAL**.

Role: third method-inspired controller in
`docs/CONTROLLED_STRESSOR_SELECTION.md`. It probes D5a and D4 boundaries for
variable/long SID interfaces without claiming to reproduce CapsID, ACERec, or
any other named method.

## Command

```bash
python3 tools/autodl_audit_sid/run_variable_depth_cost_probe.py \
  --item-metadata _gate0_artifacts/resid_musical_normalized/item_metadata.parquet \
  --interactions _gate0_artifacts/resid_musical_normalized/interactions.parquet \
  --output-dir _gate0_artifacts/controllers/variable_depth_cost_probe_20260519_1901 \
  --dataset-name Musical_Instruments \
  --width 64 \
  --max-depth 4 \
  --policies head_short_tail_long,head_long_tail_short,uniform_depth3
```

Tracked public summary:

- `paper_assets/tables/table10_variable_depth_cost_probe.csv`;
- `paper_assets/tables/table10_variable_depth_cost_probe.md`.

Ignored local details:

- `_gate0_artifacts/controllers/variable_depth_cost_probe_20260519_1901/sid_assignments.parquet`;
- `_gate0_artifacts/controllers/variable_depth_cost_probe_20260519_1901/d2_collision.csv`;
- `_gate0_artifacts/controllers/variable_depth_cost_probe_20260519_1901/d4_head_tail.csv`;
- `_gate0_artifacts/controllers/variable_depth_cost_probe_20260519_1901/d5a_deployment_cost.csv`;
- `_gate0_artifacts/controllers/variable_depth_cost_probe_20260519_1901/variable_depth_cost_manifest.json`.

## Summary

| Policy | Unique SID | Duplicate SID rate | Full collision rate | Head / mid / tail unique ratio | Standard prefix counts | Effective prefix counts |
|---|---:|---:|---:|---|---|---|
| head-long / tail-short | 19,924 | 0.160812 | 0.321624 | 1.000000 / 1.000000 / 0.539517 | `64;4096;12010;19924` | `64;4096;7914;7914` |
| head-short / tail-long | 19,924 | 0.160812 | 0.321624 | 0.537478 / 1.000000 / 1.000000 | `64;4096;12010;19924` | `64;4096;7914;7914` |
| uniform depth-3 | 23,742 | 0.000000 | 0.000000 | 1.000000 / 1.000000 / 1.000000 | `6;371;23742;23742` | `6;371;23742;0` |

## Interpretation

The result is useful as artifact-repo evidence but should be optional for the
four-page paper.

- Variable depth can shift which popularity bucket pays the collision cost:
  `head_long_tail_short` preserves head and mid uniqueness but compresses tail;
  `head_short_tail_long` does the opposite.
- Standard prefix counts and effective prefix counts differ. This supports the
  D5a boundary: fixed-column artifact schemas can overstate or obscure the
  active path surface for variable-depth SIDs.
- The current setting has equal-sized head/mid/tail buckets, so mean effective
  depth is `3.0` for all policies. This makes the result clean but less
  visually surprising than the D2b and capacity-budget controllers.

Safe paper claim if used:

> Variable-depth controllers show that head-tail capacity and active prefix
> cost can change even when the maximum SID schema is fixed.

Recommended paper decision:

- Keep this in the artifact repository by default.
- Include in the PDF only if a compact D5a paragraph needs one extra boundary
  example.

Do not claim:

- CapsID or ACERec reproduction;
- real decoding latency;
- generator invalid-path behavior.
