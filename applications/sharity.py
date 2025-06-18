from flask import render_template, request, jsonify
from main import app
from applications.models import StockCache
import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def get_stock_by_symbol(symbol):
    return StockCache.query.filter_by(symbol=symbol).first()

from applications.utils.news_fetcher import fetch_and_cache_news

@app.route('/stock_details/<symbol>')
def stock_details(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(start="1900-01-01", interval="1y")

    if hist.empty:
        hist = ticker.history(start="1900-01-01", interval="1mo")
    if hist.empty:
        return "No data found", 404

    labels = [str(d.year) if len(hist) > 100 else d.strftime("%b %Y") for d in hist.index]
    prices = hist['Close'].fillna(method='ffill').tolist()
    current_price = prices[-1] if prices else 0

    news = fetch_and_cache_news(symbol)

    return render_template(
        'stock_details.html',
        labels=labels,
        prices=prices,
        stock={"price": round(current_price, 2), "symbol": symbol.upper()},
        news=news
    )

@app.route('/predict/<symbol>')
def predict(symbol):
    try:
        # Fetch historical data for the given symbol
        df = yf.Ticker(symbol).history(period="max")
        if df.empty or len(df) < 1000:
            return jsonify({"prediction": "Insufficient data"})

        df.drop(columns=["Dividends", "Stock Splits"], inplace=True, errors="ignore")
        df["Tomorrow"] = df["Close"].shift(-1)
        df["Target"] = (df["Tomorrow"] > df["Close"]).astype(int)
        df.dropna(inplace=True)

        # Use only recent data if needed
        df = df.loc["1990-01-01":].copy()

        # Rolling feature engineering
        horizons = [2, 5, 60, 250, 1000]
        for horizon in horizons:
            rolling = df.rolling(horizon)
            df[f"Close_Ratio_{horizon}"] = df["Close"] / rolling.mean()["Close"]
            df[f"Close_Trend_{horizon}"] = df["Close"] - rolling.mean()["Close"]
        df.dropna(inplace=True)

        predictors = [col for col in df.columns if "Ratio" in col or "Trend" in col]
        model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)

        # Split train/test
        train = df.iloc[:-1]
        test = df.iloc[-1:]

        model.fit(train[predictors], train["Target"])
        proba = model.predict_proba(test[predictors])[0][1]
        prediction = "BUY" if proba >= 0.6 else "SELL"

        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"prediction": f"Error: {str(e)}"})