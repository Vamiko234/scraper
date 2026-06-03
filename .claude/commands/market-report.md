You are a sharp, balanced stock market analyst. Run the full daily market report right now by following these steps in order.

---

## STEP 1 — Market Snapshot

Use WebSearch to get today's data for:
- S&P 500, NASDAQ, DOW Jones, VIX — current price and % change
- Overall market tone: risk-on or risk-off, and the main reason why
- Any macro drivers today (Fed comments, CPI/jobs data, earnings season, geopolitical news)

---

## STEP 2 — Stocks to Watch Today

Use WebSearch to find 3-5 stocks worth watching today. Look for: unusual volume, big % movers, earnings releases, analyst upgrades/downgrades, product catalysts. For each give one line: symbol — why it's notable — trade setup (e.g. "breakout above $X", "selling into resistance at $Y").

---

## STEP 3 — Watchlist: MU (Micron Technology)

Use WebSearch to find:
- Current MU price and % change today
- Latest news headlines (at least 3, with source names)
- Any recent analyst ratings or price target changes
- Upcoming catalysts (earnings date, product launches, memory cycle trends)

Write this structured analysis:

**VERDICT:** BUY / SELL / HOLD
**CONFIDENCE:** High / Medium / Low

**BULL CASE**
• [reason 1]
• [reason 2]
• [reason 3]

**BEAR CASE**
• [reason 1]
• [reason 2]
• [reason 3]

**Price Target (3-6 months):** $X
**Key Risk:** [one sentence]

---

## STEP 4 — Watchlist: SNDK (SanDisk / Western Digital)

Repeat the same process as Step 3 for SNDK. Search for current price, news, analyst sentiment, catalysts, and write the full structured analysis.

---

## STEP 5 — Write the Reports

Using the Write tool, save two files:

**File 1: `/tmp/market_report.txt`**
Plain text version. Use this structure:

```
============================================================
  DAILY MARKET REPORT — [DATE]
============================================================

MARKET SNAPSHOT
------------------------------------------------------------
[indices table]

MARKET OVERVIEW
[4-5 sentence overview]

STOCKS TO WATCH TODAY
[bulleted list]

============================================================
WATCHLIST: MU
[price, verdict, bull/bear cases, target, risk, top news headlines]

------------------------------------------------------------
WATCHLIST: SNDK
[price, verdict, bull/bear cases, target, risk, top news headlines]

============================================================
Not financial advice · Generated [datetime UTC]
```

**File 2: `/tmp/market_report.html`**
Clean dark-themed HTML email. Use inline styles. Dark background (#13131f), white text, green (#2ecc71) for positive/bull, red (#e74c3c) for negative/bear, blue (#3498db) for headers. Include all sections. Max width 700px centered.

---

## STEP 6 — Deliver

Run this command with the Bash tool:

```bash
cd "$(dirname "$0")/../.." 2>/dev/null || cd . && python deliver.py
```

If that path fails, try:
```bash
python /home/user/scraper/deliver.py
```

---

## STEP 7 — Confirm

Print exactly one line:
`✓ Report delivered — [DATE] — MU: [VERDICT] | SNDK: [VERDICT]`
