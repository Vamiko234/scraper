import os
from dotenv import load_dotenv

load_dotenv()

# Watchlist
WATCHLIST = ["MU", "SNDK"]

# Market indices to track
MARKET_INDICES = {
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "DOW": "^DJI",
    "Russell 2000": "^RUT",
    "VIX": "^VIX",
}

# Ollama settings
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Email settings
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "vamikhus@gmail.com")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# Telegram settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Schedule time (UTC)
REPORT_HOUR_UTC = int(os.getenv("REPORT_HOUR_UTC", "8"))
REPORT_MINUTE_UTC = int(os.getenv("REPORT_MINUTE_UTC", "0"))
