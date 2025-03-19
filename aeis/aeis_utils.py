# aeis/aeis_utils.py

import logging
import requests
from web3 import Web3
from aeis.aeis_config import load_config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def format_contribution(amount):
    """
    Format the contribution amount for display.

    :param amount: The contribution amount.
    :return: Formatted string representation of the amount.
    """
    return f"{amount:.2f} AEIT"

def log_event(message, level="INFO"):
    """
    Log an event with the specified message and level.

    :param message: The message to log.
    :param level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    if level == "DEBUG":
        logger.debug(message)
    elif level == "WARNING":
        logger.warning(message)
    elif level == "ERROR":
        logger.error(message)
    elif level == "CRITICAL":
        logger.critical(message)
    else:
        logger.info(message)

def validate_address(address):
    """
    Validate an Ethereum address.

    :param address: The Ethereum address to validate.
    :return: Boolean indicating whether the address is valid.
    """
    return Web3.isAddress(address)

def validate_contribution(amount):
    """
    Validate the contribution amount.

    :param amount: The contribution amount to validate.
    :return: Boolean indicating whether the amount is valid.
    """
    return isinstance(amount, (int, float)) and amount > 0

def fetch_external_data(api_url):
    """
    Fetch data from an external API.

    :param api_url: The URL of the API to fetch data from.
    :return: The fetched data as a JSON object.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        logger.info(f"Fetched data from {api_url}: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from {api_url}: {str(e)}")
        return None

def fetch_oracle_data(oracle_address):
    """
    Fetch data from an external oracle.

    :param oracle_address: The address of the oracle contract.
    :return: The fetched data.
    """
    # Placeholder for oracle integration logic
    # This function would interact with an oracle to fetch real-time data
    logger.info(f"Fetching data from oracle at {oracle_address}.")
    # Replace with actual data fetching logic
    return 0  # Replace with actual data

# Example usage
if __name__ == "__main__":
    # Test the utility functions
    address = "0x1234567890abcdef1234567890abcdef12345678"
    amount = 100.0

    if validate_address(address):
        log_event(f"Address {address} is valid.")
    else:
        log_event(f"Address {address} is invalid.", level="ERROR")

    if validate_contribution(amount):
        log_event(f"Contribution amount {format_contribution(amount)} is valid.")
    else:
        log_event(f"Contribution amount {amount} is invalid.", level="ERROR")

    # Fetch external data (example)
    api_url = "https://api.example.com/data"  # Replace with a real API URL
    data = fetch_external_data(api_url)
    print(data)
