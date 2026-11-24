"""Tests for SIDInspector v1.1 resource upgrade (pure-Python parity, CLI, browser & HTTP demos)."""

from __future__ import annotations

import json
import math
from pathlib import Path
import subprocess
import sys
import threading
import unittest
from urllib import request, error

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
if str(ROOT / "demo") not in sys.path:
    sys.path.insert(0, str(ROOT / "demo"))
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from sidinspector import churn as pd_churn
from sidinspector import metrics as pd_metrics
from sidinspector.pure_diagnostics import (
    compute_churn_pure,
    load_csv_bundle,
    parse_sid_csv_text,
)
import browser_example
import serve_demo


class PureDiagnosticsParityTests(unittest.TestCase):
    """Verify exact numerical parity between pure-Python D1-D6 and pandas/numpy metrics."""

    def test_d1_through_d5_parity_on_quickstart(self) -> None:
        qs = ROOT / "examples" / "reviewer_quickstart_data"
        pure = load_csv_bundle(
            qs / "sid_codes.csv",
            qs / "interactions.csv",
            qs / "item_metadata.csv",
        )

        raw_sid = pd.read_csv(qs / "sid_codes.csv")
        sid_df = pd.DataFrame(
            {
                "dataset": "mini_music",
                "method": "qs",
                "item_id": raw_sid["item_id"],
                "sid_level_0": raw_sid["sid_0"],
                "sid_level_1": raw_sid["sid_1"],
                "sid_level_2": raw_sid["sid_2"],
                "sid": raw_sid[["sid_0", "sid_1", "sid_2"]].astype(str).agg("-".join, axis=1),
            }
        )
        meta_df = pd.read_csv(qs / "item_metadata.csv")
        inter_df = pd.read_csv(qs / "interactions.csv")

        # D1 parity
        d1_pd = pd_metrics.utilization(sid_df).set_index("level")
        for row in pure["d1"]:
            ref = d1_pd.loc[row["level"]]
            self.assertEqual(row["unique_codes"], int(ref["unique_codes"]))
            self.assertAlmostEqual(row["entropy"], float(ref["entropy"]), places=10)
            self.assertAlmostEqual(row["gini"], float(ref["gini"]), places=10)

        # D2 parity
        d2_pd = pd_metrics.collision(sid_df, inter_df).set_index("prefix_depth")
        for row in pure["d2"]:
            ref = d2_pd.loc[row["prefix_depth"]]
            self.assertAlmostEqual(row["full_collision_rate"], float(ref["full_collision_rate"]), places=10)
            self.assertAlmostEqual(row["prefix_collision_rate"], float(ref["prefix_collision_rate"]), places=10)
            self.assertEqual(row["prefix_collision_groups"], int(ref["prefix_collision_groups"]))

        # D3 parity
        d3_pd = pd_metrics.alignment(sid_df, meta_df, inter_df).set_index("prefix_depth")
        for row in pure["d3"]:
            ref = d3_pd.loc[row["prefix_depth"]]
            self.assertAlmostEqual(
                row["weighted_collab_prefix_recall"], float(ref["weighted_collab_prefix_recall"]), places=10
            )
            self.assertAlmostEqual(
                row["mean_collab_prefix_recall"], float(ref["mean_collab_prefix_recall"]), places=10
            )
            self.assertAlmostEqual(
                row["level0_category_purity_mean"], float(ref["level0_category_purity_mean"]), places=10
            )

        # D4 parity
        d4_pd = pd_metrics.head_tail_capacity(sid_df, inter_df).set_index("bucket")
        for row in pure["d4"]:
            ref = d4_pd.loc[row["bucket"]]
            self.assertEqual(row["items"], int(ref["items"]))
            self.assertAlmostEqual(row["sid_unique_ratio"], float(ref["sid_unique_ratio"]), places=10)
            self.assertAlmostEqual(row["level0_entropy"], float(ref["level0_entropy"]), places=10)

        # D5 parity
        d5_pd = pd_metrics.deployment_cost(sid_df).iloc[0]
        self.assertEqual(pure["d5"]["unique_sid"], int(d5_pd["unique_sid"]))
        self.assertAlmostEqual(pure["d5"]["duplicate_sid_rate"], float(d5_pd["duplicate_sid_rate"]), places=10)
        self.assertEqual(pure["d5"]["prefix_counts"], str(d5_pd["prefix_counts"]).replace(";", "/"))

    def test_d6_churn_parity(self) -> None:
        old_csv = "item_id,sid_0,sid_1,sid_2\n1,1,1,1\n2,1,1,2\n3,2,1,1\n4,2,2,1\n"
        new_csv = "item_id,sid_0,sid_1,sid_2\n1,1,1,9\n2,1,1,2\n3,3,1,1\n4,2,2,1\n"
        pure_rows = compute_churn_pure(parse_sid_csv_text(old_csv)["rows"], parse_sid_csv_text(new_csv)["rows"])

        old_df = pd.DataFrame(
            {"item_id": [1, 2, 3, 4], "sid_level_0": [1, 1, 2, 2], "sid_level_1": [1, 1, 1, 2], "sid_level_2": [1, 2, 1, 1]}
        )
        new_df = pd.DataFrame(
            {"item_id": [1, 2, 3, 4], "sid_level_0": [1, 1, 3, 2], "sid_level_1": [1, 1, 1, 2], "sid_level_2": [9, 2, 1, 1]}
        )
        pd_rows = pd_churn.compute_churn(old_df, new_df).set_index("prefix_depth")
        for row in pure_rows:
            ref = pd_rows.loc[row["prefix_depth"]]
            self.assertEqual(row["changed_items"], int(ref["changed_items"]))
            self.assertAlmostEqual(row["churn_rate_common"], float(ref["churn_rate_common"]), places=10)


