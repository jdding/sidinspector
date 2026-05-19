import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.autodl_audit_sid.run_qualified_collision_probe import run_probe


class QualifiedCollisionProbeTest(unittest.TestCase):
    def _write_inputs(self, root: Path) -> tuple[Path, Path, Path]:
        sid = pd.DataFrame(
            {
                "dataset": ["toy"] * 5,
                "method": ["toy_method"] * 5,
                "item_id": [1, 2, 3, 4, 5],
                "sid_level_0": [0, 0, 1, 1, 2],
                "sid_level_1": [0, 0, 0, 1, 0],
                "sid": ["0-0", "0-0", "1-0", "1-1", "2-0"],
            }
        )
        metadata = pd.DataFrame(
            {
                "dataset": ["toy"] * 5,
                "item_id": [1, 2, 3, 4, 5],
                "category": ["a", "a", "b", "b", "c"],
            }
        )
        interactions = pd.DataFrame(
            {
                "dataset": ["toy"] * 8,
                "user_id": [10, 10, 11, 11, 12, 12, 13, 13],
                "item_id": [1, 2, 1, 3, 2, 4, 3, 5],
                "split": ["train"] * 8,
            }
        )
        sid_path = root / "sid.csv"
        metadata_path = root / "metadata.csv"
        interactions_path = root / "interactions.csv"
        sid.to_csv(sid_path, index=False)
        metadata.to_csv(metadata_path, index=False)
        interactions.to_csv(interactions_path, index=False)
        return sid_path, metadata_path, interactions_path

    def test_probe_writes_summary_and_pair_details(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sid_path, metadata_path, interactions_path = self._write_inputs(root)
            out_dir = root / "out"

            manifest = run_probe(
                sid_paths=[sid_path],
                item_metadata_path=metadata_path,
                interactions_path=interactions_path,
                output_dir=out_dir,
                max_collision_pairs=10,
                max_pair_events=100,
                max_user_items=10,
                popularity_bins=2,
                seed=7,
            )

            summary = pd.read_csv(out_dir / "qualified_collision_summary.csv")
            pairs = pd.read_csv(out_dir / "qualified_collision_pairs.csv")

        self.assertEqual(manifest["status"], "passed")
        self.assertEqual(summary.loc[0, "method"], "toy_method")
        self.assertEqual(summary.loc[0, "collision_pairs_possible"], 1)
        self.assertEqual(summary.loc[0, "collision_pairs_sampled"], 1)
        self.assertGreaterEqual(summary.loc[0, "matched_pairs_sampled"], 0)
        self.assertIn("shares_user", pairs.columns)
        self.assertIn("matched_noncollision", set(pairs["pair_type"]))


if __name__ == "__main__":
    unittest.main()
