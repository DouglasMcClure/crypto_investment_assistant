import requests
from config import headers

def fetch_trending_list():
    """
    Fetches the trending cryptocurrency list from CoinGecko.
    """
    url = "https://api.coingecko.com/api/v3/search/trending"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Debug API response
        # print("Trending Coins API Response:", data)

        trending_coins = []
        for coin in data.get("coins", []):
            item = coin.get("item", {})
            if item:
                trending_coins.append({
                    "name": item.get("name", "Unknown"),
                    "symbol": item.get("symbol", "Unknown"),
                    "market_cap_rank": item.get("market_cap_rank", "N/A")
                })

        return trending_coins
    except Exception as e:
        print(f"Error fetching trending list: {e}")
        return []