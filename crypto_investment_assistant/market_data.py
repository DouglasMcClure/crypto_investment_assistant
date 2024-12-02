# market_data.py
import requests
import pandas as pd
from config import headers

def fetch_market_data():
    """
    Fetches market data for the top 100 cryptocurrencies by market cap.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false"

    response = requests.get(url, headers=headers)

    # Check for successful response
    if response.status_code != 200:
        print(f"Error: API returned status code {response.status_code}")
        print(response.json())
        return pd.DataFrame()  # Return an empty DataFrame

    data = response.json()
    df = pd.DataFrame(data)

    # Ensure required columns are present
    required_columns = ["id", "symbol", "current_price", "market_cap", "price_change_percentage_24h"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return pd.DataFrame()  # Return an empty DataFrame

    return df[required_columns]

def analyze_data(df):
    """
    Analyzes the DataFrame to find the top gainers and losers.
    """
    top_gainers = df.nlargest(5, "price_change_percentage_24h")
    top_losers = df.nsmallest(5, "price_change_percentage_24h")

    return {
        "top_gainers": top_gainers[["id", "current_price", "price_change_percentage_24h"]].to_dict(orient="records"),
        "top_losers": top_losers[["id", "current_price", "price_change_percentage_24h"]].to_dict(orient="records")
    }