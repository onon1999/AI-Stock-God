# nuclear_analyzer.py — TELLS YOU IF API KEY WORKS (Copy-Paste Entire File)
import yfinance as yf
import requests
from datetime import datetime
import streamlit as st

# TRY TO READ KEY FROM SECRETS
try:
    OPENROUTER_API_KEY = st.secrets["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"]
    KEY_STATUS = "Key loaded from Streamlit secrets"
except:
    OPENROUTER_API_KEY = "NO_KEY_FOUND"
    KEY_STATUS = "ERROR: No key in secrets! Add OPENROUTER_API_KEY in Settings → Secrets"

def test_api_key():
    """Test if the key actually works"""
    if "sk-or-" not in OPENROUTER_API_KEY:
        return "Invalid or missing key format"
    
    url = "https://openrouter.ai/api/v1/models"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return f"API KEY WORKING! Found {len(r.json()['data'])} models"
        elif r.status_code == 401:
            return "401 ERROR — Key is wrong or expired"
        else:
            return f"API Error {r.status_code}: {r.text}"
    except Exception as e:
        return f"Connection failed: {str(e)}"

def ask_gemini(ticker, company_name, price, pe, peg, roe, debt, revenue_growth):
    if "sk-or-" not in OPENROUTER_API_KEY:
        return f"API KEY MISSING OR INVALID\n\n{KEY_STATUS}\n\nGo to Settings → Secrets and add:\nOPENROUTER_API_KEY = sk-or-your-real-key"

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://ai-stock-god.streamlit.app",
        "X-Title": "AI Stock God",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Analyze {ticker} ({company_name})
Price: ${price:.2f} | P/E {pe:.1f}x | PEG {peg:.2f} | ROE {roe:.1%} | Debt/Equity {debt:.1f}x

Give:
- 12-month target price + upside %
- Confidence 1–10
- Verdict: STRONG BUY / BUY / HOLD / SELL
- Brief reasoning with math

Exact format:
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
            return f"API ERROR {r.status_code}\n{r.text}\n\n{test_api_key()}"
    except Exception as e:
        return f"REQUEST FAILED: {str(e)}\n\n{test_api_key()}"

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
            "gemini_analysis": f"{KEY_STATUS}\n\n{test_api_key()}\n\n{gemini_analysis}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }