import time
import random

class PeggingMechanism:
    def __init__(self, target_price=314.159, adjustment_factor=0.01):
        self.target_price = target_price
        self.current_supply = 1000000  # Initial supply of Pi Coin
        self.adjustment_factor = adjustment_factor
        self.price_history = []

    def get_current_price(self):
        # Simulate price fluctuations
        simulated_price = self.target_price + random.uniform(-5, 5)
        self.price_history.append(simulated_price)
        return simulated_price

    def adjust_supply(self):
        current_price = self.get_current_price()
        price_difference = current_price - self.target_price

        if abs(price_difference) > self.target_price * 0.01:  # 1% threshold
            adjustment = int(price_difference * self.adjustment_factor)
            self.current_supply += adjustment
            print(f"Adjusted supply by {adjustment}. New supply: {self.current_supply}")

    def run_pegging_cycle(self):
        while True:
            self.adjust_supply()
            time.sleep(60)  # Adjust supply every minute

if __name__ == "__main__":
    pegging_mechanism = PeggingMechanism()
    pegging_mechanism.run_pegging_cycle()
