"""
Reads the report from /tmp and sends via email + Telegram.
Called by the /market-report Claude routine after it writes the report files.
"""
import sys
import os
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from notifiers.email_notifier import send_email
from notifiers.telegram_notifier import send_telegram

TEXT_FILE = Path("/tmp/market_report.txt")
HTML_FILE = Path("/tmp/market_report.html")


def main():
    if not TEXT_FILE.exists():
        print(f"[deliver] ERROR: {TEXT_FILE} not found. Did the Claude routine write the report?")
        sys.exit(1)

    text = TEXT_FILE.read_text(encoding="utf-8")
    html = HTML_FILE.read_text(encoding="utf-8") if HTML_FILE.exists() else f"<pre>{text}</pre>"

    date = datetime.utcnow().strftime("%Y-%m-%d")
    subject = f"Daily Market Report — {date}"

    email_ok = send_email(subject, text, html)
    tg_ok = send_telegram(text[:4000])

    if email_ok or tg_ok:
        print("[deliver] Report sent successfully.")
    else:
        print("[deliver] WARNING: Both email and Telegram failed. Check your .env credentials.")
        sys.exit(1)


if __name__ == "__main__":
    main()
