# nuclear_analyzer.py — FINAL FREE & UNSTOPPABLE VERSION
import yfinance as yf
import requests
from datetime import datetime

def ask_llama(ticker, company_name, price, pe, peg, roe, debt, revenue_growth):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer dummy_key",  # Not needed for :free models
        "HTTP-Referer": "https://ai-stock-god.streamlit.app",
        "X-Title": "AI Stock God",
        "Content-Type": "application/json"
    }

    prompt = f"""You are a senior Goldman Sachs equity analyst.

Analyze {ticker} ({company_name})
Current Price: ${price:.2f}
P/E: {pe:.1f}x | PEG: {peg:.2f} | ROE: {roe:.1%} | Debt/Equity: {debt:.1f}x | Revenue Growth: {revenue_growth:.1%}

Give in this EXACT format:
**Target Price (12 months):** $XXX  
**Upside:** +XX%  
**Confidence:** X/10  
**Verdict:** STRONG BUY / BUY / HOLD / SELL  
**Reasoning:** [DCF + comps + brief math in 3-5 sentences]"""

    data = {
        "model": "meta-llama/llama-3.1-405b-instruct:free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 500
    }

    try:
        r = requests.post(url, headers=headers, json=data, timeout=40)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return f"API Error {r.status_code}\n{r.text}"
    except Exception as e:
        return f"Request failed: {str(e)}\nCheck internet connection"

class NuclearStockAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)
        self.info = self.stock.info

    def analyze(self):
        price = self.info.get('currentPrice') or 0
        pe = self.info.get('trailingPE') or 0
        peg = self.info.get('pegRatio') or 0
        roe = self.info.get('returnOnEquity') or 0
        debt = self.info.get('debtToEquity') or 0
        revenue_growth = self.info.get('revenueGrowth') or 0
        company_name = self.info.get('longName') or self.ticker

        llama_analysis = ask_llama(self.ticker, company_name, price, pe, peg, roe, debt, revenue_growth)

        return {
            "ticker": self.ticker,
            "company": company_name,
            "price": round(price, 2),
            "gemini_analysis": llama_analysis,  # Still works with app.py
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }