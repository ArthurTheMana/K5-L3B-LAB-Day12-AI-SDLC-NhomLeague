# Thong tin phat hanh v1.0.0 (Release Notes)

Phien ban chinh thuc v1.0.0 - Quan An Cho Noi (nhomLeague).

## Tinh nang chinh
- Thu hoach & Lan bat ca (Gather): Boi, tieu hao oxy/HP, bat 3 loai ca, hai 3 loai rau, ca sau san moi.
- Quan an (Quan): Phuc vu 4 ban an (T1..T4), bep nau 6 mon truyen thong, tinh tien va tien boa theo do tuoi.
- Cua hang (Shop) & Vong ngay (Day Loop): Nang cap binh oxy, tang mau toi da, luu tru tien va danh tieng xuyen suot 5 ngay.
- Canh bao truc quan & Tro nang: 3 canh bao (Thuy quai den gan, Oxy < 20%, Khach sap gian) va che do Tuong phan cao (phim H).
- Cong cu danh gia: Benchmark render 1280x720 dat 178+ FPS va Soak headless 10 ngay on dinh 0 loi.

## Huong dan chay
- Chay giao dien web: python -m chonoi.live --mode day
- Chay kiem thu: python -m unittest discover -s tests
- Chay benchmark: python -m chonoi.bench --seed 42 --duration 30 --out bench.json
- Chay soak test: python -m chonoi.soak --seed 7 --days 10 --out soak.json

## Bang chung xac minh
- Kiem chung day du tai docs/verification/phase-4.md.
- Ket qua do luong luu tai docs/proof/phase-4/.

## Video Demo
- Video demo đầy đủ các tính năng: [Xem trên Google Drive](https://drive.google.com/drive/folders/1i-8iecDNyMrnudIiFV2PQ_aMYfn-U6sD?usp=sharing)
