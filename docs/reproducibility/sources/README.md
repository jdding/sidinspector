# Paper Table Source Summaries

These compact files are the direct inputs used by
`tools/build_paper_tables.py` to reconstruct the paper-facing Table 2 and
Table 3 CSV snapshots.

They contain metric summaries and run manifests preserved from the original
paper evidence workspace. Local filesystem paths in the two manifests were
replaced by the public GRID repository URL; metric values and run parameters
are unchanged. The files do not contain tokenizer checkpoints, feature
embeddings, user-level interaction histories, or training caches, and the
rebuild command does not retrain upstream tokenizers. This boundary is
intentional: the release makes every reported table cell obtainable and
auditable while keeping large or upstream-controlled artifacts outside the
toolkit repository.

Run from a clean checkout:

```bash
python3 tools/build_paper_tables.py --output-dir /tmp/sidinspector_paper_tables
python3 tools/verify_reproducibility_matrix.py
```

The GRID-style feature-text row uses seed 42 in the displayed paper table;
the source summary also retains seeds 43 and 44. `grid_ft_manifest.json`
records a three-level width-64 budget. `grid_cap_manifest.json` records the
capacity ablation budget of 32/1280/1280.

The `source_evidence` fields in the rebuilt outputs point to the exact files in
this directory. These are paper-evidence source summaries, not additional
official tokenizer implementations.
