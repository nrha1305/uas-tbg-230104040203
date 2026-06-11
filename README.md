# UAS Teknologi Big Data TI23A

## Identitas

- NIM  : 230104040203
- NAMA : NOR HAYATI
- KELAS: TI23A
- NIM akhir: 3, ganjil
- Soal: Smart Retail Visitor Prediction System
- Pipeline: Visitor Tracking -> Spark Aggregation -> Parquet -> ML Forecasting -> Streamlit Dashboard

## Struktur Folder

```text
uas-tbg-230104040203/
├── app.py
├── generate_pipeline.py
├── requirements.txt
└── output/
    ├── visitor_total/
    ├── visitor_time/
    └── ml_visitor/
```

## Langkah Menjalankan di Linux Server / WSL

### 1. Masuk ke folder project

```bash
cd ~/bigdata-project/uas-tbg-230104040203
```

Jika folder belum ada, buat dulu:

```bash
mkdir -p ~/bigdata-project/uas-tbg-230104040203
cd ~/bigdata-project/uas-tbg-230104040203
```

### 2. Buat dan aktifkan virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install library Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

###45. Jalankan Spark Pipeline

```bash
python3 generate_pipeline.py
```

Output yang harus muncul:

- sample data visitor tracking
- total pengunjung tiap zona
- tren pengunjung tiap 15 menit
- dataset AI berdasarkan hour
- lokasi folder parquet berhasil dibuat
- validasi jumlah row parquet

### 6. Cek file parquet untuk screenshot

```bash
find "$(pwd)/output" -type f -name "*.parquet" -print
```

Bisa juga cek struktur folder:

```bash
tree output
```

### 7. Jalankan Dashboard Streamlit

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Buka browser:

```text
http://localhost:8501
```

Jika memakai server kampus, gunakan IP server:

```text
http://IP-SERVER:8501
```

## Screenshot yang Perlu Dikumpulkan

1. Screenshot terminal saat `python3 generate_pipeline.py` berhasil.
<img width="1918" height="1188" alt="Screenshot 2026-06-11 104358" src="https://github.com/user-attachments/assets/ebc72691-130c-4050-9087-8b5168ff0127" />

2. Screenshot terminal saat `SPARK` berhasil.
<img width="1919" height="1193" alt="Screenshot 2026-06-11 104340" src="https://github.com/user-attachments/assets/fe2756e1-5e44-4529-86fb-4ef01f8446dc" />

3. Screenshot SPARK.
<img width="1919" height="1141" alt="Screenshot 2026-06-11 103129" src="https://github.com/user-attachments/assets/8e6c38f9-15b3-44e3-aba0-1882a0181656" />

4. Screenshot folder/file parquet dari perintah `find "$(pwd)/output" -type f -name "*.parquet" -print`.
<img width="1919" height="1199" alt="Screenshot 2026-06-11 104418" src="https://github.com/user-attachments/assets/90de0fa1-27d4-4504-a4b0-e78c59395112" />

5. Screenshot dashboard Streamlit yang menampilkan:
   - filter zona
   - KPI total pengunjung
   - grafik tren pengunjung
   - prediksi Linear Regression
   - analisis jam sibuk
<img width="1919" height="1017" alt="Screenshot 2026-06-11 103950" src="https://github.com/user-attachments/assets/bd8d397c-8cd3-4043-bb1f-f539bd07fc19" />

<img width="1919" height="1013" alt="Screenshot 2026-06-11 104009" src="https://github.com/user-attachments/assets/3fb44272-bcd4-4ff2-aef6-96125ce2c9be" />

<img width="1919" height="999" alt="Screenshot 2026-06-11 104020" src="https://github.com/user-attachments/assets/f69ec828-2be6-4596-bd7d-10b213bf21ac" />

## Analisis Jam Sibuk Pengunjung

Analisis jam sibuk pengunjung dilakukan berdasarkan hasil agregasi data visitor tracking per 15 menit. Data yang digunakan berasal dari tiga zona pusat perbelanjaan, yaitu FoodCourt, FashionArea, dan Cinema. Setiap data memiliki informasi timestamp, zone, dan visitor_count. Sesuai ketentuan soal, data pengunjung dibuat selama 180 menit dengan jumlah pengunjung random antara 10 sampai 500 orang. Hasil agregasi kemudian disimpan dalam format Parquet dan digunakan untuk menampilkan tren pengunjung pada dashboard Streamlit.

Berdasarkan hasil pengolahan data menggunakan PySpark, total pengunjung tertinggi terdapat pada zona FashionArea dengan jumlah 48.037 pengunjung. Zona Cinema memiliki total 45.262 pengunjung, sedangkan FoodCourt memiliki total 44.476 pengunjung. Meskipun FashionArea memiliki total pengunjung terbesar, jam sibuk tertinggi secara keseluruhan justru terjadi pada zona Cinema.

Berdasarkan hasil agregasi tren pengunjung per 15 menit, jam tersibuk terjadi pada zona Cinema pukul 09:45 sampai 10:00 dengan jumlah 5.223 pengunjung. Pada zona FoodCourt, kepadatan tertinggi terjadi pukul 10:00 sampai 10:15 dengan jumlah 4.465 pengunjung. Sementara itu, FashionArea mencapai puncak pengunjung pada pukul 10:30 sampai 10:45 dengan jumlah 4.423 pengunjung. Hasil ini menunjukkan bahwa setiap zona memiliki waktu puncak yang berbeda, sehingga pengelola pusat perbelanjaan perlu menyesuaikan jumlah petugas, pengaturan antrean, dan kesiapan layanan berdasarkan pola kepadatan masing-masing zona.

Dari hasil tersebut, dapat disimpulkan bahwa setiap zona memiliki pola kepadatan yang berbeda. Cinema cenderung mengalami lonjakan lebih awal, FoodCourt meningkat setelahnya, sedangkan FashionArea mencapai puncak kepadatan menjelang pertengahan waktu observasi. Informasi ini dapat digunakan oleh pengelola pusat perbelanjaan untuk mengatur penempatan petugas, mengantisipasi antrean, meningkatkan pengawasan, dan menyiapkan layanan tambahan pada zona yang mengalami lonjakan pengunjung.

## Catatan Penting

- Output utama memakai Parquet, bukan CSV.
- Path output memakai absolute path dengan `Path(__file__).resolve()`.
- Machine Learning memakai Linear Regression dari Scikit-Learn.
- Visualisasi dashboard memakai Plotly.
- Dashboard interaktif karena memiliki sidebar filter zona dan slider jam prediksi.
