import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.metrics import precision_score
import matplotlib.pyplot as plt

# Download historical S&P 500 data using yfinance
sp500 = yf.Ticker("^GSPC").history(period="max")

# Visualize the closing price of the S&P 500
sp500.plot.line(y="Close", figsize=(10, 5), title="S&P 500 Closing Prices")
plt.show()

# Remove unnecessary columns
sp500.drop(columns=["Dividends", "Stock Splits"], inplace=True)

# Create target column: 1 if the next day's close is higher than today's, else 0
sp500["Tomorrow"] = sp500["Close"].shift(-1)
sp500["Target"] = (sp500["Tomorrow"] > sp500["Close"]).astype(int)
sp500.dropna(inplace=True)

# Focus only on data from 1990 onwards
sp500 = sp500.loc["1990-01-01":].copy()

# Define predictor columns and split the data into training and test sets
predictors = ["Close", "Volume", "Open", "High", "Low"]
train = sp500.iloc[:-100]
test = sp500.iloc[-100:]

# Train a Random Forest classifier
model = RFC(n_estimators=100, min_samples_split=100, random_state=1)
model.fit(train[predictors], train["Target"])

# Make predictions on the test set
predictions = model.predict(test[predictors])
predictions = pd.Series(predictions, index=test.index)

# Calculate precision score on test data
print("Initial Precision Score:", precision_score(test["Target"], predictions))

# Visualize predictions vs actual targets
combined = pd.concat([test["Target"], predictions], axis=1)
combined.columns = ["Actual", "Predicted"]
combined.plot.line(figsize=(10, 5), title="Actual vs Predicted Movements")
plt.show()

# Function to fit model and return predictions
def predict(train, test, predictors, model):
    model.fit(train[predictors], train["Target"])
    predictions = model.predict(test[predictors])
    predictions = pd.Series(predictions, index=test.index, name="Predictions")
    return pd.concat([test["Target"], predictions], axis=1)

# Function to backtest the model in chunks to simulate real-time predictions
def backtest(data, model, predictors, start=2500, step=250):
    all_predictions = []
    for i in range(start, data.shape[0], step):
        train = data.iloc[:i].copy()
        test = data.iloc[i:(i + step)].copy()
        predictions = predict(train, test, predictors, model)
        all_predictions.append(predictions)
    return pd.concat(all_predictions)

# Run backtest with basic predictors
predictions = backtest(sp500, model, predictors)
print("Backtest Precision (Basic):", precision_score(predictions["Target"], predictions["Predictions"]))

# Add rolling average–based features for various time horizons
horizons = [2, 5, 60, 250, 1000]
new_predictors = []

for horizon in horizons:
    rolling_avg = sp500.rolling(horizon).mean()
    
    # Ratio of current close to rolling average
    ratio_col = f"Close_Ratio_{horizon}"
    sp500[ratio_col] = sp500["Close"] / rolling_avg["Close"]
    
    # Difference between current close and rolling average
    trend_col = f"Close_Trend_{horizon}"
    sp500[trend_col] = sp500["Close"] - rolling_avg["Close"]
    
    new_predictors.extend([ratio_col, trend_col])

# Drop any rows with missing values from rolling calculations
sp500.dropna(inplace=True)

# Retrain the model with enhanced features
model = RFC(n_estimators=200, min_samples_split=50, random_state=1)

# Updated prediction function using probability thresholds
def predict(train, test, predictors, model):
    model.fit(train[predictors], train["Target"])
    probs = model.predict_proba(test[predictors])[:, 1]
    predictions = (probs >= 0.6).astype(int)
    predictions = pd.Series(predictions, index=test.index, name="Predictions")
    return pd.concat([test["Target"], predictions], axis=1)

# Backtest with new predictors
predictions = backtest(sp500, model, new_predictors)
print("Backtest Precision (With Rolling Features):", precision_score(predictions["Target"], predictions["Predictions"]))