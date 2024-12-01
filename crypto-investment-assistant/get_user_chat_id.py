import requests

# Replace with your Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7136936506:AAEYGzwg7MmhTHUQJ9g9p04bH9pgHJmTUKY"

# API URL to get updates
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
response = requests.get(url).json()

# Extract chat IDs from updates
for result in response.get("result", []):
    chat = result.get("message", {}).get("chat", {})
    print(f"Chat ID: {chat.get('id')} - Name: {chat.get('first_name') or chat.get('title')}")