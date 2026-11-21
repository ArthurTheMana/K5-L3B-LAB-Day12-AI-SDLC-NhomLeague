# Nhật ký dùng AI (theo phase và theo người)

| Phase | Người | Công cụ / model | Việc | Token / chi phí ước tính | Ghi chú (AI sai ở đâu?) |
|---|---|---|---|---|---|
| 3 | Người yêu cầu (chưa ghi tên) | Codex | Tích hợp kho v1.2, bàn giao Lặn–Quán và sửa regression; 177 test đạt, smoke một ngày đạt. | Chưa có số liệu | AI dừng quá sớm khi regression còn lỗi; sau phản hồi đã sửa và chạy lại toàn bộ. HUD chưa được kiểm tra trực quan. |
| 4 | DoAnhThu832004 | Claude Code (Claude Opus 5.5) | Rà soát thiếu sót P1–P4; viết harness: skill `verify-phase` + `tools/verify_phase.py`, skill `contract-check` + `tools/check_contract.py`, hook `.githooks/pre-commit`; cập nhật AGENTS.md. Chạy thật: verify phase 4 đạt 5/5 bước (`docs/proof/phase-4/verify.md`), check_contract 115 mục đạt, 1 cảnh báo thiếu `extensions`. | Chưa đo | Hook bản đầu gọi `python3`, nhưng trên Windows đó là lối tắt Microsoft Store nên mọi commit bị chặn nhầm. Phát hiện khi chạy thử hook, đã sửa để hook dò ra Python chạy được thật. |
