# 🦅 Pegasus OSINT Bot (Telegram)

Bot Telegram ringan untuk riset OSINT yang berfokus pada data teknis dan publik (domain, IP, threat intelligence, pencarian sumber publik, pelacakan ekspedisi, info kode pos). Dirancang untuk pengguna yang butuh alat bantu pengumpulan intelijen legitimate, auditing, dan respon insiden — dengan prinsip privasi, transparansi, dan kepatuhan hukum.

## 👨‍💻 Author

**Lettu Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE**

- 🌐 GitHub: [github.com/sobri3195](https://github.com/sobri3195)
- 📧 Email: [muhammadsobrimaulana31@gmail.com](mailto:muhammadsobrimaulana31@gmail.com)
- 🌐 Website: [muhammadsobrimaulana.netlify.app](https://muhammadsobrimaulana.netlify.app)
- 🌐 Portfolio: [muhammad-sobri-maulana-kvr6a.sevalla.page](https://muhammad-sobri-maulana-kvr6a.sevalla.page)

### 📱 Social Media

- 📺 YouTube: [@muhammadsobrimaulana6013](https://www.youtube.com/@muhammadsobrimaulana6013)
- 📞 Telegram: [@winlin_exploit](https://t.me/winlin_exploit)
- 🎵 TikTok: [@dr.sobri](https://www.tiktok.com/@dr.sobri)
- 💬 Grup WhatsApp: [Join Group](https://chat.whatsapp.com/B8nwRZOBMo64GjTwdXV8Bl)

### 💖 Support & Donation

Jika bot ini bermanfaat untuk Anda, pertimbangkan untuk memberikan dukungan melalui:

- ☕ [Trakteer](https://trakteer.id/g9mkave5gauns962u07t)
- 💳 [Lynk.id](https://lynk.id/muhsobrimaulana)
- 🛒 [Gumroad](https://maulanasobri.gumroad.com/)
- 🎨 [Karya Karsa](https://karyakarsa.com/muhammadsobrimaulana)
- 💰 [Nyawer](https://nyawer.co/MuhammadSobriMaulana)

## ⚠️ Penting — Batasan & Etika

**Bot ini TIDAK menyediakan, menyimpan, atau mengakses:**
- ❌ Data pribadi sensitif (NIK/KTP, data bank, NPWP)
- ❌ Rekam kriminal atau data penegak hukum
- ❌ Akun email target atau password
- ❌ Face recognition atau identifikasi biometrik
- ❌ Data internal yang dilindungi atau proprietary

**Penggunaan untuk aktivitas yang tidak sah DILARANG.**

Pastikan selalu mendapatkan **izin eksplisit** sebelum melakukan pengujian atau pengumpulan data terhadap pihak/organisasi tertentu.

## ✨ Fitur Utama (Aman & Publik)

### 🔍 IP Lookup
- WHOIS information
- ASN (Autonomous System Number)
- Geolokasi publik
- Reverse DNS lookup

### 🌐 Domain Lookup
- WHOIS domain
- DNS records (A, AAAA, MX, NS, TXT, SOA, CNAME)
- Subdomain enumeration (opsional, gunakan sumber publik)
- IP address resolution

### 🛡️ Threat Intelligence
- Query ke sumber TI publik (VirusTotal, AbuseIPDB)
- Reputasi domain/IP
- Deteksi malicious activity
- Abuse confidence scoring

### 🔓 Data Breach Check
- Cek kebocoran data berbasis domain menggunakan HaveIBeenPwned
- **Hanya untuk domain-level checks**
- Tidak untuk pengecekan massal tanpa izin

### 📦 Track Expedisi
- Pelacakan nomor resi kurir/ekspedisi
- Support untuk kurir Indonesia (JNE, J&T, SiCepat, dll)
- Menggunakan API resmi kurir

### 📮 Info Kode Pos
- Lookup kode pos berdasarkan area
- Lookup area berdasarkan kode pos
- Data kantor pos

### 👤 Check Username
- Pengecekan ketersediaan username di layanan publik
- Multi-platform checking (GitHub, Twitter, Instagram, dll)
- **Hanya untuk akun publik**

### 📊 Threat Report
- Kompilasi ringkas hasil lookup
- Export ke format teks
- Report management dengan ID unik

### 🔒 Management & Security
- Autentikasi admin
- Rate limiting per user
- Logging aktivitas dengan audit trail
- Whitelist mechanism untuk corporate use

### 🛡️ **NEW: Sensitive Data Protection**
- **Deteksi otomatis** untuk data sensitif (NIK/KTP, data bank, NPWP)
- **Auto-blocking** query yang mencoba mengakses data terlarang
- **Audit logging** untuk violation attempts
- **Ethics education** dengan command `/ethics`
- Pattern recognition untuk rekam kriminal, credentials, biometric data
- Compliance dengan UU PDP, UU ITE, dan GDPR
- [Dokumentasi lengkap](SENSITIVE_DATA_PROTECTION.md)

## 🚀 Instalasi

### Prerequisites
- Python 3.11 atau lebih tinggi
- Bot Token dari [@BotFather](https://t.me/botfather)
- (Opsional) API Keys untuk threat intelligence services

### Setup

1. **Clone repository**
```bash
git clone https://github.com/sobri3195/pegasus-osint-bot-telegram.git
cd pegasus-osint-bot-telegram
```

2. **Buat virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Konfigurasi environment variables**
```bash
cp .env.example .env
nano .env  # atau editor favorit Anda
```

Edit `.env` dengan konfigurasi Anda:
```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_IDS=123456789,987654321

# Optional API Keys
VIRUSTOTAL_API_KEY=your_virustotal_key
ABUSEIPDB_API_KEY=your_abuseipdb_key
HIBP_API_KEY=your_haveibeenpwned_key
```

5. **Jalankan bot**
```bash
python bot.py
```

### Docker Deployment (Opsional)

```bash
# Coming soon
docker-compose up -d
```

## 📚 Penggunaan

### Perintah Dasar

```
/start          - Info & peringatan penggunaan
/help           - Daftar perintah lengkap
/ethics         - Panduan etika & penggunaan legitimate
```

### Perintah Lookup

```
/ip 8.8.8.8                    - Lookup informasi IP
/domain google.com             - Lookup informasi domain
/threat example.com            - Cek threat intelligence
/breach example.com            - Cek data breach
/track JP1234567890            - Tracking paket
/postcode 12345                - Lookup kode pos
/usercheck johndoe             - Cek keberadaan username
```

### Perintah Admin

```
/admin          - Panel administrasi
/stats          - Statistik bot
/report RPT123  - Lihat report spesifik
/myreports      - Lihat daftar report Anda
/cleanup        - Bersihkan report lama
```

## 🔐 Keamanan & Kepatuhan

### Prinsip Keamanan

1. **Minimal Data Collection**: Bot hanya menyimpan metadata untuk audit (user ID, command, timestamp)
2. **No PII Storage**: Hasil lookup tidak disimpan secara permanen
3. **Encrypted API Keys**: Semua API keys harus disimpan dengan aman
4. **Rate Limiting**: Mencegah abuse dengan rate limiting per user
5. **Access Control**: Whitelist dan admin authorization

### Audit Trail

Semua aktivitas dicatat dalam audit log dengan format:
```
[timestamp] [STATUS] User: <user_id> | Command: <command> | Args: <args>
```

Log disimpan di `logs/audit.log` dengan rotasi otomatis.

### Legal Compliance

Bot ini mematuhi:
- ✅ GDPR principles (data minimization, purpose limitation)
- ✅ Indonesia UU ITE (tidak mengakses data pribadi tanpa izin)
- ✅ Terms of Service dari API providers (VirusTotal, AbuseIPDB, HIBP)

## 🛠️ Konfigurasi Lanjutan

### Rate Limiting

Edit di `.env`:
```env
RATE_LIMIT_REQUESTS=10    # Maksimal request per periode
RATE_LIMIT_PERIOD=60      # Periode dalam detik
```

### Whitelist Mode

Untuk penggunaan corporate/restricted:
```env
REQUIRE_WHITELIST=true
WHITELIST_USERS=123456789,987654321
```

### Logging Level

```env
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## 🧪 Testing

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run specific test
pytest tests/test_ip.py -v

# Coverage report
pytest --cov=modules tests/
```

## 📝 Kontribusi

Kontribusi sangat diterima! Namun pastikan:

1. ✅ PR mematuhi kebijakan privasi & etika
2. ✅ Sertakan tests untuk fitur baru
3. ✅ Update dokumentasi
4. ✅ Code mengikuti style guide (PEP 8)
5. ✅ Tidak menambahkan fitur yang mengakses PII sensitif

Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk detail lengkap.

## 🐛 Bug Reports & Security

- **Bug reports**: Buka issue di GitHub dengan label `bug`
- **Security vulnerabilities**: Jangan buka public issue! Lihat [SECURITY.md](SECURITY.md)

## 📄 License

MIT License - lihat [LICENSE](LICENSE) file untuk detail.

**Note**: License MIT memberikan kebebasan penggunaan, namun pengguna tetap bertanggung jawab untuk mematuhi hukum dan etika yang berlaku.

## 🙏 Acknowledgments

- [aiogram](https://github.com/aiogram/aiogram) - Modern Telegram Bot framework
- [VirusTotal](https://www.virustotal.com/) - Threat intelligence platform
- [AbuseIPDB](https://www.abuseipdb.com/) - IP abuse database
- [HaveIBeenPwned](https://haveibeenpwned.com/) - Breach notification service

## 📞 Support

- 📧 Email: [muhammadsobrimaulana31@gmail.com](mailto:muhammadsobrimaulana31@gmail.com)
- 💬 Telegram: [@winlin_exploit](https://t.me/winlin_exploit)
- 💬 Grup WhatsApp: [Join Group](https://chat.whatsapp.com/B8nwRZOBMo64GjTwdXV8Bl)
- 📖 Documentation: [Wiki](https://github.com/sobri3195/pegasus-osint-bot-telegram/wiki)

## ⚖️ Disclaimer

Bot ini dirancang untuk penggunaan LEGITIMATE seperti security research, incident response, dan auditing dengan izin eksplisit. Penyalahgunaan untuk aktivitas ilegal adalah tanggung jawab pengguna. Developer tidak bertanggung jawab atas misuse atau pelanggaran hukum yang dilakukan menggunakan tool ini.

---

**Dibuat dengan ❤️ untuk komunitas security & OSINT Indonesia**
