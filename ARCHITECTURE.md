# 🏗️ Architecture Overview

This document provides a technical overview of Pegasus OSINT Bot's architecture.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Telegram API                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Bot Layer (bot.py)                        │
│  - Command handlers                                          │
│  - Message routing                                           │
│  - User interaction                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Utils      │  │   Modules    │  │  External    │
│              │  │              │  │   APIs       │
│ - Auth       │  │ - IP Lookup  │  │              │
│ - Rate Limit │  │ - Domain     │  │ - VirusTotal │
│ - Logging    │  │ - Threat     │  │ - AbuseIPDB  │
│ - Config     │  │ - Breach     │  │ - HIBP       │
└──────────────┘  │ - Track      │  │ - IP-API     │
                  │ - Postcode   │  │ - Kodepos    │
                  │ - Usercheck  │  │ - Courier    │
                  │ - Report     │  │   APIs       │
                  └──────────────┘  └──────────────┘
```

## Directory Structure

```
pegasus-osint-bot-telegram/
├── bot.py                      # Main entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── pytest.ini                 # Test configuration
├── setup.sh                   # Setup script
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Docker orchestration
│
├── modules/                   # Feature modules
│   ├── __init__.py
│   ├── ip.py                 # IP lookup functionality
│   ├── domain.py             # Domain lookup functionality
│   ├── threat.py             # Threat intelligence
│   ├── breach.py             # Data breach checking
│   ├── track.py              # Package tracking
│   ├── postcode.py           # Postal code lookup
│   ├── usercheck.py          # Username checking
│   └── report.py             # Report management
│
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── config.py             # Configuration management
│   ├── logging.py            # Audit logging
│   ├── auth.py               # Authentication & authorization
│   └── rate_limiting.py      # Rate limiting
│
├── tests/                     # Unit tests
│   ├── __init__.py
│   ├── test_ip.py
│   └── test_domain.py
│
├── logs/                      # Log files (auto-created)
│   ├── bot.log
│   └── audit.log
│
└── docs/                      # Documentation
    ├── README.md
    ├── QUICKSTART.md
    ├── CONTRIBUTING.md
    ├── SECURITY.md
    ├── ARCHITECTURE.md
    └── CHANGELOG.md
```

## Component Breakdown

### Bot Layer (`bot.py`)

**Responsibilities:**
- Initialize aiogram Bot and Dispatcher
- Register command handlers
- Handle user messages
- Coordinate between modules

**Key Components:**
- Command handlers (async functions)
- Rate limit checking
- Response formatting
- Error handling

### Modules

#### IP Module (`modules/ip.py`)
- IP address validation using `ipaddress` library
- Geolocation lookup via ip-api.com
- Reverse DNS resolution
- WHOIS information retrieval

#### Domain Module (`modules/domain.py`)
- Domain name validation
- DNS record queries (A, AAAA, MX, NS, TXT, SOA, CNAME)
- Domain resolution
- WHOIS data retrieval

#### Threat Intelligence Module (`modules/threat.py`)
- Integration with VirusTotal API
- Integration with AbuseIPDB API
- Reputation scoring
- Malicious activity detection

#### Breach Module (`modules/breach.py`)
- Integration with HaveIBeenPwned API
- Domain-level breach checking
- Breach data formatting
- Secure API key handling

#### Track Module (`modules/track.py`)
- Courier detection (JNE, J&T, SiCepat, etc.)
- Package tracking via courier APIs
- Status parsing and formatting

#### Postcode Module (`modules/postcode.py`)
- Postal code lookup
- Area search
- Integration with Indonesian postal API

#### Usercheck Module (`modules/usercheck.py`)
- Multi-platform username checking
- Async concurrent requests
- Platform availability detection

#### Report Module (`modules/report.py`)
- Report generation with unique IDs
- Report storage (in-memory)
- Report retrieval and management
- Auto-cleanup of old reports

### Utils

#### Config (`utils/config.py`)
- Environment variable loading using `pydantic-settings`
- Configuration validation
- Settings singleton

#### Logging (`utils/logging.py`)
- Audit trail logging
- Structured log format
- Log rotation
- Metadata-only logging (no PII)

#### Auth (`utils/auth.py`)
- Admin authentication
- Whitelist checking
- Decorator-based authorization
- User ID validation

#### Rate Limiting (`utils/rate_limiting.py`)
- Per-user rate limiting
- Configurable limits
- Admin exemption
- In-memory tracking

## Data Flow

### Example: `/ip 8.8.8.8` Command

```
1. User sends message to bot
   ↓
2. Telegram sends update to bot
   ↓
3. bot.py receives message
   ↓
4. Check rate limit (rate_limiting.py)
   ↓
5. Parse command and arguments
   ↓
6. Call ip.get_ip_info("8.8.8.8")
   ↓
7. Validate IP address
   ↓
