---
title: "Setup Hermes Free, But Do It Like an Operator"
description: "Panduan praktis deploy model open-weight Hermes di VPS dengan konfigurasi aman, resource limits, dan reverse proxy terisolasi. Tanpa server crash."
pubDate: 2026-10-01
updatedDate: 2026-10-01
category: "build-logs"
tags: ["hermes", "vps", "docker", "open-source-ai", "operations"]
canonicalUrl: "https://sammyjason.com/blog/setup-hermes-free-operator"
heroImage: "/images/blog/setup-hermes-free-operator.webp"
leadAsset:
  keyword: "HERMES"
  title: "VPS Setup Checklist & Safe Config Template"
  downloadUrl: "/assets/downloads/hermes-operator-checklist.pdf"
draft: false
---

Menjalankan model open-weight di server sendiri selalu terdengar menarik. Kamu bisa memangkas biaya langganan API berbayar, menjaga kerahasiaan data, dan berkreasi tanpa batas kuota platform pihak ketiga. Model open-weight seperti Hermes sering menjadi pilihan favorit para builder karena kemampuannya yang solid dalam menjalankan instruksi terstruktur. Namun di lapangan, banyak kawan-kawan yang mengeluh karena baru sepuluh menit berjalan, VPS mereka mendadak hang, RAM habis, dan sesi SSH terputus total.

Banyak tutorial di internet hanya mengajarkan cara instan: sewa VPS murah, jalankan satu baris instalasi otomatis, lalu tinggalkan. Cara ini mengabaikan realita operasional sistem. Artikel ini membedah cara setup model Hermes secara disiplin ala operator sistem: sizing komputasi yang realistis, isolasi container, pembatasan sumber daya ketat, dan reverse proxy yang aman.

### Reality Check Kebutuhan Komputasi

Kegagalan deploy model mandiri paling sering berakar pada salah perhitungan hardware. Menjalankan model kuantisasi 8B membutuhkan alokasi RAM kerja yang nyata, bukan sekadar ruang hard disk. Selain bobot model itu sendiri, setiap penambahan panjang context window akan memakan memori kerja tambahan secara signifikan.

Jika kamu memaksakan model besar pada VPS dengan RAM pas-pasan tanpa swap dan batas alokasi yang jelas, Linux Out of Memory (OOM) Killer akan langsung membunuh proses mesin inferensi secara tiba-tiba saat menerima prompt panjang. Untuk menjalankan model kuantisasi 8B dengan stabil pada CPU VPS, sediakan minimal 16 GB RAM sistem. Sisihkan setidaknya 4 GB RAM secara khusus untuk kestabilan kernel Linux, Docker daemon, dan buffer antrean jaringan.

### Arsitektur Setup Minimum yang Aman

Sebagai operator sistem, kita tidak boleh menjalankan aplikasi inferensi langsung di host OS tanpa isolasi. Di lingkungan kerja praktis, setup minimum yang stabil dan aman terdiri dari tiga komponen dalam satu Docker bridge network internal:

1. **Docker Daemon:** Sebagai runtime terisolasi untuk mengelola siklus hidup aplikasi dan membatasi konsumsi memori.
2. **Inference Engine (Ollama atau vLLM Ringan):** Memuat bobot model Hermes ke memori kerja dan memproses permintaan inferensi token.
3. **Nginx Reverse Proxy:** Menjadi pintu gerbang tunggal di depan yang menerima koneksi luar, menangani enkripsi SSL, dan memvalidasi token autentikasi.

Port internal mesin inferensi sama sekali tidak boleh terekspos langsung ke IP publik. Semua akses dari luar wajib disaring terlebih dahulu oleh layer proxy.

### Langkah 1: Hardening VPS dan User Isolation

Langkah awal selalu dimulai dari penataan server Linux yang bersih. Jangan pernah menjalankan proses container engine atau aplikasi AI menggunakan akun root bawaan server. Buat satu user sistem baru dengan akses sudo terbatas, misalnya akun bernama aiops.

Selanjutnya, amankan akses masuk server dengan menonaktifkan autentikasi password pada konfigurasi SSH (PasswordAuthentication no di file /etc/ssh/sshd_config) dan wajibkan login menggunakan SSH key pair.

Pasang firewall sederhana menggunakan UFW. Kunci semua port masuk dan hanya izinkan port 22 untuk administrasi serta port 443 untuk lalu lintas web terenkripsi:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Langkah 2: Menjalankan Hermes via Container Terkendali

Saat menyusun file Docker Compose, tentukan parameter pembatas sumber daya secara eksplisit. Tanpa batas tegas, container akan mencoba mengonsumsi seluruh RAM yang tersisa saat beban kerja melonjak.

Gunakan direktif mem_limit pada konfigurasi service agar container tidak membebani sistem operasi:

```yaml
version: '3.8'
services:
  hermes-engine:
    image: ollama/ollama:latest
    container_name: hermes_service
    restart: unless-stopped
    environment:
      - OLLAMA_KEEP_ALIVE=5m
      - OLLAMA_HOST=0.0.0.0:11434
    volumes:
      - ./model_data:/root/.ollama
    deploy:
      resources:
        limits:
          memory: 12G
          cpus: '3.5'
    networks:
      - ai_internal_net

networks:
  ai_internal_net:
    internal: true
```

Pengaturan OLLAMA_KEEP_ALIVE=5m memerintahkan mesin inferensi melepaskan bobot model dari memori jika tidak ada request baru dalam lima menit. Langkah ini menjaga server tetap lega saat idle.

### Langkah 3: Mengamankan Endpoint dengan Reverse Proxy dan Auth

Banyak server dibobol karena port inferensi lokal (seperti 11434) dibiarkan terbuka ke publik tanpa password. Pihak asing dapat dengan mudah memanfaatkan komputasi VPS kamu untuk kepentingan mereka.

Solusi operator adalah mengunci network container ke mode internal dan mengalirkan semua akses melalui Nginx reverse proxy:

```nginx
server {
    listen 443 ssl http2;
    server_name ai.domainkamu.com;

    ssl_certificate /etc/letsencrypt/live/ai.domainkamu.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ai.domainkamu.com/privkey.pem;

    location / {
        proxy_pass http://hermes_service:11434;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 300s;
    }
}
```

Pastikan kamu memasang pengecekan header API key pada layer gateway atau aplikasi sebelum endpoint digunakan. Hanya tool tim internal yang memegang kunci rahasia yang dapat memanggil model.

### Sanity Check dan Verifikasi Latency

Sebelum server dipakai untuk operasional harian, lakukan uji beban ringan secara terukur. Kita harus mengetahui batas performa server sebelum pengguna mulai mengirim tugas nyata.

Kirimkan beberapa permintaan uji menggunakan perintah cURL dari terminal lokal untuk mengecek respon sistem:

```bash
curl -X POST https://ai.domainkamu.com/api/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: KUNCI_...AMU" \
  -d '{"model": "hermes-3-llama-3.1-8b", "prompt": "Jelaskan prinsip continuous integration dalam 3 poin.", "stream": false}'
```

Sambil request berjalan, pantau penggunaan CPU dan RAM via perintah docker stats pada terminal terpisah. Catat angka kecepatan token per detik dan lonjakan waktu respon pada prompt panjang. Jika kecepatan turun di bawah lima token per detik pada konteks 2000 token, batasi batas konteks maksimal pada konfigurasi aplikasi agar server tidak tumbang.

### Kesimpulan: Menjadi Operator yang Bertanggung Jawab

Menjalankan model kecerdasan buatan secara mandiri bukan ajang pamer kecepatan instalasi. Pembeda utama antara pemula yang sekadar mencoba dengan operator sistem yang matang adalah komitmen pada stabilitas: server menyala stabil berhari-hari, konsumsi memori terprediksi, dan akses terlindungi rapat.

Jika kamu ingin menerapkan setup ini di VPS milikmu tanpa perlu meraba konfigurasi dari nol, saya sudah menyusun VPS Setup Checklist & Safe Config Template. Di dalamnya tersedia checklist sizing hardware, template Docker Compose, konfigurasi Nginx reverse proxy dengan autentikasi header, dan aturan firewall siap pakai.

Kirim pesan atau tinggalkan komentar dengan kata kunci HERMES untuk mendapatkan checklist dan template konfigurasi ini secara langsung. Mari kita bangun infrastruktur yang stabil bersama.