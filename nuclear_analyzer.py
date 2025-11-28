# nuclear_analyzer.py — FINAL WORKING VERSION (fixes st.secrets bug)
import yfinance as yf
import requests
from datetime import datetime

# DO NOT use st.secrets here — we’ll pass the key from app.py
def ask_gemini(ticker, company_name, price, pe, peg, roe, debt, revenue_growth, api_key):
    if not api_key or "sk-or-" not in api_key:
        return "OPENROUTER KEY MISSING OR INVALID\n\nGo to app Settings → Secrets and add:\nOPENROUTER_API_KEY = \"sk-or-...\" (with quotes)"

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://ai-stock-god.streamlit.app",
        "X-Title": "AI Stock God",
        "Content-Type": "application/json"
    }

    prompt = f"""Analyze {ticker} ({company_name})
Price: ${price:.2f} | P/E {pe:.1f}x | PEG {peg:.2f} | ROE {roe:.1%} | Debt/Equity {debt:.1f}x

Give 12-month target + upside + confidence + verdict + brief math.

Format:
**Target Price (12 months):** $XXX
**Upside:** +XX%
**Confidence:** X/10
**Verdict:** STRONG BUY / BUY / HOLD / SELL
**Reasoning:** ...
"""

    data = {
        "model": "google/gemini-2.5-flash",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 500
    }

    try:
        r = requests.post(url, headers=headers, json=data, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return f"API ERROR {r.status_code}\n{r.text}"
    except Exception as e:
        return f"Request failed: {str(e)}"

class NuclearStockAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)
        self.info = self.stock.info

    def analyze(self, api_key):
        price = self.info.get('currentPrice') or 0
        pe = self.info.get('trailingPE') or 0
        peg = self.info.get('pegRatio') or 0
        roe = self.info.get('returnOnEquity') or 0
        debt = self.info.get('debtToEquity') or 0
        revenue_growth = self.info.get('revenueGrowth') or 0
        company_name = self.info.get('longName') or self.ticker

        gemini_analysis = ask_gemini(self.ticker, company_name, price, pe, peg, roe, debt, revenue_growth, api_key)

        return {
            "ticker": self.ticker,
            "company": company_name,
            "price": round(price, 2),
            "gemini_analysis": gemini_analysis,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }