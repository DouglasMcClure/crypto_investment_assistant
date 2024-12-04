import requests

def fetch_top_crypto_news():
    """
    Fetches cryptocurrency news from CryptoPanic API.
    """
    # API endpoint
    url = "https://cryptopanic.com/api/v1/posts/?auth_token=6e3eba4a60dbef8cc0b4424040a921a2a9c0d23e&filter=hot&regions=en&kind=news"

    try:
        response = requests.get(url)

        # Handle HTTP errors
        if response.status_code != 200:
            print(f"Error fetching news: {response.status_code} - {response.text}")
            return []

        # Parse JSON response
        data = response.json()
        articles = []

        # Extract and format results
        for item in data.get("results", [])[:10]:  # Limit to top 10 articles
            title = item.get("title", "No Title")
            link = item.get("url", "No URL")
            articles.append({"title": title, "link": link})

        return articles

    except Exception as e:
        print(f"Exception occurred while fetching news: {e}")
        return []

def fetch_crypto_news():
    """
    Fetches cryptocurrency news from CryptoPanic API.
    """
    # API endpoint
    url = "https://cryptopanic.com/api/v1/posts/?auth_token=6e3eba4a60dbef8cc0b4424040a921a2a9c0d23e&filter=hot&regions=en&kind=news"

    try:
        response = requests.get(url)

        # Handle HTTP errors
        if response.status_code != 200:
            print(f"Error fetching news: {response.status_code} - {response.text}")
            return []

        # Parse JSON response
        data = response.json()
        articles = []

        # Extract and format results
        for item in data.get("results", []):
            title = item.get("title", "No Title")
            link = item.get("url", "No URL")
            articles.append({"title": title, "link": link})

        return articles

    except Exception as e:
        print(f"Exception occurred while fetching news: {e}")
        return []
