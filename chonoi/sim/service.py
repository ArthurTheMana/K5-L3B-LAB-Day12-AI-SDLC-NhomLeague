"""Lát 4B — Phục vụ, Tiền, Boa & Đóng ca (`service`)."""

import math

from ..ids import sort_by_id

TICK = 60.0


def interact_table(sim, table, events):
    """Phục vụ món trên tay cho khách đang chờ tại bàn khớp `order_id`."""
    if sim.hand is None:
        return
    c = next((x for x in sim.customers if x["table_id"] == table["id"] and x["state"] == "waiting"), None)
    if c is None or sim.hand["order_id"] != c["id"]:
        return
    dish = sim.hand
    sim.hand = None
    c["state"] = "eating"
    c["order_status"] = "served"
    c["eat_ticks_left"] = int(round(sim.t["eat_s"] * TICK))
    c["base_price"] = dish["base_price"]
    pat_max = int(round(sim.t["patience_s"] * TICK))
    ratio = c["patience_ticks_left"] / pat_max if pat_max > 0 else 0.0
    tip = (
        int(math.floor(dish["base_price"] * float(sim.t["tip_rate"])))
        if ratio >= float(sim.t["tip_min_patience_ratio"])
        else 0
    )
    c["tip"] = tip
    events.append(("served", {
        "order_id": c["id"],
        "table_id": table["id"],
        "dish_id": c["dish_id"],
        "patience_ticks_left": c["patience_ticks_left"],
        "base_price": dish["base_price"],
        "tip": tip,
    }))


def step_service_and_closing(sim, shift_closing, events) -> bool:
    """Xử lý khách ăn xong trả tiền, hết kiên nhẫn rời bàn và đóng ca. Trả True nếu hết ca."""
    to_remove = set()
    for c in sort_by_id(sim.customers, key=lambda x: x["table_id"]):
        if c["state"] == "eating":
            if c["eat_ticks_left"] == 0 or shift_closing:
                pay_reason = "finished_eating" if c["eat_ticks_left"] == 0 else "closing"
                base_price = int(c["base_price"])
                tip = int(c["tip"])
                amount = base_price + tip
                sim.money += amount
                sim.earned += amount
                sim.shift_earned += amount
                if tip > 0:
                    sim.reputation = sim._clamp_rep(sim.reputation + float(sim.t["tip_reputation"]))
                events.append(("paid", {
                    "order_id": c["id"],
                    "table_id": c["table_id"],
                    "base_price": base_price,
                    "tip": tip,
                    "amount": amount,
                    "reason": pay_reason,
                }))
                to_remove.add(c["id"])
        elif c["state"] == "waiting":
            if shift_closing:
                events.append(("customer_left", {
                    "order_id": c["id"],
                    "table_id": c["table_id"],
                    "reason": "closing",
                    "reputation": sim.reputation,
                }))
                sim._release_customer_order(c["id"])
                to_remove.add(c["id"])
            elif c["patience_ticks_left"] == 0:
                sim.reputation = sim._clamp_rep(sim.reputation + float(sim.t["left_reputation_delta"]))
                events.append(("customer_left", {
                    "order_id": c["id"],
                    "table_id": c["table_id"],
                    "reason": "patience",
                    "reputation": sim.reputation,
                }))
                sim._release_customer_order(c["id"])
                to_remove.add(c["id"])

    if to_remove:
        sim.customers = [c for c in sim.customers if c["id"] not in to_remove]

    if shift_closing:
        sim.done = True
        sim.reason = "time"
        events.append(("quan_end", {
            "reason": "time",
            "money": sim.money,
            "earned": sim.earned,
            "shift_earned": sim.shift_earned,
            "reputation": sim.reputation,
        }))
        return True
    return False
