import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from methods.rqvae_minimal_reference import METHOD_LABEL, RQReferenceConfig, export_rqvae_minimal_reference


class RQVaeMinimalReferenceTest(unittest.TestCase):
    def _write_inputs(self, root: Path) -> tuple[Path, Path, Path, Path]:
        rng = np.random.default_rng(7)
        embeddings = rng.normal(size=(24, 8)).astype(np.float32)
        item_ids = np.arange(100, 124, dtype=np.int64)
        metadata = pd.DataFrame(
            {
                "dataset": ["toy"] * 24,
                "item_id": item_ids,
                "category": [str(i % 4) for i in range(24)],
            }
        )
        interactions = pd.DataFrame(
            {
                "dataset": ["toy"] * 48,
                "user_id": np.repeat(np.arange(12), 4),
                "item_id": np.tile(item_ids[:12], 4),
                "split": ["train"] * 48,
            }
        )
        emb_path = root / "item_embeddings.npy"
        item_ids_path = root / "item_ids.npy"
        metadata_path = root / "item_metadata.parquet"
        interactions_path = root / "interactions.parquet"
        np.save(emb_path, embeddings)
        np.save(item_ids_path, item_ids)
        metadata.to_parquet(metadata_path, index=False)
        interactions.to_parquet(interactions_path, index=False)
        return emb_path, item_ids_path, metadata_path, interactions_path

    def test_exporter_writes_sid_mapping_and_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            emb_path, item_ids_path, metadata_path, interactions_path = self._write_inputs(root)
            result = export_rqvae_minimal_reference(
                embeddings_path=emb_path,
                item_ids_path=item_ids_path,
                item_metadata_path=metadata_path,
                interactions_path=interactions_path,
                output_dir=root / "out",
                config=RQReferenceConfig(dataset_name="toy", widths=(4, 4), max_items=12, max_iter=5),
            )

            self.assertTrue(result.gate_passed)
            sid = pd.read_parquet(result.sid_assignments)
            self.assertEqual(set(sid["method"]), {METHOD_LABEL})
            self.assertEqual(len(sid), 12)
            self.assertIn("sid_level_0", sid.columns)
            self.assertIn("sid_level_1", sid.columns)
            for name in (
                "coverage_report.csv",
                "d1_utilization.csv",
                "d2_collision.csv",
                "d3_alignment.csv",
                "d4_head_tail.csv",
                "d5a_deployment_cost.csv",
            ):
                self.assertTrue((result.metrics_dir / name).exists(), name)

    def test_exporter_rejects_wrong_item_id_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            emb_path, item_ids_path, metadata_path, interactions_path = self._write_inputs(root)
            np.save(item_ids_path, np.arange(3, dtype=np.int64))

            with self.assertRaisesRegex(ValueError, "item_ids length"):
                export_rqvae_minimal_reference(
                    embeddings_path=emb_path,
                    item_ids_path=item_ids_path,
                    item_metadata_path=metadata_path,
                    interactions_path=interactions_path,
                    output_dir=root / "out",
                    config=RQReferenceConfig(dataset_name="toy", widths=(4,), max_items=12, max_iter=5),
                )


if __name__ == "__main__":
    unittest.main()
