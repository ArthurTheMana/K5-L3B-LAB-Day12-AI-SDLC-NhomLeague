# Kiểm chứng phase 3 — kho và bàn giao

Kết quả dưới đây áp dụng cho bản làm việc hiện tại; chưa gắn với commit hoặc tag bàn giao.

| Phạm vi | Bằng chứng | Kết quả |
|---|---|---|
| Regression bộ test hiện có | `python -m unittest discover -s tests -q` với Python portable 3.12.8 | Đạt: 177 test |
| Kho v1.2, ngưỡng 30, bàn giao file và trong Ngày | `tests/test_phase3_inventory_handover.py`; `docs/proof/phase-3/inventory-handover.md` | Đạt các test đã chạy |
| Chạy headless một ngày | `python -m chonoi.headless --mode day --seed 1 --days 1 --ticks 22200 --out out.jsonl` | Đạt: mã thoát 0 |
| HUD độ tươi hoặc hàng ươn | `chonoi/web/index.html` | Đã sửa; chưa kiểm tra trực quan |

Các kết quả này chưa xác nhận toàn bộ yêu cầu phase 3 hay việc đẩy tag `phase-3`.
