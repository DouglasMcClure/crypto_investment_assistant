import pandas as pd
from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json
import os
import io
log_file = "crypto_logs.txt"

def configure_prophet():
    os.environ["PROPHET_BACKEND"] = "R"
    return Prophet(
        changepoint_prior_scale=0.05,
        yearly_seasonality=False,
        weekly_seasonality=True
    )

def predict_prices(historical_prices):
    try:
        with io.open(log_file, "a", encoding="utf-8") as log:
            if "timestamp" not in historical_prices.columns or "close" not in historical_prices.columns:
                log.write("Historical prices DataFrame missing 'timestamp' or 'close' columns.\n")
                raise ValueError("Historical prices DataFrame must contain 'timestamp' and 'close' columns.")

            historical_prices["timestamp"] = pd.to_datetime(historical_prices["timestamp"], errors="coerce")
            historical_prices = historical_prices.dropna(subset=["timestamp"]).tail(90)

            df = historical_prices.rename(columns={"timestamp": "ds", "close": "y"}).dropna()
            model = configure_prophet()
            model.fit(df)

            future = model.make_future_dataframe(periods=1)
            forecast = model.predict(future)
            prediction = forecast.iloc[-1]["yhat"]
            log.write(f"Predicted price: {prediction}\n")
            return prediction

    except Exception as e:
        with io.open(log_file, "a", encoding="utf-8") as log:
            log.write(f"Error in predict_prices: {e}\n")
        return None