import requests
from flask import current_app
from datetime import datetime, timedelta
from applications.models import NewsCache  # You’ll need to define this model
from applications.database import db

def fetch_and_cache_news(symbol):
    # Check cache
    record = NewsCache.query.filter_by(symbol=symbol).first()
    if record and (datetime.utcnow() - record.last_updated).total_seconds() < 3600:
        return record.articles  # Already JSON serialized string

    # Get API key from config
    api_key = current_app.config.get("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        raise Exception("Alpha Vantage API key not configured")

    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()

        articles = data.get("feed", [])[:5]  # Get top 5
        simplified = [
            {
                "title": article["title"],
                "url": article["url"],
                "source": article["source"],
                "summary": article.get("summary", "")[:200]
            }
            for article in articles
        ]

        if record:
            record.articles = simplified
            record.last_updated = datetime.utcnow()
        else:
            record = NewsCache(symbol=symbol, articles=simplified, last_updated=datetime.utcnow())
            db.session.add(record)

        db.session.commit()
        return simplified
    except Exception as e:
        print(f"[ERROR] News fetch failed: {e}")
        return []
