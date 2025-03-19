import asyncio
import aiohttp
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OracleService:
    def __init__(self, oracle_urls: dict):
        """
        Initialize the OracleService with a dictionary of oracle URLs.
        :param oracle_urls: A dictionary where keys are asset names and values are oracle URLs.
        """
        self.oracle_urls = oracle_urls
        self.cache = {}
        self.cache_expiry = 60  # Cache expiry time in seconds

    async def fetch_price(self, session, asset: str) -> float:
        """
        Fetch the latest price for the specified asset from the oracle.
        :param session: The aiohttp session to use for the request.
        :param asset: The asset for which to fetch the price.
        :return: The latest price of the asset.
        """
        url = self.oracle_urls.get(asset)
        if not url:
            logger.error(f"No oracle URL found for asset: {asset}")
            return None

        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                price = data.get('price')
                logger.info(f"Fetched price for {asset}: {price}")
                return price
        except Exception as e:
            logger.error(f"Error fetching price for {asset}: {e}")
            return None

    async def get_price(self, asset: str) -> float:
        """
        Get the price for the specified asset, using cache if available.
        :param asset: The asset for which to get the price.
        :return: The latest price of the asset.
        """
        current_time = time.time()
        # Check if the price is cached and not expired
        if asset in self.cache and (current_time - self.cache[asset]['timestamp'] < self.cache_expiry):
            logger.info(f"Using cached price for {asset}: {self.cache[asset]['price']}")
            return self.cache[asset]['price']

        async with aiohttp.ClientSession() as session:
            price = await self.fetch_price(session, asset)
            if price is not None:
                # Cache the price with the current timestamp
                self.cache[asset] = {'price': price, 'timestamp': current_time}
            return price

# Example usage
async def main():
    oracle_urls = {
        "ETH": "https://api.example.com/oracle/eth",
        "BTC": "https://api.example.com/oracle/btc"
    }
    oracle_service = OracleService(oracle_urls)

    eth_price = await oracle_service.get_price("ETH")
    print(f"Current ETH price: {eth_price}")

    btc_price = await oracle_service.get_price("BTC")
    print(f"Current BTC price: {btc_price}")

if __name__ == "__main__":
    asyncio.run(main())
