# src/generative_ai/data_collection.py

import requests
import logging

# Set up logging for the data collection module
logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self, api_url):
        """
        Initialize the Data Collector.

        Parameters:
        - api_url (str): The URL of the API to collect data from.
        """
        self.api_url = api_url
        logger.info(f"DataCollector initialized with API URL: {self.api_url}")

    def collect_data(self):
        """
        Collect data from the specified API.

        Returns:
        - dict: The collected data in JSON format.

        Raises:
        - Exception: If the data collection fails.
        """
        try:
            logger.info("Collecting data from API...")
            response = requests.get(self.api_url)
            response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
            data = response.json()
            logger.info("Data collection successful.")
            return data
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            raise
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Request error occurred: {req_err}")
            raise
        except ValueError as json_err:
            logger.error(f"Error parsing JSON response: {json_err}")
            raise
