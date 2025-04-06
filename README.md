# Stock Vibe

## Overview

**Stock Vibe** is a Flask-based web application that provides real-time sentiment analysis of publicly traded stocks using the latest news headlines. By combining price trends with headline sentiment, Stock Vibe helps users quickly understand how a stock is performing and how it's being perceived in the media. The app is designed to be simple, fast, and free — making it a great tool for investors, analysts, and anyone interested in stock market sentiment.

---

## Technologies Used

**Languages**:  
- Python
- HTML
- CSS

**Libraries / Tools**:
- **Flask** – Serves the application through a lightweight web framework.
- **BeautifulSoup** – For scraping recent news headlines from Google News.
- **yfinance** – Retrieves historical price data and company metadata.
- **Transformers (Hugging Face)** – Performs sentiment analysis using pre-trained models.
- **Matplotlib** – Renders stock price charts as static images.

---

## Key Features / Value Proposition

- **Live Sentiment Analysis**: Extracts and analyzes real-time news headlines to determine public sentiment.
- **Visual Price Trends**: Displays recent 10-day stock price charts.
- **Fast & Lightweight**: Runs entirely on CPU with minimal resource usage.
- **Accessible via Web Browser**: No command line needed once deployed.
- **REST API Support**: Offers a simple API endpoint for integrating sentiment data into other tools or dashboards.
- **Completely Free**: No paid APIs or external services required.
- **Media-Driven Insights**: Great for quick checks on how a stock is trending in the news.

---

## Getting Started

### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/stock-vibe.git
cd stock-vibe
```
### 2. Install Necessary Dependencies and Libraries:
```bash
pip install -r requirements.txt
```
### 2. Run the Application:
```bash
flask run
```

---

## Demo
After running the application, the user will be presented with a new localhost window with the home page as shown below...

<img width="1470" alt="Screenshot 2025-04-06 at 11 06 02 AM" src="https://github.com/user-attachments/assets/a39bdb31-6f9b-43ed-a102-9595ecff0f0a" />


Users can input the ticker for any publicly traded stock on the market (case insensitive) and upon clicking the `Analyze` button, a sentiment analysis dashboard will appear on the screen. On the righthand side panel, users can view the particular news headlines that where evaluated in determining the sentimet score for the particular stock. They can also click on a given headline to be redirected to the actual news article.



https://github.com/user-attachments/assets/645a91a5-26b9-4879-ac2a-8df26012e967






