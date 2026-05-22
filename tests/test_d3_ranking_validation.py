import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.autodl_audit_sid.run_d3_ranking_validation import (
    build_train_cooccurrence,
    evaluate_fixed_reranker,
    run_validation,
)


class D3RankingValidationTest(unittest.TestCase):
    def test_fixed_reranker_uses_cooccurrence_not_prefix_hit_order(self) -> None:
        sid = pd.DataFrame(
            {
                "dataset": ["toy"] * 5,
                "method": ["m"] * 5,
                "item_id": [1, 2, 3, 4, 5],
                "sid": ["0-0", "0-1", "0-2", "1-0", "1-1"],
                "sid_level_0": [0, 0, 0, 1, 1],
                "sid_level_1": [0, 1, 2, 0, 1],
            }
        )
        interactions = pd.DataFrame(
            {
                "user_id": [1, 1, 2, 2, 3, 4, 5, 10, 10],
                "item_id": [1, 3, 1, 3, 2, 2, 2, 1, 3],
                "split": ["train", "train", "train", "train", "train", "train", "train", "train", "valid"],
            }
        )

        out = evaluate_fixed_reranker(
            sid,
            interactions,
            eval_splits={"valid"},
            top_k=1,
            max_users=10,
            max_history_items=10,
            max_targets_per_user=1,
            max_candidates_per_prefix=100,
            max_cooccurrence_users=10,
            max_cooccurrence_user_items=10,
            depths=[1],
            rankers=["cooccurrence_popularity", "popularity"],
        )
        by_ranker = {row.ranker: row for row in out.itertuples(index=False)}

        self.assertAlmostEqual(by_ranker["cooccurrence_popularity"].candidate_recall, 1.0)
        self.assertAlmostEqual(by_ranker["cooccurrence_popularity"].recall_at_k, 1.0)
        self.assertAlmostEqual(by_ranker["popularity"].candidate_recall, 1.0)
        self.assertAlmostEqual(by_ranker["popularity"].recall_at_k, 0.0)

    def test_build_train_cooccurrence_is_train_only(self) -> None:
        interactions = pd.DataFrame(
            {
                "user_id": [1, 1, 2, 2],
                "item_id": [1, 2, 1, 3],
                "split": ["train", "train", "train", "valid"],
            }
        )
        cooc = build_train_cooccurrence(
            interactions,
            eligible_items={1, 2, 3},
            max_users=10,
            max_user_items=10,
        )
        self.assertEqual(cooc[1][2], 1)
        self.assertNotIn(3, cooc.get(1, {}))

    def test_validation_requires_split_by_default(self) -> None:
        sid = pd.DataFrame(
            {
                "dataset": ["toy"] * 2,
                "method": ["m"] * 2,
                "item_id": [1, 2],
                "sid": ["0-0", "0-1"],
                "sid_level_0": [0, 0],
                "sid_level_1": [0, 1],
            }
        )
        interactions = pd.DataFrame({"user_id": [1, 1], "item_id": [1, 2]})
        with self.assertRaisesRegex(ValueError, "requires a train split|missing required columns"):
            evaluate_fixed_reranker(
                sid,
                interactions,
                eval_splits={"valid"},
                top_k=1,
                max_users=10,
                max_history_items=10,
                max_targets_per_user=1,
                max_candidates_per_prefix=100,
                max_cooccurrence_users=10,
                max_cooccurrence_user_items=10,
                depths=[1],
                rankers=["popularity"],
            )

    def test_no_candidate_target_counts_as_miss(self) -> None:
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
        interactions = pd.DataFrame(
            {
                "user_id": [10, 10, 11, 11],
                "item_id": [1, 2, 3, 2],
                "split": ["train", "valid", "train", "valid"],
            }
        )
        out = evaluate_fixed_reranker(
            sid,
            interactions,
            eval_splits={"valid"},
            top_k=10,
            max_users=10,
            max_history_items=10,
            max_targets_per_user=1,
            max_candidates_per_prefix=100,
            max_cooccurrence_users=10,
            max_cooccurrence_user_items=10,
            depths=[1],
            rankers=["popularity"],
        ).iloc[0]

        self.assertEqual(out["targets_seen"], 2)
        self.assertEqual(out["targets_evaluated"], 2)
        self.assertAlmostEqual(out["candidate_recall"], 0.5)
        self.assertAlmostEqual(out["recall_at_k"], 0.5)

    def test_no_history_target_counts_as_miss(self) -> None:
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
        interactions = pd.DataFrame(
            {
                "user_id": [10, 10, 12, 12],
                "item_id": [1, 2, 4, 2],
                "split": ["train", "valid", "train", "valid"],
            }
        )
        out = evaluate_fixed_reranker(
            sid,
            interactions,
            eval_splits={"valid"},
            top_k=10,
            max_users=10,
            max_history_items=10,
            max_targets_per_user=1,
            max_candidates_per_prefix=100,
            max_cooccurrence_users=10,
            max_cooccurrence_user_items=10,
            depths=[1],
            rankers=["popularity"],
        ).iloc[0]

        self.assertEqual(out["targets_seen"], 2)
        self.assertEqual(out["targets_evaluated"], 2)
        self.assertAlmostEqual(out["candidate_recall"], 0.5)
        self.assertAlmostEqual(out["recall_at_k"], 0.5)

    def test_run_validation_writes_summary_correlations_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
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
            metadata = pd.DataFrame({"dataset": ["toy"] * 4, "item_id": [1, 2, 3, 4], "category": ["a", "a", "b", "b"]})
            interactions = pd.DataFrame(
                {
                    "dataset": ["toy"] * 6,
                    "user_id": [1, 1, 2, 2, 10, 10],
                    "item_id": [1, 2, 3, 4, 1, 2],
                    "split": ["train", "train", "train", "train", "train", "valid"],
                }
            )
            sid_path = root / "sid.csv"
            metadata_path = root / "metadata.csv"
            interactions_path = root / "interactions.csv"
            sid.to_csv(sid_path, index=False)
            metadata.to_csv(metadata_path, index=False)
            interactions.to_csv(interactions_path, index=False)

            summary, correlations, manifest = run_validation(
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
                max_cooccurrence_users=10,
                max_cooccurrence_user_items=10,
                depths=[1],
                eval_splits={"valid"},
                rankers=["cooccurrence_popularity"],
                d3_top_k=1,
                d3_max_pair_events=100,
                d3_max_user_items=20,
            )

            self.assertFalse(summary.empty)
            self.assertIn("recall_at_k", summary.columns)
            self.assertIn("weighted_collab_prefix_recall", summary.columns)
            self.assertTrue(correlations.empty or "spearman_with_d3_weighted" in correlations.columns)
            self.assertTrue((root / "out" / "d3_ranking_validation_summary.csv").exists())
            self.assertTrue((root / "out" / "d3_ranking_validation_correlations.csv").exists())
            self.assertEqual(manifest["methods"], ["m"])


if __name__ == "__main__":
    unittest.main()
