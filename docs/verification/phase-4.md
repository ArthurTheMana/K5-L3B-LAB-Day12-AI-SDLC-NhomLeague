# Ma trận truy vết Phase 4 (v1.3 / Phát hành v1.0.0)

| AC | Cách kiểm chứng | Bằng chứng (`docs/proof/phase-4/...`) | Kết quả |
|---|---|---|---|
| AC-P4-01 | Chạy `<bench_cmd> --seed 42 --duration 30 --out docs/proof/phase-4/bench.json` | [bench.json](file:///Users/mac/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/docs/proof/phase-4/bench.json) (`tests/test_bench.py`) | Đạt |
| AC-P4-02 | Chạy `<soak_cmd> --seed 7 --days 10 --out docs/proof/phase-4/soak.json` (`days_completed == 10`, `crashes == 0`) | [soak.json](file:///Users/mac/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/docs/proof/phase-4/soak.json) (`tests/test_soak.py`) | Đạt |
| AC-P4-03 | 3 cảnh báo (Thủy quái, Oxy `< 20%`, Khách sắp giận `😠`) + Chế độ tương phản cao (`H`) | `chonoi/web/index.html`, `tests/test_ui_alerts.py` | Đạt |
| AC-P4-04 | Contract v1.3 (`bench_cmd`, `soak_cmd`), `CHANGELOG.md` và regression P1–P3 | `game.contract.json`, `CHANGELOG.md`, `unittest discover -s tests` | Đạt |
