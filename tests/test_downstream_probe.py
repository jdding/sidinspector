import tempfile
import unittest
from pathlib import Path

import pandas as pd

from sidinspector.downstream_probe import run_probe


class DownstreamProbeTest(unittest.TestCase):
    def test_runs_leave_last_probe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sid_path = root / "sid.parquet"
            interactions_path = root / "interactions.parquet"
            manifest_path = root / "manifest.csv"
            out_dir = root / "out"

            sid = pd.DataFrame(
                {
                    "item_id": [1, 2, 3, 4],
                    "method": ["toy"] * 4,
                    "dataset": ["toy"] * 4,
                    "sid_level_0": [0, 0, 0, 0],
                    "sid_level_1": [0, 1, 0, 1],
                    "sid": ["0-0", "0-1", "1-0", "1-1"],
                }
            )
            interactions = pd.DataFrame(
                {
                    "user_id": [10, 10, 10, 11, 11, 11],
                    "item_id": [1, 2, 3, 3, 4, 1],
                    "position": [0, 1, 2, 0, 1, 2],
                }
            )
            sid.to_parquet(sid_path, index=False)
            interactions.to_parquet(interactions_path, index=False)
            pd.DataFrame(
                [
                    {
                        "label": "toy",
                        "method": "toy",
                        "dataset": "toy",
                        "sid_assignments": str(sid_path),
                        "interactions": str(interactions_path),
                    }
                ]
            ).to_csv(manifest_path, index=False)

            metadata = run_probe(
                manifest=pd.read_csv(manifest_path),
                output_dir=out_dir,
                depths=[1],
                rec_ks=[2],
                rankers=["popularity"],
                d3_top_k=1,
                max_users=100,
                max_pair_events=100,
                max_user_items=20,
                eval_strategy="leave_last",
                bootstrap_samples=10,
                seed=7,
            )

            summary = pd.read_csv(out_dir / "downstream_probe_summary.csv")
            self.assertEqual(metadata["rows"], 1)
            self.assertEqual(len(summary), 1)
            self.assertEqual(summary.loc[0, "users_with_eval_targets"], 2)
            self.assertIn("recall_at_k_ci_low", summary.columns)


if __name__ == "__main__":
    unittest.main()
