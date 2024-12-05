from dotenv import load_dotenv
import os

# Load .env file
load_dotenv(dotenv_path='config.env')

# Securely access environment variables
headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
}

CRYPTO_PANIC_API_KEY = os.getenv("CRYPTO_PANIC_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")