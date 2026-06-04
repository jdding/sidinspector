# D7 Generator-Trace Diagnostics

This directory is the starting point for SIDInspector V1 experiments.

Initial gate:

1. Define the generator-trace input schema.
2. Implement SID-to-item reverse lookup over normalized SIDInspector mappings.
3. Measure invalid paths, stale/out-of-catalog paths, duplicate generated
   candidates, and next-token uncertainty from bounded generator traces.
4. Run a small Musical/Beauty smoke before expanding adapters or datasets.

Non-goals for the first gate:

- no tokenizer leaderboard;
- no broad adapter sweep;
- no serving-latency claim;
- no rewrite of D1-D5;
- no trained-generator quality claim before trace collection is stable.
