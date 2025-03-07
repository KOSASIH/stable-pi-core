import time
import random
import logging
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PeggingMechanism:
    def __init__(self, config_file='config.json'):
        self.load_config(config_file)
        self.current_supply = 1000000  # Initial supply of Pi Coin
        self.price_history = []

    def load_config(self, config_file):
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.target_price = config.get('target_price', 314159.00)
                self.adjustment_factor = config.get('adjustment_factor', 0.01)
                self.price_fluctuation_range = config.get('price_fluctuation_range', 5)
        else:
            logging.warning(f"Config file {config_file} not found. Using default values.")
            self.target_price = 314159.00
            self.adjustment_factor = 0.01
            self.price_fluctuation_range = 5

    def get_current_price(self):
        # Simulate price fluctuations
        simulated_price = self.target_price + random.uniform(-self.price_fluctuation_range, self.price_fluctuation_range)
        self.price_history.append(simulated_price)
        logging.info(f"Current simulated price: {simulated_price:.2f}")
        return simulated_price

    def adjust_supply(self):
        current_price = self.get_current_price()
        price_difference = current_price - self.target_price

        # Adjust supply based on price difference and a simulated demand factor
        demand_factor = random.uniform(0.8, 1.2)  # Simulate demand fluctuations
        adjustment = int(price_difference * self.adjustment_factor * demand_factor)

        if abs(price_difference) > self.target_price * 0.01:  # 1% threshold
            self.current_supply += adjustment
            logging.info(f"Adjusted supply by {adjustment}. New supply: {self.current_supply}")

    def save_data(self):
        with open('price_history.json', 'w') as f:
            json.dump(self.price_history, f)
        logging.info("Price history saved.")

    def run_pegging_cycle(self):
        try:
            while True:
                self.adjust_supply()
                time.sleep(60)  # Adjust supply every minute
        except KeyboardInterrupt:
            logging.info("Pegging cycle stopped by user.")
            self.save_data()
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            self.save_data()

if __name__ == "__main__":
    pegging_mechanism = PeggingMechanism()
    logging.info("Starting pegging mechanism...")
    pegging_mechanism.run_pegging_cycle()
