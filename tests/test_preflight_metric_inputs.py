import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sidinspector.preflight import preflight_inputs


class PreflightMetricInputsTest(unittest.TestCase):
    def _write_inputs(self, root: Path) -> tuple[Path, Path, Path]:
        sid = pd.DataFrame(
            {
                "dataset": ["toy"] * 3,
                "method": ["m"] * 3,
                "item_id": [1, 2, 3],
                "sid": ["0-0", "0-1", "1-0"],
                "sid_level_0": [0, 0, 1],
                "sid_level_1": [0, 1, 0],
            }
        )
        metadata = pd.DataFrame(
            {
                "dataset": ["toy"] * 3,
                "item_id": [1, 2, 3],
                "category": ["a", "a", "b"],
            }
        )
        interactions = pd.DataFrame(
            {
                "dataset": ["toy"] * 4,
                "user_id": [10, 10, 11, 11],
                "item_id": [1, 2, 1, 3],
                "split": ["train"] * 4,
            }
        )
        sid_path = root / "sid_assignments.csv"
        metadata_path = root / "item_metadata.csv"
        interactions_path = root / "interactions.csv"
        sid.to_csv(sid_path, index=False)
        metadata.to_csv(metadata_path, index=False)
        interactions.to_csv(interactions_path, index=False)
        return sid_path, metadata_path, interactions_path

    def test_preflight_outputs_coverage_and_bounded_metric_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sid_path, metadata_path, interactions_path = self._write_inputs(Path(tmp))

            out = preflight_inputs(
                sid_path,
                metadata_path,
                interactions_path,
                run_metric_smoke=True,
                top_k=1,
                max_pair_events=100,
            )

        self.assertEqual(out["status"], "passed")
        self.assertEqual(out["coverage"][0]["sid_items"], 3)
        self.assertEqual(out["tables"]["sid_assignments"]["rows"], 3)
        summary = out["metric_smoke_summary"][0]
        self.assertEqual(summary["dataset"], "toy")
        self.assertEqual(summary["method"], "m")
        self.assertEqual(summary["unique_sid"], 3)
        self.assertAlmostEqual(summary["full_collision_rate"], 0.0)
        self.assertAlmostEqual(summary["d3_depth1_mean_collab_recall"], 2 / 3)

    def test_preflight_rejects_missing_required_columns_before_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sid_path, metadata_path, interactions_path = self._write_inputs(Path(tmp))
            broken = pd.read_csv(interactions_path).drop(columns=["user_id"])
            broken.to_csv(interactions_path, index=False)

            with self.assertRaisesRegex(ValueError, "interactions is missing required columns: user_id"):
                preflight_inputs(sid_path, metadata_path, interactions_path, run_metric_smoke=True)

    def test_metric_smoke_respects_item_bound(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sid_path, metadata_path, interactions_path = self._write_inputs(Path(tmp))

            with self.assertRaisesRegex(ValueError, "metric smoke is bounded"):
                preflight_inputs(
                    sid_path,
                    metadata_path,
                    interactions_path,
                    run_metric_smoke=True,
                    max_metric_items=2,
                )


if __name__ == "__main__":
    unittest.main()
