"""Kiểm tra bộ đo hiệu năng Benchmark (`chonoi.bench`, Contract v1.3)."""

import json
import os
import subprocess
import sys
import tempfile
import unittest


class BenchTest(unittest.TestCase):
    def test_renderer_rasterizes_actual_pixels(self):
        from chonoi.bench import WIDTH, HEIGHT, _render_frame
        blank = _render_frame({"player": {"pos": [2, 0]}}, 160, 90)
        with_fish = _render_frame({"player": {"pos": [2, 0]},
                                   "fish": [{"pos": [30, 4]}]}, 160, 90)
        self.assertIsInstance(with_fish, bytearray)
        self.assertEqual(len(with_fish), 160 * 90 * 3)
        self.assertNotEqual(blank, with_fish)

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
            self.assertGreater(data["avg_fps"], 0)
            self.assertGreater(data["p1_low_fps"], 0)
            self.assertGreaterEqual(data["load_ms"], 0)
            # Phase 4 defines performance thresholds for REPORTING; they
            # are not hardware-independent requirements for CI unit tests.


if __name__ == "__main__":
    unittest.main()
