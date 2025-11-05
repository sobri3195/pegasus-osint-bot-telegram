# 🤝 Contributing to Pegasus OSINT Bot

Terima kasih atas minat Anda untuk berkontribusi! Kami sangat menghargai kontribusi dari komunitas.

## 📋 Code of Conduct

Dengan berpartisipasi dalam project ini, Anda setuju untuk menjunjung tinggi:

1. **Etika & Legalitas**: Tidak membuat fitur yang melanggar privasi atau hukum
2. **Respect**: Hormati kontributor lain dan maintainers
3. **Transparency**: Komunikasikan niat dan perubahan dengan jelas
4. **Responsibility**: Bertanggung jawab atas kode yang Anda kontribusikan

## 🚫 Apa yang TIDAK Boleh Dikontribusikan

**DILARANG KERAS** membuat PR yang:
- ❌ Menambahkan fitur untuk mengakses data pribadi sensitif (NIK, KTP, rekening bank, dll)
- ❌ Mengimplementasikan scraping atau crawling yang melanggar ToS
- ❌ Menambahkan fitur tracking/surveillance tanpa consent
- ❌ Bypass security measures atau rate limiting
- ❌ Mengeksploitasi vulnerability untuk tujuan jahat

**PR yang melanggar akan langsung ditolak dan direport.**

## ✅ Apa yang Kami Terima

Kontribusi yang diterima:
- ✅ Bug fixes
- ✅ Performance improvements
- ✅ Documentation improvements
- ✅ New legitimate OSINT features (dengan diskusi terlebih dahulu)
- ✅ Unit tests
- ✅ Security improvements
- ✅ UI/UX improvements

## 🔄 Contribution Workflow

### 1. Fork & Clone

```bash
# Fork repository via GitHub UI

# Clone fork Anda
git clone https://github.com/YOUR_USERNAME/pegasus-osint-bot-telegram.git
cd pegasus-osint-bot-telegram

# Add upstream remote
git remote add upstream https://github.com/original/pegasus-osint-bot-telegram.git
```

### 2. Create Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
# atau
git checkout -b fix/bug-description
```

Branch naming conventions:
- `feature/` - untuk fitur baru
- `fix/` - untuk bug fixes
- `docs/` - untuk dokumentasi
- `refactor/` - untuk refactoring
- `test/` - untuk menambah tests

### 3. Make Changes

```bash
# Make your changes
# ...

# Add tests untuk perubahan Anda
# ...

# Run tests
pytest tests/

# Check code style
flake8 .
black --check .
```

### 4. Commit

Gunakan commit message yang descriptive:

```bash
git add .
git commit -m "feat: add subdomain enumeration feature"

# atau
git commit -m "fix: resolve rate limiting bug in IP lookup"
```

Commit message format:
- `feat:` - fitur baru
- `fix:` - bug fix
- `docs:` - dokumentasi
- `test:` - menambah/update tests
- `refactor:` - refactoring code
- `perf:` - performance improvement
- `chore:` - maintenance tasks

### 5. Push & Create PR

```bash
# Push ke fork Anda
git push origin feature/your-feature-name
```

Kemudian buat Pull Request di GitHub dengan:
- Judul yang jelas dan descriptive
- Deskripsi lengkap tentang perubahan
- Screenshot/demo jika applicable
- Link ke related issues
- Checklist yang sudah dilengkapi

## 📝 Pull Request Template

```markdown
## Description
[Jelaskan perubahan yang Anda buat]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## How Has This Been Tested?
[Jelaskan testing yang sudah dilakukan]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review sudah dilakukan
- [ ] Comments ditambahkan untuk code yang complex
- [ ] Dokumentasi sudah diupdate
- [ ] No new warnings generated
- [ ] Tests ditambahkan/updated
- [ ] All tests passing
- [ ] No breaking changes (atau sudah didokumentasikan)
- [ ] Mematuhi kebijakan etika & privasi

## Security Considerations
[Jelaskan security implications dari perubahan ini]

