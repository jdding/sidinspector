import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.autodl_audit_sid.preflight_card_nurqvae import (
    audit_official_source_state,
    check_generate_code_contract,
    create_import_overlay,
    preflight_card_nurqvae,
)


CARD_DIR = ROOT / "_gate0_repos/CARD"


@unittest.skipUnless(CARD_DIR.exists(), "local CARD clone is not available")
class CardNuRQVAEPreflightTest(unittest.TestCase):
    def test_generate_code_contract_is_present(self) -> None:
        out = check_generate_code_contract(CARD_DIR)

        self.assertEqual(out["status"], "passed")
        self.assertTrue(out["checks"]["imports_official_nurqvae"])
        self.assertTrue(out["checks"]["exports_codes_npy"])
        self.assertTrue(out["checks"]["exports_sibling_item_ids"])
        self.assertTrue(out["checks"]["preserves_itemid_when_present"])

    def test_import_overlay_uses_official_nurqvae_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            package_dir = create_import_overlay(CARD_DIR, Path(tmp))

            copied = package_dir / "models/nu_rqvae.py"
            official = CARD_DIR / "nu-rq-vae/models/nu_rqvae.py"
            self.assertTrue(copied.exists())
            self.assertEqual(copied.read_text(encoding="utf-8"), official.read_text(encoding="utf-8"))

    def test_full_preflight_static_and_import_smoke(self) -> None:
        out = preflight_card_nurqvae(CARD_DIR, run_export=False)

        self.assertEqual(out["status"], "passed")
        self.assertEqual(out["import_smoke"]["tiny_forward"]["indices_shape"], [7, 2])
        self.assertIn("official_source_audit", out)
        self.assertFalse(out["next_step_ready"])

    def test_official_source_audit_detects_local_repairs(self) -> None:
        out = audit_official_source_state(CARD_DIR)

        self.assertIn(out["status"], {"local_repair_required", "official_source_complete", "no_git_metadata"})
        if out["status"] == "local_repair_required":
            self.assertIn("rqvae4/models/vq.py", out["missing_from_official_tree"])
            self.assertFalse(out["faithful_named_evidence_ready"])


if __name__ == "__main__":
    unittest.main()
