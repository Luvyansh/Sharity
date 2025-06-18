# Sharity: Stock Analysis & Prediction Web Application

Sharity is an intelligent, real-time stock analysis and prediction platform built using Flask, scikit-learn, Chart.js, and various financial APIs. It integrates market data, predictive modeling, charting, and news aggregation into one powerful and user-friendly tool to assist investors in making informed decisions.

Developed by **Anurag Pandey** as a part of the Major Project requirement for the B.Tech degree in Computer Science and Engineering (AI & DS).

---

## 🔍 Overview

Sharity simplifies the process of stock market analysis by providing:

- Real-time and historical stock data using the `yfinance` API
- BUY/SELL predictions via a trained `RandomForestClassifier` model
- Interactive candlestick charting with Chart.js
- Live financial news based on stock ticker using Alpha Vantage News API
- Data caching using SQLite3 to improve performance

---

## ✨ Features

- 📈 **Stock Visualization**: Real-time rendering of historical OHLCV data
- 🤖 **ML-Based Prediction**: Predictive insights powered by Random Forest Classifier
- 🗂 **Data Caching**: Efficient local caching of stock data using SQLite3
- 📰 **News Integration**: Financial news fetched per symbol
- 💻 **Full-stack Integration**: Flask backend, HTML/CSS/JS frontend, and REST APIs

---

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Database**: SQLite3
- **Machine Learning**: scikit-learn (RandomForestClassifier)
- **APIs**:
  - [yfinance](https://github.com/ranaroussi/yfinance) – Stock data
  - [Alpha Vantage](https://www.alphavantage.co/documentation/) – Financial news

---

## ⚙️ Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Luvyansh/Sharity.git
   cd Sharity
