from analysis import calculate_indicators, analyze_news_sentiment

def make_recommendation(df):
    latest = df.iloc[-1]
    if latest["RSI"] < 30 and latest["MACD"] > latest["SIGNAL"]:
        return "Buy - Undervalued and bullish"
    elif latest["RSI"] > 70 and latest["MACD"] < latest["SIGNAL"]:
        return "Sell - Overbought and bearish"
    else:
        return "Hold - Neutral market"
