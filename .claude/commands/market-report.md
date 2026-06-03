You are a sharp, data-driven market analyst. Run the full daily market report routine right now.

## Step 1 — Market Overview
Use WebSearch to find current data for:
- S&P 500, NASDAQ, DOW, VIX (price + % change today)
- Overall market sentiment (risk-on or risk-off, and why)
- Top 3 sector movers today
- Any macro news driving the market (Fed, earnings, geopolitics)

Write a concise 4-5 sentence market overview.

## Step 2 — Stocks to Watch Today
Use WebSearch to find 3-5 stocks that are notable today (high volume, big movers, catalyst events, earnings, etc). For each give: symbol, why it's notable, and a one-line trade setup.

## Step 3 — Watchlist Deep Dive: MU and SNDK
For each stock, use WebSearch to find:
- Current price and % change today
- Latest 3-5 news headlines (with source names)
- Recent analyst ratings or price target changes
- Any catalysts: earnings, product launches, macro tailwinds/headwinds

Then write a structured analysis for each:

**VERDICT:** BUY / SELL / HOLD  
**CONFIDENCE:** High / Medium / Low  

**BULL CASE** (3 bullets — concrete reasons to buy)  
**BEAR CASE** (3 bullets — concrete reasons to avoid)  

**Price Target:** your 3-6 month target  
**Key Risk:** single biggest risk in one sentence  

Be balanced. Show both sides even if your verdict leans one way.

## Step 4 — Deliver the Report
Once your analysis is complete, run this Python script to send it via email and Telegram.
Pass the full report as the REPORT variable.

Run the following Python code (use the Bash tool):

```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else '.')

REPORT = """<PASTE YOUR FULL PLAIN TEXT REPORT HERE>"""

HTML = """<PASTE YOUR FULL HTML REPORT HERE — wrap each section in basic divs, bullet the cases>"""

from notifiers.email_notifier import send_email
from notifiers.telegram_notifier import send_telegram
from datetime import datetime

date = datetime.utcnow().strftime("%Y-%m-%d")
send_email(f"Daily Market Report — {date}", REPORT, HTML)
send_telegram(REPORT[:4000])
```

Actually, write the report to a temp file and run it like this via Bash:

```bash
python -c "
import sys, os
sys.path.insert(0, '.')
from notifiers.email_notifier import send_email
from notifiers.telegram_notifier import send_telegram
from datetime import datetime
import pathlib

report = pathlib.Path('/tmp/market_report.txt').read_text()
html = pathlib.Path('/tmp/market_report.html').read_text()
date = datetime.utcnow().strftime('%Y-%m-%d')
send_email(f'Daily Market Report — {date}', report, html)
send_telegram(report[:4000])
print('Delivered.')
"
```

Before running the delivery step, write your complete plain-text report to `/tmp/market_report.txt` and a styled HTML version to `/tmp/market_report.html` using the Write tool.

## Output
After delivery, print a one-line confirmation:
`Report delivered — [date] — MU: [verdict] | SNDK: [verdict]`
