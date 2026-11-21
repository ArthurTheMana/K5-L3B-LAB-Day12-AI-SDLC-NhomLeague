# Phạm Đình Nam (`dinhnam269`) — Phản tư cá nhân

Họ và tên: Phạm Đình Nam · GitHub: `dinhnam269` · Vai trò: `client/ui` & `sim/quan` (Bếp), QA lead

- **Tôi đã làm:**
  - Triển khai module Bếp (`chonoi/sim/kitchen.py`) qua 3 phase: nấu/chín/bưng món, hỗ trợ 2 bếp và 6 món (`v1.1`), tính giá theo độ tươi và cháy món (`v1.2`) ([`b423099`](https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/commit/b423099), [`3be9d5b`](https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/commit/3be9d5b)).
  - Thiết kế UI/UX, trang chủ chọn chế độ, bộ sprite 2D, 3 cảnh báo và chế độ tương phản cao `H` (`chonoi/web/index.html`, `chonoi/live.py`) ([`23d7f24`](https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/commit/23d7f24)).
  - Bổ sung `bench.py`, `soak.py`, ma trận `phase-1.md`, `phase-4.md` và test (`test_phase2_kitchen.py`, `test_phase3_kitchen.py`, `test_ui_alerts.py`) ([`5ebf863`](https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/commit/5ebf863)).
- **Tôi đã review & hỗ trợ:** Tích hợp `service.py` với `quan.py`, phát hiện và sửa lệch trạng thái `"waiting"` / `"waiting_dish"` ([`ab3bb7e`](https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/commit/ab3bb7e)).
- **AI sai ở đâu & cách phát hiện:** AI từng dùng `python` thay vì `python3` trên macOS và viết `read_inventory` chỉ nhận đúng `"1.2"` khiến chuyển sang `"1.3"` bị lỗi; tôi phát hiện khi chạy full test suite (`unittest discover`) và sửa ngay.
- **Điều tôi học được:** Luôn giữ đúng ranh giới module khi chia việc, và chạy kiểm thử tự động sau mỗi lần đổi hợp đồng.
