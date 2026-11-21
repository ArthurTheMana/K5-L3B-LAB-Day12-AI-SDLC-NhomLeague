"""Lát 4A — Bếp & Bưng món (`kitchen`): đếm giờ nấu, chín món, bắt đầu nấu và lấy món lên tay."""

from ..ids import id_key, sort_by_id

TICK = 60.0

# Sáng tạo (chỉ dùng cho UI/thoại, không ảnh hưởng logic/snapshot headless):
DISH_QUOTES = {
    "ca_loc_nuong_trui": "Má Tư: \"Cá lóc đồng nướng trui rơm thơm lừng, trở đều tay kẻo khét nghen Út!\"",
    "goi_bong_sung": "Má Tư: \"Bông súng giòn rụm trộn nước mắm me chua ngọt là hết sẩy!\"",
    "lau_ca_linh_dien_dien": "Má Tư: \"Mùa nước nổi có nồi lẩu cá linh bông điên điển là khách thương nhớ hoài!\"",
}


def kitchen_story_note(stoves, hand) -> str:
    """Trả về lời thoại Nam Bộ theo trạng thái bếp (tắt ở headless, chỉ phục vụ hiển thị)."""
    if hand is not None:
        return "Út Sen: \"Món nóng hổi rồi, bưng ra bàn cho khách lẹ tay thôi!\""
    for s in sort_by_id(stoves):
        if s["state"] == "ready" and s.get("dish"):
            return "Má Tư: \"Chín tới rồi Út ơi, nhấc xuống bưng ra cho khách kẻo nguội!\""
        if s["state"] == "cooking" and s.get("dish"):
            return DISH_QUOTES.get(s["dish"]["dish_id"], "Má Tư: \"Giữ lửa than củi tràm đều tay nghen con!\"")
    return "Má Tư: \"Bếp than hồng sẵn sàng rồi, chờ khách gọi món là lên lửa liền!\""


def step_stoves(sim, events):
    """Cập nhật bộ đếm bếp đầu bước và chuyển các bếp nấu xong sang `ready`."""
    for s in sort_by_id(sim.stoves):
        if s["state"] == "cooking":
            s["cook_ticks_left"] = max(0, s["cook_ticks_left"] - 1)
        elif s["state"] == "ready":
            s["ready_ticks"] += 1

    for s in sort_by_id(sim.stoves):
        if s["state"] == "cooking" and s["cook_ticks_left"] == 0:
            s["state"] = "ready"
            s["ready_ticks"] = 0
            events.append(("dish_ready", {
                "stove_id": s["id"],
                "order_id": s["dish"]["order_id"],
                "dish_id": s["dish"]["dish_id"],
            }))


def interact_stove(sim, stove, events):
    """Tương tác với bếp: bếp `idle` nhận đơn `reserved` cũ nhất, bếp `ready` giao lên tay trống."""
    if stove["state"] == "idle":
        waiting_res = [
            c for c in sim.customers
            if c["state"] == "waiting" and c["order_status"] == "reserved"
        ]
        if not waiting_res:
            return
        waiting_res.sort(key=lambda c: (c["order_tick"], id_key(c["table_id"])))
        c = waiting_res[0]
        items_used = []
        for k in sorted(c["reserved"].keys()):
            qty = c["reserved"][k]
            sim.stock[k] = sim.stock.get(k, 0) - qty
            if sim.stock[k] <= 0:
                sim.stock.pop(k, None)
            items_used.extend([k] * qty)
        c["reserved"] = {}
        c["order_status"] = "assigned"
        base_price = int(sim.menu[c["dish_id"]]["price"])
        stove["state"] = "cooking"
        stove["dish"] = {"order_id": c["id"], "dish_id": c["dish_id"], "base_price": base_price}
        stove["cook_ticks_left"] = int(round(sim.menu[c["dish_id"]]["cook_s"] * TICK))
        stove["ready_ticks"] = 0
        events.append(("cook_started", {
            "stove_id": stove["id"],
            "order_id": c["id"],
            "dish_id": c["dish_id"],
            "items": items_used,
            "base_price": base_price,
        }))
    elif stove["state"] == "ready" and sim.hand is None:
        dish = stove["dish"]
        sim.hand = dish
        stove["state"] = "idle"
        stove["dish"] = None
        stove["cook_ticks_left"] = 0
        stove["ready_ticks"] = 0
        events.append(("dish_picked", {
            "stove_id": stove["id"],
            "order_id": dish["order_id"],
            "dish_id": dish["dish_id"],
        }))
