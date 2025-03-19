import requests
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BlockchainIntegration:
    def __init__(self, blockchain_api_url):
        """
        Initialize the BlockchainIntegration class with the blockchain API URL.

        :param blockchain_api_url: URL of the blockchain service
        """
        self.blockchain_api_url = blockchain_api_url

    def log_transaction(self, transaction_data):
        """
        Log a transaction to the blockchain.

        :param transaction_data: A dictionary containing transaction details
        :return: The transaction ID if successful, None otherwise
        :raises Exception: If the request fails or the response is invalid
        """
        try:
            logging.info("Logging transaction to blockchain...")
            response = requests.post(f"{self.blockchain_api_url}/log_transaction", json=transaction_data)

            # Check if the response is successful
            if response.status_code == 200:
                transaction_response = response.json()
                if 'transaction_id' in transaction_response:
                    logging.info("Transaction logged successfully.")
                    return transaction_response['transaction_id']
                else:
                    logging.error("Invalid response format: 'transaction_id' not found.")
                    raise Exception("Invalid response format.")
            else:
                logging.error(f"Failed to log transaction: {response.status_code} - {response.text}")
                raise Exception(f"Request failed with status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception occurred: {e}")
            raise Exception("Error occurred while logging transaction.")

if __name__ == "__main__":
    # Example usage
    blockchain_api_url = "http://example-blockchain-api.com"  # Replace with actual blockchain API URL
    blockchain_integration = BlockchainIntegration(blockchain_api_url)

    # Example transaction data
    transaction_data = {
        "quantum_key": "example_quantum_key",
        "encrypted_data": "example_encrypted_data",
        "timestamp": "2023-10-01T12:00:00Z"
    }

    try:
        transaction_id = blockchain_integration.log_transaction(transaction_data)
        print(f"Transaction ID: {transaction_id}")
    except Exception as e:
        print(f"Error: {e}")
