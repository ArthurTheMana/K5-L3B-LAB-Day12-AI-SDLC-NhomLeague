---
name: contract-check
description: Đối chiếu game.contract.json với số chuẩn của đề (v1.1–v1.3, 6 món, day_plan, shop, freshness, Cá Sấu, 2 bếp/4 bàn), team_size với TEAM.md và số mục extensions. Dùng mỗi khi sửa game.contract.json, docs/contracts/, schema kho, hoặc trước khi tag.
---

# contract-check

`game.contract.json` là hợp đồng chung của mọi module. Sửa sai một số là hỏng test ẩn của cả nhóm.

## Các bước

1. Chạy:
   ```bash
   python3 tools/check_contract.py
   ```
   - `[LỖI]`: số lệch chuẩn, thiếu khóa, `day_plan.ingredients` không bằng tổng công thức × số suất, `team_size` lệch TEAM.md → mã 1, phải sửa.
   - `[CẢNH BÁO]`: chưa đủ mục `extensions` theo cỡ nhóm (5 người ≥ 1, 6 người ≥ 2). Không chặn nhưng phải xử lý trước phase-4.
2. Nếu thay đổi là **cố ý** (đề phát hành số mới, thêm mở rộng):
   - Sửa hằng số chuẩn trong `tools/check_contract.py` **cùng commit** với `game.contract.json`.
   - Khi bật mở rộng: thêm mã vào `extensions` (ví dụ `"burn"`, `"reservations"`, `"leaderboard"`) và khóa tuning tương ứng theo mục 4.1 của TICKET-02 / mục 2 của TICKET-03.
   - Chạy test liên quan: `PYTHONPATH=tests:. python3 -m unittest tests.test_phase2_data tests.test_contract_fish_initial -v`.
   - Ghi breaking change vào `CHANGELOG.md`; nếu đổi schema kho/sự kiện thì cập nhật `docs/contracts/` và `docs/contracts/inventory.sample.json`.
3. Báo cả nhóm trước khi push (AGENTS.md: "Không sửa contract khi chưa báo cả nhóm"). Đổi schema kho nên có 2 người đọc lại.
4. Chạy `verify-phase` (skill kia) nếu sửa đụng tới luật hoặc schema kho.

## Không làm

- Không đổi số chuẩn chỉ để một test xanh.
- Không thêm khóa tự chế vào `tuning` mà không tắt ở headless (xem README "Tự do sáng tạo").
