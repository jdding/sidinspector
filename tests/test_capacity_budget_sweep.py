import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.autodl_audit_sid.run_capacity_budget_sweep import run_sweep


class CapacityBudgetSweepTest(unittest.TestCase):
    def _write_inputs(self, root: Path) -> tuple[Path, Path]:
        metadata = pd.DataFrame(
            {
                "dataset": ["toy"] * 6,
                "item_id": [1, 2, 3, 4, 5, 6],
                "category": ["a", "a", "b", "b", "c", "c"],
            }
        )
        interactions = pd.DataFrame(
            {
                "dataset": ["toy"] * 9,
                "user_id": [1, 1, 1, 2, 2, 3, 3, 4, 4],
                "item_id": [1, 2, 3, 1, 4, 2, 5, 3, 6],
                "split": ["train"] * 9,
            }
        )
        metadata_path = root / "metadata.csv"
        interactions_path = root / "interactions.csv"
        metadata.to_csv(metadata_path, index=False)
        interactions.to_csv(interactions_path, index=False)
        return metadata_path, interactions_path

    def test_sweep_writes_summary_and_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            metadata_path, interactions_path = self._write_inputs(root)
            out_dir = root / "out"

            manifest = run_sweep(
                item_metadata_path=metadata_path,
                interactions_path=interactions_path,
                output_dir=out_dir,
                dataset="toy",
                widths=[1, 2],
                depth=2,
                policies=["rank_mod", "head_reserved"],
            )
            summary = pd.read_csv(out_dir / "capacity_budget_summary.csv")

        self.assertEqual(manifest["status"], "passed")
        self.assertEqual(len(summary), 4)
        self.assertIn("duplicate_sid_rate", summary.columns)
        self.assertTrue((summary["items"] == 6).all())
        self.assertTrue((summary["nominal_capacity"] <= 4).all())


if __name__ == "__main__":
    unittest.main()
