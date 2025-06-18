import yfinance as yf
from applications.models import StockCache
from applications.database import db
from datetime import datetime

def fetch_usd_to_inr():
    """Fetch live USD to INR conversion rate using yfinance."""
    try:
        fx_pair = yf.Ticker("USDINR=X")
        return fx_pair.info.get("regularMarketPrice", 83.0)  # fallback to approx
    except Exception as e:
        print(f"[ERROR] Could not fetch USD to INR rate: {e}")
        return 83.0

def fetch_and_cache_stocks(force_refresh=False):
    COMPANY_SYMBOLS = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'BHARTIARTL.NS', 'SBIN.NS', 'INFY.NS', 'LICI.NS', 'HINDUNILVR.NS', 'ITC.NS', 'LT.NS', 'BAJFINANCE.NS', 'HCLTECH.NS', 'MARUTI.NS', 'KOTAKBANK.NS', 'SUNPHARMA.NS', 'ADANIENT.NS', 'TITAN.NS', 'ONGC.NS', 'TATAMOTORS.NS', 'NTPC.NS', 'AXISBANK.NS', 'DMART.NS', 'BAJAJFINSV.NS', 'ASIANPAINT.NS', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B', 'V', 'LLY', 'JPM', 'WMT', 'UNH', 'XOM', 'MA', 'JNJ', 'PG', 'HD', 'ORCL', 'CVX', 'AVGO', 'ABBV', 'COST', 'PEP', 'ADBE', 'KO', 'BABA', 'CRM', 'CSCO', 'MCD', 'ACN', 'PFE', 'NFLX', 'TMO', 'LIN', 'ABT', 'TM', 'NKE', 'DIS', 'WFC', 'BAC', 'DHR', 'VZ', 'INTC', 'NEE', 'AMD', 'HON', 'QCOM', 'TXN', 'UPS', 'MDT', 'SBUX', 'RTX', 'IBM', 'GS', 'LOW', 'BLK', 'CAT', 'DE', 'GE', 'BA', 'NOW', 'PYPL', 'INTU', 'UBER', 'SQ', 'ZM', 'SNOW', 'SHOP', 'ABNB', 'PLTR', 'RIVN', 'LCID', 'SPOT', 'COIN', 'TWLO']

    usd_to_inr = fetch_usd_to_inr()
    cached_data = []

    for symbol in COMPANY_SYMBOLS:
        try:
            record = StockCache.query.filter_by(symbol=symbol).first()

            should_refresh = (
                force_refresh or
                not record or
                (datetime.utcnow() - record.last_updated).total_seconds() > 3600
            )

            if should_refresh:
                stock = yf.Ticker(symbol)
                info = stock.info

                if not record:
                    record = StockCache(symbol=symbol)
                    db.session.add(record)

                # Get values and convert to INR if currency is USD
                currency = info.get("currency", "N/A")
                price = info.get("currentPrice", 0.0)
                market_cap = info.get("marketCap", 0)

                if currency == "USD":
                    price *= usd_to_inr
                    market_cap *= usd_to_inr

                record.name = info.get("longName", "N/A")
                record.price = round(price, 2)
                record.currency = "INR"  # Mark all as INR now
                record.market_cap = round(market_cap, 2)
                record.sector = info.get("sector", "N/A")
                record.last_updated = datetime.utcnow()

                db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Failed fetching {symbol}: {e}")
            continue

        cached_data.append(record)

    return cached_data