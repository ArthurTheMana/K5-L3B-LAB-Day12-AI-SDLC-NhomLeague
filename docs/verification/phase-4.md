# Ma trận truy vết Phase 4 (v1.3 / Phát hành v1.0.0)

| AC | Cách kiểm chứng | Bằng chứng (`docs/proof/phase-4/...`) | Kết quả |
|---|---|---|---|
| AC-P4-01 | Chạy `<bench_cmd> --seed 42 --duration 30 --out docs/proof/phase-4/bench.json` | [bench.json](../proof/phase-4/bench.json) (`tests/test_bench.py`) | Đạt |
| AC-P4-02 | Chạy `<soak_cmd> --seed 7 --days 10 --out docs/proof/phase-4/soak.json` (`days_completed == 10`, `crashes == 0`) | [soak.json](../proof/phase-4/soak.json) (`tests/test_soak.py`) | Đạt |
| AC-P4-03 | 3 cảnh báo (Thủy quái, Oxy `< 20%`, Khách sắp giận `😠`) + Chế độ tương phản cao (`H`) | `chonoi/web/index.html`, `tests/test_ui_alerts.py` | Đạt |
| AC-P4-04 | Contract v1.3 (`bench_cmd`, `soak_cmd`), `CHANGELOG.md` và regression P1–P3 | `game.contract.json`, `CHANGELOG.md`, [verify.md](../proof/phase-4/verify.md) (`tools/verify_phase.py --phase 4`: 180 test, smoke kho v1.2, kho đếm → mã 2, ngưỡng ươn, day), `tools/check_contract.py` | Đạt |
| AC-P4-05 | Clone sạch, chạy bản có giao diện bằng ≤ 3 lệnh theo README | [clean-clone.md](../proof/phase-4/clean-clone.md) | Đạt trên Windows. Chưa thử trên macOS/Linux thật |
| AC-P4-06 | README có yêu cầu môi trường, điều khiển, cách tính điểm, lệnh test/headless/bench/soak, giới hạn đã biết | [README.md](../../README.md) | Đạt |
| AC-P4-07 | Rà `CREDITS.md` và `LICENSE` cho tài sản đã dùng | [CREDITS.md](../../CREDITS.md), [LICENSE](../../LICENSE) | Một phần: đã có LICENSE (MIT) và nguồn âm thanh/phông. Nguồn 8 sprite còn chờ dinhnam269 xác nhận công cụ tạo |
| AC-P4-08 | Tag `phase-4` và GitHub Release v1.0.0 cùng trỏ một commit trên `main`, có bản đóng gói và release notes | [GitHub Release v1.0.0](https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/releases/tag/v1.0.0) | Đạt |
| AC-P4-09 | Retro rà hành động P2, phản tư cá nhân đủ 5 người | `docs/retro.md`, `docs/members/` | Đạt |
| — | Mở rộng (nhóm 5 người ≥ 1 mục) | `game.contract.json` → `extensions` | Chưa làm |

## Ghi chú

- **Benchmark** đo raster phần mềm RGB 1280×720 offscreen, làm nóng 3 s rồi đo 30 s (`measured_s: 30.0027`, `frames: 5363`, `avg_fps: 178.75`, `p1_low_fps: 106.21`, `load_ms: 11.2`). Mốc báo cáo avg ≥ 60, 1% low ≥ 30, load ≤ 10 s đều đạt. Đây không phải FPS của Canvas trình duyệt (xem README, Giới hạn đã biết).
- **Bằng chứng kiểm chứng tự động** (`verify.md`) phải được tạo lại trên đúng commit gắn tag `phase-4`: `python3 tools/verify_phase.py --phase 4`.
