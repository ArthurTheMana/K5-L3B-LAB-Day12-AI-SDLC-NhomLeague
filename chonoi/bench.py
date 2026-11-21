"""Benchmark có render cảnh lặn 1280x720 (TICKET-04, Contract v1.3).

Chạy:
    python3 -m chonoi.bench --seed 42 --duration 30 --out bench.json
"""

import argparse
import json
import math
import os
import sys
import time

from .contract import load_contract
from .ids import IdAllocator
from .inputs import InputState
from .rng import Streams
from .sim.gather import GatherSim

WIDTH = 1280
HEIGHT = 720
TICK_DT = 1.0 / 60.0


def _rectangle(buffer: bytearray, width: int, height: int, x: int, y: int,
               w: int, h: int, color: bytes) -> None:
    """Rasterize one RGB rectangle into the actual offscreen pixel buffer."""
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(width, x + w), min(height, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    scanline = color * (x1 - x0)
    stride = width * 3
    for row in range(y0, y1):
        start = row * stride + x0 * 3
        buffer[start:start + len(scanline)] = scanline


def _render_frame(snap: dict, width: int = WIDTH, height: int = HEIGHT) -> bytearray:
    """Render real RGB pixels at 1280x720 in software (offscreen).

    This measures raster work rather than merely counting draw calls. It does
    NOT measure browser Canvas/GPU performance; that requires a browser run.
    """
    # Every pixel is written into a fresh 1280x720 RGB buffer.
    pixels = bytearray(bytes((14, 64, 94)) * (width * height))
    sx = width / 104.0
    sy = (height - 120) / 36.0
    _rectangle(pixels, width, height, 0, 0, width, 35, b"\x80\xce\xe8")
    for n in snap.get("nodes", []):
        _rectangle(pixels, width, height, int(n["pos"][0] * sx),
                   int(n["pos"][1] * sy) + 35, 12, 9, b"\x55\xd0\x78")
    for f in snap.get("fish", []):
        _rectangle(pixels, width, height, int(f["pos"][0] * sx),
                   int(f["pos"][1] * sy) + 35, 15, 8, b"\xff\xc8\x64")
    for m in snap.get("monsters", []):
        _rectangle(pixels, width, height, int(m["pos"][0] * sx),
                   int(m["pos"][1] * sy) + 35, 35, 17, b"\xd4\x43\x42")
    player = snap.get("player", {})
    pos = player.get("pos", (0, 0))
    _rectangle(pixels, width, height, int(pos[0] * sx), int(pos[1] * sy) + 35,
               12, 24, b"\xff\xf3\xd7")
    oxygen = player.get("oxygen_ticks", 0) / max(1, player.get("oxygen_max_ticks", 1))
    _rectangle(pixels, width, height, 16, height - 54, 210, 12, b"\x32\x40\x52")
    _rectangle(pixels, width, height, 16, height - 54,
               int(210 * max(0, min(1, oxygen))), 12, b"\x6c\xde\xff")
    hold_count = len(snap.get("hold", []))
    _rectangle(pixels, width, height, 16, height - 32,
               min(210, hold_count * 16), 10, b"\xff\xdb\x83")
    return pixels


def run_bench(seed: int, duration_s: float, out_path: str, warmup_s: float = 3.0) -> dict:
    t_boot = time.perf_counter()
    tuning = load_contract()["tuning"]
    sim = GatherSim(tuning, {}, Streams(seed), IdAllocator(), day=1)
    idle_inp = InputState((0.0, 0.0), set(), set())

    # Load time = startup to FIRST rendered frame (not end of warmup).
    _render_frame(sim.snapshot())
    load_ms = round((time.perf_counter() - t_boot) * 1000.0, 3)

    # Làm nóng
    acc = 0.0
    last = time.perf_counter()
    while time.perf_counter() - t_boot < warmup_s:
        now = time.perf_counter()
        acc += now - last
        last = now
        while acc >= TICK_DT:
            if sim.done:
                sim = GatherSim(tuning, {}, Streams(seed), IdAllocator(), day=1)
            sim.step(idle_inp)
            acc -= TICK_DT
        _render_frame(sim.snapshot())

    # Khung hình đầu tiên của cảnh đo
    t_measure_start = time.perf_counter()
    frame_times = []
    acc = 0.0
    last = t_measure_start
    deadline = t_measure_start + duration_s
    while True:
        f_start = time.perf_counter()
        if f_start >= deadline and frame_times:
            break
        acc += f_start - last
        last = f_start
        while acc >= TICK_DT:
            if sim.done:
                sim = GatherSim(tuning, {}, Streams(seed), IdAllocator(), day=1)
            sim.step(idle_inp)
            acc -= TICK_DT
        _render_frame(sim.snapshot())
        # Throttle CPU; do not manufacture an FPS number: timings use real wall time.
        time.sleep(0.004)
        f_end = time.perf_counter()
        frame_times.append(max(1e-6, f_end - f_start))

    measured_s = max(1e-6, time.perf_counter() - t_measure_start)
    frames = len(frame_times)
    avg_fps = frames / measured_s
    k = max(1, math.ceil(0.01 * frames))
    slowest = sorted(frame_times, reverse=True)[:k]
    p1_low_fps = 1.0 / (sum(slowest) / k)

    payload = {
        "avg_fps": round(avg_fps, 2),
        "p1_low_fps": round(p1_low_fps, 2),
        "frames": frames,
        "measured_s": round(measured_s, 4),
        "load_ms": load_ms,
    }
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return payload


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Benchmark cảnh lặn 1280x720.")
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--duration", type=float, default=30.0)
    ap.add_argument("--warmup", type=float, default=3.0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.duration <= 0 or a.warmup < 0:
        sys.stderr.write("--duration phải > 0 và --warmup >= 0\n")
        return 2
    run_bench(a.seed, a.duration, a.out, warmup_s=a.warmup)
    return 0


if __name__ == "__main__":
    sys.exit(main())
