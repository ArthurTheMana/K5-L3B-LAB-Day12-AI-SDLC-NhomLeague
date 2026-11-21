# Credits

## Đề bài và khung starter
- Đề, nhân vật, bối cảnh và Test Contract: lab **K5-L3B Day 12 — AI SDLC** của VinUni-AI20k (repo gốc `VinUni-AI20k/K5-L3B-LAB-Day12-AI-SDLC`).
- Khung Python `chonoi/{headless,inputs,scenario,contract,rng,ids,jsonl,inventory,runner,live}.py` và `chonoi/web/` do giảng viên cấp. Nhóm đã mở rộng các file này.

## Hình ảnh (`chonoi/web/assets/`)

| File | Nội dung | Nguồn | Người thêm |
|---|---|---|---|
| `ut_sen_dive.png`, `ut_sen_quan.png` | Út Sen lúc lặn và lúc ở quán | Ảnh do công cụ AI tạo cho nhóm. **Chờ xác nhận tên công cụ** | dinhnam269 (commit `23d7f24`) |
| `fish_ca_loc.png`, `fish_ca_linh.png`, `fish_ca_keo.png` | Cá lóc, cá linh, cá kèo | Như trên. **Chờ xác nhận** | dinhnam269 (`23d7f24`) |
| `croc.png` | Cá Sấu Năm Chèo | Như trên. **Chờ xác nhận** | dinhnam269 (`23d7f24`) |
| `customer_quan.png` | Khách ở quán | Như trên. **Chờ xác nhận** | dinhnam269 (`23d7f24`) |
| `quan_bg.png` | Nền nhà bè | Như trên. **Chờ xác nhận** | dinhnam269 (`23d7f24`) |

> **TODO(dinhnam269):** ghi tên công cụ tạo ảnh và điều khoản sử dụng của công cụ đó. Nếu có ảnh nào lấy từ nguồn ngoài, ghi URL và giấy phép (chỉ dùng CC0/CC-BY/MIT). Các ảnh không có metadata nguồn (đã kiểm chunk PNG ngày 2026-11-21).

## Âm thanh và phông chữ
- Âm báo Cá Sấu được tổng hợp trực tiếp bằng Web Audio API (sóng sine 330 Hz, 0,25 s) trong `chonoi/web/index.html`. Không dùng file âm thanh ngoài.
- Không nhúng phông chữ ngoài, dùng phông mặc định của trình duyệt.

## Công cụ AI đã dùng
Chi tiết theo người và theo phase: [`docs/ai-usage-log.md`](docs/ai-usage-log.md).
- **Claude Code** (Anthropic): rà soát, harness (`tools/`, `.agents/skills/`, `.githooks/`), README, tài liệu Phase 4.
- **Codex** (OpenAI): tích hợp kho v1.2 và bàn giao Lặn–Quán ở Phase 3.
- Công cụ tạo ảnh cho sprite: xem TODO ở trên.

## Giấy phép
Mã nguồn và tài liệu của nhóm theo [MIT](LICENSE).
