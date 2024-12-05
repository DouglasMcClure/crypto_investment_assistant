# market_data.py
import requests
import pandas as pd
from config import headers
import io
import requests
import pandas as pd
from config import headers

log_file = "crypto_logs.txt"

def fetch_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24&locale=en&precision=full"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data)
        required_columns = ["id", "symbol", "current_price", "market_cap", "price_change_percentage_24h"]
        if any(col not in df.columns for col in required_columns):
            with io.open(log_file, "a", encoding="utf-8") as log:
                log.write("API response missing required columns.\n")
            return pd.DataFrame()

        return df[required_columns]

    except Exception as e:
        with io.open(log_file, "a", encoding="utf-8") as log:
            log.write(f"Error fetching market data: {e}\n")
        return pd.DataFrame()
def analyze_data(market_data):
    """
    Analyzes the DataFrame to find the top gainers and losers.
    """
    if market_data.empty:
        print("Market data is empty. Cannot analyze top gainers or losers.")
        return {"top_gainers": [], "top_losers": []}

    try:
        # Find top gainers and losers
        top_gainers = market_data.nlargest(5, "price_change_percentage_24h").to_dict(orient="records")
        top_losers = market_data.nsmallest(5, "price_change_percentage_24h").to_dict(orient="records")
        return {"top_gainers": top_gainers, "top_losers": top_losers}
    except Exception as e:
        print(f"Error analyzing market data: {e}")
        return {"top_gainers": [], "top_losers": []}