class BrowserAndCliTests(unittest.TestCase):
    def test_browser_example_runs_and_verifies_tables(self) -> None:
        payload = browser_example.run_example()
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(len(payload["table2"]), 7)
        self.assertEqual(len(payload["table3"]), 3)
        self.assertEqual(payload["quickstart"]["d5"]["items"], 12)
        self.assertEqual(payload["quickstart"]["d5"]["unique_sid"], 11)

    def test_custom_csv_audit_and_rejection(self) -> None:
        ok = browser_example.audit_custom_csv("item_id,sid_0,sid_1\n1,0,1\n2,0,1\n3,1,2\n")
        self.assertEqual(ok["report"]["d5"]["items"], 3)
        self.assertTrue(math.isclose(ok["report"]["d2"][0]["full_collision_rate"], 2 / 3))

        with self.assertRaises(ValueError):
            browser_example.audit_custom_csv("item_id,sid_0\n1,0\n1,1\n")  # duplicate item_id

    def test_cli_audit_subcommand(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "sidinspector.cli",
                "audit",
                "--sid-csv",
                str(ROOT / "examples/reviewer_quickstart_data/sid_codes.csv"),
                "--interactions-csv",
                str(ROOT / "examples/reviewer_quickstart_data/interactions.csv"),
                "--metadata-csv",
                str(ROOT / "examples/reviewer_quickstart_data/item_metadata.csv"),
                "--json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(proc.stdout)
        self.assertEqual(data["d5"]["items"], 12)
        self.assertEqual(data["d5"]["unique_sid"], 11)

    def test_local_http_demo_endpoints_and_guards(self) -> None:
        server = serve_demo.ThreadingHTTPServer(("127.0.0.1", 0), serve_demo.Handler)
        server.bind_host = "127.0.0.1"
        server.workflow_lock = threading.Lock()
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            with request.urlopen(f"{base}/health", timeout=5) as resp:
                health = json.loads(resp.read().decode("utf-8"))
                self.assertEqual(health["status"], "ready")
                self.assertEqual(health["version"], "1.1.0")

            with request.urlopen(f"{base}/", timeout=5) as resp:
                html = resp.read().decode("utf-8")
                self.assertIn("SIDInspector", html)
                self.assertIn("nonce-", resp.headers.get("Content-Security-Policy", ""))

            req = request.Request(
                f"{base}/api/audit",
                data=json.dumps({"sid_csv": "item_id,sid_0,sid_1\n1,2,3\n2,2,3\n"}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with request.urlopen(req, timeout=5) as resp:
                audit_resp = json.loads(resp.read().decode("utf-8"))
                self.assertEqual(audit_resp["report"]["d5"]["items"], 2)
                self.assertAlmostEqual(audit_resp["report"]["d2"][0]["full_collision_rate"], 1.0)

            bad_origin = request.Request(
                f"{base}/api/run",
                data=b"{}",
                headers={"Content-Type": "application/json", "Origin": "https://evil.example"},
                method="POST",
            )
            with self.assertRaises(error.HTTPError) as ctx:
                request.urlopen(bad_origin, timeout=5)
            self.assertEqual(ctx.exception.code, 403)
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
