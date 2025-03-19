import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Oracle:
    def __init__(self, oracle_url: str):
        """Initialize the oracle service."""
        self.oracle_url = oracle_url
        logging.info(f"Oracle service initialized at {oracle_url}")

    def get_price(self, asset: str) -> float:
        """Fetch the current price of an asset from the oracle."""
        logging.info(f"Fetching price for asset: {asset}")
        response = requests.get(f"{self.oracle_url}/price/{asset}")

        if response.status_code == 200:
            price_data = response.json()
            logging.info(f"Price for {asset} fetched successfully: {price_data['price']}")
            return price_data['price']
        else:
            logging.error(f"Failed to fetch price for {asset} with status code: {response.status_code}")
            return None

# Example usage
if __name__ == "__main__":
    oracle = Oracle(oracle_url="https://api.example.com/oracle")
    
    # Simulate fetching asset price
    price = oracle.get_price("ETH")
    print(f"Current ETH Price: {price}")
