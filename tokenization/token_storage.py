# tokenization/token_storage.py

import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TokenStorage:
    def __init__(self, blockchain_url):
        """
        Initialize the TokenStorage with the blockchain URL.
        
        :param blockchain_url: The URL of the blockchain API.
        """
        self.blockchain_url = blockchain_url

    def store_token(self, token, metadata):
        """
        Store a token in the blockchain along with its metadata.
        
        :param token: The token to store.
        :param metadata: Additional metadata associated with the token.
        :return: Response from the blockchain API.
        """
        payload = {
            "token": token,
            "metadata": metadata
        }
        
        try:
            response = requests.post(f"{self.blockchain_url}/store_token", json=payload)
            response.raise_for_status()  # Raise an error for bad responses
            logging.info(f"Token stored successfully: {token}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to store token: {e}")
            return None

    def retrieve_token(self, token_id):
        """
        Retrieve a token from the blockchain using its identifier.
        
        :param token_id: The identifier of the token to retrieve.
        :return: The token data if found, otherwise None.
        """
        try:
            response = requests.get(f"{self.blockchain_url}/retrieve_token/{token_id}")
            response.raise_for_status()  # Raise an error for bad responses
            logging.info(f"Token retrieved successfully: {token_id}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to retrieve token: {e}")
            return None

if __name__ == "__main__":
    # Example usage
    blockchain_url = "http://localhost:5000/api"  # Replace with your blockchain API URL
    token_storage = TokenStorage(blockchain_url)

    # Sample token and metadata
    token = "example_token_123456"
    metadata = {
        "owner": "user_001",
        "timestamp": 1633072800,
        "data_type": "DNA",
        "description": "Sample DNA sequence token"
    }

    # Store the token
    store_response = token_storage.store_token(token, metadata)
    print("Store Response:", store_response)

    # Retrieve the token
    token_id = "example_token_123456"  # Replace with the actual token ID
    retrieve_response = token_storage.retrieve_token(token_id)
    print("Retrieve Response:", retrieve_response)
