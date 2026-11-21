# Thử chạy từ clone sạch (AC-P4-05)

- Ngày: 2026-11-21 · Người chạy: DoAnhThu832004 (cùng Claude Code)
- Commit được clone: `58c95cd` (main sau merge PR #17)
- Máy: Windows 11, Python 3.13.2, Git Bash. Không cài thêm gói nào.

## Lệnh (đúng 3 lệnh như README)

```bash
git clone <repo> clean && cd clean
python -m chonoi.live --mode day --port 8765
```

## Kết quả

| Kiểm tra | Kết quả |
|---|---|
| Server in địa chỉ | `Mở trình duyệt tại http://127.0.0.1:8765/  (chế độ day, seed 1). Ctrl+C để dừng.` |
| `GET /` (trang game) | HTTP 200 |
| `GET /state` | Snapshot `{"type":"snapshot","tick":0,"mode":"day","phase":"gather","state":"playing","time_left_ticks":10800,...}` |
| `GET /assets/ut_sen_dive.png` (sprite) | HTTP 200 |

**Đạt.** Không cần `pip install` hay bước build nào.

## Lưu ý trung thực

- Trên Windows, khi **chuyển hướng stdout** vào file (`> live.log`), `print` tiếng Việt bị lỗi `UnicodeEncodeError` vì bảng mã cp1258. Chạy với `PYTHONIOENCODING=utf-8` thì hết lỗi. Chạy trực tiếp trong terminal, hoặc trên macOS/Linux (UTF-8 mặc định), thì không gặp lỗi này. `python -m chonoi.bench --help` và `chonoi.soak --help` cũng bị lỗi tương tự trên Windows.
- Lần thử này dùng Windows, chưa chạy trên máy macOS/Linux thật. Nên có một bạn dùng Mac chạy lại 3 lệnh trong README để xác nhận.
