# hand-detection

# ✋ Deteksi Bahasa Isyarat Menggunakan Python, MediaPipe, OpenCV, dan gTTS

Proyek ini adalah aplikasi sederhana yang mendeteksi **gerakan tangan (jumlah jari yang terangkat)** menggunakan kamera laptop dan menerjemahkannya menjadi **kata dan suara bahasa Indonesia**.

Aplikasi ini memanfaatkan **komputer visi (Computer Vision)** dan **Text-to-Speech (TTS)** untuk membuat sistem interaktif berbasis gestur.

---

## 🧩 Library yang Digunakan

Berikut penjelasan setiap library yang digunakan dalam program:

### 🔹 1. `cv2` (OpenCV)
- Digunakan untuk **mengakses kamera**, **membaca frame video**, dan **menampilkan hasil deteksi secara real-time.
- Fungsi penting:
  - `cv2.VideoCapture(0)` → membuka kamera.
  - `cv2.imshow()` → menampilkan tampilan video.
  - `cv2.circle()` & `cv2.putText()` → menggambar titik dan teks pada gambar.

### 🔹 2. `mediapipe`
- Library dari Google untuk **deteksi pose, wajah, dan tangan** secara cepat.
- Di proyek ini, digunakan modul:
  - `mp.solutions.hands` → untuk mendeteksi 21 titik koordinat tangan.
  - `mp.solutions.drawing_utils` → untuk menggambar garis koneksi antar titik.
- MediaPipe digunakan untuk menentukan **jari mana yang terbuka/tertutup**, lalu dihitung jumlah jari terbuka.

### 🔹 3. `pygame`
- Modul multimedia untuk Python.
- Di sini digunakan hanya bagian **`pygame.mixer`** untuk **memutar suara hasil konversi teks dari gTTS**.
- Fungsi penting:
  - `pygame.mixer.init()` → inisialisasi sistem audio.
  - `pygame.mixer.Sound(file)` → memuat file suara `.mp3`.
  - `sound.play()` → memutar suara.

### 🔹 4. `os`
- Library bawaan Python.
- Dipakai untuk **memeriksa keberadaan file suara (`voice_xxx.mp3`)**.
- Jika belum ada, maka program akan membuat file baru menggunakan gTTS.

### 🔹 5. `gtts` (Google Text-to-Speech)
- Library untuk mengubah teks menjadi suara dengan layanan Google Translate.
- Digunakan untuk **menghasilkan suara dari kata hasil deteksi gestur**, misalnya "halo", "nama", "saya".
- Fungsi penting:
  - `gTTS(text='halo', lang='id')` → membuat objek TTS bahasa Indonesia.
  - `.save(filename)` → menyimpan hasil ke file `.mp3`.

---

## Cara Kerja Program

1. Inisialisasi semua library:
   - `mediapipe` disiapkan untuk deteksi tangan.
   - `pygame` untuk suara.
   - Kamera dibuka dengan OpenCV.

2. Setiap frame dari kamera dianalisis:
   - Jika tangan terdeteksi, maka koordinat 21 titik tangan diproses.
   - Sistem menentukan jari mana yang terbuka berdasarkan posisi titik ujung dan sendi jari.

3. Menghitung jumlah jari terbuka:
   - Jika jumlahnya 1–5, program mencocokkan dengan kamus (`gesture_words`):
     ```python
     gesture_words = {
         1: "halo",
         2: "saya",
         3: "zidan",
         4: "naufal",
         5: "dendy"
     }
     ```

4. Menampilkan dan mengucapkan hasil:
   - Teks ditampilkan di layar (`cv2.putText`).
   - Suara diputar dengan `pygame.mixer.Sound`.

5. Stabilitas deteksi:
   - Program menunggu beberapa frame agar hasil tidak salah deteksi (menggunakan variabel `STABILITY_THRESHOLD`).

6. Program berhenti jika pengguna menekan tombol `Q` atau `ESC`.

---


---

## 🖥️ Instalasi & Menjalankan Program

### 1️⃣ Instal Library
```bash
pip install opencv-python mediapipe pygame gtts

## Jalankan Program
python deteksi_tangan.py

## 📸 Hasil Deteksi Tangan
Berikut contoh hasil deteksi jari oleh program:

![Hasil Deteksi](https://raw.githubusercontent.com/mnaufalrona/main/hasil.png)





