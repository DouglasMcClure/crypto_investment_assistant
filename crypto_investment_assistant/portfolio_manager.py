class PortfolioManager:
    def __init__(self):
        self.holdings = {}  # Format: {"coin": {"amount": float, "buy_price": float}}

    def add_holding(self, coin, amount, buy_price):
        self.holdings[coin] = {"amount": amount, "buy_price": buy_price}




    def calculate_profit_loss(self, market_data):
        total_value = 0
        for coin, details in self.holdings.items():
            current_price = market_data.get(coin, {}).get("current_price", None)
            if current_price is not None:
                total_value += current_price * details["amount"]
            else:
                print(f"Warning: Current price for {coin} not found in market data.")
        return total_value

