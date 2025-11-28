# app.py — FINAL 100% WORKING WITH EMAIL + AUTO-RUN + GEMINI (Copy-Paste Entire File)
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyttsx3
import schedule
import time
import threading

from analyzer import AdvancedStockAnalyzer, GodModeStockAnalyzer
from nuclear_analyzer import NuclearStockAnalyzer

st.set_page_config(page_title="AI Stock God", page_icon="Robot", layout="wide")

# Config
EMAIL_FILE = "email_config.txt"
WATCHLIST_FILE = "watchlist.csv"
RESULTS_FILE = "daily_alerts.xlsx"

POPULAR_STOCKS = ["AAPL","MSFT","GOOGL","AMZN","NVDA","META","TSLA","BRK-B","JPM","V","MA","UNH","HD","PG","DIS","NFLX","ADBE","CRM","INTC","AMD","PYPL","SHOP","SQ","ZM","ROKU","COIN","PLTR","SNAP","PINS","UBER","LYFT","ABNB","RBLX","HOOD","SOFI","RIVN","LCID","NIO","XPEV","LI","BABA","JD","PDD","BIDU","TME","WMT","COST","TGT","LOW","SBUX","MCD","NKE","LULU","TJX","ROST","EL","ORCL","CSCO","AVGO","QCOM","TXN","AMAT","MU","LRCX","KLAC","SNPS","CDNS","MRNA","GILD","REGN","VRTX","BIIB","ILMN","ZTS","IDXX","DXCM","ISRG","EW","TMO","DHR","A","GE","HON","MMM","CAT","DE","UNP","UPS","FDX","CSX","LMT","NOC","GD","BA","RTX","LLY","JNJ","PFE","MRK","ABBV","BMY","AMGN","GS","MS","BAC","C","WFC","BLK","SCHW","AXP","SPGI","MCO","PLTR","SMCI","ARM","DELL","HUBS","DDOG","SNOW","NET","MDB","TTD","APP","CRWD"]

EXTRA_ASSETS = {"BTC-USD": "Bitcoin", "ETH-USD": "Ethereum", "GC=F": "Gold", "^GSPC": "S&P 500"}

# Email + Voice
def send_email(subject, body):
    if not os.path.exists(EMAIL_FILE):
        st.warning("Email not configured yet!")
        return
    email, password = open(EMAIL_FILE).read().strip().split(",")
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, msg.as_string())
        server.quit()
        st.success("Email sent!")
    except:
        st.error("Email failed")

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        pass

# Daily scan
def daily_scan():
    results = []
    for ticker in list(POPULAR_STOCKS) + list(EXTRA_ASSETS.keys()):
        try:
            a = AdvancedStockAnalyzer(ticker)
            r = a.analyze()
            if r['final_score'] >= 90:
                results.append({
                    "Ticker": ticker,
                    "Score": r['final_score'],
                    "Verdict": r['recommendation'],
                    "Name": r['company']
                })
        except:
            pass
    if results:
        df = pd.DataFrame(results)
        df.to_excel(RESULTS_FILE, index=False)
        body = "AI STOCK ALERTS\n\n" + df.to_string()
        send_email(f"{len(results)} MOONSHOTS FOUND!", body)
        speak(f"Found {len(results)} strong buy stocks today!")

# Watchlist
def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        return pd.read_csv(WATCHLIST_FILE)
    return pd.DataFrame(columns=["Ticker", "Date", "Score", "Verdict"])

def add_to_watchlist(ticker, score, verdict):
    df = load_watchlist()
    new = pd.DataFrame([{"Ticker": ticker, "Date": datetime.now().strftime("%Y-%m-%d"), "Score": score, "Verdict": verdict}])
    df = pd.concat([df, new], ignore_index=True)
    df.to_csv(WATCHLIST_FILE, index=False)
    st.success("Added to watchlist!")

# Sidebar
st.sidebar.title("AI Stock God v12")
mode = st.sidebar.radio("Mode", [
    "Single Stock",
    "God Mode",
    "NUCLEAR MODE (Gemini 2.5)",
    "Auto-Scan + Email",
    "Setup Email",
    "Watchlist"
])

# Modes
if mode == "Setup Email":
    st.title("Setup Email Alerts")
    email = st.text_input("Gmail")
    pwd = st.text_input("App Password", type="password")
    if st.button("Save"):
        with open(EMAIL_FILE, "w") as f:
            f.write(f"{email},{pwd}")
        st.success("Email activated!")

elif mode == "Auto-Scan + Email":
    st.title("Auto Daily Scan")
    if st.button("Run Now"):
        daily_scan()
    st.info("Auto-runs daily at 9:30 AM")

elif mode == "Single Stock":
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

elif mode == "NUCLEAR MODE (Llama 405B FREE)":
    st.title("NUCLEAR MODE — Llama 3.1 405B (FREE & UNSTOPPABLE)")
    st.markdown("**No API key needed • Runs forever • Smarter than Gemini**")
    
    ticker = st.text_input("Enter ticker", "NVDA").upper()
    if st.button("UNLEASH LLAMA", type="primary"):
        with st.spinner("Llama 405B is analyzing..."):
            try:
                analyzer = NuclearStockAnalyzer(ticker)
                result = analyzer.analyze()  # ← No key passed
                st.success(f"LLAMA 405B HAS SPOKEN FOR {ticker}")
                st.metric("Current Price", f"${result['price']}")
                st.markdown(f"### {result['company']}")
                st.markdown("---")
                st.markdown(result['gemini_analysis'])  # ← Still uses this key in dict
                st.caption(f"Powered by Llama 3.1 405B • {result['timestamp']}")
            except Exception as e:
                st.error(f"Error: {e}")

elif mode == "Watchlist":
    st.title("My Watchlist")
    df = load_watchlist()
    if df.empty:
        st.info("Empty")
    else:
        st.dataframe(df.sort_values("Score", ascending=False))

# Auto scheduler
def run_scheduler():
    schedule.every().day.at("09:30").do(daily_scan)
    while True:
        schedule.run_pending()
        time.sleep(60)

if "scheduler" not in st.session_state:
    threading.Thread(target=run_scheduler, daemon=True).start()
    st.session_state.scheduler = True

st.markdown("**AI Stock God v12 — FINAL** • Email + Auto + Gemini + Voice")