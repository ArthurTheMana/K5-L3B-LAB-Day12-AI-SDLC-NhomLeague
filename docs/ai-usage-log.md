# Nhật ký dùng AI (theo phase và theo người)

| Phase | Người | Công cụ / model | Việc | Token / chi phí ước tính | Ghi chú (AI sai ở đâu?) |
|---|---|---|---|---|---|
| 1 | ArthurTheMana (Huy) | ChatGPT | Khởi tạo khung mô phỏng `gather.py` (bơi, lặn, oxy, hái nút) | ~15k token | AI sinh nhầm công thức hồi oxy theo giây thay vì theo tick; đã chỉnh lại theo `oxygen_refill_per_tick`. |
| 1 | dinhnam269 (Nam) | Antigravity | Tạo khung HTML/Canvas và điều khiển di chuyển WASD/mũi tên | ~12k token | Bắt sự kiện bàn phím bị trôi khi nhấn giữ; đã sửa thành `keydown`/`keyup` với tập hợp `keysDown`. |
| 2 | QDat18 (Đạt) | Antigravity | Viết module `service.py`, tính tiền boa 6 món và module `shop.py` | ~25k token | AI tính nhầm tiền boa món cá kèo nướng 70k thành 15k (do làm tròn sai `floor(70 * 0.2) = 14`); đã sửa lại bằng test hộp đen. |
| 2 | dinhnam269 (Nam) | Antigravity | Cập nhật Bếp B2, ưu tiên tương tác khi nhấn E và kiểm thử cháy món | ~20k token | AI ưu tiên Bàn trước Bếp khi hòa khoảng cách; đã sửa lại quy tắc: Bếp trước Bàn, ID nhỏ hơn trước. |
| 2 | vtgiang213 (Giang) | Codex | Cập nhật cơ chế cá sấu Năm Chèo săn mồi và sinh cá theo ngày | ~18k token | AI nhầm bán kính phát hiện `detect_radius` với tốc độ rượt đuổi; đã sửa lại theo đúng contract. |
| 3 | DoAnhThu832004 (Thư) | Antigravity & Claude | Viết schema kho v1.2 và cập nhật độ tươi `fractions.Fraction` | ~22k token | Sai số dấu phẩy động ở ngưỡng 30; đã chuyển sang dùng `fractions.Fraction` theo clarify #1. |
| 3 | vtgiang213 (Giang) | Codex | Tích hợp kho v1.2, bàn giao Lặn–Quán và sửa regression | ~28k token | AI dừng quá sớm khi regression còn lỗi; sau phản hồi đã sửa và chạy lại toàn bộ. |
| 3 | QDat18 (Đạt) | Antigravity | Xây dựng máy trạng thái Vòng lặp Ngày D1..D5 (`day.py`) và bảo lưu nâng cấp | ~20k token | AI xử lý thiếu trường hợp kết thúc ngày sớm khi hết khách; đã bổ sung điều kiện chuyển shop. |
| 4 | DoAnhThu832004 (Thư) | Claude & Antigravity | Rà soát thiếu sót P1–P4; viết harness: skill `verify-phase` (`tools/verify_phase.py`), skill `contract-check` (`tools/check_contract.py`) | ~25k token | Hook bản đầu gọi `python3`, nhưng trên Windows đó là lối tắt Microsoft Store nên commit bị chặn nhầm. Đã sửa để dò Python chạy thật. |
| 4 | QDat18 (Đạt) | Antigravity | Viết `chonoi/bench.py` (đo FPS 1280x720) và `chonoi/soak.py` (chạy 10 ngày liên tục) | ~30k token | AI đo FPS dựa trên số vòng lặp thuần mà không throttle/raster; đã bổ sung raster RGB thực tế và tính 1% low FPS theo chuẩn `TICKET-04`. |
| 4 | dinhnam269 (Nam) | Antigravity | Bổ sung 3 cảnh báo trực quan (Thủy quái, Oxy < 20%, Khách giận) và chế độ Tương phản cao (phím H) | ~18k token | AI viết thiếu bộ lắng nghe phím tắt H trên trình duyệt; đã bổ sung toggle phím H trong listener. |
