import requests
import json
from typing import Dict, Any

class BlockchainInterface:
    """
    A class to interact with the blockchain for logging biosensor data.

    Attributes:
        blockchain_url (str): The URL of the blockchain API.
        api_key (str): The API key for authentication.
    """

    def __init__(self, blockchain_url: str, api_key: str):
        self.blockchain_url = blockchain_url
        self.api_key = api_key

    def log_data(self, sensor_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Logs biosensor data to the blockchain.

        Args:
            sensor_id (str): The ID of the biosensor.
            data (Dict[str, Any]): The data to be logged.

        Returns:
            Dict[str, Any]: The response from the blockchain API.
        """
        url = f"{self.blockchain_url}/api/blockchain/smart_contracts/log_data"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "sensor_id": sensor_id,
            "timestamp": data["timestamp"],
            "value": data["value"],
            "unit": data["unit"]
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f"Failed to log data to blockchain: {response.text}")

        return response.json()


def log_data_to_blockchain(sensor_id: str, data: Dict[str, Any], blockchain_url: str, api_key: str) -> Dict[str, Any]:
    """
    Logs biosensor data to the blockchain using the BlockchainInterface.

    Args:
        sensor_id (str): The ID of the biosensor.
        data (Dict[str, Any]): The data to be logged.
        blockchain_url (str): The URL of the blockchain API.
        api_key (str): The API key for authentication.

    Returns:
        Dict[str, Any]: The response from the blockchain API.
    """
    blockchain_interface = BlockchainInterface(blockchain_url, api_key)
    return blockchain_interface.log_data(sensor_id, data)
