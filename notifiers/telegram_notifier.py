import requests
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

TELEGRAM_MAX_LENGTH = 4096


def _send_chunk(text: str) -> bool:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        return True
    except Exception as e:
        print(f"[Telegram] Chunk send failed: {e}")
        return False


def send_telegram(text: str) -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[Telegram] Skipped: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set.")
        return False

    # Split into chunks if message exceeds Telegram's limit
    chunks = [text[i:i + TELEGRAM_MAX_LENGTH] for i in range(0, len(text), TELEGRAM_MAX_LENGTH)]
    success = True
    for chunk in chunks:
        if not _send_chunk(chunk):
            success = False
    if success:
        print(f"[Telegram] Sent {len(chunks)} message(s) to chat {TELEGRAM_CHAT_ID}")
    return success


def format_for_telegram(overview: dict, market_sentiment: str, analyses: list[dict]) -> str:
    date = overview.get("date", "")
    lines = [f"<b>Daily Market Report — {date}</b>\n"]

    # Indices
    lines.append("<b>Indices</b>")
    for name, data in overview.get("indices", {}).items():
        if "error" not in data:
            arrow = "🟢" if data["pct_change"] >= 0 else "🔴"
            lines.append(f"{arrow} {name}: ${data['price']:,}  ({'+' if data['pct_change'] >= 0 else ''}{data['pct_change']}%)")

    lines.append("")
    lines.append(f"<b>Overview</b>\n{market_sentiment}\n")

    # Top movers brief
    gainers = overview.get("top_gainers", [])
    losers = overview.get("top_losers", [])
    if gainers:
        lines.append("📈 <b>Gainers:</b> " + "  ".join(f"{g['symbol']} +{g['pct_change']}%" for g in gainers[:3]))
    if losers:
        lines.append("📉 <b>Losers:</b>  " + "  ".join(f"{l['symbol']} {l['pct_change']}%" for l in losers[:3]))

    lines.append("\n<b>─── Watchlist ───</b>")

    for entry in analyses:
        sym = entry["symbol"]
        price = f"${entry['price']:,}" if entry.get("price") else "N/A"
        pct = entry.get("pct_change_today")
        pct_str = f"({'+' if pct and pct >= 0 else ''}{pct}%)" if pct else ""
        arrow = "🟢" if pct and pct >= 0 else "🔴"

        lines.append(f"\n{arrow} <b>{sym}</b>  {price}  {pct_str}")

        # Extract verdict line from analysis
        analysis = entry.get("analysis", "")
        for line in analysis.split("\n"):
            if line.startswith("VERDICT:"):
                lines.append(f"  <b>{line}</b>")
            elif line.startswith("CONFIDENCE:") or line.startswith("PRICE TARGET:") or line.startswith("KEY RISK:"):
                lines.append(f"  {line}")
            elif line.startswith("BULL CASE") or line.startswith("BEAR CASE"):
                lines.append(f"\n  <b>{line}</b>")
            elif line.strip().startswith("•"):
                lines.append(f"  {line.strip()}")

    lines.append(f"\n<i>Not financial advice · {date}</i>")
    return "\n".join(lines)
