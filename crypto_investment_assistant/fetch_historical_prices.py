import pandas as pd
import requests

def fetch_historical_prices(coin_id, days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}&interval=daily"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-ox3aZDyf2EQVJp12UswYZ48s"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extract and validate prices
        prices = data.get("prices", [])
        if not prices:
            print(f"No price data available for {coin_id}.")
            return pd.DataFrame()  # Return empty DataFrame on failure

        df = pd.DataFrame(prices, columns=["timestamp", "close"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", errors="coerce")
        df = df.dropna(subset=["timestamp"])

        # Add placeholder columns if needed
        df["open"] = df["close"]
        df["high"] = df["close"]
        df["low"] = df["close"]
        df["volume"] = 0

        return df
    except Exception as e:
        print(f"Error fetching historical prices for {coin_id}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error


