# 🛡️ Sensitive Data Protection

## Overview

Pegasus OSINT Bot memiliki sistem proteksi otomatis untuk mencegah akses ke data sensitif yang dilarang oleh kebijakan privasi dan hukum yang berlaku.

## Fitur Proteksi

### 1. Deteksi Otomatis

Bot akan secara otomatis mendeteksi dan memblokir query yang mengandung:

#### ❌ Data Pribadi Sensitif
- **NIK/KTP**: Nomor Induk Kependudukan (16 digit)
- **Data Bank**: Nomor rekening, kartu kredit (dengan Luhn validation)
- **NPWP**: Nomor Pokok Wajib Pajak

#### ❌ Data Kriminal & Penegak Hukum
- Rekam kriminal
- Data kepolisian
- Informasi tahanan/penjara
- Data internal law enforcement

#### ❌ Credentials & Authentication
- Password atau kata sandi
- Email credentials
- Login information
- Breach credentials

#### ❌ Data Biometrik
- Face recognition
- Fingerprint data
- Retina/iris scan
- Identifikasi biometrik lainnya

#### ❌ Data Proprietary & Internal
- Confidential company data
- Trade secrets
- Internal non-public data
- Protected information

### 2. Pattern Recognition

Sistem menggunakan multiple detection methods:

1. **Regex Pattern Matching**
   - NIK: `\b\d{16}\b`
   - NPWP: `\b\d{2}[.\s]?\d{3}[.\s]?\d{3}[.\s]?\d[-.\s]?\d{3}[.\s]?\d{3}\b`
   - Credit Card: Luhn algorithm validation

2. **Keyword Detection**
   - Case-insensitive matching
   - Multi-language support (Indonesian & English)
   - Context-aware filtering

3. **Heuristic Analysis**
   - Kombinasi pattern + keyword untuk akurasi tinggi
   - False positive reduction

### 3. Audit Logging

Setiap attempt untuk mengakses data sensitif dicatat:

```
[timestamp] [VIOLATION] User: <user_id> | Command: SENSITIVE_DATA_VIOLATION | Args: <partial_input>
```

Log mencakup:
- User ID (bukan username untuk privacy)
- Timestamp
- Command yang diblokir
- Tipe violation terdeteksi
- Tidak menyimpan input lengkap (privacy by design)

## Cara Kerja

### Flow Diagram

```
User Input
    ↓
Rate Limiting Check
    ↓
Sensitive Data Detection ←→ Pattern Matching
    ↓                         Keyword Detection
    ↓                         Heuristic Analysis
    ↓
[BLOCKED] ←---- Violation Detected
    ↓                 ↓
    ↓            Audit Log
    ↓                 ↓
    ↓            Warning Message
    ↓
[ALLOWED] ←---- Clean Input
    ↓
Command Processing
```

### Integration Points

Proteksi terintegrasi di semua command handlers:

```python
@dp.message(Command("ip"))
async def cmd_ip(message: Message):
    # Rate limiting
    if not await check_rate_limit(message):
        return
    
    # Sensitive data check
    if not await check_sensitive_data(message, ip_address):
        return  # Blocked & logged
    
    # Normal processing continues...
```

## User Experience

### Ketika Query Diblokir

User akan menerima pesan:

```
🚫 PELANGGARAN TERDETEKSI

Query Anda mengandung data sensitif yang dilarang:

• NIK/KTP (16 digit detected)
• Kata kunci data bank terdeteksi

Bot ini TIDAK DAPAT dan TIDAK AKAN mengakses:
❌ Data pribadi sensitif (NIK/KTP, data bank, NPWP)
❌ Rekam kriminal atau data penegak hukum
❌ Akun email target atau password
❌ Face recognition atau identifikasi biometrik
❌ Data internal yang dilindungi atau proprietary

PERINGATAN HUKUM:
Penggunaan bot untuk mengakses data sensitif tanpa izin melanggar:
• UU Perlindungan Data Pribadi (UU PDP)
• UU Informasi dan Transaksi Elektronik (UU ITE)
• Peraturan internasional (GDPR, dll)

Aktivitas ini telah dicatat dalam audit log.

Gunakan /ethics untuk memahami penggunaan yang legitimate.
```

### Command `/ethics`

User dapat mengakses panduan lengkap:

```
/ethics
```

Menampilkan:
- ✅ Penggunaan yang diperbolehkan
- ❌ Penggunaan yang dilarang
- 🎯 Prinsip yang harus diikuti
- 📖 Contoh kasus penggunaan
- 🔗 Resources tambahan

## Testing

### Unit Tests

