# nuclear_analyzer.py — SAFE FOR GITHUB (No API key inside)
import yfinance as yf
import requests
from datetime import datetime

# Key is now loaded from Streamlit secrets (100% safe)
try:
    from streamlit import secrets
    OPENROUTER_API_KEY = secrets["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"]
except:
    # Fallback for local testing
    OPENROUTER_API_KEY = "YOUR_KEY_HERE"  # Only used locally

def ask_gemini(ticker, company_name, price, pe, peg, roe, debt, revenue_growth):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://ai-stock-god.streamlit.app",
        "X-Title": "AI Stock God",
        "Content-Type": "application/json"
    }
    
    prompt = f"""You are a Goldman Sachs equity analyst analyzing {ticker} ({company_name}).

Price: ${price:.2f} | P/E: {pe:.1f}x | PEG: {peg:.2f} | ROE: {roe:.1%} | Debt/Equity: {debt:.1f}x | Revenue growth: {revenue_growth:.1%}

Give:
1. 12-month target price + % upside
2. Confidence 1–10
3. Verdict: STRONG BUY / BUY / HOLD / SELL
4. Brief reasoning with valuation math

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
        "max_tokens": 600
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"API Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Connection failed: {str(e)}"

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

        gemini_analysis = ask_gemini(self.ticker, company_name, price, pe, peg, roe, debt, revenue_growth)

        return {
            "ticker": self.ticker,
            "company": company_name,
            "price": round(price, 2),
            "gemini_analysis": gemini_analysis,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }