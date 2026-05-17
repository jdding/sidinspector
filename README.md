# Lifecycle OPE Preflight

This repository tracks the public-data preflight for lifecycle-adaptive off-policy evaluation (OPE) in sequential recommendation.

The current goal is to test whether public datasets can support a method paper around lifecycle-adaptive shrinkage/switching for sparse-support OPE before any production deployment or internal business-data study.

## Start Here

- `START_HERE_PUBLIC_OPE.md`
- `RESEARCH_BRIEF.md`
- `idea-stage/IDEA_REPORT.md`
- `refine-logs/METHOD_DIRECTION_RETHINK.md`
- `docs/PUBLIC_DATASETS.md`
- `refine-logs/EXPERIMENT_PLAN.md`
- `refine-logs/EXPERIMENT_TRACKER.md`

## Current Thesis

Lifecycle transitions can create structured support and positivity failures. The method thesis is that global DR/switch/clipping rules are miscalibrated under this structure, and lifecycle-adaptive shrinkage can improve worst-state reliability without sacrificing aggregate value accuracy.

## Stage Boundary

This repository currently covers public research only. No Huawei business data or internal logs should be committed here.
