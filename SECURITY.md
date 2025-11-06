# 🔒 Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## 🛡️ Security Principles

Pegasus OSINT Bot dibangun dengan prinsip security-first:

1. **Privacy by Design**: Tidak mengumpulkan atau menyimpan PII
2. **Minimal Data Collection**: Hanya metadata untuk audit
3. **Secure by Default**: Rate limiting & access control built-in
4. **Transparency**: Open source untuk audit
5. **Legal Compliance**: Mematuhi GDPR, UU ITE, dan ToS providers

## 🚨 Reporting a Vulnerability

**PENTING**: Jangan melaporkan vulnerability sebagai public issue!

### Cara Melaporkan

Jika Anda menemukan security vulnerability:

1. **Email**: security@example.com
2. **Subject**: `[SECURITY] Brief description`
3. **Include**:
   - Deskripsi lengkap vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (jika ada)
   - Your contact info

### Response Timeline

- **24 hours**: Acknowledgment of report
- **72 hours**: Initial assessment & severity classification
- **7 days**: Detailed response & fix timeline (untuk critical issues)
- **30 days**: Fix deployed & advisory published (setelah koordinasi dengan reporter)

### Severity Classification

#### 🔴 Critical
- Remote code execution
- Authentication bypass
- Exposure of API keys atau credentials
- Mass data exfiltration

**Response**: Immediate fix & emergency patch release

#### 🟠 High
- Privilege escalation
- SQL injection atau command injection
- Rate limiting bypass
- Unauthorized access to reports

**Response**: Fix dalam 7 hari

#### 🟡 Medium
- XSS atau injection attacks (limited scope)
- Information disclosure (non-sensitive)
- DoS vulnerabilities

**Response**: Fix dalam 14 hari

#### 🟢 Low
- Minor information leaks
- Non-exploitable bugs
- Configuration issues

**Response**: Fix dalam 30 hari atau next release

## 🏆 Bug Bounty

Saat ini kami tidak memiliki formal bug bounty program, namun:

- ✅ Recognition di SECURITY.md & release notes
- ✅ Swag (stickers, t-shirt) untuk critical findings
- ✅ Special contributor badge

**Note**: Vulnerability disclosure harus koordinated (tidak public disclosure tanpa izin).

## 🚫 Data Sensitif yang Dilarang

Bot ini **TIDAK BOLEH** digunakan untuk mengakses, mencari, atau mengumpulkan:

- ❌ Data pribadi sensitif (NIK/KTP, data bank, NPWP)
- ❌ Rekam kriminal atau data penegak hukum
- ❌ Akun email target atau password
- ❌ Face recognition atau identifikasi biometrik
- ❌ Data internal yang dilindungi atau proprietary

Setiap fitur atau vulnerability yang berkaitan dengan akses ke data-data di atas harus segera dilaporkan sebagai **Critical Security Issue**.

## ⚠️ Out of Scope

Issues berikut **tidak dianggap** security vulnerabilities:

- ❌ Social engineering attacks (phishing, dll)
- ❌ Brute force attacks (sudah ada rate limiting)
- ❌ Issues yang require physical access ke server
- ❌ DoS attacks yang require significant resources
- ❌ Issues di third-party dependencies (report ke upstream)
- ❌ Best practice recommendations tanpa exploitable impact

## 🔐 Security Features

### Authentication & Authorization

- ✅ Admin authentication via Telegram user ID
- ✅ Whitelist mode untuk restricted access
- ✅ Command-level ACL

### Rate Limiting

- ✅ Per-user rate limiting (default: 10 req/min)
- ✅ Automatic cooldown period
- ✅ Admin exemption

### Data Protection

- ✅ No PII storage
- ✅ Minimal logging (metadata only)
- ✅ API keys dari environment variables
- ✅ No plaintext credentials in code/logs

### Input Validation

