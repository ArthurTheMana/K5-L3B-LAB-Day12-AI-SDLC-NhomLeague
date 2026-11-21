# Bằng chứng tích hợp kho phase 3

- Phạm vi: schema kho v1.2, Lặn → file → Quán, chuyển pha trong Ngày, ngưỡng 30 và hiển thị số hàng ươn trên HUD.
- Thay đổi ảnh hưởng nhóm: `game.contract.json`, bộ đọc/ghi kho, scenario, JSONL, Lặn, Quán, vòng Ngày, headless/live và HUD. Cần thông báo nhóm trước khi tích hợp; fixture v1.1 phải đổi sang mảng cá thể theo CHANGELOG.
- Thứ tự tích hợp: bộ kiểm schema và cấp ID → Lặn và Quán → file và vòng Ngày → HUD. Bản hiện tại bật v1.2 cho cả hai đầu; file v1.1 bị từ chối với mã 2.
- Kiểm thử 2026-11-21 với Python portable 3.12.8: `python -m unittest tests.test_phase3_inventory_handover tests.test_gather_freshness tests.test_phase3_kitchen tests.test_phase3_customers_fresh -q`: 29 test đạt. Có kiểm tra file không bị ghi khi chưa kết thúc, file sai bị từ chối, ID nối tiếp giữa ngày và không hao thêm ở tick chuyển pha.
- Smoke `python -m chonoi.headless --mode day --seed 1 --days 1 --ticks 22200 --out out.jsonl`: mã thoát 0.
- Regression đầy đủ sau khi chuyển fixture liên quan sang v1.2: `python -m unittest discover -s tests -q`, 177 test đạt (Python portable 3.12.8). Giữ kiểm tra thứ tự rơi LIFO, thời điểm, bàn giao, thứ tự đơn và sự kiện; giá chốt sau hao tươi thay đổi theo luật v1.2. Sửa thêm lỗi tự giữ hàng khi nhiều đơn chưa có reserved, đơn đã phục vụ và tuần tự hóa độ tươi trong sự kiện nấu. Một số unit test còn kiểm tra nhánh tương thích dữ liệu đếm trực tiếp; headless v1.2 vẫn từ chối schema đếm.
- HUD chưa được kiểm tra trực quan trong trình duyệt.
