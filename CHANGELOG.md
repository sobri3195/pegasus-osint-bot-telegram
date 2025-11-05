# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-01

### Added
- Initial release of Pegasus OSINT Bot
- IP lookup functionality (WHOIS, geolocation, ASN)
- Domain lookup functionality (WHOIS, DNS records)
- Threat intelligence integration (VirusTotal, AbuseIPDB)
- Data breach checking (HaveIBeenPwned integration)
- Package tracking for Indonesian couriers
- Postal code lookup
- Username availability checking across platforms
- Report management system with unique IDs
- Admin authentication and authorization
- Rate limiting per user
- Audit logging system
- Whitelist mode for restricted access
- Comprehensive documentation (README, CONTRIBUTING, SECURITY)
- Unit tests for core modules
- Docker support
- Setup script for easy installation

### Security
- No PII collection or storage
- API keys loaded from environment variables
- Rate limiting to prevent abuse
- Audit trail for all commands
- Admin-only commands with proper authorization

## [Unreleased]

### Planned Features
- Subdomain enumeration
- SSL/TLS certificate checking
- Email reputation checking
- More courier integrations
- Export reports to PDF
- Telegram webhook mode
- Redis integration for distributed rate limiting
- Web dashboard for admins
- Multi-language support

---

For detailed release notes, see [GitHub Releases](https://github.com/yourusername/pegasus-osint-bot-telegram/releases).
