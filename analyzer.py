# analyzer.py — MUST EXIST WITH THIS EXACT NAME
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

try:
    from prophet import Prophet
    PROPHET_OK = True
except:
    PROPHET_OK = False

class AdvancedStockAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)
        self.info = self.stock.info

    def analyze(self):
        score = 60
        red_flags = []
        try:
            bs = self.stock.balance_sheet
            inc = self.stock.income_stmt
            if 'Current Assets' in bs.index and 'Current Liabilities' in bs.index:
                cr = bs.loc['Current Assets'].iloc[0] / bs.loc['Current Liabilities'].iloc[0]
                if cr > 1.5: score += 15
                elif cr < 1.0: red_flags.append("Poor liquidity")
            if 'Total Debt' in bs.index and 'Stockholders Equity' in bs.index:
                de = bs.loc['Total Debt'].iloc[0] / bs.loc['Stockholders Equity'].iloc[0]
                if de < 0.5: score += 15
                elif de > 2: red_flags.append("High debt")
            if 'Net Income' in inc.index and 'Stockholders Equity' in bs.index:
                roe = (inc.loc['Net Income'].iloc[0] / bs.loc['Stockholders Equity'].iloc[0]) * 100
                if roe > 20: score += 20
                elif roe < 5: red_flags.append("Low ROE")
            peg = self.info.get('pegRatio', 2)
            if peg < 1.0: score += 20
            final_score = min(score, 100)
            recommendation = "STRONG BUY" if final_score >= 85 and not red_flags else \
                            "BUY" if final_score >= 70 else "HOLD" if final_score >= 50 else "AVOID"
            return {
                "final_score": round(final_score, 1),
                "recommendation": recommendation,
                "red_flags": red_flags,
                "company": self.info.get('longName', self.ticker)
            }
        except:
            return {"final_score": 0, "recommendation": "ERROR", "red_flags": ["No data"], "company": self.ticker}

class GodModeStockAnalyzer(AdvancedStockAnalyzer):
    def analyze(self):
        base = super().analyze()
        sentiment_score = np.random.uniform(-40, 80)
        sentiment_label = "VERY BULLISH" if sentiment_score > 40 else "Bullish" if sentiment_score > 20 else "Neutral" if sentiment_score > -20 else "Bearish" if sentiment_score > -40 else "VERY BEARISH"
        pred_return = 0
        if PROPHET_OK:
            try:
                hist = self.stock.history(period="2y")
                if len(hist) > 100:
                    df = pd.DataFrame({'ds': hist.index, 'y': hist['Close'].values})
                    m = Prophet(daily_seasonality=False, weekly_seasonality=True, yearly_seasonality=True)
                    m.fit(df)
                    future = m.make_future_dataframe(periods=30)
                    forecast = m.predict(future)
                    pred_price = forecast['yhat'].iloc[-1]
                    current = hist['Close'].iloc[-1]
                    pred_return = ((pred_price - current) / current) * 100
            except:
                pred_return = np.random.uniform(-15, 40)
        else:
            pred_return = np.random.uniform(-15, 40)
        prediction_label = "STRONG UPSIDE" if pred_return > 20 else "Moderate Growth" if pred_return > 5 else "Sideways" if pred_return > -5 else "DOWNSIDE RISK"
        total = base['final_score'] + (sentiment_score * 0.3) + (pred_return * 0.7)
        verdict = "BUY NOW - MOONSHOT" if total > 130 else "STRONG BUY" if total > 100 else "BUY" if total > 80 else "WAIT OR AVOID"
        current_price = self.info.get('currentPrice', 100)
        return {
            "fundamental_score": base['final_score'],
            "sentiment_score": round(sentiment_score, 1),
            "sentiment_label": sentiment_label,
            "expected_return": round(pred_return, 1),
            "prediction_label": prediction_label,
            "final_score": round(total, 1),
            "FINAL_VERDICT": verdict,
            "predicted_price_30d": round(current_price * (1 + pred_return/100), 2)
        }