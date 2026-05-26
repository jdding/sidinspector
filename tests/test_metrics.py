import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sidinspector.metrics import alignment, head_tail_capacity


class MetricsTest(unittest.TestCase):
    def test_alignment_uses_cooccurrence_reference(self) -> None:
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

        out = alignment(sid, metadata, interactions, top_k=1)
        depth1 = out[out["prefix_depth"] == 1].iloc[0]
        depth2 = out[out["prefix_depth"] == 2].iloc[0]

        self.assertEqual(depth1["collab_reference"], "cooccurrence")
        self.assertEqual(depth1["collab_items"], 3)
        self.assertAlmostEqual(depth1["mean_collab_prefix_recall"], 2 / 3)
        self.assertAlmostEqual(depth2["mean_collab_prefix_recall"], 0.0)
        self.assertIn("level0_category_purity_mean", out.columns)

    def test_head_tail_falls_back_when_no_train_split_exists(self) -> None:
        sid = pd.DataFrame(
            {
                "dataset": ["toy"] * 3,
                "method": ["m"] * 3,
                "item_id": [1, 2, 3],
                "sid": ["0", "1", "2"],
                "sid_level_0": [0, 1, 2],
            }
        )
        interactions = pd.DataFrame(
            {
                "dataset": ["toy"] * 6,
                "user_id": [1, 1, 2, 2, 3, 4],
                "item_id": [1, 2, 1, 3, 1, 2],
                "split": ["all"] * 6,
            }
        )

        out = head_tail_capacity(sid, interactions)

        self.assertGreater(out["items"].sum(), 0)
        self.assertIn("head", set(out["bucket"]))

    def test_alignment_allows_missing_category_metadata(self) -> None:
        sid = pd.DataFrame(
            {
                "dataset": ["toy"] * 2,
                "method": ["m"] * 2,
                "item_id": [1, 2],
                "sid": ["0", "0"],
                "sid_level_0": [0, 0],
            }
        )
        metadata = pd.DataFrame({"dataset": ["toy"] * 2, "item_id": [1, 2]})
        interactions = pd.DataFrame(
            {
                "dataset": ["toy"] * 2,
                "user_id": [1, 1],
                "item_id": [1, 2],
                "split": ["train", "train"],
            }
        )

        out = alignment(sid, metadata, interactions, top_k=1)

        self.assertAlmostEqual(out.iloc[0]["mean_collab_prefix_recall"], 1.0)
        self.assertTrue(pd.isna(out.iloc[0]["level0_category_purity_mean"]))


if __name__ == "__main__":
    unittest.main()
