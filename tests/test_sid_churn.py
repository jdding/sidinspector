import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sidinspector.churn import compute_churn


class SidChurnTest(unittest.TestCase):
    def test_compute_churn_reports_common_item_denominator_and_collisions(self) -> None:
        old = pd.DataFrame(
            {
                "item_id": [1, 2, 3],
                "sid_level_0": [0, 0, 1],
                "sid_level_1": [0, 1, 0],
            }
        )
        new = pd.DataFrame(
            {
                "item_id": [1, 2, 4],
                "sid_level_0": [0, 1, 1],
                "sid_level_1": [0, 1, 1],
            }
        )

        out = compute_churn(old, new)
        depth1 = out[out["prefix_depth"] == 1].iloc[0]
        depth2 = out[out["prefix_depth"] == 2].iloc[0]

        self.assertEqual(depth1["old_items"], 3)
        self.assertEqual(depth1["new_items"], 3)
        self.assertEqual(depth1["common_items"], 2)
        self.assertEqual(depth1["old_only_items"], 1)
        self.assertEqual(depth1["new_only_items"], 1)
        self.assertEqual(depth1["changed_items"], 1)
        self.assertAlmostEqual(depth1["churn_rate_common"], 0.5)
        self.assertEqual(depth1["old_prefix_collision_items"], 2)
        self.assertEqual(depth2["new_prefix_collision_items"], 2)

    def test_compute_churn_uses_dataset_item_key_when_dataset_exists(self) -> None:
        old = pd.DataFrame(
            {
                "dataset": ["a", "b"],
                "item_id": [1, 1],
                "sid_level_0": [0, 0],
            }
        )
        new = pd.DataFrame(
            {
                "dataset": ["a", "b"],
                "item_id": [1, 1],
                "sid_level_0": [1, 0],
            }
        )

        out = compute_churn(old, new).sort_values("dataset").reset_index(drop=True)

        self.assertEqual(list(out["dataset"]), ["a", "b"])
        self.assertEqual(list(out["changed_items"]), [1, 0])

    def test_compute_churn_rejects_mismatched_dataset_columns(self) -> None:
        old = pd.DataFrame({"dataset": ["a"], "item_id": [1], "sid_level_0": [0]})
        new = pd.DataFrame({"item_id": [1], "sid_level_0": [0]})

        with self.assertRaisesRegex(ValueError, "both contain dataset"):
            compute_churn(old, new)


if __name__ == "__main__":
    unittest.main()
