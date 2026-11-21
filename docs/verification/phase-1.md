# Ma trận truy vết Phase 1

| AC | Cách kiểm chứng | Bằng chứng (link `docs/proof/phase-1/...`) | Kết quả (đạt / chưa đạt — ghi trung thực) |
|---|---|---|---|
| AC-P1-01 | Lát 1–2: Bơi, oxy, ngạt, hái nút mặt nước & bắt cá dưới nước | [harvest.md](../proof/phase-1/harvest.md), [catch.md](../proof/phase-1/catch.md) | Đạt (`test_gather_harvest.py`, `test_gather_catch.py`, `test_phase1_rules.py`) |
| AC-P1-02 | Lát 3: Khách đến, giữ chỗ, kiên nhẫn & đóng ca | `tests/test_quan_customers.py` | Đạt |
| AC-P1-03 | Lát 4: Bếp nấu, bưng, phục vụ, tiền & boa | `tests/test_service.py`, `tests/test_phase1_rules.py` | Đạt |
| AC-P1-04 | Tích hợp 2 tiến trình `gather` → `quan` qua file kho | `tests/test_smoke_p1.py` (`test_inv_01_*`) | Đạt |

## Đánh giá ngắn
- Yêu cầu nào đạt / chưa đạt: Hoàn thành toàn bộ phạm vi lõi Phase 1 (4 lát).
- Điều cần chỉnh cho phase sau: Tiếp tục nâng cấp số liệu chuẩn và vòng ngày ở Phase 2.
