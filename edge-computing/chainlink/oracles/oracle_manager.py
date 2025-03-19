import asyncio
import logging
import json
import aiohttp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OracleManager:
    def __init__(self, oracle_endpoints):
        """
        Initialize the OracleManager with a list of oracle endpoints.
        
        :param oracle_endpoints: List of oracle service URLs
        """
        self.oracle_endpoints = oracle_endpoints

    async def fetch_data(self, session, endpoint):
        """
        Fetch data from a single oracle endpoint.
        
        :param session: aiohttp session
        :param endpoint: Oracle service URL
        :return: Parsed JSON response or None if failed
        """
        try:
            async with session.get(endpoint) as response:
                response.raise_for_status()  # Raise an error for bad responses
                data = await response.json()
                logger.info(f"Data fetched from {endpoint}: {data}")
                return data
        except Exception as e:
            logger.error(f"Error fetching data from {endpoint}: {e}")
            return None

    async def fetch_all_data(self):
        """
        Fetch data from all configured oracle endpoints concurrently.
        
        :return: List of responses from all oracles
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_data(session, endpoint) for endpoint in self.oracle_endpoints]
            results = await asyncio.gather(*tasks)
            return [result for result in results if result is not None]

    def get_latest_data(self):
        """
        Public method to fetch the latest data from all oracles.
        
        :return: List of latest data from all oracles
        """
        loop = asyncio.get_event_loop()
        latest_data = loop.run_until_complete(self.fetch_all_data())
        return latest_data

if __name__ == "__main__":
    # Example usage
    oracle_endpoints = [
        "https://api.oracle1.com/data",
        "https://api.oracle2.com/data",
        "https://api.oracle3.com/data"
    ]
    
    oracle_manager = OracleManager(oracle_endpoints)
    latest_data = oracle_manager.get_latest_data()
    
    # Output the latest data
    print(json.dumps(latest_data, indent=4))
