def analyze_data(df):
    """
    Analyzes the DataFrame to find the top gainers and losers.
    """
    top_gainers = df.nlargest(5, "price_change_percentage_24h")
    top_losers = df.nsmallest(5, "price_change_percentage_24h")

    return {
        "top_gainers": top_gainers[["id", "current_price", "price_change_percentage_24h"]].to_dict(orient="records"),
        "top_losers": top_losers[["id", "current_price", "price_change_percentage_24h"]].to_dict(orient="records")
    }
