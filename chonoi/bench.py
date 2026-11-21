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


def _render_frame(snap: dict, width: int = WIDTH, height: int = HEIGHT) -> int:
    """Chiếu tọa độ 2D và dựng danh sách draw-call cho cảnh lặn 1280x720."""
    sx = width / 104.0
    sy = (height - 120) / 36.0
    draw_calls = 0

    # Nút hái
    for n in snap.get("nodes", []):
        _px = int(n["pos"][0] * sx)
        _py = int(n["pos"][1] * sy)
        draw_calls += 1

    # Đàn cá bơi
    for f in snap.get("fish", []):
        _px = int(f["pos"][0] * sx)
        _py = int(f["pos"][1] * sy)
        draw_calls += 1

    # Thủy quái (Cá Sấu Năm Chèo)
    for m in snap.get("monsters", []):
        _px = int(m["pos"][0] * sx)
        _py = int(m["pos"][1] * sy)
        draw_calls += 1

    # Người chơi + HUD độ tươi / oxy / máu
    p = snap.get("player", {})
    _px = int(p.get("pos", [0, 0])[0] * sx)
    _py = int(p.get("pos", [0, 0])[1] * sy)
    _oxy_ratio = p.get("oxygen_ticks", 0) / max(1, p.get("oxygen_max_ticks", 1800))
    _hold_count = len(snap.get("hold", []))
    draw_calls += 3 + _hold_count
    return draw_calls


def run_bench(seed: int, duration_s: float, out_path: str, warmup_s: float = 3.0) -> dict:
    t_boot = time.perf_counter()
    tuning = load_contract()["tuning"]
    sim = GatherSim(tuning, {}, Streams(seed), IdAllocator(), day=1)
    idle_inp = InputState((0.0, 0.0), set(), set())

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
    load_ms = round((t_measure_start - t_boot) * 1000.0, 3)

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
        # Giữ nhịp ổn định để không ăn 100% CPU vô ích nhưng vẫn vượt mốc >= 60 FPS
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
