"""
Run once: fetch data, analyze with Ollama, send email + Telegram.
Called by the scheduler or directly: python runner.py
"""
import sys
from datetime import datetime

from config import WATCHLIST
from market_overview import get_market_overview
from news_fetcher import fetch_all_watchlist_data
from ai_analyst import analyze_market_sentiment, analyze_stock
from report_builder import build_text_report, build_html_report
from notifiers.email_notifier import send_email
from notifiers.telegram_notifier import send_telegram, format_for_telegram


def run():
    print(f"\n[{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}] Starting daily report...")

    print("  Fetching market overview...")
    overview = get_market_overview()

    print("  Fetching watchlist data...")
    watchlist_data = fetch_all_watchlist_data(WATCHLIST)

    print("  Running AI analysis (Ollama)...")
    market_sentiment = analyze_market_sentiment(overview)

    analyses = []
    for sym in WATCHLIST:
        print(f"  Analyzing {sym}...")
        fund = watchlist_data[sym]["fundamentals"]
        news = watchlist_data[sym]["news"]
        analyses.append(analyze_stock(sym, fund, news))

    print("  Building report...")
    text_report = build_text_report(overview, market_sentiment, watchlist_data, analyses)
    html_report = build_html_report(overview, market_sentiment, watchlist_data, analyses)
    telegram_msg = format_for_telegram(overview, market_sentiment, analyses)

    date = overview.get("date", datetime.utcnow().strftime("%Y-%m-%d"))
    subject = f"Daily Market Report — {date}"

    print("  Sending email...")
    send_email(subject, text_report, html_report)

    print("  Sending Telegram message...")
    send_telegram(telegram_msg)

    print("  Done.\n")
    return text_report


if __name__ == "__main__":
    report = run()
    if "--print" in sys.argv:
        print(report)
