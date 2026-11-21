# Kiểm chứng Cá Sấu

- Lệnh: `python -m unittest discover -s tests` (môi trường Python có `python3`).
- Kết quả: 116 test đạt (`Ran 116 tests in 12.040s`, `OK`).
- Phạm vi test mới: tuần tra/đuổi, va chạm nhiều Cá Sấu, rơi hàng LIFO, bất tử, recoil 60 bước, ngạt cùng tick, ngất, scenario sai và bố trí gather Ngày 1.
- Chưa kiểm chứng M2 trong vòng ngày: `--mode day` chưa được tích hợp. Cần review các thay đổi ở contract và scenario cùng nhóm.
