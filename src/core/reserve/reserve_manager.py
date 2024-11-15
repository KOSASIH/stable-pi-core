import random
import requests
import json

class ReserveManager:
    def __init__(self):
        self.reserve_assets = {
            "USD": 1000000,  # Initial reserve in USD
            "BTC": 10,       # Initial reserve in Bitcoin
            "ETH": 100,      # Initial reserve in Ethereum
        }
        self.total_value = self.calculate_total_value()
        self.price_feed_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

    def fetch_current_prices(self):
        try:
            response = requests.get(self.price_feed_url)
            data = response.json()
            return {
                "BTC": data["bitcoin"]["usd"],
                "ETH": data["ethereum"]["usd"],
            }
        except Exception as e:
            print(f"Error fetching prices: {e}")
            return None

    def calculate_total_value(self):
        current_prices = self.fetch_current_prices()
        if current_prices is None:
            return None  # Handle error in price fetching

        total_value = self.reserve_assets["USD"]
        total_value += self.reserve_assets["BTC"] * current_prices["BTC"]
        total_value += self.reserve_assets["ETH"] * current_prices["ETH"]
        return total_value

    def adjust_reserve(self, asset, amount):
        if asset in self.reserve_assets:
            self.reserve_assets[asset] += amount
            self.total_value = self.calculate_total_value()
            print(f"Adjusted {asset} reserve by {amount}. New reserve: {self.reserve_assets[asset]}")
        else:
            print(f"Asset {asset} not found in reserves.")

    def rebalance_reserves(self, target_distribution):
        current_value = self.calculate_total_value()
        if current_value is None:
            print("Cannot rebalance due to price fetch error.")
            return

        for asset, target_percentage in target_distribution.items():
            target_value = current_value * target_percentage
            current_value_of_asset = self.reserve_assets[asset] * (self.fetch_current_prices().get(asset, 1) if asset != "USD" else 1)
            adjustment = target_value - current_value_of_asset
            self.adjust_reserve(asset, adjustment / (self.fetch_current_prices().get(asset, 1) if asset != "USD" else 1))

    def get_reserve_status(self):
        return self.reserve_assets, self.total_value

if __name__ == "__main__":
    reserve_manager = ReserveManager()
    print("Initial Reserve Status:", reserve_manager.get_reserve_status())
    reserve_manager.adjust_reserve("BTC", 1)  # Adjust BTC reserve
    print("Updated Reserve Status:", reserve_manager.get_reserve_status())
    target_distribution = {
        "USD": 0.5,
        "BTC": 0.3,
        "ETH": 0.2,
    }
    reserve_manager.rebalance_reserves(target_distribution)
    print("Rebalanced Reserve Status:", reserve_manager.get_reserve_status())
