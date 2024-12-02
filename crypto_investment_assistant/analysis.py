import pandas as pd


def analyze_data(market_data):
    """
    Analyze the market data to find the top gainers and losers.
    """
    # Convert market_data dictionary into a DataFrame
    df = pd.DataFrame.from_dict(market_data, orient='index')

    # Ensure the DataFrame has the necessary columns
    if "price_change_percentage_24h" not in df.columns:
        print("Error: Market data missing 'price_change_percentage_24h' column")
        return {"top_gainers": [], "top_losers": []}

    # Find the top 5 gainers and losers
    try:
        top_gainers = df.nlargest(5, "price_change_percentage_24h").to_dict(orient="records")
        top_losers = df.nsmallest(5, "price_change_percentage_24h").to_dict(orient="records")
    except Exception as e:
        print(f"Error analyzing data: {e}")
        return {"top_gainers": [], "top_losers": []}

    return {"top_gainers": top_gainers, "top_losers": top_losers}