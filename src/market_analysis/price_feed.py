# src/market_analysis/price_feed.py

import requests
import logging

# Set up logging for the price feed module
logger = logging.getLogger(__name__)

class PriceFeed:
    def __init__(self, oracles):
        """
        Initialize the Price Feed.

        Parameters:
        - oracles (list): A list of oracle URLs to retrieve price data from.
        """
        self.oracles = oracles
        logger.info("PriceFeed initialized with oracles: %s", self.oracles)

    def get_prices(self):
        """
        Retrieve prices from all configured oracles.

        Returns:
        - list: A list of prices retrieved from the oracles.

        Raises:
        - Exception: If price retrieval fails.
        """
        prices = []
        for oracle in self.oracles:
            try:
                logger.info(f"Fetching price from oracle: {oracle}")
                response = requests.get(oracle)
                response.raise_for_status()  # Raise an error for bad responses
                price_data = response.json()
                prices.append(price_data['price'])  # Assuming the price is in the 'price' key
            except Exception as e:
                logger.error(f"Error fetching price from {oracle}: {e}")
                continue  # Skip this oracle and continue with the next one
        return prices
