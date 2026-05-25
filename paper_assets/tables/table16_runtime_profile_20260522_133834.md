# D1-D5 Runtime Profile

Measured on the local Musical artifact bundle used by the paper-facing verifier. The table profiles five SID/profile rows plus sanity controls over the same 23,742-item universe; timings are wall-clock seconds on the local development machine.

| probe                     |   seconds |   sid_rows |   items_per_method |   methods |   interaction_rows |   output_rows | notes                                  |
|:--------------------------|----------:|-----------:|-------------------:|----------:|-------------------:|--------------:|:---------------------------------------|
| input_load                |    0.1767 |     166194 |              23742 |         7 |             433164 |             0 | mapping-level preflight                |
| validation                |    0.1921 |     166194 |              23742 |         7 |             433164 |             7 | mapping-level preflight                |
| D1_utilization            |    0.0244 |     166194 |              23742 |         7 |             433164 |            24 | mapping-level preflight                |
| D2_aliasing               |    1.4052 |     166194 |              23742 |         7 |             433164 |            24 | mapping-level preflight                |
| D3_neighborhood_alignment |    5.4671 |     166194 |              23742 |         7 |             433164 |            24 | dominant interaction-neighborhood step |
| D4_popularity_allocation  |    0.2042 |     166194 |              23742 |         7 |             433164 |            21 | mapping-level preflight                |
| D5_structural_cost        |    0.0402 |     166194 |              23742 |         7 |             433164 |             7 | mapping-level preflight                |

Environment:

```json
{
  "python": "3.9.6",
  "platform": "macOS-26.4.1-arm64-arm-64bit"
}
```
