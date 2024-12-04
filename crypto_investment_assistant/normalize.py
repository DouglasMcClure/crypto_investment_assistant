import numpy as np

# Normalize historical prices
def normalize_prices(prices):
    if not prices or len(prices) == 0:
        raise ValueError("Price list is empty or invalid.")

    min_price = np.min(prices)
    max_price = np.max(prices)

    if min_price == max_price:
        print("Warning: All prices are the same. Returning zeros.")
        return [0.0] * len(prices)

    normalized = [(p - min_price) / (max_price - min_price) for p in prices]
    print(f"Debug: Normalized Prices: {normalized}")
    return normalized


def calculate_wma(prices, weights=None):
    if not weights:
        weights = range(1, len(prices) + 1)
    return np.sum(np.array(prices) * np.array(weights)) / np.sum(weights)


