from prophet import Prophet
import pandas as pd

def predict_prices(historical_prices):
    """
    Predict the next price using Prophet.
    :param historical_prices: DataFrame with 'timestamp' and 'close' columns.
    """
    try:
        # Validate that required columns exist
        if "timestamp" not in historical_prices.columns or "close" not in historical_prices.columns:
            raise ValueError("Historical prices DataFrame must contain 'timestamp' and 'close' columns.")

        # Ensure timestamps are in correct format
        historical_prices["timestamp"] = pd.to_datetime(historical_prices["timestamp"], errors="coerce")
        historical_prices = historical_prices.dropna(subset=["timestamp"])  # Drop rows with invalid timestamps

        # Prepare data for Prophet
        df = historical_prices.rename(columns={"timestamp": "ds", "close": "y"})
        df = df[["ds", "y"]].sort_values("ds")

        # Fit and predict using Prophet
        model = Prophet()
        model.fit(df)
        future = model.make_future_dataframe(periods=1)
        forecast = model.predict(future)
        return forecast.iloc[-1]["yhat"]
    except Exception as e:
        print(f"Error in predict_prices: {e}")
        return None
