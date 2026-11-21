"""Soak headless nhiều Ngày (TICKET-04, Contract v1.3).

Chạy:
    python3 -m chonoi.soak --seed 7 --days 10 --out soak.json
"""

import argparse
import copy
import json
import math
import os
import sys
import time

from .contract import load_contract
from .ids import IdAllocator, id_key
from .inputs import InputState
from .rng import Streams
from .sim.day_contract import ContractDaySim


def _move_toward(pos, target):
    dx = target[0] - pos[0]
    dy = target[1] - pos[1]
    dist = math.hypot(dx, dy)
    if dist < 1e-6:
        return (0.0, 0.0)
    return (dx / dist, dy / dist)


def _bot_input(sim) -> InputState:
    phase = sim.phase
    active = sim.active
    edges = set()
    move = (0.0, 0.0)

    if phase == "gather":
        p = active.pos
        oxy_frac = active.oxygen_ticks / max(1, active.oxygen_max)
        if len(active.hold) >= active.t["hold_capacity"] or oxy_frac < 0.35 or active.time_left_ticks < 300:
            move = _move_toward(p, active.t["dock_pos"])
            if active._in_dock():
                edges.add("interact")
        elif active.fish:
            target = min(active.fish, key=lambda f: (math.dist(p, f["pos"]), id_key(f["id"])))
            move = _move_toward(p, target["pos"])
            if not active._at_surface() and math.dist(p, target["pos"]) <= active.t["catch_radius"]:
                edges.add("catch")
        else:
            ready_nodes = [n for n in active.nodes if n["regrow_ticks"] == 0]
            if ready_nodes:
                target = min(ready_nodes, key=lambda n: (math.dist(p, n["pos"]), id_key(n["id"])))
                move = _move_toward(p, target["pos"])
                if active._at_surface() and math.dist(p, target["pos"]) <= active.t["interact_radius"]:
                    edges.add("interact")
            else:
                move = _move_toward(p, active.t["dock_pos"])

    elif phase == "quan":
        p = active.pos
        ir = active.t["interact_radius"]
        target_pos = None
        if active.hand is not None:
            cust = next((c for c in active.customers if c["id"] == active.hand["order_id"]), None)
            if cust:
                tb = next((t for t in active.tables if t["id"] == cust["table_id"]), None)
                if tb:
                    target_pos = tb["pos"]
        else:
            ready_stove = next((s for s in active.stoves if s["state"] == "ready"), None)
            if ready_stove:
                target_pos = ready_stove["pos"]
            else:
                has_reserved = any(c.get("order_status") == "reserved" for c in active.customers)
                idle_stove = next((s for s in active.stoves if s["state"] == "idle"), None)
                if has_reserved and idle_stove:
                    target_pos = idle_stove["pos"]
        if target_pos is not None:
            move = _move_toward(p, target_pos)
            if math.dist(p, target_pos) <= ir:
                edges.add("interact")

    elif phase == "shop":
        edges.add("shop_done")

    return InputState(move, set(edges), edges)


def run_soak(seed: int, days: int, out_path: str) -> dict:
    t0 = time.perf_counter()
    tuning = copy.deepcopy(load_contract()["tuning"])
    base_plans = list(tuning["day_plan"])
    extended_plans = []
    for d in range(1, days + 1):
        src = copy.deepcopy(base_plans[(d - 1) % len(base_plans)])
        src["day"] = d
        extended_plans.append(src)
    tuning["day_plan"] = extended_plans

    sim = ContractDaySim(tuning, {}, Streams(seed), IdAllocator(), days=days)
    mult = tuning["score"]["reputation_multiplier"]
    results = []
    crashes = 0

    try:
        while not sim.done:
            day_before = sim.day
            inp = _bot_input(sim)
            events = sim.step(inp)
            for name, _ in events:
                if name == "shop_end":
                    results.append({
                        "day": day_before,
                        "earned": sim.earned,
                        "reputation": round(float(sim.reputation), 4),
                        "score": sim.earned + mult * math.floor(sim.reputation),
                    })
    except Exception as e:
        crashes += 1
        sys.stderr.write(f"soak crash: {e}\n")

    payload = {
        "days": days,
        "days_completed": sim.days_completed,
        "crashes": crashes,
        "results": results,
        "duration_s": round(time.perf_counter() - t0, 4),
    }
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return payload


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Chạy soak headless nhiều Ngày cho Quán Ăn Chợ Nổi.")
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--days", type=int, default=10)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.days < 1:
        sys.stderr.write("--days phải >= 1\n")
        return 2
    res = run_soak(a.seed, a.days, a.out)
    return 0 if res["crashes"] == 0 and res["days_completed"] == a.days else 1


if __name__ == "__main__":
    sys.exit(main())
