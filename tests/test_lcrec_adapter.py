import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from sidinspector.adapters.lcrec import main as lcrec_main


class LCRecAdapterTest(unittest.TestCase):
    def test_cli_normalizes_lcrec_json_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            index_path = root / "Instruments.index.json"
            item_path = root / "Instruments.item.json"
            inter_path = root / "Instruments.inter.json"
            out_dir = root / "out"
            index_path.write_text(json.dumps({"0": ["<a_1>", "<b_2>"], "1": ["<a_3>", "<b_4>"]}))
            item_path.write_text(json.dumps({"0": {"title": "A"}, "1": {"title": "B", "category": "strings"}}))
            inter_path.write_text(json.dumps({"10": [0, 1]}))

            import sys

            old_argv = sys.argv
            try:
                sys.argv = [
                    "lcrec",
                    "--index-json",
                    str(index_path),
                    "--item-json",
                    str(item_path),
                    "--inter-json",
                    str(inter_path),
                    "--dataset-name",
                    "LCRec_Instruments",
                    "--output-dir",
                    str(out_dir),
                ]
                lcrec_main()
            finally:
                sys.argv = old_argv

            sid = pd.read_parquet(out_dir / "sid_assignments.parquet")
            meta = pd.read_parquet(out_dir / "item_metadata.parquet")
            inter = pd.read_parquet(out_dir / "interactions.parquet")

        self.assertEqual(sid.loc[0, "method"], "lcrec_official_index")
        self.assertEqual(list(sid["sid"]), ["1-2", "3-4"])
        self.assertEqual(meta.loc[0, "category"], "unknown")
        self.assertEqual(list(inter["item_id"]), [0, 1])


if __name__ == "__main__":
    unittest.main()
