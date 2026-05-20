import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.autodl_audit_sid.run_variable_depth_cost_probe import run_probe


class VariableDepthCostProbeTest(unittest.TestCase):
    def _write_inputs(self, root: Path) -> tuple[Path, Path]:
        metadata = pd.DataFrame(
            {
                "dataset": ["toy"] * 8,
                "item_id": list(range(1, 9)),
                "category": ["a", "a", "b", "b", "c", "c", "d", "d"],
            }
        )
        interactions = pd.DataFrame(
            {
                "dataset": ["toy"] * 12,
                "user_id": [1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5],
                "item_id": [1, 2, 3, 1, 4, 2, 5, 3, 6, 1, 7, 8],
                "split": ["train"] * 12,
            }
        )
        metadata_path = root / "metadata.csv"
        interactions_path = root / "interactions.csv"
        metadata.to_csv(metadata_path, index=False)
        interactions.to_csv(interactions_path, index=False)
        return metadata_path, interactions_path

    def test_probe_writes_effective_depth_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            metadata_path, interactions_path = self._write_inputs(root)
            out_dir = root / "out"

            manifest = run_probe(
                item_metadata_path=metadata_path,
                interactions_path=interactions_path,
                output_dir=out_dir,
                dataset="toy",
                width=4,
                max_depth=4,
                policies=["head_short_tail_long", "uniform_depth3"],
            )
            summary = pd.read_csv(out_dir / "variable_depth_cost_summary.csv")

        self.assertEqual(manifest["status"], "passed")
        self.assertEqual(len(summary), 2)
        self.assertIn("mean_effective_depth", summary.columns)
        self.assertIn("effective_prefix_counts", summary.columns)
        self.assertTrue((summary["items"] == 8).all())


if __name__ == "__main__":
    unittest.main()
