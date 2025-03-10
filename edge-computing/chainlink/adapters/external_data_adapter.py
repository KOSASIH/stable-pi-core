# external_data_adapter.py

import requests
import logging

class ExternalDataAdapter:
    def __init__(self, data_source_url, api_key=None):
        """
        Initializes the ExternalDataAdapter.

        :param data_source_url: URL of the external data source
        :param api_key: Optional API key for authenticated requests
        """
        self.data_source_url = data_source_url
        self.api_key = api_key
        self.logger = self.setup_logging()

    def setup_logging(self):
        """
        Sets up logging for the adapter.

        :return: Logger instance
        """
        logger = logging.getLogger('ExternalDataAdapter')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('external_data_adapter.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def fetch_data(self, endpoint, params=None):
        """
        Fetches data from the external data source.

        :param endpoint: Specific endpoint to fetch data from
        :param params: Optional dictionary of query parameters
        :return: Parsed JSON response or None if an error occurs
        """
        try:
            headers = {}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'

            response = requests.get(f"{self.data_source_url}/{endpoint}", headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                self.logger.info(f"Fetched data from {endpoint}: {data}")
                return data
            else:
                self.logger.error(f"Failed to fetch data: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            self.logger.exception("An error occurred while fetching external data.")
            return None

    def get_market_data(self, symbol):
        """
        Fetches market data for a specific symbol.

        :param symbol: Symbol of the asset to fetch market data for
        :return: Market data as a dictionary or None if an error occurs
        """
        endpoint = "market_data"
        params = {"symbol": symbol}
        return self.fetch_data(endpoint, params)

    def get_weather_data(self, location):
        """
        Fetches weather data for a specific location.

        :param location: Location to fetch weather data for
        :return: Weather data as a dictionary or None if an error occurs
        """
        endpoint = "weather"
        params = {"location": location}
        return self.fetch_data(endpoint, params)

if __name__ == "__main__":
    # Example usage
    data_source_url = "https://api.example.com/data"  # Replace with actual data source URL
    api_key = "your_api_key_here"                      # Optional API key

    external_data_adapter = ExternalDataAdapter(data_source_url, api_key)

    # Fetch market data
    market_symbol = "BTC"
    market_data = external_data_adapter.get_market_data(market_symbol)
    print(f"Market data for {market_symbol}: {market_data}")

    # Fetch weather data
    location = "New York"
    weather_data = external_data_adapter.get_weather_data(location)
    print(f"Weather data for {location}: {weather_data}")
