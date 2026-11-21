---
name: verify-phase
description: Kiểm chứng một phase trên commit hiện tại (unittest, smoke bàn giao kho v1.2, kho đếm bị từ chối, ngưỡng ươn 30, smoke day) và lưu bằng chứng vào docs/proof/phase-N/verify.md kèm commit hash. Dùng trước khi gắn tag phase-N, sau khi tích hợp nhánh, hoặc khi được hỏi "đã đạt chưa".
---

# verify-phase

Mục tiêu: bằng chứng trong `docs/proof/phase-N/` và `docs/verification/phase-N.md` **khớp đúng commit gắn tag**, không phải "bản làm việc hiện tại".

## Các bước

1. Đảm bảo cây làm việc sạch: `git status --porcelain` rỗng. Nếu còn thay đổi chưa commit, commit trước (hoặc ghi rõ trong báo cáo là chạy trên bản chưa commit).
2. Chạy:
   ```bash
   python3 tools/verify_phase.py --phase N
   ```
   Script gọi `headless_cmd` từ `game.contract.json` (hộp đen), ghi `docs/proof/phase-N/verify.md` với commit hash, phiên bản Python và bảng Đạt/Chưa đạt. Mã thoát 0 = mọi bước đạt.
   - `--quick` bỏ bộ unittest khi chỉ cần smoke nhanh.
3. Nếu có bước **Chưa đạt**: KHÔNG sửa test cho xanh. Đọc chi tiết trong bảng, sửa luật ở `chonoi/sim/*`, chạy lại. Nếu buộc phải đổi test vì luật mới, ghi lý do trong commit.
4. Mở `docs/verification/phase-N.md`, mỗi dòng AC-PN-xx trỏ tới bằng chứng (đường dẫn **tương đối**, không dùng `file:///…`) và ghi kết quả trung thực. Thêm dòng: `Kiểm chứng trên commit <hash> — xem docs/proof/phase-N/verify.md`.
5. Commit bằng chứng: `git add docs/proof/phase-N docs/verification/phase-N.md && git commit -m "docs(phase-N): bằng chứng kiểm chứng"`.
6. Báo Integrator commit hash để gắn tag `phase-N` (người gắn tag quyết, agent không tự push tag).

## Bổ sung theo phase

| Phase | Chạy thêm |
|---|---|
| 1–2 | Không có gì thêm; smoke kho trong script đã theo schema hiện hành (v1.2). Regression P1–P2 nằm trong bộ unittest. |
| 3 | Lưu thêm JSONL mẫu của ca ươn nếu cần dẫn chứng: xem `check_spoiled` trong script. |
| 4 | `python3 -m chonoi.bench --seed 42 --duration 30 --out docs/proof/phase-4/bench.json` (đúng **30 s**), `python3 -m chonoi.soak --seed 7 --days 10 --out docs/proof/phase-4/soak.json`. |

## Ghi nhật ký

Thêm một dòng vào `docs/ai-usage-log.md` (phase, người, công cụ, việc, AI sai ở đâu nếu có).
