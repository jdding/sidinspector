import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.autodl_audit_sid.run_d3_ranking_context import evaluate_prefix_retrieval, run_context


class D3RankingContextTest(unittest.TestCase):
    def test_prefix_retrieval_hits_target_sharing_history_prefix(self) -> None:
        sid = pd.DataFrame(
            {
                "dataset": ["toy"] * 4,
                "method": ["m"] * 4,
                "item_id": [1, 2, 3, 4],
                "sid": ["0-0", "0-1", "1-0", "1-1"],
                "sid_level_0": [0, 0, 1, 1],
                "sid_level_1": [0, 1, 0, 1],
            }
        )
        interactions = pd.DataFrame(
            {
                "user_id": [10, 10, 20, 20],
                "item_id": [1, 2, 3, 4],
                "split": ["train", "valid", "train", "valid"],
            }
        )

        out = evaluate_prefix_retrieval(
            sid,
            interactions,
            eval_splits={"valid"},
            top_k=10,
            max_users=10,
            max_history_items=10,
            max_targets_per_user=1,
            max_candidates_per_prefix=100,
            depths=[1, 2],
        )
        depth1 = out[out["prefix_depth"] == 1].iloc[0]
        depth2 = out[out["prefix_depth"] == 2].iloc[0]

        self.assertEqual(depth1["targets_evaluated"], 2)
        self.assertAlmostEqual(depth1["hit_rate_at_k"], 1.0)
        self.assertAlmostEqual(depth1["candidate_coverage_rate"], 1.0)
        self.assertAlmostEqual(depth2["hit_rate_at_k"], 0.0)

    def test_run_context_writes_csv_and_json_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
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
            metadata = pd.DataFrame({"dataset": ["toy"] * 3, "item_id": [1, 2, 3], "category": ["a", "a", "b"]})
            interactions = pd.DataFrame(
                {
                    "dataset": ["toy"] * 4,
                    "user_id": [10, 10, 11, 11],
                    "item_id": [1, 2, 1, 3],
                    "split": ["train", "valid", "train", "valid"],
                }
            )
            sid_path = root / "sid.csv"
            metadata_path = root / "metadata.csv"
            interactions_path = root / "interactions.csv"
            sid.to_csv(sid_path, index=False)
            metadata.to_csv(metadata_path, index=False)
            interactions.to_csv(interactions_path, index=False)

            summary, manifest = run_context(
                sid_paths=[sid_path],
                item_metadata_path=metadata_path,
                interactions_path=interactions_path,
                dataset_name="toy",
                methods=None,
                output_dir=root / "out",
                top_k=5,
                max_users=10,
                max_items=None,
                max_history_items=10,
                max_targets_per_user=1,
                max_candidates_per_prefix=100,
                depths=[1],
                eval_splits={"valid"},
                d3_top_k=1,
                d3_max_pair_events=100,
                d3_max_user_items=20,
            )

            self.assertFalse(summary.empty)
            self.assertIn("weighted_collab_prefix_recall", summary.columns)
            self.assertTrue((root / "out" / "d3_ranking_context_summary.csv").exists())
            self.assertTrue((root / "out" / "d3_ranking_context_summary.json").exists())
            self.assertEqual(manifest["methods"], ["m"])


if __name__ == "__main__":
    unittest.main()
