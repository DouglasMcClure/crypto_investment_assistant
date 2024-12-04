import pandas as pd

from analysis import analyze_news_sentiment, calculate_indicators
from recommendations import make_recommendation
from fetch_historical_prices import fetch_historical_prices
from market_data import fetch_market_data, analyze_data
from news_scraper import fetch_crypto_news, fetch_top_crypto_news
from portfolio_manager import PortfolioManager
from predictor import predict_prices
from trending_list import fetch_trending_list
from alerts import send_telegram_alert
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

portfolio_manager = PortfolioManager()

def generate_summary():
    # Fetch market data
    market_data = fetch_market_data()

    if market_data.empty:
        print("Error: Market data is empty or invalid.")
        top_gainers, top_losers = [], []  # Ensure variables are always defined
    else:
        print("______Beginning Crypto Summary Generation______\n")

        # Analyze market data
        analysis = analyze_data(market_data)
        top_gainers = analysis.get("top_gainers", [])
        top_losers = analysis.get("top_losers", [])


    # Fetch trending coins
    try:
        trending_coins = fetch_trending_list()
        if not trending_coins:
            print("Error: No trending coins fetched.")
    except Exception as e:
        print(f"Error fetching trending coins: {e}")
        trending_coins = []

    # Fetch news and calculate sentiment
    top_news = fetch_top_crypto_news()
    news = fetch_crypto_news()
    sentiment = analyze_news_sentiment(news)

    # Add holdings
    portfolio_manager.add_holding("ripple", 57.46763811, 1.53651695)
    portfolio_manager.add_holding("ripple", 52.49026983, 1.16974061)

    # Analyze portfolio
    holdings_data = portfolio_manager.fetch_holdings()
    portfolio_value, portfolio_profit, earnings_report = portfolio_manager.calculate_profit_loss(holdings_data)

    # Recommendations
    recommendations = []
    for coin, details in portfolio_manager.holdings.items():
        historical_prices = fetch_historical_prices(coin, days=30)
        if not historical_prices.empty:
            indicators = calculate_indicators(historical_prices)
            recommendation = make_recommendation(indicators)
            recommendations.append(f"{coin.capitalize()}: {recommendation}")

    # Price predictions
    predictions = {}
    for coin in portfolio_manager.holdings.keys():
        historical_prices = fetch_historical_prices(coin, days=30)
        if not historical_prices.empty:
            predictions[coin] = predict_prices(historical_prices)
        else:
            print(f"No historical data available for {coin}.")

    # Generate summary
    summary = "===== Daily Crypto Summary =====\n\n"

    # Top gainers/losers
    summary += "Top Gainers (24h):\n"
    for gainer in top_gainers:
        summary += f"{gainer['id']} - ${gainer['current_price']} | +{gainer['price_change_percentage_24h']:.2f}%\n"

    summary += "\nTop Losers (24h):\n"
    for loser in top_losers:
        summary += f"{loser['id']} - ${loser['current_price']} | {loser['price_change_percentage_24h']:.2f}%\n"

    # Trending coins
    summary += "\nTrending Coins:\n"
    for coin in trending_coins:
        summary += f"{coin['name']} ({coin['symbol']}) - Market Cap Rank: {coin['market_cap_rank']}\n"

    # Portfolio report
    summary += f"\nPortfolio Value: ${portfolio_value:.2f}\nTotal Profit: ${portfolio_profit:.2f}\n\n"
    summary += "\nEarnings by Coin:\n"
    for coin, report in earnings_report.items():
        summary += f"{coin.capitalize()}: Current Price: ${report['current_price']:.2f}, Value: ${report['current_value']:.2f}, Investment: ${report['investment']:.2f}, Profit: ${report['profit']:.2f}\n"

    # Recommendations
    summary += "\nRecommendations:\n" + "\n".join(recommendations) + "\n"

    # Predictions
    summary += "\nPredictions:\n"
    for coin, prediction in predictions.items():
        summary += f"{coin.capitalize()}: Predicted Price ${prediction}\n"

    # News Sentiment Score
    summary += "\nNews Sentiment Score: {:.2f}\n".format(sentiment)

    # Top Crypto News
    summary += "\nTop Crypto News:\n"
    for article in top_news:
        summary += f"{article['title']} - {article['link']}\n"

    # Define your coins and their common aliases
    my_coins = {
        "xrp": ["ripple", "xrp"],
        "cybro": ["cybro", "cybrochain", "cyb"],
        "xyzverse": ["xyzverse", "xyz"],
        "dogen": ["dogen", "dogecoin next"]
    }

    # Top News For My Coins
    summary += "\nTop News For My Coins:\n"

    for coin, aliases in my_coins.items():
        # Filter articles for the specific coin and its aliases
        articles_found = [
            article for article in news
            if any(alias in article["title"].lower() for alias in aliases)
        ]

        if not articles_found:
            summary += f"\nNo news found for {coin.upper()}.\n"
        else:
            summary += f"\nNews for {coin.upper()}:\n"
            for article in articles_found:
                title = article.get("title", "").strip()
                link = article.get("link", "#")
                if len(title) < 5:  # Skip very short or invalid titles
                    continue
                summary += f"{title} - {link}\n"
            summary += "\n"  # Add spacing between coins


    return summary


def main():
    """
    Main function to run the bot and send the summary to Telegram.
    """
    try:
        summary = generate_summary()
        send_telegram_alert(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, summary)
        print(summary)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

