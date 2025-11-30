# 🚀 Codashop Multi-Account Wallet Checker
Script Python untuk melakukan pengecekan **wallet Codashop** secara otomatis pada banyak akun (multi-account).  
Dilengkapi fitur **Realtime Logging, Auto Save Results, Balance Detector, Country Mapping, dan Deteksi WAF (Web Application Firewall)**.

---

## ✨ Fitur Utama

### 🔐 Login Multi-Akun
- Membaca list akun dari file `akun.txt`
- Format auto-detect: `email:password`

### 💼 Cek Wallet Codashop (Full Data)
Mendapatkan data terbaca:
- Balance
- Mobile / nomor yang terhubung
- Country Code + nama negara otomatis
- Wallet ID
- User ID
- Total Spent

### ⚠️ Sistem Keamanan Anti WAF
- Script otomatis mendeteksi **WAF Block**
- Logging WAF ke file `waf_block_log.txt`
- Program langsung berhenti agar IP tidak diblok permanen

### 📁 Auto Save Hasil (Realtime)
Script otomatis membuat dua file output:
- `hasil_wallet_live_YYYYMMDD_HHMMSS.txt` → Semua hasil pengecekan
- `hasil_balance_YYYYMMDD_HHMMSS.txt` → Akun yang memiliki balance > 0

### 🌍 Country Mapping
Kode negara otomatis dikonversi menjadi:
- Nama negara  
- Simbol mata uang (Rp, ₱, RM, ฿, S$, dll)

### 📊 Summary Otomatis
Setiap 5 akun, script update summary:
- Jumlah sukses
- Jumlah gagal
- Akun dengan balance
- Progress berjalan

---

## 📦 Cara Penggunaan

### 1. Siapkan file `akun.txt`
Format:
