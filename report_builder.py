from datetime import datetime


def _fmt_pct(val):
    if val is None:
        return "N/A"
    arrow = "▲" if val >= 0 else "▼"
    return f"{arrow}{abs(val):.2f}%"


def _fmt_price(val):
    if val is None:
        return "N/A"
    return f"${val:,.2f}"


def _fmt_mcap(val):
    if val is None:
        return "N/A"
    if val >= 1e12:
        return f"${val/1e12:.2f}T"
    if val >= 1e9:
        return f"${val/1e9:.2f}B"
    return f"${val/1e6:.2f}M"


def build_text_report(overview: dict, market_sentiment: str, watchlist_data: dict, analyses: list[dict]) -> str:
    date = overview.get("date", datetime.utcnow().strftime("%Y-%m-%d"))
    lines = []

    lines.append(f"{'='*60}")
    lines.append(f"  DAILY MARKET REPORT — {date}")
    lines.append(f"{'='*60}\n")

    # Market indices
    lines.append("MARKET INDICES")
    lines.append("-" * 40)
    for name, data in overview.get("indices", {}).items():
        if "error" not in data:
            lines.append(f"  {name:<18} {_fmt_price(data['price'])}  {_fmt_pct(data['pct_change'])}")
    lines.append("")

    # AI market overview
    lines.append("MARKET OVERVIEW (AI)")
    lines.append("-" * 40)
    lines.append(market_sentiment)
    lines.append("")

    # Top movers
    gainers = overview.get("top_gainers", [])
    losers = overview.get("top_losers", [])
    if gainers or losers:
        lines.append("TOP MOVERS")
        lines.append("-" * 40)
        if gainers:
            lines.append("  Gainers: " + "  |  ".join(f"{g['symbol']} {_fmt_pct(g['pct_change'])}" for g in gainers))
        if losers:
            lines.append("  Losers:  " + "  |  ".join(f"{l['symbol']} {_fmt_pct(l['pct_change'])}" for l in losers))
        lines.append("")

    # Watchlist analysis
    lines.append("WATCHLIST ANALYSIS")
    lines.append("=" * 60)
    for entry in analyses:
        sym = entry["symbol"]
        data = watchlist_data.get(sym, {})
        fund = data.get("fundamentals", {})
        news = data.get("news", [])

        lines.append(f"\n{sym} — {_fmt_price(entry['price'])}  {_fmt_pct(entry['pct_change_today'])}")
        lines.append(f"  52W Range: {_fmt_price(fund.get('52w_low'))} – {_fmt_price(fund.get('52w_high'))}")
        lines.append(f"  Mkt Cap: {_fmt_mcap(fund.get('market_cap'))}  |  P/E: {fund.get('pe_ratio', 'N/A')}  |  Beta: {fund.get('beta', 'N/A')}")
        lines.append(f"  Analyst Target: {_fmt_price(fund.get('analyst_target'))}  |  Recommendation: {(fund.get('recommendation') or 'N/A').upper()}")
        lines.append("")

        lines.append("  AI ANALYSIS:")
        for line in entry["analysis"].split("\n"):
            lines.append(f"  {line}")
        lines.append("")

        if news:
            lines.append("  RECENT NEWS:")
            for n in news[:4]:
                lines.append(f"  • {n['title']}")
                if n.get("url"):
                    lines.append(f"    {n['url']}")
        lines.append("-" * 60)

    lines.append(f"\nGenerated at {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    return "\n".join(lines)


def build_html_report(overview: dict, market_sentiment: str, watchlist_data: dict, analyses: list[dict]) -> str:
    date = overview.get("date", datetime.utcnow().strftime("%Y-%m-%d"))

    def pct_color(val):
        if val is None:
            return "#888"
        return "#2ecc71" if val >= 0 else "#e74c3c"

    indices_rows = ""
    for name, data in overview.get("indices", {}).items():
        if "error" not in data:
            color = pct_color(data["pct_change"])
            indices_rows += f"""
            <tr>
              <td>{name}</td>
              <td>{_fmt_price(data['price'])}</td>
              <td style="color:{color}; font-weight:bold">{_fmt_pct(data['pct_change'])}</td>
            </tr>"""

    gainers_html = "".join(
        f'<span style="color:#2ecc71; margin-right:12px">{g["symbol"]} {_fmt_pct(g["pct_change"])}</span>'
        for g in overview.get("top_gainers", [])
    )
    losers_html = "".join(
        f'<span style="color:#e74c3c; margin-right:12px">{l["symbol"]} {_fmt_pct(l["pct_change"])}</span>'
        for l in overview.get("top_losers", [])
    )

    watchlist_html = ""
    for entry in analyses:
        sym = entry["symbol"]
        data = watchlist_data.get(sym, {})
        fund = data.get("fundamentals", {})
        news = data.get("news", [])

        price_color = pct_color(entry.get("pct_change_today"))
        analysis_lines = entry["analysis"].replace("\n", "<br>")

        news_items = "".join(
            f'<li><a href="{n.get("url","#")}" style="color:#3498db">{n["title"]}</a> <small style="color:#888">({n.get("source","")})</small></li>'
            for n in news[:4]
        )

        watchlist_html += f"""
        <div style="background:#1e1e2e; border-radius:8px; padding:20px; margin-bottom:20px; border-left:4px solid #3498db">
          <h2 style="margin:0 0 8px 0; color:#fff">{sym}
            <span style="font-size:1rem; font-weight:normal; margin-left:12px">{_fmt_price(entry['price'])}</span>
            <span style="font-size:1rem; color:{price_color}; margin-left:8px">{_fmt_pct(entry.get('pct_change_today'))}</span>
          </h2>
          <table style="color:#ccc; font-size:0.85rem; margin-bottom:14px">
            <tr>
              <td style="padding-right:20px">52W: {_fmt_price(fund.get('52w_low'))} – {_fmt_price(fund.get('52w_high'))}</td>
              <td style="padding-right:20px">Mkt Cap: {_fmt_mcap(fund.get('market_cap'))}</td>
              <td style="padding-right:20px">P/E: {fund.get('pe_ratio','N/A')}</td>
              <td>Target: {_fmt_price(fund.get('analyst_target'))}</td>
            </tr>
          </table>
          <div style="background:#12121f; border-radius:6px; padding:14px; color:#ddd; font-size:0.9rem; line-height:1.7; margin-bottom:14px">
            {analysis_lines}
          </div>
          <div>
            <strong style="color:#aaa; font-size:0.8rem">RECENT NEWS</strong>
            <ul style="color:#ccc; margin:6px 0; padding-left:18px; font-size:0.85rem">{news_items}</ul>
          </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Market Report {date}</title>
</head>
<body style="margin:0; padding:0; background:#13131f; font-family: 'Segoe UI', Arial, sans-serif; color:#e0e0e0">
  <div style="max-width:700px; margin:0 auto; padding:24px">
    <h1 style="color:#fff; border-bottom:2px solid #3498db; padding-bottom:10px">
      Daily Market Report <span style="font-size:1rem; font-weight:normal; color:#888">{date}</span>
    </h1>

    <h2 style="color:#aaa; font-size:1rem; text-transform:uppercase; letter-spacing:1px">Market Indices</h2>
    <table style="width:100%; border-collapse:collapse; margin-bottom:20px">
      <thead>
        <tr style="color:#888; font-size:0.8rem; text-transform:uppercase">
          <th style="text-align:left; padding:6px">Index</th>
          <th style="text-align:right; padding:6px">Price</th>
          <th style="text-align:right; padding:6px">Change</th>
        </tr>
      </thead>
      <tbody style="font-size:0.95rem">{indices_rows}</tbody>
    </table>

    <h2 style="color:#aaa; font-size:1rem; text-transform:uppercase; letter-spacing:1px">Market Overview</h2>
    <div style="background:#1e1e2e; border-radius:8px; padding:16px; margin-bottom:20px; color:#ddd; line-height:1.7">
      {market_sentiment.replace(chr(10), '<br>')}
    </div>

    <div style="background:#1e1e2e; border-radius:8px; padding:14px; margin-bottom:20px">
      <div style="margin-bottom:6px"><strong style="color:#aaa; font-size:0.8rem">TOP GAINERS</strong><br>{gainers_html}</div>
      <div><strong style="color:#aaa; font-size:0.8rem">TOP LOSERS</strong><br>{losers_html}</div>
    </div>

    <h2 style="color:#aaa; font-size:1rem; text-transform:uppercase; letter-spacing:1px">Watchlist Analysis</h2>
    {watchlist_html}

    <p style="color:#555; font-size:0.75rem; text-align:center; margin-top:30px">
      Generated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} · Not financial advice
    </p>
  </div>
</body>
</html>"""
