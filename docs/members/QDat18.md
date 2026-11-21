# QDat18 — phản tư cá nhân (≤ 200 từ)

- **Tôi đã làm (kèm link commit)**:
  - Phụ trách module Phục vụ 4 bàn, tính giá & tiền boa 6 món Phase 2 (`chonoi/sim/service.py`, `tests/test_service.py`, `tests/test_phase2_service.py`).
  - Xây dựng module Cửa hàng & Nâng cấp Shop (`chonoi/sim/shop.py`, `tests/test_shop.py`).
  - Xây dựng máy trạng thái Vòng lặp Ngày D1..D5 (`chonoi/sim/day.py`, `tests/test_day_loop.py`).
  - Phát triển bộ chạy Soak Headless 10 ngày và Benchmark khung hình Phase 4 (`chonoi/soak.py`, `chonoi/bench.py`, `tests/test_soak.py`, `tests/test_bench.py`).
  - Nâng cấp `game.contract.json` lên v1.3.
- **Tôi đã review (kèm link)**:
  - Review và hợp nhất PR #6 của nhánh `feature/service` vào `main`.
  - Phối hợp và kiểm thử tích hợp với module Bếp (`kitchen.py`) của bạn Nam (Người A) và module Bắt cá (`gather.py`) của Trường Giang.
- **AI sai ở đâu và tôi phát hiện thế nào**:
  - Khi nâng số bàn từ 1 lên 4 ở contract v1.1, AI ban đầu để test cũ `test_quan_customers.py` mong đợi khách C2 xuất hiện ở tick 3720, nhưng thực tế có 4 bàn nên khách thứ 5 (C5) mới xuất hiện lúc đó. Tôi phát hiện qua việc chạy test suite và đã kịp thời chuẩn hóa assertion.
- **Điều tôi học được**:
  - Hiểu sâu về thiết kế hợp đồng hướng dữ liệu (Data-driven Contract), kiểm thử tự động hộp đen/hộp trắng và cách phân rã module để làm việc nhóm song song không bị xung đột.
