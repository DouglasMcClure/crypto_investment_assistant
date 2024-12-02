from market_data import fetch_market_data, analyze_data
from news_scraper import fetch_crypto_news
from portfolio_manager import PortfolioManager
from predictor import predict_prices
from trending_list import fetch_trending_list
from alerts import send_telegram_alert
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

portfolio_manager = PortfolioManager()

def generate_summary():
    # Fetch market data
    market_data = fetch_market_data()

    # Analyze data
    analysis = analyze_data(market_data)

    # Fetch trending coins
    trending_coins = fetch_trending_list()

    # Fetch news
    news = fetch_crypto_news()

    # Portfolio analysis
    portfolio_manager.add_holding("XRP", 109.95790794, 1.6)
    portfolio_value = portfolio_manager.calculate_profit_loss(market_data)

    # Price predictions
    predicted_prices = {}
    for coin in ["XRP"]:  # Add coins you want predictions for
        real_time_prices = market_data.get(coin, {}).get("price_history", [])
        print(f"{coin} price history: {real_time_prices}")  # Debug price history
        if real_time_prices:
            predicted_prices[coin] = predict_prices(real_time_prices)

    # Generate summary
    summary = "===== Daily Crypto Summary =====\n\n"

    # Top gainers/losers
    summary += "Top Gainers (24h):\n"
    for coin in analysis["top_gainers"]:
        summary += f"{coin['id']} - ${coin['current_price']} | +{coin['price_change_percentage_24h']:.2f}%\n"

    summary += "\nTop Losers (24h):\n"
    for coin in analysis["top_losers"]:
        summary += f"{coin['id']} - ${coin['current_price']} | {coin['price_change_percentage_24h']:.2f}%\n"

    # Trending coins
    summary += "\nTrending Coins:\n"
    for coin in trending_coins:
        summary += f"{coin['name']} ({coin['symbol']}) - Market Cap Rank: {coin['market_cap_rank']}\n"

    # Portfolio value
    summary += f"\nPortfolio Value: ${portfolio_value:.2f}\n"

    # Predictions
    summary += "\nPrice Predictions:\n"
    for coin, price in predicted_prices.items():
        summary += f"{coin.capitalize()}: Predicted Price: ${price[0][0]:.2f}\n" if price else f"{coin.capitalize()}: Not enough data for prediction\n"

    # News
    summary += "\nLatest News:\n"
    for article in news:
        summary += f"{article['title']} - {article['link']}\n"

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
