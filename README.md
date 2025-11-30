# 🚀 Codashop Multi-Account Wallet Checker

Script Python untuk melakukan pengecekan **wallet Codashop** secara
otomatis pada banyak akun (multi-account).\
Dilengkapi fitur **Realtime Logging, Auto Save Results, Balance
Detector, Country Mapping, dan Deteksi WAF (Web Application Firewall)**.

------------------------------------------------------------------------

## ✨ Fitur Utama

### 🔐 Login Multi-Akun

-   Membaca list akun dari file `akun.txt`
-   Format auto-detect: `email:password`

### 💼 Cek Wallet Codashop (Full Data)

Mendapatkan data terbaca: - Balance - Mobile / nomor yang terhubung -
Country Code + nama negara otomatis - Wallet ID - User ID - Total Spent

### ⚠️ Sistem Keamanan Anti WAF

-   Script otomatis mendeteksi **WAF Block**
-   Logging WAF ke file `waf_block_log.txt`
-   Program langsung berhenti agar IP tidak diblok permanen

### 📁 Auto Save Hasil (Realtime)

Script otomatis membuat dua file output: -
`hasil_wallet_live_YYYYMMDD_HHMMSS.txt` → Semua hasil pengecekan -
`hasil_balance_YYYYMMDD_HHMMSS.txt` → Akun yang memiliki balance \> 0

### 🌍 Country Mapping

Kode negara otomatis dikonversi menjadi: - Nama negara\
- Simbol mata uang (Rp, ₱, RM, ฿, S\$, dll)

### 📊 Summary Otomatis

Setiap 5 akun, script update summary: - Jumlah sukses - Jumlah gagal -
Akun dengan balance - Progress berjalan

------------------------------------------------------------------------

## 📦 Cara Penggunaan

### 1. Siapkan file `akun.txt`

Format:

    email1@example.com:qwerty123
    email2@example.com:mypass123
    email3@example.com:password

### 2. Jalankan script

    python codashopchecker3.py

### 3. Hasil akan otomatis dibuat

-   File detail semua akun\
-   File khusus akun yang memiliki balance\
-   Log WAF jika terjadi pemblokiran

------------------------------------------------------------------------

## 📂 Struktur File Output

  File                        Keterangan
  --------------------------- ---------------------------------------
  `hasil_wallet_live_*.txt`   Semua hasil pengecekan secara lengkap
  `hasil_balance_*.txt`       Hanya akun yang memiliki saldo
  `waf_block_log.txt`         Catatan ketika script mendeteksi WAF

------------------------------------------------------------------------

## 📸 Contoh Output Console

    [3/20] 🔐 Memproses: user@gmail.com
       ✅ Login berhasil, mengecek wallet...
       ✅ Berhasil - Balance: Rp12000, Mobile: +628xxx, Negara: Indonesia
       💰 AKUN INI MEMILIKI BALANCE!

------------------------------------------------------------------------

## 🛡️ Peringatan

Script ini hanya untuk: - Pengujian - Edukasi - Monitoring akun milik
sendiri

Penggunaan di luar itu merupakan tanggung jawab masing-masing pengguna.

------------------------------------------------------------------------

## 🧑‍💻 Kontribusi

Pull request dipersilakan! Silakan buat *issue* untuk request fitur baru
atau laporan bug.

------------------------------------------------------------------------

## 📄 Lisensi

Lisensi bebas (MIT).\
Silakan gunakan, modifikasi, dan kembangkan.
