from flask import Flask, render_template, jsonify
import yfinance as yf
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

CURRENCIES = [
    ("USD", "Dolar Amerika Serikat", "USDIDR=X", "$"),
    ("EUR", "Euro", "EURIDR=X", "€"),
    ("JPY", "Yen Jepang", "JPYIDR=X", "¥"),
    ("GBP", "Pound Sterling Inggris", "GBPIDR=X", "£"),
    ("CHF", "Franc Swiss", "CHFIDR=X", "Fr"),
    ("AUD", "Dolar Australia", "AUDIDR=X", "A$"),
    ("CAD", "Dolar Kanada", "CADIDR=X", "C$"),
    ("NZD", "Dolar Selandia Baru", "NZDIDR=X", "NZ$"),
    ("SGD", "Dolar Singapura", "SGDIDR=X", "S$"),
    ("HKD", "Dolar Hong Kong", "HKDIDR=X", "HK$"),
    ("CNY", "Yuan Tiongkok", "CNYIDR=X", "¥"),
    ("MYR", "Ringgit Malaysia", "MYRIDR=X", "RM"),
]

SPREAD_SIDE = 0.0045  # 0.45% each side -> 0.90% total spread


def get_rates():
    results = []
    for code, name, ticker, symbol in CURRENCIES:
        try:
            data = yf.Ticker(ticker).history(period="1d", interval="1m")
            if data.empty:
                data = yf.Ticker(ticker).history(period="5d")
            if data.empty:
                raise ValueError("Tidak ada data")

            mid = float(data["Close"].dropna().iloc[-1])
            buy = mid * (1 - SPREAD_SIDE)
            sell = mid * (1 + SPREAD_SIDE)

            results.append({
                "code": code,
                "name": name,
                "ticker": ticker,
                "symbol": symbol,
                "mid": mid,
                "buy": buy,
                "sell": sell,
            })
        except Exception as e:
            results.append({
                "code": code,
                "name": name,
                "ticker": ticker,
                "symbol": symbol,
                "mid": None,
                "buy": None,
                "sell": None,
                "error": str(e),
            })

    jakarta = timezone(timedelta(hours=7))
    updated = datetime.now(jakarta).strftime("%d %b %Y • %H:%M:%S WIB")
    return results, updated


@app.route("/")
def index():
    rates, updated = get_rates()
    return render_template("index.html", rates=rates, updated=updated)


@app.route("/api/rates")
def api_rates():
    rates, updated = get_rates()
    return jsonify({"updated": updated, "rates": rates})


if __name__ == "__main__":
    app.run(debug=True)
