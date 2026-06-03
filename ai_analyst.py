import json
import requests
from config import OLLAMA_BASE_URL, OLLAMA_MODEL


def _call_ollama(prompt: str) -> str:
    try:
        resp = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except Exception as e:
        return f"[Ollama unavailable: {e}]"


def analyze_market_sentiment(overview: dict) -> str:
    indices_text = []
    for name, data in overview.get("indices", {}).items():
        if "error" not in data:
            arrow = "▲" if data["pct_change"] >= 0 else "▼"
            indices_text.append(f"{name}: {data['price']} ({arrow}{abs(data['pct_change'])}%)")

    gainers_text = ", ".join(
        f"{g['symbol']} +{g['pct_change']}%" for g in overview.get("top_gainers", [])
    )
    losers_text = ", ".join(
        f"{l['symbol']} {l['pct_change']}%" for l in overview.get("top_losers", [])
    )

    prompt = f"""You are a concise stock market analyst. Today's date: {overview.get('date')}.

Market data:
Indices: {'; '.join(indices_text)}
Top gainers: {gainers_text}
Top losers: {losers_text}

Write a 3-4 sentence market overview covering: overall sentiment (risk-on/risk-off), key themes driving moves, and what traders should watch today. Be direct and data-driven."""

    return _call_ollama(prompt)


def analyze_stock(symbol: str, fundamentals: dict, news: list[dict]) -> dict:
    news_headlines = "\n".join(
        f"- {n['title']} ({n['source']})" for n in news[:5]
    )

    fund_text = json.dumps({k: v for k, v in fundamentals.items() if k != "description"}, indent=2)

    prompt = f"""You are a balanced stock analyst. Analyze {symbol} and give a structured response.

Fundamentals:
{fund_text}

Recent news headlines:
{news_headlines}

Respond in this exact format:

VERDICT: [BUY / SELL / HOLD]
CONFIDENCE: [High / Medium / Low]

BULL CASE (3 bullet points why to buy):
•
•
•

BEAR CASE (3 bullet points why to sell/avoid):
•
•
•

PRICE TARGET: [your 3-6 month price target or N/A]
KEY RISK: [single biggest risk in one sentence]

Be concise, data-driven, and balanced."""

    raw = _call_ollama(prompt)

    return {
        "symbol": symbol,
        "analysis": raw,
        "price": fundamentals.get("price"),
        "pct_change_today": fundamentals.get("pct_change_today"),
        "recommendation": fundamentals.get("recommendation"),
    }
