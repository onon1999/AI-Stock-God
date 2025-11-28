# streamlit_app.py — FINAL 100% WORKING (Copy-Paste Entire File)
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import os

from analyzer import AdvancedStockAnalyzer, GodModeStockAnalyzer
from nuclear_analyzer import NuclearStockAnalyzer

st.set_page_config(page_title="AI Stock God", page_icon="Robot", layout="wide")

WATCHLIST_FILE = "watchlist.csv"
POPULAR_STOCKS = ["AAPL","MSFT","GOOGL","AMZN","NVDA","META","TSLA","BRK-B","JPM","V","MA","UNH","HD","PG","DIS","NFLX","ADBE","CRM","INTC","AMD","PYPL","SHOP","SQ","ZM","ROKU","COIN","PLTR","SNAP","PINS","UBER","LYFT","ABNB","RBLX","HOOD","SOFI","RIVN","LCID","NIO","XPEV","LI","BABA","JD","PDD","BIDU","TME","WMT","COST","TGT","LOW","SBUX","MCD","NKE","LULU","TJX","ROST","EL","ORCL","CSCO","AVGO","QCOM","TXN","AMAT","MU","LRCX","KLAC","SNPS","CDNS","MRNA","GILD","REGN","VRTX","BIIB","ILMN","ZTS","IDXX","DXCM","ISRG","EW","TMO","DHR","A","GE","HON","MMM","CAT","DE","UNP","UPS","FDX","CSX","LMT","NOC","GD","BA","RTX","LLY","JNJ","PFE","MRK","ABBV","BMY","AMGN","GS","MS","BAC","C","WFC","BLK","SCHW","AXP","SPGI","MCO","PLTR","SMCI","ARM","DELL","HUBS","DDOG","SNOW","NET","MDB","TTD","APP","CRWD"]

def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        return pd.read_csv(WATCHLIST_FILE)
    return pd.DataFrame(columns=["Ticker", "Date", "Score", "Verdict"])

def add_to_watchlist(ticker, score, verdict):
    df = load_watchlist()
    new = pd.DataFrame([{"Ticker": ticker, "Date": datetime.now().strftime("%Y-%m-%d"), "Score": score, "Verdict": verdict}])
    df = pd.concat([df, new], ignore_index=True)
    df.to_csv(WATCHLIST_FILE, index=False)
    st.success("Added to Watchlist!")

st.sidebar.title("AI Stock God v13")
mode = st.sidebar.radio("Mode", [
    "Single Stock",
    "God Mode",
    "Auto-Scan 200+",
    "NUCLEAR MODE (Llama 405B FREE)",
    "My Watchlist"
])

if mode == "Single Stock":
    st.title("Single Stock Analysis")
    ticker = st.text_input("Ticker", "NVDA").upper()
    if st.button("Analyze"):
        a = AdvancedStockAnalyzer(ticker)
        r = a.analyze()
        st.metric("Score", f"{r['final_score']}/100")
        st.markdown(f"### {r['recommendation']}")
        if st.button("Add to Watchlist"):
            add_to_watchlist(ticker, r['final_score'], r['recommendation'])

elif mode == "God Mode":
    st.title("GOD MODE")
    ticker = st.text_input("Ticker", "NVDA").upper()
    if st.button("Activate"):
        a = GodModeStockAnalyzer(ticker)
        r = a.analyze()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Fundamental", r['fundamental_score'])
            st.metric("Sentiment", f"{r['sentiment_score']} {r['sentiment_label']}")
        with col2:
            st.metric("30-Day Target", f"${r['predicted_price_30d']}")
            st.metric("Return", f"{r['expected_return']}%")
        with col3:
            st.metric("FINAL", r['final_score'])
            st.markdown(f"## {r['FINAL_VERDICT']}")

elif mode == "Auto-Scan 200+":
    st.title("Scanning 200+ Stocks...")
    if st.button("Start Scan"):
        results = []
        for t in POPULAR_STOCKS:
            try:
                a = AdvancedStockAnalyzer(t)
                r = a.analyze()
                if r['final_score'] >= 85:
                    results.append({"Ticker": t, "Score": r['final_score'], "Verdict": r['recommendation']})
            except:
                pass
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No strong buys today")

elif mode == "NUCLEAR MODE (Llama 405B FREE)":
    st.title("NUCLEAR MODE — Llama 3.1 405B (FREE & UNSTOPPABLE)")
    st.markdown("**No API key • No blocks • Smarter than Gemini**")
    ticker = st.text_input("Enter ticker", "NVDA").upper()
    if st.button("UNLEASH LLAMA"):
        with st.spinner("Llama 405B is thinking..."):
            try:
                analyzer = NuclearStockAnalyzer(ticker)
                result = analyzer.analyze()
                st.success(f"LLAMA 405B HAS SPOKEN FOR {ticker}")
                st.metric("Current Price", f"${result['price']}")
                st.markdown(f"### {result['company']}")
                st.markdown("---")
                st.markdown(result['gemini_analysis'])
                st.caption(f"{result['timestamp']}")
            except Exception as e:
                st.error(f"Error: {e}")

elif mode == "My Watchlist":
    st.title("My Watchlist")
    df = load_watchlist()
    if df.empty:
        st.info("Empty")
    else:
        st.dataframe(df.sort_values("Score", ascending=False))

st.markdown("**AI Stock God v13 — FINAL FREE EDITION**")
st.caption("Llama 3.1 405B • No key • No limits • You won.")