import asyncio
from telegram import Bot

async def send_telegram_alert_async(bot_token, chat_id, message):
    """
    Sends a message asynchronously via Telegram to a specific chat.
    """
    bot = Bot(token=bot_token)
    max_length = 4096  # Telegram's maximum message length

    # Send message in chunks if it exceeds the max length
    for i in range(0, len(message), max_length):
        try:
            await bot.send_message(chat_id=chat_id, text=message[i:i + max_length])
        except Exception as e:
            print(f"Error sending Telegram message: {e}")

def send_telegram_alert(bot_token, chat_id, message):
    """
    Wrapper function to call the asynchronous alert function.
    """
    asyncio.run(send_telegram_alert_async(bot_token, chat_id, message))

def check_price_alerts(market_data, alert_thresholds):
    for coin, price in market_data.items():
        if price >= alert_thresholds.get(coin, float('inf')):
            print(f"Alert: {coin} has reached {price}")