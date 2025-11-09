# Single-Session-CLI-Chatbot-AI

Ini adalah script tunggal python yang berfungsi untuk mengakses Gemini AI menggunakan API dari [Google Studio AI](https://aistudio.google.com/api-keys)

Script ini baru dapat dijalankan di Termux atau lingkungan Python lainnya.

## Struktur Direktori

```
Single-Session-CLI-Chatbot-AI
├── .geminikey
├── .gitignore
├── .role                                n├── .session
├── README.md                             ├── ai.py
├── dependencies.txt
├── install.sh                            └── requirements.txt
```
## File dan Fungsinya

- `.geminikey`: File ini menyimpan API key untuk mengakses Gemini AI.
- `.role`: File ini menyimpan peran atau konteks yang akan digunakan oleh chatbot.
- `.session`: File ini menyimpan riwayat sesi percakapan.
- `ai.py`: Script utama yang menjalankan chatbot CLI.
- `dependencies.txt`: Daftar dependensi yang diperlukan untuk menjalankan script.
- `install.sh`: Script untuk menginstal dependensi yang diperlukan.
- `requirements.txt`: File yang berisi daftar paket Python yang diperlukan.

## Prasyarat
- Termux atau lingkungan Python lainnya
- Python 3.x
- API key dari Google Studio AI

## Cara Menggunakan

1. Clone repositori ini ke dalam lingkungan Python Anda:
```
git clone https://github.com/Rovikin/Single-Session-CLI-Chatbot-AI.git
```
2. Masuk ke direktori proyek:
```
cd Single-Session-CLI-Chatbot-AI
```
3. Jalankan script instalasi untuk menginstal dependensi:
```
chmod +x install.sh
./install.sh
```
4. Masukkan API key Anda ke dalam file `.geminikey`. Anda bisa mendapatkan API key dari [Google Studio AI](https://aistudio.google.com/api-keys).
5. (Opsional) Tentukan peran atau konteks chatbot dengan mengedit file `.role`. misalnya:
```
Kamu adalah asisten AI yang ramah dan membantu. Gunakan bahasa Indonesia informal, casual, bergaya genz, dan berikan jawaban yang singkat dan jelas. Gunakan "gw" untuk merujuk pada diri sendiri dan "elo" untuk merujuk pada pengguna.
```
simpan teks di atas ke dalam file `.role` dengan cara:
```
echo "Kamu adalah asisten AI yang ramah dan membantu. Gunakan bahasa Indonesia informal, casual, bergaya genz, dan berikan jawaban yang singkat dan jelas. Gunakan \"gw\" untuk merujuk pada diri sendiri dan \"elo\" untuk merujuk pada pengguna." > .role
```
6. Jalankan chatbot dengan perintah:
```
python ai.py
```
atau jika menggunakan Python 3 secara spesifik:
```
python3 ai.py
```
atau jika anda ingin menjalankannya langsung sebagai executable:
```
chmod +x ai.py
```
lalu jalankan dengan:
```
./ai.py
```
7. Mulai berinteraksi dengan chatbot melalui terminal.
## Catatan
- Pastikan untuk menjaga kerahasiaan API key Anda.
- File `.session` akan dibuat secara otomatis untuk menyimpan riwayat percakapan Anda.
- Anda dapat menghapus file `.session` jika ingin memulai sesi percakapan baru tanpa riwayat sebelumnya.
## Lisensi
Proyek ini tentunya dapat digunakan secara bebas. Silakan gunakan sesuai kebutuhan Anda. Namun, harap diingat untuk tetap mematuhi kebijakan penggunaan API dari Google Studio AI. Pastikan untuk tidak menyalahgunakan layanan ini dan gunakan dengan bijak.
