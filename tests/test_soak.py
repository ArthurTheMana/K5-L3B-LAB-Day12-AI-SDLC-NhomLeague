"""Kiểm tra bộ chạy Soak headless 10 Ngày (`chonoi.soak`, Contract v1.3)."""

import json
import os
import subprocess
import sys
import tempfile
import unittest


class SoakTest(unittest.TestCase):
    def test_soak_10_days_completes_and_is_deterministic(self):
        with tempfile.TemporaryDirectory() as d:
            out1 = os.path.join(d, "soak1.json")
            out2 = os.path.join(d, "soak2.json")
            for out in (out1, out2):
                p = subprocess.run(
                    [sys.executable, "-m", "chonoi.soak", "--seed", "7", "--days", "10", "--out", out],
                    capture_output=True, text=True,
                )
                self.assertEqual(p.returncode, 0, p.stderr)
            with open(out1, encoding="utf-8") as f1, open(out2, encoding="utf-8") as f2:
                d1, d2 = json.load(f1), json.load(f2)
            self.assertEqual(d1["days"], 10)
            self.assertEqual(d1["days_completed"], 10)
            self.assertEqual(d1["crashes"], 0)
            self.assertEqual(len(d1["results"]), 10)
            self.assertGreater(d1["duration_s"], 0)
            self.assertEqual([r["day"] for r in d1["results"]], list(range(1, 11)))
            self.assertEqual(d1["results"], d2["results"])


if __name__ == "__main__":
    unittest.main()
