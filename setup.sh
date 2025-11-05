#!/bin/bash

echo "🦅 Pegasus OSINT Bot - Setup Script"
echo "===================================="
echo ""

if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

echo "🔄 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your configuration!"
    echo "   Required: BOT_TOKEN, ADMIN_IDS"
    echo "   Optional: API keys for threat intelligence services"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your bot token and configuration"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the bot: python bot.py"
echo "4. Run tests: pytest tests/"
echo ""
