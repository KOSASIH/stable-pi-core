# price_feed_adapter.py

import requests
import json
import logging

class PriceFeedAdapter:
    def __init__(self, oracle_url, asset_symbol, api_key=None):
        """
        Initializes the PriceFeedAdapter.

        :param oracle_url: URL of the price feed oracle
        :param asset_symbol: Symbol of the asset to fetch price for (e.g., 'ETH', 'BTC')
        :param api_key: Optional API key for authenticated requests
        """
        self.oracle_url = oracle_url
        self.asset_symbol = asset_symbol
        self.api_key = api_key
        self.logger = self.setup_logging()

    def setup_logging(self):
        """
        Sets up logging for the adapter.

        :return: Logger instance
        """
        logger = logging.getLogger('PriceFeedAdapter')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('price_feed_adapter.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def fetch_price(self):
        """
        Fetches the latest price for the specified asset from the oracle.

        :return: Latest price as a float, or None if an error occurs
        """
        try:
            headers = {}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'

            response = requests.get(f"{self.oracle_url}/price/{self.asset_symbol}", headers=headers)

            if response.status_code == 200:
                price_data = response.json()
                price = price_data.get('price')
                self.logger.info(f"Fetched price for {self.asset_symbol}: {price}")
                return price
            else:
                self.logger.error(f"Failed to fetch price: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            self.logger.exception("An error occurred while fetching price data.")
            return None

    def convert_price(self, amount, target_currency):
        """
        Converts the given amount from the asset's price to the target currency.

        :param amount: Amount of the asset
        :param target_currency: Currency to convert to (e.g., 'USD')
        :return: Converted amount as a float, or None if an error occurs
        """
        try:
            price = self.fetch_price()
            if price is None:
                return None

            # Assuming the price is in USD for this example
            converted_amount = amount * price
            self.logger.info(f"Converted {amount} {self.asset_symbol} to {converted_amount} {target_currency}")
            return converted_amount
        except Exception as e:
            self.logger.exception("An error occurred during price conversion.")
            return None

if __name__ == "__main__":
    # Example usage
    oracle_url = "https://api.example.com/oracle"  # Replace with actual oracle URL
    asset_symbol = "ETH"                            # Example asset symbol
    api_key = "your_api_key_here"                  # Optional API key

    price_feed_adapter = PriceFeedAdapter(oracle_url, asset_symbol, api_key)
    latest_price = price_feed_adapter.fetch_price()
    print(f"Latest price for {asset_symbol}: {latest_price}")

    amount = 2.0  # Example amount of asset
    target_currency = "USD"
    converted_amount = price_feed_adapter.convert_price(amount, target_currency)
    print(f"{amount} {asset_symbol} is equivalent to {converted_amount} {target_currency}")
