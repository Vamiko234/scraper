import yfinance as yf
from datetime import datetime, timedelta
from config import MARKET_INDICES


def fetch_index_data():
    results = {}
    for name, ticker in MARKET_INDICES.items():
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="2d")
            if len(hist) >= 2:
                prev_close = hist["Close"].iloc[-2]
                current = hist["Close"].iloc[-1]
                change = current - prev_close
                pct = (change / prev_close) * 100
                results[name] = {
                    "price": round(current, 2),
                    "change": round(change, 2),
                    "pct_change": round(pct, 2),
                }
            elif len(hist) == 1:
                current = hist["Close"].iloc[-1]
                results[name] = {"price": round(current, 2), "change": 0, "pct_change": 0}
        except Exception as e:
            results[name] = {"error": str(e)}
    return results


def fetch_top_movers():
    # Use a broad set of liquid large-caps to find top movers
    candidates = [
        "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "AMD",
        "INTC", "NFLX", "PYPL", "BA", "JPM", "GS", "XOM", "CVX",
        "MU", "SNDK", "QCOM", "AVGO",
    ]
    movers = []
    for sym in candidates:
        try:
            t = yf.Ticker(sym)
            hist = t.history(period="2d")
            if len(hist) >= 2:
                prev = hist["Close"].iloc[-2]
                curr = hist["Close"].iloc[-1]
                pct = ((curr - prev) / prev) * 100
                movers.append({"symbol": sym, "price": round(curr, 2), "pct_change": round(pct, 2)})
        except Exception:
            pass

    movers.sort(key=lambda x: abs(x.get("pct_change", 0)), reverse=True)
    gainers = [m for m in movers if m.get("pct_change", 0) > 0][:5]
    losers = [m for m in movers if m.get("pct_change", 0) < 0][:5]
    return gainers, losers


def get_market_overview():
    indices = fetch_index_data()
    gainers, losers = fetch_top_movers()
    return {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "indices": indices,
        "top_gainers": gainers,
        "top_losers": losers,
    }
