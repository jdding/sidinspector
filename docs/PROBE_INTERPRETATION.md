# Probe Interpretation Guide

SIDInspector probes support artifact triage before downstream training. They
do not define universal pass/fail thresholds and do not predict Recall@K or
NDCG by themselves. Interpret a row against the tokenizer's intended budget,
item universe, and same-dataset controls.

| Probe | Inspect when | Artifact risk exposed | Next action |
| --- | --- | --- | --- |
| D1 utilization | code use is concentrated or levels contain dead/rare codes | nominal capacity is not becoming usable address space | inspect codebook width, collapse by level, and whether the observed item universe matches the export |
| D2 aliasing | many items share a full code or early prefix | items are not uniquely addressable, or prefixes remain broad | inspect collision groups and their popularity/co-occurrence composition; do not infer downstream harm without an exposure or intervention study |
| D3 neighborhood alignment | train-only co-occurrence neighbors rarely share early prefixes | prefix-constrained retrieval may expose weak collaborative neighborhoods | compare with same-dataset controls and run the optional fixed-reranker exposure probe before changing a tokenizer |
| D4 popularity allocation | head, mid, and tail uniqueness differ sharply | capacity is concentrated in one popularity region, often compressing the tail | inspect per-bucket collision groups and decide whether the allocation matches the deployment objective |
| D5 structural cost | realized depth, fan-out, or active prefixes are unexpectedly high | the mapping can create more trie expansion or decoding pressure | compare structural profiles under a fixed item universe; measure latency only with the actual generator and serving stack |

D6 is an optional paired-refresh churn report. D7 is an input hook for
generator traces. Neither is required for the mapping-first D1-D5 workflow.