- ✅ IP address validation
- ✅ Domain name validation
- ✅ Username sanitization
- ✅ SQL injection prevention (no DB queries exposed)

### Audit Trail

- ✅ Complete audit logging
- ✅ Log rotation & retention policy
- ✅ Tamper-evident logging

## 🔧 Security Best Practices for Deployment

### Environment Variables

```bash
# NEVER commit .env to git
echo ".env" >> .gitignore

# Use strong bot token
BOT_TOKEN=your_secure_random_token

# Restrict admin access
ADMIN_IDS=your_user_id_only

# Use API keys from official sources
VIRUSTOTAL_API_KEY=your_official_key
```

### File Permissions

```bash
# Restrict permissions
chmod 600 .env
chmod 600 logs/audit.log

# Run as non-root user
useradd -m -s /bin/bash pegasus
su - pegasus
```

### Network Security

```bash
# Use firewall
ufw enable
ufw allow 443/tcp  # For webhook mode
ufw deny 6379/tcp  # Redis (if used, restrict to localhost)

# Use HTTPS for webhooks
# Never use HTTP for production
```

### Updates

```bash
# Regularly update dependencies
pip install --upgrade -r requirements.txt

# Check for security advisories
pip-audit

# Subscribe to security mailing list
```

## 🕵️ Security Audit

### Self-Audit Checklist

- [ ] No hardcoded credentials
- [ ] Environment variables properly loaded
- [ ] Input validation on all user inputs
- [ ] Output sanitization (prevent XSS)
- [ ] Rate limiting active
- [ ] Audit logging enabled
- [ ] No sensitive data in logs
- [ ] API keys rotated regularly
- [ ] Dependencies up-to-date
- [ ] No known CVEs in dependencies

### External Audit

Kami welcome external security audits. Silakan contact security@example.com untuk:
- Penetration testing permission
- Security review collaboration
- Responsible disclosure coordination

## 📚 Security Resources

### For Developers

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [Telegram Bot Security](https://core.telegram.org/bots/api#security)

### For Users

- [How to Secure Your Telegram Account](https://telegram.org/faq#q-how-do-i-enable-2-step-verification)
- [API Key Security](https://www.virustotal.com/gui/user/apikey)

## 🚫 Abuse Reporting

Jika Anda menemukan instance bot ini yang disalahgunakan:

1. **Email**: abuse@example.com
2. **Include**:
   - Bot username/ID
   - Evidence of abuse (screenshots, logs)
   - Impact description

Kami akan:
- Investigate report dalam 48 jam
- Take appropriate action
- Notify relevant authorities if illegal activity detected

## 📜 Compliance

### GDPR Compliance

- ✅ Data minimization
- ✅ Purpose limitation
- ✅ No profiling
- ✅ Right to erasure (auto-cleanup after 24h)
- ✅ Transparent processing

### Indonesia UU ITE

- ✅ Tidak mengakses data pribadi tanpa izin
- ✅ Tidak menyimpan data sensitif
- ✅ Hanya menggunakan sumber publik
- ✅ Audit trail untuk accountability

## 🔄 Incident Response

### In Case of Security Incident

1. **Containment**: Immediately stop bot if compromise detected
2. **Assessment**: Evaluate scope & impact
3. **Notification**: Inform affected users within 72 hours
4. **Remediation**: Deploy fixes
5. **Post-Mortem**: Document & learn from incident

### Contact

- **Emergency**: security-emergency@example.com
- **General**: security@example.com
- **PGP Key**: Available on request

## 📅 Version History

### Security Patches

- **1.0.0** (2024-01-01): Initial release with security features
  - Rate limiting implemented
  - Audit logging enabled
  - Input validation added

## 🙏 Acknowledgments

Kami mengucapkan terima kasih kepada security researchers yang telah membantu mengamankan project ini:

- (Coming soon - your name here!)

---

**Security is everyone's responsibility. Thank you for helping keep Pegasus OSINT Bot secure! 🛡️**
