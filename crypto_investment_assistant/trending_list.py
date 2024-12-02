import requests

def fetch_trending_list():
    """
    Fetches the trending cryptocurrency list from CoinGecko.
    """
    url = "https://api.coingecko.com/api/v3/search/trending"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-ox3aZDyf2EQVJp12UswYZ48s"  # Replace if using your actual API key
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching trending list: {response.status_code}")
        return []

    data = response.json()
    trending_coins = []
    for coin in data.get("coins", []):
        item = coin.get("item", {})
        trending_coins.append({
            "name": item.get("name"),
            "symbol": item.get("symbol"),
            "market_cap_rank": item.get("market_cap_rank")
        })

    return trending_coins