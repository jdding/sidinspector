import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from sidinspector.adapters.card import normalize_card_codes


class CardAdapterTest(unittest.TestCase):
    def test_normalizes_codes_with_explicit_item_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            codes_path = root / "card_codes.npy"
            ids_path = root / "card_item_ids.npy"
            np.save(codes_path, np.asarray([[1, 2, 3], [1, 2, 4]], dtype=np.int64))
            np.save(ids_path, np.asarray([101, 105], dtype=np.int64))

            out = normalize_card_codes(codes_path, method="card_nurqvae", dataset="toy", item_ids_path=ids_path)

        self.assertEqual(list(out["item_id"]), [101, 105])
        self.assertEqual(list(out["sid"]), ["1-2-3", "1-2-4"])

    def test_requires_item_ids_unless_dense_assumption_is_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            codes_path = Path(tmp) / "card_codes.npy"
            np.save(codes_path, np.asarray([[7, 8]], dtype=np.int64))

            with self.assertRaises(ValueError):
                normalize_card_codes(codes_path, method="card_nurqvae", dataset="toy")

            out = normalize_card_codes(
                codes_path,
                method="card_nurqvae",
                dataset="toy",
                unsafe_assume_dense_item_ids=True,
            )

        self.assertEqual(list(out["item_id"]), [1])
        self.assertEqual(out.loc[0, "sid"], "7-8")


if __name__ == "__main__":
    unittest.main()