## Screenshots (jika applicable)
[Tambahkan screenshots]
```

## 🧪 Testing Requirements

Semua PR harus include tests yang adequate:

```python
# Example test
import pytest
from modules.ip import get_ip_info

@pytest.mark.asyncio
async def test_get_ip_info_valid():
    result = await get_ip_info("8.8.8.8")
    assert "ip" in result
    assert result["ip"] == "8.8.8.8"
    assert "error" not in result

@pytest.mark.asyncio
async def test_get_ip_info_invalid():
    result = await get_ip_info("invalid_ip")
    assert "error" in result
```

Run tests:
```bash
pytest tests/ -v
pytest tests/ --cov=modules --cov-report=html
```

## 📐 Code Style Guidelines

### Python Style

Ikuti **PEP 8** dengan beberapa exceptions:
- Line length: 100 characters (bukan 79)
- Use type hints untuk fungsi public
- Use docstrings untuk modules dan fungsi complex

Format code dengan Black:
```bash
black modules/ bot.py
```

Lint dengan flake8:
```bash
flake8 modules/ bot.py
```

### Naming Conventions

```python
# Variables & functions: snake_case
user_id = 123
def get_ip_info():
    pass

# Classes: PascalCase
class ReportManager:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
API_TIMEOUT = 30
```

### Import Order

```python
# 1. Standard library
import asyncio
import logging
from typing import Dict, List

# 2. Third-party
from aiogram import Bot, Dispatcher
import aiohttp

# 3. Local
from utils.config import settings
from modules.ip import get_ip_info
```

## 🔒 Security Review Process

Setiap PR yang melibatkan:
- Authentication/authorization
- API key handling
- External API calls
- Data processing
- File operations

Akan melalui **security review** tambahan sebelum di-merge.

### Security Checklist

- [ ] No hardcoded credentials
- [ ] API keys diambil dari environment variables
- [ ] Input validation untuk semua user input
- [ ] Output sanitization untuk prevent injection
- [ ] No sensitive data logging
- [ ] Rate limiting implemented
- [ ] Error messages tidak expose sensitive info

## 📚 Documentation

Update dokumentasi jika PR Anda:
- Menambah fitur baru → Update README.md
- Mengubah API → Update docstrings
- Mengubah konfigurasi → Update .env.example
- Menambah dependency → Update requirements.txt

## 🐛 Bug Reports

Gunakan template berikut untuk bug reports:

```markdown
**Describe the bug**
[Clear description]

**To Reproduce**
Steps:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
[What should happen]

**Screenshots**
[If applicable]

**Environment:**
- OS: [e.g. Ubuntu 22.04]
- Python version: [e.g. 3.11.0]
- Bot version: [e.g. 1.0.0]

**Additional context**
[Any other relevant info]
```

## 💡 Feature Requests

Sebelum membuat feature request:
1. Check existing issues untuk avoid duplicates
2. Diskusikan di Discussions terlebih dahulu
3. Pastikan fitur mematuhi kebijakan etika

Template feature request:

```markdown
**Is your feature related to a problem?**
[Describe the problem]

**Describe the solution**
[Your proposed solution]

**Alternatives considered**
[Other solutions you've considered]

**Ethics & Privacy Considerations**
[Explain how this respects privacy and legal boundaries]

**Additional context**
[Any other context]
```

## 🏆 Recognition

Kontributor akan diakui di:
- README.md (Contributors section)
- Release notes
- GitHub contributors page

## 📞 Getting Help

Butuh bantuan?
- 💬 Join Telegram group: [@pegasus_osint_dev](https://t.me/pegasus_osint_dev)
- 📧 Email: dev@example.com
- 📖 Check [Wiki](https://github.com/yourusername/pegasus-osint-bot-telegram/wiki)

## 📜 License

Dengan berkontribusi, Anda setuju bahwa kontribusi Anda akan dilisensikan di bawah MIT License yang sama dengan project ini.

---

**Terima kasih telah berkontribusi! 🙏**
