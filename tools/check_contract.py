"""Đối chiếu game.contract.json với số chuẩn của đề (Test Contract v1.1–v1.3).

    python3 tools/check_contract.py            # in từng mục ĐẠT/LỖI, mã 1 nếu có lỗi

Kiểm: khóa gốc và lệnh, team_size khớp TEAM.md, số chuẩn gather/quan/freshness/shop,
6 món và công thức, day_plan.ingredients = tổng công thức × số suất, dải hợp lệ của PRD-0 mục A.
Chỉ dùng thư viện chuẩn. Đổi số chuẩn thì phải sửa script này CÙNG LÚC và ghi lý do vào CHANGELOG.
"""

import json
import math
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

INGREDIENTS = {"ca_loc", "ca_linh", "ca_keo", "bong_dien_dien", "bong_sung", "keo_neo"}
MENU = {
    "ca_loc_nuong_trui": ({"ca_loc": 1}, 6, 60),
    "goi_bong_sung": ({"bong_sung": 2}, 4, 40),
    "lau_ca_linh_dien_dien": ({"ca_linh": 3, "bong_dien_dien": 1}, 10, 120),
    "canh_chua_ca_loc": ({"ca_loc": 1, "bong_dien_dien": 1}, 8, 90),
    "ca_keo_nuong": ({"ca_keo": 2}, 6, 70),
    "lau_mam": ({"ca_linh": 2, "ca_keo": 1, "keo_neo": 1, "bong_dien_dien": 1}, 12, 200),
}
DAY_PLAN = [
    {"ca_loc_nuong_trui": 3, "goi_bong_sung": 3},
    {"ca_loc_nuong_trui": 2, "lau_ca_linh_dien_dien": 2},
    {"goi_bong_sung": 2, "canh_chua_ca_loc": 2, "ca_keo_nuong": 2},
    {"lau_mam": 1, "ca_loc_nuong_trui": 2, "goi_bong_sung": 1},
    {"lau_mam": 1, "lau_ca_linh_dien_dien": 1, "ca_loc_nuong_trui": 1},
]
GATHER = {
    "duration_s": 180, "bounds": {"x": [0, 100], "d": [0, 30]}, "dock_pos": [2, 0], "dock_radius": 3,
    "start_pos": [2, 0], "start_heading_deg": 0, "swim_speed": 4.0, "surface_depth": 0.5,
    "oxygen_max_s": 30, "oxygen_refill_per_tick": 6, "choke_interval_ticks": 60, "hp_max": 3,
    "hold_capacity": 12, "interact_radius": 2.0, "node_yield": 1, "regrow_s": 20,
    "catch_radius": 2.0, "catch_cooldown_s": 0.5, "fish_yield": {"ca_linh": 3, "ca_loc": 1, "ca_keo": 2},
    "fish_initial": 8, "fish_speed": 1.5, "fish_max": 12, "fish_x": [4, 96],
    "fish_spawn_x": [15, 30, 45, 60, 75, 90],
}
QUAN = {
    "duration_s": 180, "bounds": {"x": [0, 16], "z": [0, 10]}, "start_pos": [8, 5], "walk_speed": 4.0,
    "interact_radius": 1.5, "first_customer_tick": 120, "customer_interval_s": 15, "patience_s": 60,
    "eat_s": 10, "burn_s": None, "carry_limit": 1, "tip_rate": 0.2, "tip_min_patience_ratio": 0.5,
    "tip_reputation": 0.2, "left_reputation_delta": -0.5, "reputation_initial": 3.0,
    "reputation_min": 0, "reputation_max": 5,
    "stoves": [{"id": "B1", "pos": [2, 8]}, {"id": "B2", "pos": [5, 8]}],
    "tables": [{"id": "T1", "pos": [9, 2]}, {"id": "T2", "pos": [13, 2]},
               {"id": "T3", "pos": [9, 6]}, {"id": "T4", "pos": [13, 6]}],
}
FRESHNESS = {"initial": 100, "gather_decay_per_s": 0.5, "quan_decay_per_s": 0.25, "spoiled_below": 30}
SHOP = {"max_ticks": 600, "upgrades": {
    "oxygen": [{"level": 1, "price": 200, "oxygen_max_s": 45}, {"level": 2, "price": 400, "oxygen_max_s": 60}],
    "hp": [{"level": 1, "price": 250, "hp_max": 4}, {"level": 2, "price": 500, "hp_max": 5}]}}
NODES = {"N1": ("bong_dien_dien", [12, 0]), "N2": ("bong_dien_dien", [28, 0]), "N3": ("bong_sung", [44, 0]),
         "N4": ("bong_sung", [60, 0]), "N5": ("keo_neo", [76, 0]), "N6": ("keo_neo", [90, 0])}


class Checker:
    def __init__(self):
        self.errors, self.warnings, self.passed = [], [], 0

    def warn(self, label, cond, detail=""):
        if not cond:
            self.warnings.append(f"{label}{': ' + detail if detail else ''}")

    def eq(self, label, got, want):
        if got == want or (isinstance(got, (int, float)) and isinstance(want, (int, float))
                           and not isinstance(got, bool) and math.isclose(got, want)):
            self.passed += 1
        else:
            self.errors.append(f"{label}: đang là {json.dumps(got, ensure_ascii=False)}, chuẩn là {json.dumps(want, ensure_ascii=False)}")

    def ok(self, label, cond, detail=""):
        if cond:
            self.passed += 1
        else:
            self.errors.append(f"{label}{': ' + detail if detail else ''}")