```bash
pytest tests/test_sensitive_data.py -v
```

Coverage:
- Pattern detection untuk setiap kategori
- False positive testing
- Legitimate query handling
- Multiple violation detection
- Case sensitivity
- Warning message generation

### Manual Testing

Test cases yang harus dijalankan:

```python
# Should be BLOCKED
/ip NIK 1234567890123456
/domain rekening bank mandiri
/threat password email hack
/usercheck face recognition

# Should be ALLOWED
/ip 8.8.8.8
/domain google.com
/threat example.com
/usercheck johndoe
```

## Configuration

Tidak ada configuration diperlukan - proteksi aktif secara default.

Untuk development/testing, Anda dapat:

```python
# Temporary disable untuk testing (NOT for production!)
# Edit utils/sensitive_data.py
DEBUG_MODE = False  # Set to True to log only, not block
```

⚠️ **WARNING**: Jangan disable proteksi di production!

## Performance Impact

- **Overhead**: < 5ms per query
- **Regex compilation**: Cached (compiled once)
- **Async processing**: Non-blocking
- **Memory**: < 1MB for pattern storage

## Compliance

### Legal Framework

Proteksi ini membantu compliance dengan:

1. **Indonesia UU PDP (2022)**
   - Pasal 16: Larangan pengolahan data pribadi tanpa consent
   - Pasal 65: Sanksi pidana untuk pelanggaran

2. **UU ITE No. 19 Tahun 2016**
   - Pasal 30: Larangan akses ilegal ke sistem elektronik
   - Pasal 32: Larangan akses data pribadi tanpa izin

3. **GDPR (European Union)**
   - Article 5: Principles of processing personal data
   - Article 6: Lawfulness of processing
   - Article 9: Processing of special categories (biometric, etc.)

### Ethical Compliance

Mengikuti guidelines dari:
- OWASP Code of Conduct
- SANS Ethics Guidelines
- EC-Council Code of Ethics
- Indonesia Kode Etik Profesi TI

## False Positives

### Handling

Jika legitimate query terblokir:

1. **Review Pattern**: Apakah input mengandung keyword yang sensitif?
2. **Reformulate Query**: Gunakan terminology yang lebih specific
3. **Contact Admin**: Report false positive untuk improvement

### Known Cases

```python
# Might be flagged (false positive)
"Check if IP belongs to bank network"  # Contains "bank"

# Solution: Rephrase
"Check if IP belongs to financial institution network"
```

### Improvement

False positive reports dapat disubmit via:
- GitHub Issues (label: `enhancement`)
- Email: security@example.com

## Future Enhancements

### Planned Features

1. **Machine Learning Model**
   - NLP-based context understanding
   - Improved false positive reduction
   - Multi-language support enhancement

2. **Admin Override**
   - Temporary whitelist untuk testing
   - Audit trail untuk override actions
   - Approval workflow

3. **Custom Patterns**
   - Configurable via environment variables
   - Organization-specific rules
   - Industry compliance templates

4. **Reporting Dashboard**
   - Violation statistics
   - Trend analysis
   - User behavior insights

## Contributing

Untuk berkontribusi pada improvement proteksi:

1. Fork repository
2. Buat feature branch: `git checkout -b feat/improve-sensitive-detection`
3. Tambahkan tests untuk pattern baru
4. Submit PR dengan description lengkap
5. Include test results

### Guidelines

- Prioritaskan privacy user
- Minimize false positives
- Document setiap pattern dengan contoh
- Include unit tests (coverage > 90%)
- Update dokumentasi

## Support

### Issues

- **Bug Reports**: GitHub Issues (label: `bug`)
- **Security Concerns**: security@example.com (private)
- **False Positives**: GitHub Issues (label: `enhancement`)

### FAQ

**Q: Apakah proteksi bisa di-bypass?**
A: Tidak. Proteksi terintegrasi di level application logic, bukan client-side.

**Q: Bagaimana dengan query legitimate yang mengandung keyword sensitif?**
A: Reformulate query atau contact admin untuk review.

**Q: Apakah log violation menyimpan data sensitif?**
A: Tidak. Hanya metadata (user_id, timestamp, violation type) yang disimpan.

**Q: Apakah ini affect performance?**
A: Minimal (<5ms overhead), dan async sehingga non-blocking.

## Credits

Developed with security-first approach, following:
- OWASP Security Principles
- Privacy by Design Framework
- NIST Cybersecurity Framework
- Indonesia Cybersecurity Standards

---

**Remember**: Proteksi ini adalah safeguard, bukan invitation. Gunakan bot hanya untuk tujuan legitimate dan legal. 🛡️
