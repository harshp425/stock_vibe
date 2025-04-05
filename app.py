import os
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
from transformers import pipeline
import yfinance as yf

app = Flask(__name__)

sentiment_analyzer = pipeline("sentiment-analysis")

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="10d")  
    info = stock.info

    if hist.empty:
        return None, None, None, None

    dates = hist.index.strftime('%Y-%m-%d').tolist()
    prices = hist["Close"].tolist()

    if not os.path.exists("static"):
        os.makedirs("static")

    plt.figure(figsize=(6, 3))
    plt.plot(dates, prices, marker="o", linestyle="-", label="Close Price")
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Close Price ($)")
    plt.title(f"Stock Prices for {ticker.upper()}")
    plt.legend()
    plt.grid()
    
    chart_path = "static/stock_prices.png"
    plt.savefig(chart_path)
    plt.close()

    stock_info = {
        "Name": info.get("shortName", "N/A"),
        "Sector": info.get("sector", "N/A"),
        "Industry": info.get("industry", "N/A"),
        "Market Cap": f"${info.get('marketCap', 'N/A'):,}" if info.get('marketCap') else "N/A",
        "Previous Close": f"${info.get('previousClose', 'N/A')}" if info.get('previousClose') else "N/A",
    }
    
    return chart_path, stock_info, dates, prices

def get_news(ticker):
    url = f"https://news.google.com/search?q={ticker}+stock&hl=en-US&gl=US&ceid=US:en"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article", limit=15)  
    

    news_list = []
    for article in articles:
        title_tag = article.find("a", class_='JtKRv')
        if title_tag:
            title = title_tag.text.strip()
            link = "https://news.google.com" + title_tag["href"][1:]  
            news_list.append((title, link))

    return news_list

def analyze_sentiment(news_list):
    sentiments = {"POSITIVE": 0, "NEGATIVE": 0}
    analyzed_news = []

    for title, link in news_list:
        result = sentiment_analyzer(title)[0]
        sentiment_label = result["label"]
        sentiments[sentiment_label] += 1
        analyzed_news.append((title, link, sentiment_label, result["score"]))

    return analyzed_news, sentiments

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ticker = request.form["ticker"].upper()
        stock_chart, stock_info, dates, prices = get_stock_data(ticker)
        
        if stock_chart is None:
            return render_template(
                "index.html",
                error=f"No data found for ticker: {ticker}"
            )
        
        news_list = get_news(ticker)
        analyzed_news, sentiment_counts = analyze_sentiment(news_list)

        return render_template(
            "index.html",
            ticker=ticker,
            stock_chart=stock_chart,
            stock_info=stock_info,
            analyzed_news=analyzed_news,
            sentiment_counts=sentiment_counts,
            dates=dates,
            prices=prices
        )

    return render_template("index.html")

@app.route("/api/stock/<ticker>", methods=["GET"])
def get_stock_api(ticker):
    stock_chart, stock_info, dates, prices = get_stock_data(ticker.upper())
    if stock_chart is None:
        return jsonify({"error": "Stock not found"}), 404
    
    news_list = get_news(ticker)
    analyzed_news, sentiment_counts = analyze_sentiment(news_list)
    
    return jsonify({
        "ticker": ticker.upper(),
        "dates": dates,
        "prices": prices,
        "stock_info": stock_info,
        "analyzed_news": [
            {
                "title": title,
                "link": link,
                "sentiment": sentiment,
                "score": float(score)
            } for title, link, sentiment, score in analyzed_news
        ],
        "sentiment_counts": sentiment_counts
    })

if __name__ == "__main__":
    app.run(debug=True)