8. Query multiple sources:
   - Reverse DNS (socket)
   - Geolocation (ip-api.com)
   - WHOIS (ipinfo.io)
   ↓
9. Aggregate results
   ↓
10. Format output (ip.format_ip_result)
   ↓
11. Create report (report_manager.create_report)
   ↓
12. Send response to user
   ↓
13. Log to audit trail (audit_logger.log_command)
```

## Security Architecture

### Authentication Flow

```
User Message
    ↓
Rate Limit Check
    ↓ (if admin)
Bypass Rate Limit
    ↓
Command Authorization Check
    ↓ (if restricted command)
Check Admin Status
    ↓ (if whitelist required)
Check Whitelist
    ↓
Execute Command
    ↓
Audit Log
```

### API Key Management

```
.env file (not in git)
    ↓
pydantic Settings
    ↓
Environment Variables
    ↓
Settings Singleton
    ↓
Modules (read-only)
```

### Logging Strategy

**What We Log:**
- User ID (numeric)
- Command executed
- Timestamp
- Success/failure status
- Error messages (sanitized)

**What We DON'T Log:**
- Command arguments (may contain sensitive data)
- API responses
- User PII
- Chat content

## Technology Stack

### Core
- **Python 3.11+**: Programming language
- **aiogram 3.x**: Telegram Bot framework
- **aiohttp**: Async HTTP client
- **pydantic**: Data validation
- **pydantic-settings**: Configuration management

### DNS & Network
- **dnspython**: DNS queries
- **socket**: Reverse DNS
- **ipaddress**: IP validation

### Testing
- **pytest**: Test framework
- **pytest-asyncio**: Async test support
- **pytest-mock**: Mocking utilities

### Infrastructure
- **Docker**: Containerization
- **Redis** (optional): Distributed rate limiting
- **systemd** (optional): Service management

## API Integrations

### Free APIs
- **ip-api.com**: IP geolocation (no key required)
- **kodepos.vercel.app**: Indonesian postal codes (no key required)

### Paid/Limited APIs
- **VirusTotal**: Threat intelligence (free tier: 4 req/min)
- **AbuseIPDB**: IP abuse database (free tier: 1000 req/day)
- **HaveIBeenPwned**: Breach database (paid API)
- **Courier APIs**: Package tracking (requires API keys)

## Performance Considerations

### Async Operations
- All external API calls are async
- Concurrent username checking
- Non-blocking DNS queries

### Rate Limiting
- In-memory tracking (fast)
- Per-user limits
- Configurable thresholds

### Memory Management
- Reports auto-cleanup after 24h
- No persistent storage of results
- Minimal in-memory caching

## Scalability

### Horizontal Scaling
To scale horizontally:
1. Use Redis for shared rate limiting
2. Use database for report storage
3. Deploy multiple bot instances
4. Use webhook mode instead of long polling

### Vertical Scaling
- Increase rate limits
- Add more API keys (VirusTotal allows multiple keys)
- Optimize async operations

## Deployment Options

### Option 1: Direct Python
```bash
python bot.py
```

### Option 2: systemd Service
```ini
[Unit]
Description=Pegasus OSINT Bot
After=network.target

[Service]
Type=simple
User=pegasus
WorkingDirectory=/opt/pegasus-osint-bot
ExecStart=/opt/pegasus-osint-bot/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Option 3: Docker
```bash
docker-compose up -d
```

### Option 4: Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pegasus-osint-bot
spec:
  replicas: 3
  ...
```

## Monitoring & Observability

### Logs
- Application logs: `logs/bot.log`
- Audit logs: `logs/audit.log`
- Container logs: `docker logs pegasus-osint-bot`

### Metrics (Future)
- Commands per minute
- Response times
- Error rates
- API quota usage

### Health Checks
- Bot polling status
- API connectivity
- Rate limit usage

## Future Enhancements

### Planned Features
- [ ] Web dashboard for admins
- [ ] PostgreSQL integration for persistent storage
- [ ] Redis for distributed rate limiting
- [ ] Webhook mode support
- [ ] SSL certificate checking
- [ ] Subdomain enumeration
- [ ] Export to PDF/CSV
- [ ] Multi-language support
- [ ] Scheduled scans
- [ ] Alert notifications

### Infrastructure
- [ ] Kubernetes deployment
- [ ] Prometheus metrics
- [ ] Grafana dashboards
- [ ] ELK stack integration
- [ ] CI/CD pipeline

## Contributing to Architecture

When adding new features:
1. Follow the module pattern
2. Keep modules independent
3. Use async/await for I/O
4. Add proper error handling
5. Write tests
6. Update this document

## Questions?

For architectural questions or proposals:
- Open a GitHub Issue with `[Architecture]` tag
- Join our Telegram dev group: [@pegasus_osint_dev](https://t.me/pegasus_osint_dev)
- Email: dev@example.com

---

**Last Updated**: 2024-01-01
