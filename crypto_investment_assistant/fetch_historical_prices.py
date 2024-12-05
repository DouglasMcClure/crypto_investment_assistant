import pandas as pd
import requests
import io

log_file = "crypto_logs.txt"

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

        prices = data.get("prices", [])
        if not prices:
            with io.open(log_file, "a", encoding="utf-8") as log:
                log.write(f"No price data available for {coin_id}.\n")
            return pd.DataFrame()

        df = pd.DataFrame(prices, columns=["timestamp", "close"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", errors="coerce")
        df = df.dropna(subset=["timestamp"])

        df["open"] = df["close"]
        df["high"] = df["close"]
        df["low"] = df["close"]
        df["volume"] = 0

        with io.open(log_file, "a", encoding="utf-8") as log:
            log.write(f"Fetched historical prices for {coin_id}: {len(df)} records retrieved.\n")
        return df

    except Exception as e:
        with io.open(log_file, "a", encoding="utf-8") as log:
            log.write(f"Error fetching historical prices for {coin_id}: {e}\n")
        return pd.DataFrame()
