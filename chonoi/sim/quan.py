"""Buổi tối — Mở Quán (`quan`).

Luật chơi Phase 1 theo PRD-0 mục F:
- Khách đến theo lịch (first_customer_tick, customer_interval_s), chọn món nấu được, giữ chỗ nguyên liệu.
- Bếp & bưng món: `chonoi/sim/kitchen.py` (`step_stoves`, `interact_stove`).
- Phục vụ, thanh toán & đóng ca: `chonoi/sim/service.py` (`interact_table`, `step_service_and_closing`).
"""


import math

from ..errors import BadInput
from ..ids import id_key, sort_by_id
from .kitchen import interact_stove, step_stoves

from .ramp import ramp_velocity
from .service import handle_table_interact, update_service

TICK = 60.0


class QuanSim:
    mode = "quan"
    phase = "quan"

    def __init__(self, tuning, scenario, streams, ids, inventory=None):
        t = tuning["quan"]
        self.t = t
        self.menu = tuning["menu"]
        self.rng = streams
        self.ids = ids
        p = scenario.get("player", {})
        self.pos = [float(c) for c in p.get("pos", t["start_pos"])]
        self.vel = [float(c) for c in p.get("vel", [0.0, 0.0])]
        self._tgt = None
        self._ramp_left = 0
        # kho: --inventory HOẶC scenario.stock (cả hai -> cli đã báo mã 2)
        self.stock = dict(inventory if inventory is not None else scenario.get("stock", {}))

        self.hand = dict(scenario["hand"]) if scenario.get("hand") is not None else None
        self.time_left_ticks = scenario.get("time_left_ticks", int(round(t["duration_s"] * TICK)))
        self.phase_tick = 0
        self.random_customers = scenario.get("random_customers", True)
        self.reputation = float(scenario.get("reputation", t["reputation_initial"]))
        self.stoves = [
            dict(
                s,
                pos=[float(c) for c in s["pos"]],
                state=s.get("state", "idle"),
                dish=dict(s["dish"]) if s.get("dish") is not None else None,
                cook_ticks_left=s.get("cook_ticks_left", 0),
                ready_ticks=s.get("ready_ticks", 0),
            )
            for s in self._merge(t["stoves"], scenario.get("stoves", []))
        ]
        self.tables = [
            dict(tb, pos=[float(c) for c in tb["pos"]])
            for tb in self._merge(t["tables"], scenario.get("tables", []))
        ]
        pat_max = int(round(t["patience_s"] * TICK))
        self.customers = []
        for c in scenario.get("customers", []):
            cust = {
                "id": c["id"],
                "table_id": c["table_id"],
                "dish_id": c["dish_id"],
                "order_tick": c.get("order_tick", 0),
                "state": c.get("state", "waiting"),
                "patience_ticks_left": c.get("patience_ticks_left", pat_max),
                "eat_ticks_left": c.get("eat_ticks_left", 0),
                "order_status": c.get("order_status", "reserved"),
                "reserved": dict(c["reserved"]) if "reserved" in c else None,
                "base_price": c.get("base_price", 0),
                "tip": c.get("tip", 0),
            }
            self.customers.append(cust)
        # Thiếu reserved ở đơn reserved thì cấp theo công thức theo order_tick rồi id bàn
        missing_res = [c for c in self.customers if c["order_status"] == "reserved" and c["reserved"] is None]
        missing_res.sort(key=lambda c: (c["order_tick"], id_key(c["table_id"])))
        for c in missing_res:
            c["reserved"] = dict(self.menu[c["dish_id"]]["recipe"])
        for c in self.customers:
            if c["reserved"] is None:
                c["reserved"] = {}
            ids.reserve(c["id"])
        # Kiểm tra tổng giữ chỗ không vượt tồn kho
        total_res = {}
        for c in self.customers:
            for k, q in c["reserved"].items():
                total_res[k] = total_res.get(k, 0) + q
        for k, q in total_res.items():
            if q > self.stock.get(k, 0):
                raise BadInput(f"giữ chỗ vượt quá tồn kho cho {k}: {q} > {self.stock.get(k, 0)}")


        self.money = 0
        self.earned = 0
        self.shift_earned = 0
        self.done = False
        self.reason = None

    @staticmethod
    def _merge(defaults, updates):
        by_id = {d["id"]: dict(d) for d in defaults}
        for u in updates:
            if u["id"] not in by_id:
                raise BadInput(f"id bếp/bàn không tồn tại: {u['id']}")
            by_id[u["id"]].update(u)
        return sort_by_id(list(by_id.values()))

    def _clamp_rep(self, val: float) -> float:
        return min(float(self.t["reputation_max"]), max(float(self.t["reputation_min"]), val))

    def _release_customer_order(self, order_id: str):
        if self.hand is not None and self.hand["order_id"] == order_id:
            self.hand = None
        for s in self.stoves:
            if s["dish"] is not None and s["dish"]["order_id"] == order_id:
                s["state"] = "idle"
                s["dish"] = None
                s["cook_ticks_left"] = 0
                s["ready_ticks"] = 0

    def snapshot(self) -> dict:
        occupied = {c["table_id"]: c["id"] for c in self.customers}
        return {
            "player": {"pos": self.pos, "vel": self.vel},
            "stock": {k: self.stock[k] for k in sorted(self.stock) if self.stock[k] > 0},
            "hand": self.hand,
            "stoves": [{k: s.get(k) for k in ("id", "pos", "state", "dish", "cook_ticks_left", "ready_ticks")}
                       for s in sort_by_id(self.stoves)],
            "tables": [{"id": tb["id"], "pos": tb["pos"], "customer_id": occupied.get(tb["id"])}
                       for tb in sort_by_id(self.tables)],
            "customers": sort_by_id(self.customers),
        }

    def step(self, inp):
        events = []

        # 1. Tăng đồng hồ và giảm timer ca
        self.phase_tick += 1
        self.time_left_ticks = max(0, self.time_left_ticks - 1)
        shift_closing = self.time_left_ticks <= 0

        # 2. Bếp: đếm nấu / ready_ticks và chuyển cooking -> ready (Người A)
        step_stoves(self, events)

        # 3. Di chuyển rồi xét tối đa một interact (Người A: bếp | Người B: bàn)
        self._move(inp)
        if inp.pressed("interact"):
            self._handle_interact(events)

        # 4. Tiến trình ăn, kiên nhẫn, thanh toán (Người B) & đóng ca
        events.extend(update_service(self))
        if shift_closing:

            self.done = True
            self.reason = "time"
            events.append(("quan_end", {
                "reason": "time",
                "money": self.money,
                "earned": self.earned,
                "shift_earned": self.shift_earned,
                "reputation": self.reputation,
            }))
            return events

        # 5. Khách mới theo lịch
        if self.random_customers:
            first = int(self.t["first_customer_tick"])
            interval = int(round(self.t["customer_interval_s"] * TICK))
            if self.phase_tick >= first and (self.phase_tick - first) % interval == 0:
                occupied = {c["table_id"] for c in self.customers}
                free_tables = [tb for tb in sort_by_id(self.tables) if tb["id"] not in occupied]
                if free_tables:
                    avail = dict(self.stock)
                    for c in self.customers:
                        for k, q in c.get("reserved", {}).items():
                            avail[k] = avail.get(k, 0) - q
                    affordable = [
                        dish_id for dish_id in sorted(self.menu.keys())
                        if all(avail.get(k, 0) >= q for k, q in self.menu[dish_id]["recipe"].items())
                    ]
                    if not affordable:
                        events.append(("no_dish", {}))
                    else:
                        tb = free_tables[0]
                        dish_id = self.rng.get("customer_dish").choice(affordable)
                        cid = self.ids.new("C")
                        recipe = dict(self.menu[dish_id]["recipe"])
                        self.customers.append({
                            "id": cid,
                            "table_id": tb["id"],
                            "dish_id": dish_id,
                            "order_tick": self.phase_tick,
                            "state": "waiting",
                            "patience_ticks_left": int(round(self.t["patience_s"] * TICK)),
                            "eat_ticks_left": 0,
                            "order_status": "reserved",
                            "reserved": recipe,
                            "base_price": 0,
                            "tip": 0,
                        })
                        events.append(("customer_arrived", {
                            "order_id": cid,
                            "table_id": tb["id"],
                            "dish_id": dish_id,
                        }))

        return events

    def _handle_interact(self, events):
        ir = float(self.t["interact_radius"])
        cands = []
        for s in self.stoves:
            d = math.dist(self.pos, s["pos"])
            if d <= ir:
                cands.append((d, 0, id_key(s["id"]), "stove", s))
        for tb in self.tables:
            d = math.dist(self.pos, tb["pos"])
            if d <= ir:
                cands.append((d, 1, id_key(tb["id"]), "table", tb))
        if not cands:
            return
        cands.sort(key=lambda x: (x[0], x[1], x[2]))
        _, _, _, kind, obj = cands[0]

        if kind == "stove":
            interact_stove(self, obj, events)
        elif kind == "table":
            events.extend(handle_table_interact(self, obj))

    def _move(self, inp):
        speed = self.t["walk_speed"]
        mx, mz = inp.move
        self.vel = ramp_velocity(self, (mx * speed, mz * speed), int(self.t.get("ramp_max_ticks", 6)))
        b = self.t["bounds"]
        for i, axis in enumerate(("x", "z")):
            self.pos[i] += self.vel[i] / self.hz
            lo, hi = b[axis]
            if self.pos[i] <= lo:
                self.pos[i], self.vel[i] = lo, max(0.0, self.vel[i])
            elif self.pos[i] >= hi:
                self.pos[i], self.vel[i] = hi, min(0.0, self.vel[i])
