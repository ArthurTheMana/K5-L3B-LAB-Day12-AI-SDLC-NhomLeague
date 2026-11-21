"""Kiểm tra bộ đo hiệu năng Benchmark (`chonoi.bench`, Contract v1.3)."""

import json
import os
import subprocess
import sys
import tempfile
import unittest


class BenchTest(unittest.TestCase):
    def test_bench_outputs_required_fields_and_meets_targets(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "bench.json")
            p = subprocess.run(
                [sys.executable, "-m", "chonoi.bench", "--seed", "42", "--warmup", "0.05", "--duration", "0.2", "--out", out],
                capture_output=True, text=True,
            )
            self.assertEqual(p.returncode, 0, p.stderr)
            with open(out, encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(set(data.keys()), {"avg_fps", "p1_low_fps", "frames", "measured_s", "load_ms"})
            self.assertGreater(data["frames"], 0)
            self.assertGreater(data["measured_s"], 0)
            self.assertGreaterEqual(data["avg_fps"], 60)
            self.assertGreaterEqual(data["p1_low_fps"], 30)
            self.assertLessEqual(data["load_ms"], 10000)


if __name__ == "__main__":
    unittest.main()
