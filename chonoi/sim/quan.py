"""Buổi tối — Mở Quán. KHUNG: đi lại, chặn biên, đồng hồ, kho nạp từ file/scenario.

Nhóm viết tiếp (PRD-0 mục F, Quán):
  TODO(nhóm, lát 3): khách đến theo lịch, chọn món nấu được, giữ chỗ nguyên liệu, kiên nhẫn,
                     bỏ đi (customer_left), no_dish, vòng đời khách.
  TODO(nhóm, lát 4): interact tại bếp/bàn (cook_started, dish_ready, dish_picked, served),
                     ăn xong trả tiền (paid), boa, uy tín, hết ca (quan_end).
"""
from ..errors import BadInput
from ..ids import id_key, sort_by_id
from .ramp import ramp_velocity

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
        self.pos = list(p.get("pos", t["start_pos"]))
        self.vel = [float(c) for c in p.get("vel", [0.0, 0.0])]
        self._tgt = None
        self._ramp_left = 0
        # kho: --inventory HOẶC scenario.stock (cả hai -> cli đã báo mã 2)
        self.stock = dict(inventory if inventory is not None else scenario.get("stock", {}))
        self.hand = scenario.get("hand")
        self.tuning = tuning
        self.hz = tuning["tick_hz"]
        self.time_left_ticks = scenario.get("time_left_ticks", self._ticks(t["duration_s"]))
        self.reputation = scenario.get("reputation", t["reputation_initial"])
        self.stoves = [dict(s, state=s.get("state", "idle"), dish=s.get("dish"),
                            cook_ticks_left=s.get("cook_ticks_left", 0), ready_ticks=s.get("ready_ticks", 0))
                       for s in self._merge(t["stoves"], scenario.get("stoves", []))]
        self.tables = self._merge(t["tables"], scenario.get("tables", []))
        self.phase_tick = 0
        self.random_customers = scenario.get("random_customers", True)

        # Khởi tạo khách từ scenario (nếu có)
        self.customers = []
        for c in scenario.get("customers", []):
            dish_id = c.get("dish_id")
            if dish_id not in self.menu:
                raise BadInput(f"Món không có trong menu: {dish_id}")

            recipe = dict(self.menu[dish_id]["recipe"])
            cust = dict(c)
            cust.setdefault("state", "waiting")
            cust.setdefault("order_tick", 0)
            cust.setdefault("order_status", "reserved")
            cust.setdefault("patience_ticks_left", self._ticks(t["patience_s"]))
            cust.setdefault("eat_ticks_left", 0)  # Bộ đếm chưa kích hoạt mặc định 0 (Lỗi 4)
            cust.setdefault("reserved", recipe if cust["order_status"] == "reserved" else {})
            cust.setdefault("base_price", None)  # Chưa chốt giá khi mới gọi (Lỗi 5)
            cust.setdefault("tip", 0)
            self.customers.append(cust)
            ids.reserve(cust["id"])
        self._validate_reserved()
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
                from ..errors import BadInput
                raise BadInput(f"id bếp/bàn không tồn tại: {u['id']}")
            by_id[u["id"]].update(u)
        return sort_by_id(list(by_id.values()))

    def snapshot(self) -> dict:
        occupied = {c["table_id"]: c["id"] for c in self.customers}
        return {
            "player": {"pos": self.pos},
            "stock": {k: self.stock[k] for k in sorted(self.stock) if self.stock[k] > 0},
            "hand": self.hand,
            "stoves": [{k: s.get(k) for k in ("id", "pos", "state", "dish", "cook_ticks_left", "ready_ticks")}
                       for s in self.stoves],
            "tables": [{"id": tb["id"], "pos": tb["pos"], "customer_id": occupied.get(tb["id"])} for tb in self.tables],
            "customers": sort_by_id(self.customers),
        }

    def step(self, inp):
        events = []
        self.phase_tick += 1
        self.time_left_ticks = max(0, self.time_left_ticks - 1)

        # 1. Bước 1: Giảm kiên nhẫn của khách đang chờ (Lát 3)
        self._tick_patience()

        # 2. Bước 2: [Lát 4 sẽ cập nhật bếp nấu tại đây]

        # 3. Bước 3: Di chuyển và Người chơi tương tác (Lát 4)
        self._move(inp)

        # 4. Bước 4: Xét khách rời bàn (Lát 3 bỏ về / closing; Lát 4 ăn xong trả tiền)
        self._leave_customers(events)

        # 5. Bước 5: Sinh khách mới theo lịch (Lát 3)
        self._spawn_customer(events)

        # 6. Đóng ca nếu hết giờ
        if self.time_left_ticks <= 0:
            self.done = True
            self.reason = "time"
            events.append(("quan_end", {"reason": "time", "money": self.money, "earned": self.earned,
                                        "shift_earned": self.shift_earned, "reputation": self.reputation}))
        return events

    def _release(self, c: dict):
        """Nhả nguyên liệu giữ chỗ, dọn bếp và tay nếu đang giữ món của khách này."""
        c["reserved"] = {}
        for s in self.stoves:
            if (s.get("dish") or {}).get("order_id") == c["id"]:
                s.update(state="idle", dish=None, cook_ticks_left=0, ready_ticks=0)
        if self.hand and self.hand.get("order_id") == c["id"]:
            self.hand = None

    def _tick_patience(self):
        """Bước 1: Chỉ giảm timer kiên nhẫn của khách đang chờ."""
        for c in self.customers:
            if c["state"] == "waiting" and c["patience_ticks_left"] > 0:
                c["patience_ticks_left"] -= 1

    def _leave_customers(self, events: list):
        """Bước 4: Xét khách bỏ về sau bước interact, duyệt theo id bàn."""
        remaining = []
        sorted_custs = sorted(self.customers, key=lambda c: id_key(c["table_id"]))

        for c in sorted_custs:
            if c["state"] != "waiting":
                remaining.append(c)
                continue

            if self.time_left_ticks <= 0:
                self._release(c)
                events.append(("customer_left", {
                    "order_id": c["id"],
                    "table_id": c["table_id"],
                    "reason": "closing",
                    "reputation": self.reputation,
                }))
            elif c["patience_ticks_left"] == 0:
                self._release(c)
                self.reputation = max(
                    self.t["reputation_min"],
                    min(self.t["reputation_max"], self.reputation + self.t["left_reputation_delta"]),
                )
                events.append(("customer_left", {
                    "order_id": c["id"],
                    "table_id": c["table_id"],
                    "reason": "patience",
                    "reputation": self.reputation,
                }))
            else:
                remaining.append(c)

        self.customers = remaining

    def _validate_reserved(self):
        """Contract D: giữ chỗ khác công thức hoặc vượt tồn kho -> mã 2 (BadInput)."""
        for c in self.customers:
            recipe = self.menu[c["dish_id"]]["recipe"]
            if c["order_status"] == "reserved" and c["reserved"] != recipe:
                raise BadInput(f"customers.{c['id']}: reserved khác công thức món {c['dish_id']}")
            if c["order_status"] != "reserved" and c["reserved"]:
                raise BadInput(f"customers.{c['id']}: chỉ đơn reserved mới được giữ chỗ")
        over = {k: v for k, v in self._available_stock().items() if v < 0}
        if over:
            raise BadInput(f"tổng giữ chỗ vượt tồn kho: {over}")

    def _available_stock(self) -> dict:
        avail = dict(self.stock)
        for c in self.customers:
            for k, qty in c.get("reserved", {}).items():
                avail[k] = avail.get(k, 0) - qty
        return avail

    def _can_cook(self, dish_id: str, avail_stock: dict) -> bool:
        recipe = self.menu[dish_id]["recipe"]
        return all(avail_stock.get(k, 0) >= q for k, q in recipe.items())

    def _spawn_customer(self, events: list):
        """Bước 5: Xét khách mới theo lịch."""
        if not self.random_customers or self.time_left_ticks <= 0:
            return

        t = self.t
        first_tick = t["first_customer_tick"]
        interval = self._ticks(t["customer_interval_s"])

        is_turn = (self.phase_tick == first_tick) or (
            self.phase_tick > first_tick and (self.phase_tick - first_tick) % interval == 0
        )
        if not is_turn:
            return

        # 1. Tìm bàn trống có ID nhỏ nhất
        occupied_tables = {c["table_id"] for c in self.customers}
        free_tables = [tb for tb in sort_by_id(self.tables) if tb["id"] not in occupied_tables]
        if not free_tables:
            return

        target_table = free_tables[0]

        # 2. Lọc món đủ nguyên liệu khả dụng (sắp theo mã Unicode)
        avail = self._available_stock()
        candidate_dishes = [
            d for d in sorted(self.menu.keys())
            if self._can_cook(d, avail)
        ]

        if not candidate_dishes:
            events.append(("no_dish", {}))
            return

        # 3. Chọn món ngẫu nhiên bằng RNG stream 'customers'
        chosen_dish = self.rng.get("customers").choice(candidate_dishes)
        cid = self.ids.new("C")

        new_cust = {
            "id": cid,
            "table_id": target_table["id"],
            "dish_id": chosen_dish,
            "order_tick": self.phase_tick,
            "state": "waiting",
            "patience_ticks_left": self._ticks(t["patience_s"]),
            "eat_ticks_left": 0,
            "order_status": "reserved",
            "reserved": dict(self.menu[chosen_dish]["recipe"]),
            "base_price": None,
            "tip": 0,
        }
        self.customers.append(new_cust)
        events.append(("customer_arrived", {
            "order_id": cid,
            "table_id": target_table["id"],
            "dish_id": chosen_dish,
        }))

    def _ticks(self, seconds: float) -> int:
        """Quy đổi giây sang tick theo tuning['tick_hz'], không hard-code số 60."""
        return int(round(seconds * self.hz))

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
