# Retro nhóm nhomLeague

## Phase 2 (nhanh)
- **Điều tốt**: Nhóm phân tách việc rõ ràng: bạn Nam phụ trách bếp & menu, Đạt phụ trách service & shop, Giang phụ trách crocodile & cá. Bộ test độc lập giúp phát hiện sớm sai lệch.
- **Điều tệ**: Khi hợp đồng nâng lên 4 bàn và 6 món, một số test cũ bị gãy do hard-code số lượng khách C2/C5 và tick xuất hiện. Việc merge nhánh còn một số xung đột nhỏ ở `game.contract.json`.
- **1 hành động cho Phase 3**: Luôn chạy bộ regression `unittest discover` trước khi mở PR và chốt sớm schema kho v1.2 qua file contract mẫu.

## Phase 4 (cuối)
- **Rà lại hành động Phase 2**: Đã thực hiện nghiêm túc; ở Phase 3 và 4 nhóm đã có file schema `inventory.sample.json` và chạy harness tự động trước khi merge nên không còn xung đột hợp đồng.
- **Điều tốt / điều tệ**:
  - *Điều tốt*: Hoàn thành toàn bộ các yêu cầu từ P1 đến P4; 180 test đều PASS; tích hợp thành công benchmark 178+ FPS, soak 10 ngày 0 crash và 3 cảnh báo trực quan + chế độ tương phản cao.
  - *Điều tệ*: Quá trình viết tài liệu retro và nhật ký AI bị dồn lại vào cuối phase do tập trung nhiều thời gian xử lý regression và tối ưu render.
- **Số liệu**:
  - Commit theo người: dinhnam269 (16), Hoang Quang Dat / QDat18 (9), DoAnhThu832004 (10), ArthurHighRisk (8), Truong Giang / vtgiang213 (12).
  - Cách đọc code của nhau: Review chéo PR trên GitHub, thảo luận trực tiếp qua Discord/Zalo khi có thay đổi hợp đồng.
  - Ước tính token theo người: ~30k - 50k token/người qua các công cụ AI (Claude, Codex, Antigravity).
- **Một lần AI sai và cách nhóm phát hiện**:
  - Khi nâng số bàn từ 1 lên 4 ở contract v1.1, AI ban đầu viết test mong đợi khách C2 xuất hiện ở tick 3720. Nhưng thực tế 4 bàn tiếp nhận C1..C4 cùng lúc, đến tick 3720 thì khách thứ 5 (C5) mới tới lượt ngồi vào bàn T1 khi C1 rời đi. Nhóm phát hiện khi chạy `test_quan_customers.py` bị `AssertionError: 'C5' != 'C2'` và đã sửa lại assertion để chấp nhận đúng quy luật bàn.
- **Nếu làm lại, đổi gì**:
  - Cập nhật tài liệu và nhật ký AI ngay sau mỗi commit thay vì để dồn cuối buổi.
  - Viết test hợp đồng tự động (contract linter) ngay từ Phase 1 để tự động chặn các sai lệch thông số trước khi merge.
