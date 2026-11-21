# Quán Ăn Chợ Nổi — nhóm nhomLeague

Game quản lý quán ăn 2D mang bản sắc miền Tây. Út Sen lặn bắt cá, hái bông trên sông Chín Khúc vào buổi sáng; tối về nấu và phục vụ khách trên nhà bè của Má Tư; cuối ngày dùng tiền mua nâng cấp ở Shop. Một lượt chuẩn gồm 5 Ngày (kế hoạch D1–D5).

Bản v1.0.0 · Test Contract **v1.3** (gameplay, tuning, kho và JSONL theo v1.2) · Đề bài và lab board: **[Chợ Nổi Lab](https://claude.ai/artifact/E35v787wSx2wDgPTNhMVDg)**.

## Yêu cầu môi trường

- **Python 3.10 trở lên** (đã chạy trên 3.12 và 3.13). Chỉ dùng thư viện chuẩn, **không cần `pip install`**.
- Một trình duyệt hiện đại (Chrome, Firefox, Safari, Edge) để mở bản có giao diện. Khung chơi 1280×720.
- macOS hoặc Linux. Trên Windows dùng `python` thay cho `python3`.

## Chạy từ clone sạch (3 lệnh)

```bash
git clone https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague.git
cd K5-L3B-LAB-Day12-AI-SDLC-NhomLeague
python3 -m chonoi.live --mode day
```

Mở địa chỉ `http://127.0.0.1:8000` mà terminal in ra, rồi bấm chọn một chế độ ở menu chính: **Chơi Trọn Vòng Ngày** (5 Ngày), **Bắt Cá & Hái Rau** hoặc **Mở Quán Chợ Nổi**. Đổi cổng bằng `--port 8080`, đổi seed bằng `--seed 7`. Có thể chơi riêng từng buổi bằng `--mode gather` hoặc `--mode quan`. `build_cmd` là `true` vì không có bước build.

## Điều khiển

| Phím | Tác dụng |
|---|---|
| **WASD** / **mũi tên** | Bơi (sáng) · đi trong quán (tối) |
| **E** | Cập bến, hái bông (sáng) · nấu, bưng, phục vụ (tối) |
| **Space** | Bắt cá (chỉ khi đang ở dưới nước) |
| **Shift** (giữ) | Bơi nhanh, tốn thể lực (chỉ có ở bản chơi, xem mục Sáng tạo) |
| **P** / **Esc** | Tạm dừng / tiếp tục. Trong menu tạm dừng, **M** để về menu chính. Nút 🏠 về trang chủ |
| **1** / **2** | Ở Shop: mua cấp Bình oxy / Áo phao |
| **Enter** | Ở Shop: đóng Shop, sang Ngày kế |
| **H** | Bật/tắt **chế độ tương phản cao** (có cả nút trên màn hình) |
| **R** | Chơi lại từ đầu |

**Cảnh báo trên HUD**, có chữ hoặc biểu tượng, đọc được cả ở chế độ tương phản cao:
- Thủy quái gần (Cá Sấu đang đuổi hoặc cách ≤ 10 m): băng chữ "⚠ THỦY QUÁI ĐẾN GẦN!" và viền màn hình nhấp nháy tím/đỏ, kèm âm báo.
- Oxy sắp hết (< 20%): thanh oxy nhấp nháy kèm "⚠" và băng chữ "⚠ OXY SẮP HẾT". Khi oxy cạn có chữ "Hết hơi!".
- Khách sắp giận (kiên nhẫn < 25%): thanh kiên nhẫn ở bàn đổi màu, kèm biểu tượng 😠.

## Cách chơi và cách tính điểm

- **Sáng (Lặn & Hái):** 180 s. Lấy đủ nguyên liệu Má Tư cần cho thực đơn của Ngày, giỏ chứa 12 ô. Lặn thì tốn oxy, oxy cạn thì mất Máu. Cá Sấu Năm Chèo chạm vào làm mất Máu và rơi hàng. Máu về 0 thì ngất, mất cả giỏ. Nguyên liệu hao tươi 0,5/s, dưới 30 là bị ươn.
- **Tối (Mở Quán):** 180 s, có 2 bếp và 4 bàn. Khách gọi món nấu được bằng kho hiện có. Giá món tính theo độ tươi trung bình của nguyên liệu dùng. Phục vụ khi khách còn ≥ 50% kiên nhẫn thì được boa 20% và +0,2 uy tín. Khách bỏ đi vì hết kiên nhẫn thì −0,5 uy tín.
- **Shop:** mua Bình oxy (45 s / 60 s) và Áo phao (4 / 5 Máu). Cấp vừa mua có hiệu lực từ Ngày kế.
- **Điểm** = `earned + 100 × floor(reputation)`. `earned` là tổng thu cả lượt, gồm tiền món và boa. Mua nâng cấp trừ vào `money` nhưng không trừ vào `earned`.

## Lệnh cho kiểm thử và chấm

Các lệnh lấy từ `game.contract.json`:

```bash
# Bộ test của nhóm (1 lệnh, ~30 s)
python3 -m unittest discover -s tests -v

# Headless theo Test Contract (gather | quan | day)
python3 -m chonoi.headless --mode day --seed 1 --days 1 --ticks 22200 --out out.jsonl
python3 -m chonoi.headless --mode gather --seed 42 --scenario dock.json --inputs dock-inputs.json \
        --ticks 1 --out gather.jsonl --inventory-out catch.json
python3 -m chonoi.headless --mode quan --seed 42 --inventory catch.json --ticks 0 --out quan.jsonl

# Benchmark cảnh lặn 1280×720 (bench_cmd)
python3 -m chonoi.bench --seed 42 --duration 30 --out bench.json

# Soak 10 Ngày (soak_cmd)
python3 -m chonoi.soak --seed 7 --days 10 --out soak.json
```

Harness của nhóm (xem [`AGENTS.md`](AGENTS.md)):
- `python3 tools/verify_phase.py --phase N` chạy test và các smoke, rồi ghi `docs/proof/phase-N/verify.md` kèm commit hash.
- `python3 tools/check_contract.py` đối chiếu contract với số chuẩn của đề.
- Bật pre-commit hook một lần cho mỗi clone: `git config core.hooksPath .githooks`.

## Mở rộng

**Chưa làm mục mở rộng nào có mã trong Test Contract.** `game.contract.json` chưa có khóa `extensions`. Theo đề, nhóm 5 người cần làm ít nhất 1 mục, nên đây là phần còn thiếu, có ghi ở mục Giới hạn đã biết.

## Sáng tạo của nhóm

Các phần dưới đây chỉ có ở giao diện trình duyệt (`chonoi/live.py`, `chonoi/web/`) và **tắt ở headless**, nên không đổi tick, sự kiện, tiền, uy tín hay snapshot theo contract.

| Ý tưởng | Mô tả | Bằng chứng lõi vẫn đúng |
|---|---|---|
| Cá Sấu "có hồn" | Khi đuổi người chơi, Cá Sấu đổi màu, nước gợn và có âm báo ngắn. Âm thanh cần người chơi nhấn phím trước. | `docs/proof/phase-2/crocodile.md` |
| Sprite 2D | Út Sen (lặn và trong quán), 3 loài cá, Cá Sấu, khách, nền nhà bè. Có menu chính. | Chỉ ảnh hưởng hình vẽ. Regression 180 test đạt |
| Ngạt chậm hơn ở bản chơi | Khi oxy cạn dưới nước, bản chơi trừ 1 Máu mỗi 600 tick (10 s) để người mới dễ chơi. Headless và contract vẫn là 60 tick. | `chonoi/live.py` đặt `live_choke_interval_ticks = 600` chỉ cho phiên live. Headless đọc `choke_interval_ticks: 60` từ contract, regression 180 test đạt |
| Thể lực và bơi nhanh | Giữ Shift để bơi ×1,5, tốn thể lực, có HUD "Stamina". Chỉ bật khi `LiveGame` đặt `_live_stamina_enabled`. | `chonoi/sim/gather.py` (`_move`): headless không bật cờ này. `docs/proof/phase-4/verify.md` |

## Giới hạn đã biết

- **Benchmark** (`chonoi/bench.py`) dựng pixel RGB 1280×720 thật bằng phần mềm, offscreen, rồi đo FPS. Đây **không phải** FPS của Canvas trong trình duyệt, vì bản chơi chạy trên trình duyệt còn Python không mở cửa sổ đồ họa. Kết quả: `docs/proof/phase-4/bench.json`.
- Chưa có mục mở rộng nào theo Test Contract (xem trên).
- Bản chơi trên trình duyệt ngạt chậm hơn luật lõi (600 tick thay vì 60 tick mỗi Máu, xem mục Sáng tạo). Muốn chơi đúng luật lõi thì dùng headless.
- Bản chơi trên trình duyệt chưa được đo FPS bằng công cụ. Đã chơi thử bằng tay.

## Tài liệu nhóm

[`TEAM.md`](TEAM.md) · [`CHANGELOG.md`](CHANGELOG.md) · [`CREDITS.md`](CREDITS.md) · [`docs/contracts/`](docs/contracts/) · [`docs/verification/`](docs/verification/) · [`docs/proof/`](docs/proof/) · [`docs/clarify.md`](docs/clarify.md) · [`docs/ai-usage-log.md`](docs/ai-usage-log.md) · [`docs/retro.md`](docs/retro.md) · [`docs/members/`](docs/members/) · Khung starter: [`docs/STARTER.md`](docs/STARTER.md)

## Quy định của lab

Dùng AI thoải mái, nhưng không sao chép repo của nhóm khác và bằng chứng phải thật. Nhân vật và bối cảnh là bản gốc của lab. Asset ngoài chỉ được dùng CC0/CC-BY/MIT hoặc tự tạo, và phải ghi nguồn trong `CREDITS.md`. Không commit API key, token, `.env`.
