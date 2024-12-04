import pandas as pd
import numpy as np
from textblob import TextBlob
from finta import TA


def analyze_data(market_data):
    """
    Analyze the market data to find the top gainers and losers.
    """
    if not market_data or not isinstance(market_data, dict):
        print("Error: Invalid or empty market data.")
        return {"top_gainers": [], "top_losers": []}

    try:
        # Convert market_data to a DataFrame
        df = pd.DataFrame.from_dict(market_data, orient="index")

        # Debugging the structure of the DataFrame
        # print("Market DataFrame Debug:\n", df)

        # Ensure required column exists
        if "price_change_percentage_24h" not in df.columns:
            print("Error: Market data missing 'price_change_percentage_24h' column.")
            return {"top_gainers": [], "top_losers": []}

        # Check for empty DataFrame
        if df.empty:
            print("Market DataFrame is empty.")
            return {"top_gainers": [], "top_losers": []}

        # Find top gainers and losers safely
        top_gainers = df.nlargest(5, "price_change_percentage_24h", default=pd.DataFrame()).to_dict(orient="records")
        top_losers = df.nsmallest(5, "price_change_percentage_24h", default=pd.DataFrame()).to_dict(orient="records")

        return {"top_gainers": top_gainers, "top_losers": top_losers}

    except Exception as e:
        print(f"Error processing market data: {e}")
        return {"top_gainers": [], "top_losers": []}


def calculate_indicators(df):
    df["RSI"] = TA.RSI(df)
    macd = TA.MACD(df)
    df["MACD"] = macd["MACD"]
    df["SIGNAL"] = macd["SIGNAL"]
    df["EMA_20"] = TA.EMA(df, 20)
    return df



def analyze_news_sentiment(news_articles):
    """
    Analyze sentiment of crypto news articles.
    :param news_articles: List of news articles (title and content).
    :return: Average sentiment polarity.
    """

    """
       Calculate sentiment for news articles specifically about Ripple (XRP).
    """
    ripple_articles = [article for article in news_articles if
                       "ripple" in article["title"].lower() or "xrp" in article["title"].lower()]

    if not ripple_articles:
        print("No Ripple-related news found.")
        return 0  # Default to neutral if no articles are found

    sentiments = []
    for article in ripple_articles:
        title = article.get("title", "").strip()
        if len(title) < 5:  # Skip very short or invalid titles
            print(f"Skipping short or invalid title: {title}")
            continue
        sentiment = TextBlob(title).sentiment.polarity
        sentiments.append(sentiment)

    avg_sentiment = np.mean(sentiments) if sentiments else 0
    # print(f"Calculated Sentiments: {sentiments}")
    return round(avg_sentiment, 2)
