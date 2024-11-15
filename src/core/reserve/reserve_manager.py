import random

class ReserveManager:
    def __init__(self):
        self.reserve_assets = {
            "USD": 1000000,  # Initial reserve in USD
            "BTC": 10,       # Initial reserve in Bitcoin
            "ETH": 100,      # Initial reserve in Ethereum
        }
        self.total_value = self.calculate_total_value()

    def calculate_total_value(self):
        # Simulate current market prices for assets
        current_prices = {
            "USD": 1,          # 1 USD
            "BTC": random.uniform(30000, 60000),  # Simulated BTC price
            "ETH": random.uniform(2000, 4000),    # Simulated ETH price
        }
        total_value = sum(self.reserve_assets[asset] * current_prices[asset] for asset in self.reserve_assets)
        return total_value

    def adjust_reserve(self, asset, amount):
        if asset in self.reserve_assets:
            self.reserve_assets[asset] += amount
            self.total_value = self.calculate_total_value()
            print(f"Adjusted {asset} reserve by {amount}. New reserve: {self.reserve_assets[asset]}")
        else:
            print(f"Asset {asset} not found in reserves.")

    def get_reserve_status(self):
        return self.reserve_assets, self.total_value

if __name__ == "__main__":
    reserve_manager = ReserveManager()
    print("Initial Reserve Status:", reserve_manager.get_reserve_status())
    reserve_manager.adjust_reserve("BTC", 1)  # Adjust BTC reserve
    print("Updated Reserve Status:", reserve_manager.get_reserve_status())
