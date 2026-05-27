import json
import tempfile
import unittest
from pathlib import Path

from sidinspector.adapters.letter import (
    normalize_letter_index,
    normalize_letter_interactions,
    normalize_letter_metadata,
)


class LetterAdapterTest(unittest.TestCase):
    def test_normalizes_letter_index_tokens(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "index.json"
            path.write_text(json.dumps({"0": ["<a_1>", "<b_2>"], "1": ["<a_1>", "<b_3>"]}))
            out = normalize_letter_index(path, method="letter", dataset="toy")

        self.assertEqual(list(out["item_id"]), [0, 1])
        self.assertEqual(list(out["sid_level_0"]), [1, 1])
        self.assertEqual(list(out["sid_level_1"]), [2, 3])
        self.assertEqual(list(out["sid"]), ["1-2", "1-3"])

    def test_normalizes_optional_metadata_and_interactions(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            item_path = tmp_path / "item.json"
            inter_path = tmp_path / "inter.json"
            item_path.write_text(json.dumps({"0": {"title": "A", "brand": "B", "categories": ["x", "y"]}}))
            inter_path.write_text(json.dumps({"2": [0, 1]}))
            metadata = normalize_letter_metadata(item_path, dataset="toy")
            interactions = normalize_letter_interactions(inter_path, dataset="toy")

        self.assertEqual(metadata.loc[0, "category"], "x > y")
        self.assertEqual(len(interactions), 2)
        self.assertEqual(list(interactions["position"]), [0, 1])


if __name__ == "__main__":
    unittest.main()
