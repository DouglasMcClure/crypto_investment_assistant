import time
import pandas as pd
from market_data import fetch_market_data
from fetch_historical_prices import fetch_historical_prices
from analysis import calculate_indicators
from predictor import predict_prices
from recommendations import make_recommendation
import io

log_file = "crypto_logs.txt"

def suggest_profitable_coins():
    try:
        with io.open(log_file, "a", encoding="utf-8") as log:
            market_data = fetch_market_data()
            if market_data.empty:
                log.write("Market data is empty. Cannot suggest profitable coins.\n")
                return []

            batch_size = 10
            recommendations = []
            profit_threshold = 0.1  # Lower threshold for more results

            for i in range(0, len(market_data), batch_size):
                batch = market_data.iloc[i:i + batch_size]
                log.write(f"Processing batch: {i // batch_size + 1}\n")
                for _, coin in batch.iterrows():
                    coin_id = coin['id']
                    try:
                        log.write(f"Processing coin: {coin_id}\n")
                        historical_prices = fetch_historical_prices(coin_id)
                        if historical_prices.empty or len(historical_prices) < 30:
                            log.write(f"Insufficient historical data for {coin_id}. Skipping.\n")
                            continue

                        indicators = calculate_indicators(historical_prices)
                        if indicators.empty:
                            log.write(f"Failed to calculate indicators for {coin_id}. Skipping.\n")
                            continue

                        recommendation = make_recommendation(indicators)
                        predicted_price = predict_prices(historical_prices)
                        if predicted_price is None:
                            log.write(f"Prediction failed for {coin_id}. Skipping.\n")
                            continue

                        current_price = coin['current_price']
                        profit_potential = predicted_price - current_price
                        log.write(f"Profit Potential: {profit_potential}, Recommendation: {recommendation}\n")

                        if recommendation.startswith("Buy") and profit_potential > profit_threshold:
                            recommendations.append({
                                "coin": coin_id,
                                "current_price": current_price,
                                "predicted_price": predicted_price,
                                "profit_potential": profit_potential,
                                "recommendation": recommendation
                            })
                        else:
                            log.write(
                                f"Coin: {coin_id} excluded. Profit Potential: {profit_potential}, "
                                f"Recommendation: {recommendation}, Threshold: {profit_threshold}\n"
                            )

                    except Exception as e:
                        log.write(f"Error processing coin {coin_id}: {e}\n")

                time.sleep(5)

            sorted_recommendations = sorted(recommendations, key=lambda x: x['profit_potential'], reverse=True)
            log.write(f"Generated {len(sorted_recommendations)} profitable and safe coin recommendations.\n")
            return sorted_recommendations

    except Exception as e:
        with io.open(log_file, "a", encoding="utf-8") as log:
            log.write(f"Error in suggest_profitable_coins: {e}\n")
        return []
