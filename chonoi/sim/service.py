"""Lát 4B — Phục vụ, Tiền, Boa & Đóng ca (`service`).

KHUNG CHỜ NGƯỜI B VIẾT TIẾP (không làm thay phần Người B):
  1. `interact_table(sim, table, events)` — feat(service): handle serving dish to table and trigger served event
  2. `step_eating(sim)` — feat(service): handle customer eating countdown
  3. `step_service_and_closing(sim, shift_closing, events)` — feat(service): calculate bill payment, tip logic and reputation gain
"""


def interact_table(sim, table, events):
    """TODO(Người B): Phục vụ món trên tay (`sim.hand`) cho khách đang chờ tại `table` (`served`)."""
    pass


def step_eating(sim):
    """TODO(Người B): Mỗi tick trừ `eat_ticks_left` cho khách đang `eating`."""
    pass


def step_service_and_closing(sim, shift_closing, events) -> bool:
    """TODO(Người B): Thanh toán (`paid`), tính boa (`tip`), cập nhật `reputation`, khách rời bàn (`customer_left`) và đóng ca (`quan_end`)."""
    if shift_closing:
        sim.done = True
        sim.reason = "time"
        return True
    return False
