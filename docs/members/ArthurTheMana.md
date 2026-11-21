# Nguyễn Tài Minh Huy - 2A202603828 - Phản tư cá nhân

Họ và tên: Nguyễn Tài Minh Huy (NguyenTaiMinhHuy)
MSSV: 2A202603828
GitHub: ArthurTheMana

- **Tôi đã làm:** Phase 1, triển khai Swimming, Oxygen, HP và cơ chế ngất. Phase 2, kiểm tra Fish Movement, Spawning và điều chỉnh Contract. Phase 3, triển khai Gather Freshness, cấp ID cho từng nguyên liệu, xử lý `spoiled`, LIFO và snapshot. Đã kiểm tra 19/19 Gather tests PASS. [Commit Phase 3](https://github.com/ArthurTheMana/K5-L3B-LAB-Day12-AI-SDLC-NhomLeague/commit/5ba0e92). Phase 4, cải thiện Benchmark, bổ sung tests và bằng chứng QA.

- **Tôi đã review:** Kiểm tra tính tương thích của Gather với Inventory v1.2 và chạy regression. Kiểm tra Benchmark 30 giây trên Windows, đạt 167.39 FPS trung bình.

- **AI sai ở đâu:** AI ban đầu hướng dẫn chuyển Inventory mà chưa kiểm tra toàn bộ các module phụ thuộc. Tôi phát hiện rủi ro khi đối chiếu `gather.py`, `inventory.py` và `quan.py`, sau đó giữ tương thích v1.1 trong lúc chờ tích hợp v1.2.

- **Điều tôi học được:** Phải kiểm tra Contract, viết tests trước khi merge và xác minh kết quả AI bằng code thực tế. Làm việc nhóm hiệu quả cần phân chia trách nhiệm rõ ràng và lưu bằng chứng trên GitHub.
