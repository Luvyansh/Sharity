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
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your API key for Alpha Vantage:**
   Add your API key to a `.env` file or directly into the config if preferred.

5. **Run the Flask app:**
   ```bash
   flask run
   ```

6. **Access the app:**
   Open your browser and navigate to `http://127.0.0.1:5000`

---

## 🧠 Model Information

- The RandomForestClassifier model was trained on historical technical indicators including:
  - Moving Average (SMA/EMA)
  - RSI
  - MACD
- Labels (BUY/SELL) were assigned using pre-defined thresholds
- The model is saved and loaded via `joblib` for production use

---

## 📂 Project Structure

```
.
Sharity/
├── .env
├── main.py
├── project_structure.txt
├── requirements.txt
│
├── applications/
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── routes.py
│   ├── sharity.py
│   ├── __init__.py
│   │
│   └── utils/
│       ├── news_fetcher.py
│       └── stock_cache.py
│
├── controllers/
│   └── controllers.py
│
├── instance/
│   └── sharity.db
│
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   │
│   └── versions/
│       └── 92e61c57f542_initial_migration.py
│
└── predictor/
    ├── requirements.txt
    ├── stocks.ipynb
    └── stocks.py
```

---

## 📸 Screenshots

### 📊 GSPC Stock Chart  
![GSPC Stock Chart](https://github.com/user-attachments/assets/8458f390-486a-4b98-962c-2e6d2653042a)

### 📈 Data Parameters  
![Data Parameters](https://github.com/user-attachments/assets/04a066d9-8485-4191-931e-969a2f54a6ca)

### 🏠 Home Page  
![Home](https://github.com/user-attachments/assets/741d46bd-3f8a-409b-9f58-899d779131d1)

### 📝 Register Page  
![Register](https://github.com/user-attachments/assets/3438dd41-935c-4d46-9a2c-2c2ffcef0155)

### 🔐 Login Page  
![Login](https://github.com/user-attachments/assets/430562c4-4e66-449a-a545-6aa3d3bfde64)

### 📂 User Dashboard  
![User Dashboard](https://github.com/user-attachments/assets/113058c2-393a-4683-ac79-111ce331aa1d)

### 📃 Stock Details  
![Stock Details](https://github.com/user-attachments/assets/ea587bd9-250e-4e50-a62e-496451997a53)

### ⏳ Prediction Loading  
![Prediction Loading](https://github.com/user-attachments/assets/b791350e-7d0b-4634-ae63-181ca7bd438b)

### 🟢 Sample Prediction - BUY  
![Sample Prediction BUY](https://github.com/user-attachments/assets/e848a437-c03d-42e8-ba9e-e465572b64f7)

### 🔴 Sample Prediction - SELL  
![Sample Prediction SELL](https://github.com/user-attachments/assets/e1fc17f1-11b2-4d84-8c41-8942ca68d862)

### 🛠️ Admin Dashboard (User Management)  
![Admin Dashboard](https://github.com/user-attachments/assets/d5d714f4-2ab2-4d15-9a85-af7a1767a1af)

---

## 👨‍💻 Developer

**Anurag Pandey**  
Roll Number: 2108252002  
Email: [luvyansh2001@gmail.com]
LinkedIN: [https://www.linkedin.com/in/luvyansh/]
GitHub: [github.com/Luvyansh](https://github.com/Luvyansh)

---

## 📃 License

This project is licensed under the [MIT License](LICENSE).

---

## 🌲 Acknowledgements

- [Scikit-learn](https://scikit-learn.org/)
- [yfinance](https://github.com/ranaroussi/yfinance)
- [Alpha Vantage](https://www.alphavantage.co/)
- [Chart.js](https://www.chartjs.org/)
- [Flask](https://flask.palletsprojects.com/)
