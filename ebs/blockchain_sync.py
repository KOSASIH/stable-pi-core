# ebs/blockchain_sync.py

import logging
import requests
import json
import time

class BlockchainSync:
    def __init__(self, blockchain_url):
        """
        Initialize the BlockchainSync module.
        :param blockchain_url: The URL of the external blockchain network.
        """
        self.blockchain_url = blockchain_url
        self.max_sync_attempts = 5  # Default maximum sync attempts
        logging.info("Blockchain Synchronization module initialized.")

    def set_max_sync_attempts(self, attempts):
        """
        Set the maximum number of attempts to sync with the external network.
        :param attempts: Maximum sync attempts.
        """
        if attempts > 0:
            self.max_sync_attempts = attempts
            logging.info(f"Max sync attempts set to {self.max_sync_attempts}.")
        else:
            logging.error("Maximum sync attempts must be a positive integer.")
            raise ValueError("Maximum sync attempts must be a positive integer.")

    def sync_with_external_network(self, data):
        """
        Synchronize data with the external blockchain network.
        :param data: The data to synchronize.
        :return: Response from the blockchain network.
        """
        for attempt in range(1, self.max_sync_attempts + 1):
            try:
                logging.info(f"Attempting to sync data with external network (Attempt {attempt})...")
                response = requests.post(f"{self.blockchain_url}/sync", json=data)

                if response.status_code == 200:
                    logging.info("Data synchronized successfully.")
                    return response.json()
                else:
                    logging.warning(f"Failed to sync data: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Error during synchronization: {e}")

            time.sleep(2)  # Wait before retrying

        logging.error("Max sync attempts reached. Synchronization failed.")
        return None

    def get_blockchain_status(self):
        """
        Get the status of the external blockchain network.
        :return: Status information from the blockchain network.
        """
        try:
            response = requests.get(f"{self.blockchain_url}/status")
            if response.status_code == 200:
                logging.info("Blockchain status retrieved successfully.")
                return response.json()
            else:
                logging.warning(f"Failed to retrieve blockchain status: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving blockchain status: {e}")
            return None
