# 🎓 Sistem Penentuan Mahasiswa Berprestasi
### Fuzzy Inference System — Metode Mamdani

Sistem ini merupakan implementasi **Fuzzy Inference System (FIS) Mamdani** untuk menentukan tingkat prestasi mahasiswa berdasarkan empat kriteria input. Dibangun menggunakan Python dengan antarmuka GUI berbasis Tkinter.

---

## 📋 Deskripsi

Program studi membutuhkan sistem yang objektif untuk memilih mahasiswa berprestasi setiap semester. Sistem ini menggunakan logika fuzzy metode Mamdani untuk mengolah empat variabel input dan menghasilkan keputusan berupa kategori tingkat prestasi mahasiswa.

---

## 🔢 Variabel Sistem

### Input
| Variabel | Domain | Himpunan Fuzzy |
|---|---|---|
| IPK | 0 – 4.00 | Rendah, Sedang, Tinggi |
| Prestasi Lomba | 0 – 100 poin | Rendah, Sedang, Tinggi |
| Organisasi | 0 – 10 skor | Rendah, Sedang, Tinggi |
| Kehadiran | 0 – 100% | Rendah, Sedang, Tinggi |

### Output
| Variabel | Domain | Himpunan Fuzzy |
|---|---|---|
| Tingkat Prestasi | 0 – 100 | Cukup, Baik, Sangat Baik |

---

## ⚙️ Fungsi Keanggotaan

### IPK
- **Rendah** : Linear turun, a=1.5, b=2.5
- **Sedang** : Segitiga, a=2.0, b=2.75, c=3.5
- **Tinggi** : Linear naik, a=3.0, b=4.0

### Prestasi Lomba
- **Rendah** : Linear turun, a=20, b=40
- **Sedang** : Segitiga, a=20, b=45, c=70
- **Tinggi** : Linear naik, a=50, b=100

### Organisasi
- **Rendah** : Linear turun, a=2, b=4
- **Sedang** : Segitiga, a=2, b=5, c=8
- **Tinggi** : Linear naik, a=6, b=10

### Kehadiran
- **Rendah** : Linear turun, a=50, b=65
- **Sedang** : Segitiga, a=55, b=75, c=90
- **Tinggi** : Linear naik, a=75, b=100

### Output — Tingkat Prestasi
- **Cukup**      : Linear turun, a=20, b=50
- **Baik**       : Segitiga, a=30, b=55, c=80
- **Sangat Baik**: Linear naik, a=60, b=100

---

## 📏 Rule Base (11 Aturan)

| Rule | IPK | Prestasi | Organisasi | Kehadiran | Output |
|---|---|---|---|---|---|
| R1 | Tinggi | Tinggi | Tinggi | Tinggi | Sangat Baik |
| R2 | Tinggi | Tinggi | Sedang | Tinggi | Sangat Baik |
| R3 | Tinggi | Sedang | Tinggi | Tinggi | Baik |
| R4 | Sedang | Tinggi | Tinggi | Tinggi | Baik |
| R5 | Tinggi | Rendah | Rendah | Tinggi | Cukup |
| R6 | Sedang | Sedang | Sedang | Sedang | Baik |
| R7 | Rendah | Rendah | Rendah | Rendah | Cukup |
| R8 | Rendah | Sedang | Sedang | Sedang | Cukup |
| R9 | Tinggi | Tinggi | Rendah | Sedang | Baik |
| R10 | Sedang | Rendah | Tinggi | Tinggi | Cukup |
| R11 | Tinggi | Sedang | Sedang | Sedang | Baik |

---

## 🔄 Alur Proses Fuzzy Mamdani

```
Input Nilai
    ↓
Tahap 1: Fuzzifikasi
(nilai crisp → derajat keanggotaan)
    ↓
Tahap 2: Inferensi
(α-predikat = MIN per rule)
    ↓
Tahap 3: Komposisi
(MAX antar rule)
    ↓
Tahap 4: Defuzzifikasi
(Center of Area → nilai crisp output)
    ↓
Output Kategori
```

---

## 🖥️ Tampilan GUI

Aplikasi menampilkan:
- 4 field input untuk memasukkan nilai secara manual
- Tombol **HITUNG** untuk memproses
- Skor hasil defuzzifikasi (0–100)
- Indikator kategori: **Cukup / Baik / Sangat Baik**

---

## 🚀 Cara Menjalankan

### Prasyarat
- Python 3.x (download di [python.org](https://python.org))
- Library Tkinter (sudah built-in, tidak perlu install tambahan)

### Langkah
```bash
# Clone repository
git clone https://github.com/USERNAMEKAMU/fuzzy-mamdani-prestasi.git

# Masuk ke folder
cd fuzzy-mamdani-prestasi

# Jalankan program
python fuzzy_mamdani_v3.py
```

---

## 🧮 Contoh Perhitungan

| Input | Nilai |
|---|---|
| IPK | 3.5 |
| Prestasi Lomba | 75 |
| Organisasi | 7 |
| Kehadiran | 85% |

**Hasil Fuzzifikasi:**
| Variabel | Rendah | Sedang | Tinggi |
|---|---|---|---|
| IPK | 0 | 0 | 0.5 |
| Prestasi | 0 | 0 | 0.5 |
| Organisasi | 0 | 0.333 | 0.25 |
| Kehadiran | 0 | 0.333 | 0.4 |

**Rule Aktif:**
- R1: α = min(0.5, 0.5, 0.25, 0.4) = **0.25** → Sangat Baik
- R2: α = min(0.5, 0.5, 0.333, 0.4) = **0.333** → Sangat Baik

**Komposisi MAX:** α_SangatBaik = 0.333

**Hasil Defuzzifikasi:** z* = **83.14** → **Sangat Baik** ✅

---

## 🛠️ Teknologi

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![Metode](https://img.shields.io/badge/FIS-Mamdani-orange)

---

## 👤 Informasi

| | |
|---|---|
| **Mata Kuliah** | Kecerdasan Buatan |
| **Topik** | Sistem Penentuan Mahasiswa Berprestasi |
| **Metode** | Fuzzy Inference System Mamdani |
| **Nama** | [Nama Mahasiswa] |
| **NIM** | [NIM] |
| **Program Studi** | [Nama Prodi] |
| **Universitas** | [Nama Universitas] |

