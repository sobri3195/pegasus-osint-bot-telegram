# 🚀 Quick Start Guide

Get Pegasus OSINT Bot up and running in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- A Telegram account
- (Optional) API keys for threat intelligence services

## Step 1: Get a Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the prompts to create your bot
4. Copy the bot token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Step 2: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/pegasus-osint-bot-telegram.git
cd pegasus-osint-bot-telegram

# Run setup script
chmod +x setup.sh
./setup.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

## Step 3: Configure

Edit `.env` file:

```env
# Required
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_IDS=your_telegram_user_id

# Optional (for enhanced features)
VIRUSTOTAL_API_KEY=your_vt_api_key
ABUSEIPDB_API_KEY=your_abuseipdb_key
HIBP_API_KEY=your_hibp_api_key
```

**How to get your Telegram User ID:**
- Message [@userinfobot](https://t.me/userinfobot)
- It will reply with your user ID

## Step 4: Run the Bot

```bash
# Activate virtual environment (if not already)
source venv/bin/activate

# Run the bot
python bot.py
```

You should see:
```
INFO - Starting Pegasus OSINT Bot...
INFO - Admin IDs: [123456789]
```

## Step 5: Test the Bot

1. Open Telegram
2. Search for your bot (the name you gave to BotFather)
3. Send `/start` command
4. Try some commands:

```
/help
/ip 8.8.8.8
/domain google.com
```

## 🐳 Using Docker (Alternative)

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop
docker-compose down
```

## 🔑 Getting API Keys (Optional)

### VirusTotal
1. Sign up at [virustotal.com](https://www.virustotal.com/)
2. Go to your profile → API Key
3. Copy the key to `.env`

### AbuseIPDB
1. Sign up at [abuseipdb.com](https://www.abuseipdb.com/)
2. Go to Account → API Key
3. Copy the key to `.env`

### HaveIBeenPwned
1. Purchase API key at [haveibeenpwned.com/API/Key](https://haveibeenpwned.com/API/Key)
2. Add to `.env`

## 🧪 Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=modules --cov-report=html

# Run specific test
pytest tests/test_ip.py -v
```

## 🛠️ Troubleshooting

### Bot doesn't respond
- Check if bot is running (`python bot.py`)
- Verify BOT_TOKEN in `.env` is correct
- Check logs in `logs/bot.log`

### Rate limit errors
- Adjust `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_PERIOD` in `.env`
- Admin users bypass rate limits

### Module import errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

### API errors
- Verify API keys are correct in `.env`
- Check if you've exceeded API quotas
- Some features work without API keys (basic lookups)

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute
- Review [SECURITY.md](SECURITY.md) for security best practices
- Join our Telegram group for support: [@pegasus_osint_support](https://t.me/pegasus_osint_support)

## ⚠️ Important Reminders

- **Never commit your `.env` file** - it contains sensitive credentials
- **Use bot responsibly** - respect privacy and legal boundaries
- **Get permission** before testing on production systems
- **Keep dependencies updated** - run `pip install --upgrade -r requirements.txt` regularly

## 🎉 You're Ready!

Your bot is now running and ready to help with OSINT tasks. Start exploring the features and stay ethical! 🦅
