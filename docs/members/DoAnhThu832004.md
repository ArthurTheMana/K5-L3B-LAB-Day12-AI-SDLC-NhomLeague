# DoAnhThu832004 — phản tư cá nhân (≤ 200 từ)

Đỗ Anh Thư · PO · lát 3 (`chonoi/sim/quan.py`)

- **Tôi đã làm:**
  - P1: khách, giữ chỗ, kiên nhẫn, `no_dish` ([`4efa3a8`](https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/commit/4efa3a8)).
  - P2: B2, T1–T4 và 6 món trong contract ([`82018c7`](https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/commit/82018c7), [`2748865`](https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/commit/2748865)), lọc món theo kế hoạch ngày ([`b65ee19`](https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/commit/b65ee19)).
  - P3: kho cá thể v1.2, hao tươi, `spoiled`, giữ lại khi ươn ([`ec34f8b`](https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/commit/ec34f8b)).
  - P4: điền TEAM.md ([`f09a632`](https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/commit/f09a632)), harness gồm 2 skill và pre-commit hook ([`976bcfd`](https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/commit/976bcfd)), README phát hành, LICENSE, CREDITS.
- **Tôi đã review:**
  - Gộp `origin/main` vào nhánh mình ([`a1e3e02`](https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/commit/a1e3e02)), giữ cả `day_plan` lẫn test thứ tự bàn.
  - Rà repo trước Release: bench chỉ đo 2 s, link `file:///` hỏng, bản chơi ngạt 600 tick thay vì 60 tick.
- **AI sai ở đâu:**
  - Hook gọi `python3`, trên Windows đó là lối tắt Store nên mọi commit bị chặn. Tôi phát hiện khi chạy thử hook.
  - AI viết câu cảnh báo vào README theo trí nhớ. Tôi grep UI thì thấy chữ thật khác.
- **Điều tôi học được:** dùng `Fraction` và test biên ở ngưỡng 30 để tránh sai số float. Điều AI khẳng định phải kiểm bằng lệnh chạy thật.
