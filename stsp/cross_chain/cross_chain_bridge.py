# stsp/cross_chain/cross_chain_bridge.py

import logging
import requests

class CrossChainBridge:
    """
    Implements the cross-chain bridge functionality for transferring data
    between different blockchain networks.
    """

    def __init__(self, source_chain_url, target_chain_url):
        """
        Initialize the CrossChainBridge instance.

        :param source_chain_url: The API URL for the source blockchain.
        :param target_chain_url: The API URL for the target blockchain.
        """
        self.source_chain_url = source_chain_url
        self.target_chain_url = target_chain_url
        logging.info("CrossChainBridge initialized with Source: %s and Target: %s", source_chain_url, target_chain_url)

    def transfer_data(self, data):
        """
        Transfer data from the source blockchain to the target blockchain.

        :param data: The data to transfer.
        :return: Response from the target blockchain.
        """
        try:
            # Send data to the target blockchain
            response = requests.post(f"{self.target_chain_url}/receive_data", json=data)
            response.raise_for_status()  # Raise an error for bad responses
            logging.info("Data transferred successfully to target blockchain: %s", data)
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error("Failed to transfer data to target blockchain: %s", e)
            raise

    def fetch_data(self):
        """
        Fetch data from the source blockchain.

        :return: The fetched data from the source blockchain.
        """
        try:
            response = requests.get(f"{self.source_chain_url}/fetch_data")
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            logging.info("Data fetched successfully from source blockchain: %s", data)
            return data
        except requests.exceptions.RequestException as e:
            logging.error("Failed to fetch data from source blockchain: %s", e)
            raise

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    source_chain_url = "http://localhost:5001/api/source"  # Replace with actual source chain API URL
    target_chain_url = "http://localhost:5002/api/target"  # Replace with actual target chain API URL
    bridge = CrossChainBridge(source_chain_url, target_chain_url)

    # Simulate fetching data from the source blockchain
    data_to_transfer = bridge.fetch_data()

    # Simulate transferring data to the target blockchain
    response = bridge.transfer_data(data_to_transfer)
    print(f"Response from Target Blockchain: {response}")
