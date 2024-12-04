import requests

class PortfolioManager:
    def __init__(self):
        self.holdings = {}  # Format: {"coin_id": {"amount": float, "buy_price": float}}

    def add_holding(self, coin_id, amount, buy_price):
        """
        Add or update holdings for a coin. Combines amounts if the coin already exists.
        """
        if coin_id in self.holdings:
            existing = self.holdings[coin_id]
            total_amount = existing["amount"] + amount
            # Weighted average buy price
            total_investment = (existing["amount"] * existing["buy_price"]) + (amount * buy_price)
            weighted_buy_price = total_investment / total_amount
            self.holdings[coin_id] = {"amount": total_amount, "buy_price": weighted_buy_price}
        else:
            self.holdings[coin_id] = {"amount": amount, "buy_price": buy_price}

    def fetch_holdings(self):
        """
        Fetch real-time prices and additional data for all holdings.
        """
        if not self.holdings:
            print("No holdings to fetch.")
            return {}

        coin_ids = ",".join(self.holdings.keys())
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_ids}&vs_currencies=usd"
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": "CG-ox3aZDyf2EQVJp12UswYZ48s"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching holdings data. Status code: {response.status_code}")
            return {}

        data = response.json()
        for coin in self.holdings.keys():
            if coin not in data:
                print(f"Warning: No price data for {coin}. Response: {response.text}")
        return data

    def calculate_profit_loss(self, market_data):
        """
        Calculate the total portfolio value, total investment, and earnings for each holding.
        """
        current_price = 0
        total_value = 0
        total_investment = 0
        earnings_report = {}

        for coin, details in self.holdings.items():
            coin_data = market_data.get(coin, {})
            current_price = coin_data.get("usd", None)

            if current_price is not None:
                coin_value = current_price * details["amount"]
                coin_investment = details["buy_price"] * details["amount"]
                coin_profit = coin_value - coin_investment

                total_value += coin_value
                total_investment += coin_investment
                earnings_report[coin] = {
                    "current_price": current_price,
                    "current_value": coin_value,
                    "investment": coin_investment,
                    "profit": coin_profit
                }
            else:
                print(f"Warning: No price data for {coin}. Market data: {coin_data}")

        total_profit = total_value - total_investment
        return total_value, total_profit, earnings_report

