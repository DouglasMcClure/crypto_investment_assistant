import pandas as pd
from analysis import analyze_news_sentiment, calculate_indicators
from profitable_coins import suggest_profitable_coins
from recommendations import make_recommendation
from fetch_historical_prices import fetch_historical_prices
from market_data import fetch_market_data, analyze_data
from news_scraper import fetch_crypto_news, fetch_top_crypto_news
from portfolio_manager import PortfolioManager
from predictor import predict_prices
from trending_list import fetch_trending_list
from alerts import send_telegram_alert
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import sys
import os
if os.name == "nt":
    os.system('chcp 65001')  # Set Windows command line to UTF-8
import io

portfolio_manager = PortfolioManager()

def generate_summary():
    log_file = "crypto_logs.txt"

    with io.open(log_file, "a", encoding="utf-8") as log:
        # Fetch market data
        market_data = fetch_market_data()

        if market_data.empty:
            log.write("Error: Market data is empty or invalid.\n")
            top_gainers, top_losers = [], []  # Ensure variables are always defined
        else:
            log.write("______Beginning Crypto Summary Generation______\n\n")

            # Analyze market data
            analysis = analyze_data(market_data)
            top_gainers = analysis.get("top_gainers", [])
            top_losers = analysis.get("top_losers", [])

        # Fetch trending coins
        try:
            trending_coins = fetch_trending_list()
            if not trending_coins:
                log.write("Error: No trending coins fetched.\n")
        except Exception as e:
            log.write(f"Error fetching trending coins: {e}\n")
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
                log.write(f"No historical data available for {coin}.\n")

        # Generate summary
        summary = "===== Daily Crypto Summary =====\n\n"

        # Top gainers/losers
        summary += "\n===== Top Gainers (24h) =====\n"
        for gainer in top_gainers:
            summary += f"{gainer['id']} - ${gainer['current_price']} | +{gainer['price_change_percentage_24h']:.2f}%\n"

        summary += "\n===== Top Losers (24h): =====\n"
        for loser in top_losers:
            summary += f"{loser['id']} - ${loser['current_price']} | {loser['price_change_percentage_24h']:.2f}%\n"

        # Trending coins
        summary += "\n===== Trending Coins: =====\n"
        for coin in trending_coins:
            summary += f"{coin['name']} ({coin['symbol']}) - Market Cap Rank: {coin['market_cap_rank']}\n"

        # Portfolio report
        summary += "\n===== Portfolio Report =====\n"
        summary += f"\nPortfolio Value: ${portfolio_value:.2f}\nTotal Profit: ${portfolio_profit:.2f}\n\n"
        summary += "\nEarnings by Coin:\n"
        for coin, report in earnings_report.items():
            summary += f"{coin.capitalize()}: Current Price: ${report['current_price']:.2f}, Value: ${report['current_value']:.2f}, Investment: ${report['investment']:.2f}, Profit: ${report['profit']:.2f}\n"

        summary += "\nRecommendations:\n" + "\n".join(recommendations) + "\n"
        summary += "\nPredictions:\n"
        for coin, prediction in predictions.items():
            summary += f"{coin.capitalize()}: Predicted Price ${prediction}\n"

        # Suggest profitable coins
        summary += "\n===== Profitable Coins =====\n"
        profitable_coins = suggest_profitable_coins()

        if not profitable_coins:
            summary += "No profitable and safe coins found.\n"
        else:
            for rec in profitable_coins:
                summary += (
                    f"\nCoin: {rec['coin']}, Current Price: ${rec['current_price']:.2f}, "
                    f"Predicted Price: ${rec['predicted_price']:.2f}, "
                    f"Profit Potential: ${rec['profit_potential']:.2f}, "
                    f"Recommendation: {rec['recommendation']}\n"
                )

        # Top Crypto News
        summary += "\n===== Top Crypto News =====\n"
        for article in top_news:
            summary += f"{article['title']} - {article['link']}\n"

        # Write summary to the log file
        log.write(summary)

    return summary


def main():
    """
    Main function to run the bot and send the summary to Telegram.
    """
    try:
        summary = generate_summary()
        send_telegram_alert(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, summary)
        print(summary)  # Display the summary on the console
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()