def _team_size():
    try:
        from check_team import parse_team
        with open(os.path.join(ROOT, "TEAM.md"), encoding="utf-8") as f:
            return len(parse_team(f.read()))
    except Exception:
        return None


def check(c, ck):
    ck.eq("contract_version", c.get("contract_version"), "1.3")
    for k in ("team", "team_size", "headless_cmd", "run_cmd", "build_cmd", "bench_cmd", "soak_cmd"):
        ck.ok(f"thiếu khóa gốc {k}", k in c)
    n = _team_size()
    ck.ok("team_size khớp số người trong TEAM.md", n is None or c.get("team_size") == n,
          f"team_size={c.get('team_size')}, TEAM.md có {n} người")
    size = c.get("team_size", 0)
    ext = c.get("extensions") or []
    need = {5: 1, 6: 2}.get(size, 0)
    ck.warn("extensions đủ số mục mở rộng cho nhóm", len(ext) >= need,
          f"nhóm {size} người cần ≥ {need} mục, đang khai {ext}")

    t = c.get("tuning", {})
    ck.eq("tuning.tick_hz", t.get("tick_hz"), 60)
    ck.eq("tuning.score.reputation_multiplier", t.get("score", {}).get("reputation_multiplier"), 100)
    for k, v in FRESHNESS.items():
        ck.eq(f"freshness.{k}", t.get("freshness", {}).get(k), v)

    g = t.get("gather", {})
    for k, v in GATHER.items():
        got = len(g.get(k, [])) if k == "fish_initial" and isinstance(g.get(k), list) else g.get(k)
        ck.eq(f"gather.{k}", got, v)
    nodes = {n["id"]: (n["kind"], n["pos"]) for n in g.get("nodes", [])}
    ck.eq("gather.nodes (N1–N6)", nodes, NODES)
    mon = g.get("monsters", {})
    spawns = {s["id"]: s for s in mon.get("spawns", [])}
    ck.ok("gather.monsters có M1 (Ngày 1) và M2 (từ Ngày 3)",
          spawns.get("M1", {}).get("from_day") == 1 and spawns.get("M2", {}).get("from_day") == 3,
          json.dumps(list(spawns), ensure_ascii=False))
    ck.eq("gather.monsters.invuln_ticks", mon.get("invuln_ticks"), 90)
    ck.eq("gather.monsters.loss_ratio", mon.get("loss_ratio"), 0.5)
    sau = mon.get("species", {}).get("ca_sau", {})
    for k, v in {"patrol_speed": 1.0, "chase_speed": 3.0, "detect_radius": 10, "exit_radius": 16,
                 "hit_radius": 1.5, "recoil_ticks": 60}.items():
        ck.eq(f"monsters.species.ca_sau.{k}", sau.get(k), v)

    q = t.get("quan", {})
    for k, v in QUAN.items():
        ck.eq(f"quan.{k}", q.get(k), v)

    m = t.get("menu", {})
    ck.eq("menu: đúng 6 id món", sorted(m), sorted(MENU))
    for dish, (recipe, cook, price) in MENU.items():
        d = m.get(dish, {})
        ck.eq(f"menu.{dish}.recipe", d.get("recipe"), recipe)
        ck.eq(f"menu.{dish}.cook_s", d.get("cook_s"), cook)
        ck.eq(f"menu.{dish}.price", d.get("price"), price)
        ck.ok(f"menu.{dish} chỉ dùng nguyên liệu hợp lệ", set(d.get("recipe", {})) <= INGREDIENTS)

    plan = t.get("day_plan", [])
    ck.eq("day_plan có 5 Ngày", len(plan), 5)
    for i, want in enumerate(DAY_PLAN):
        if i >= len(plan):
            break
        p = plan[i]
        ck.eq(f"day_plan[{i}].day", p.get("day"), i + 1)
        ck.eq(f"day_plan[{i}].dishes", p.get("dishes"), want)
        total = {}
        for dish, n_ in want.items():
            for kind, q_ in MENU[dish][0].items():
                total[kind] = total.get(kind, 0) + q_ * n_
        ck.eq(f"day_plan[{i}].ingredients = tổng công thức", p.get("ingredients"), total)

    s = t.get("shop", {})
    ck.eq("shop.max_ticks", s.get("max_ticks"), SHOP["max_ticks"])
    for kind in ("oxygen", "hp"):
        ck.eq(f"shop.upgrades.{kind}", s.get("upgrades", {}).get(kind), SHOP["upgrades"][kind])

    # Dải hợp lệ PRD-0 mục A (bắt lỗi khi ai đó chỉnh tay)
    ck.ok("ramp_max_ticks trong 0–6", 0 <= g.get("ramp_max_ticks", -1) <= 6 and 0 <= q.get("ramp_max_ticks", -1) <= 6)
    ck.ok("first_customer_tick trước khi đóng ca", 0 < q.get("first_customer_tick", 0) < q.get("duration_s", 0) * 60)


def main():
    with open(os.path.join(ROOT, "game.contract.json"), encoding="utf-8") as f:
        c = json.load(f)
    ck = Checker()
    check(c, ck)
    for e in ck.errors:
        print(f"[LỖI] {e}")
    for w in ck.warnings:
        print(f"[CẢNH BÁO] {w}")
    print(f"{ck.passed} mục đạt, {len(ck.errors)} lỗi, {len(ck.warnings)} cảnh báo")
    return 1 if ck.errors else 0


if __name__ == "__main__":
    sys.exit(main())
