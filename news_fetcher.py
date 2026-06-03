import yfinance as yf
from datetime import datetime


def fetch_stock_news(symbol: str, max_items: int = 5) -> list[dict]:
    try:
        t = yf.Ticker(symbol)
        raw_news = t.news or []
        articles = []
        for item in raw_news[:max_items]:
            content = item.get("content", {})
            title = content.get("title", item.get("title", "No title"))
            summary = content.get("summary", item.get("summary", ""))
            provider = content.get("provider", {})
            source = provider.get("displayName", item.get("publisher", "Unknown"))
            pub_date = content.get("pubDate", "")
            url = ""
            click_through = content.get("clickThroughUrl", {})
            if click_through:
                url = click_through.get("url", "")
            if not url:
                url = item.get("link", "")

            articles.append({
                "title": title,
                "summary": summary,
                "source": source,
                "published": pub_date,
                "url": url,
            })
        return articles
    except Exception as e:
        return [{"title": f"Error fetching news for {symbol}", "summary": str(e), "source": "", "published": "", "url": ""}]


def fetch_stock_fundamentals(symbol: str) -> dict:
    try:
        t = yf.Ticker(symbol)
        info = t.info
        hist = t.history(period="5d")
        price = round(hist["Close"].iloc[-1], 2) if not hist.empty else None
        prev = round(hist["Close"].iloc[-2], 2) if len(hist) >= 2 else None
        pct_change = round(((price - prev) / prev) * 100, 2) if price and prev else None

        return {
            "symbol": symbol,
            "price": price,
            "pct_change_today": pct_change,
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "revenue_growth": info.get("revenueGrowth"),
            "earnings_growth": info.get("earningsGrowth"),
            "analyst_target": info.get("targetMeanPrice"),
            "recommendation": info.get("recommendationKey"),
            "short_ratio": info.get("shortRatio"),
            "beta": info.get("beta"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "description": (info.get("longBusinessSummary", "") or "")[:500],
        }
    except Exception as e:
        return {"symbol": symbol, "error": str(e)}


def fetch_all_watchlist_data(watchlist: list[str]) -> dict:
    result = {}
    for sym in watchlist:
        result[sym] = {
            "fundamentals": fetch_stock_fundamentals(sym),
            "news": fetch_stock_news(sym),
        }
    return result
