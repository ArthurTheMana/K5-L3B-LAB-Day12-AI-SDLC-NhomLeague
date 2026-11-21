# Changelog

### Phase 4 — Phát hành v1.0.0 (Contract v1.3)
- Cập nhật `game.contract.json` lên `"contract_version": "1.3"` với `bench_cmd` (`python3 -m chonoi.bench`) và `soak_cmd` (`python3 -m chonoi.soak`).
- Thêm hệ thống 3 cảnh báo trực quan (Thủy quái đến gần, Oxy `< 20%`, Khách sắp giận `😠`) và chế độ Tương phản cao (nút bấm + phím tắt `H`) trong `chonoi/web/index.html`.
- Thêm `chonoi/bench.py` (đo FPS cảnh lặn `1280×720`) và `chonoi/soak.py` (chạy soak headless 10 ngày liên tục D1–D10).

### Phase 3 — tích hợp bàn giao kho v1.2
- Breaking: `items`, `gather.hold` và `quan.stock` dùng mảng `{id, kind, fresh}`; kho đếm v1.1 không được nhận khi chạy v1.2. Chuyển fixture cũ bằng cách tạo một cá thể cho từng đơn vị, cấp ID duy nhất và `fresh: 100` (hoặc độ tươi fixture cần kiểm thử); cập nhật các khẳng định theo schema mới.
- Bàn giao cùng tick, giữ ID và độ tươi qua file và Ngày; `fresh` trong JSONL không bị làm tròn để tránh đổi nhánh tại ngưỡng. HUD đếm hàng ươn và không tính hàng ươn vào kho khả dụng.
- Các test tích hợp cũ đã chuyển fixture kho đếm và giỏ chuỗi sang cá thể v1.2, giữ kiểm tra hành vi; giá chốt được cập nhật do hao tươi trước khi nấu. Một số unit test vẫn kiểm tra riêng nhánh tương thích kho đếm nội bộ.
- Sửa tự giữ hàng khi nhiều khách chưa có `reserved`, xác thực đơn đã phục vụ và tuần tự hóa độ tươi trong sự kiện `cook_started`.
- Kiểm thử: toàn bộ 177 test regression đạt với Python 3.12.8; smoke headless một ngày đạt. HUD chưa được kiểm tra trực quan.
## Unreleased

### Phase 3 — Bếp & Độ tươi (Contract v1.2, `chonoi/sim/kitchen.py`)
- **Breaking / Schema mới (v1.2):**
  - `sim.stock` hỗ trợ mảng cá thể `[{"id": "I1", "kind": "...", "fresh": 100}, ...]` và `customers[].reserved` là mảng `id` cá thể (vẫn giữ tương thích ngược khi `sim.stock` là `dict` đếm theo loại ở v1.0/v1.1).
  - `cook_started.data.items` xuất mảng cá thể sắp theo `(kind, id_key)` và chốt `base_price = floor(giá niêm yết × trung bình fresh / 100)` (nhân thêm `1.5` rồi `floor` nếu là đơn đặt trước `reservation_id`).
  - Khi cháy món (`burn_s`), bỏ qua cá thể ươn (`fresh < spoiled_below`), giữ lại cá thể tươi nhất (hòa theo `id_key`), hoặc chuyển `failed` nếu là đơn đặt trước.
