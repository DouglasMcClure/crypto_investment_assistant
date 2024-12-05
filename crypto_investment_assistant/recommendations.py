import io
log_file = "crypto_logs.txt"

def make_recommendation(df):
    try:
        latest = df.iloc[-1]
        recommendation = None
        if latest["RSI"] < 40 and latest["MACD"] > latest["SIGNAL"]:
            recommendation = "Buy - Bullish trend forming"
        elif latest["RSI"] > 60 and latest["MACD"] < latest["SIGNAL"]:
            recommendation = "Sell - Bearish trend forming"
        else:
            recommendation = "Hold - Neutral market"

        with io.open(log_file, "a", encoding="utf-8") as log:
            log.write(f"Recommendation based on latest data: {recommendation}\n")
        return recommendation
    except Exception as e:
        with io.open(log_file, "a", encoding="utf-8") as log:
            log.write(f"Error in make_recommendation: {e}\n")
        return "Hold - Neutral market"
