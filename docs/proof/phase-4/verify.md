# Kiểm chứng tự động — phase 4

- Commit: `2be8307` (có thay đổi chưa commit)
- Lệnh: `python3 tools/verify_phase.py --phase 4`
- Python: 3.13.2 · win32

| Bước | Kết quả | Chi tiết |
|---|---|---|
| Bộ unittest | Đạt | Ran 180 tests in 22.780s / OK (23.0s) |
| Smoke bàn giao kho v1.2 (gather → file → quan) | Đạt | gather end=docked, kho=[{"id": "I1", "kind": "ca_linh", "fresh": 99.99166666666666}], stock tick0 khớp=True |
| Kho dạng đếm v1.0 bị từ chối | Đạt | kho đếm -> mã 2 (cần 2) |
| Ngưỡng ươn fresh 30 → spoiled tick 1 | Đạt | rc=0, spoiled=[{"type": "event", "tick": 1, "phase": "gather", "name": "spoiled", "data": {"item_id": "I1", "kind": "ca_linh", "location": "hold"}}] |
| Smoke day --days 1 --ticks 22200 | Đạt | reason=days_complete, days_completed=1, earned=0, score=300, 0.9s (cần ≤ 20s) |
