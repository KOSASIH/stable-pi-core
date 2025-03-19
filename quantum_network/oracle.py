# quantum_network/oracle.py

import hashlib
import json
from typing import Any, Dict

class QuantumOracle:
    def __init__(self):
        """
        Initialize the Quantum Oracle.
        This oracle will manage data interactions and provide secure access.
        """
        self.data_store: Dict[str, Any] = {}  # Store data with unique keys
        self.blockchain: list = []              # Simulated blockchain

    def update_data(self, key: str, value: Any) -> str:
        """
        Update data in the oracle and add a new block to the blockchain.

        Args:
            key (str): Unique key for the data.
            value (Any): The data to store.

        Returns:
            str: The hash of the new block added to the blockchain.
        """
        # Store the data
        self.data_store[key] = value
        print(f"Oracle: Updated data for key '{key}' with value '{value}'.")

        # Create a new block and add it to the blockchain
        block = self.create_block(key, value)
        self.blockchain.append(block)
        print(f"Oracle: Added new block to blockchain: {block}")

        return block['hash']

    def fetch_data(self, key: str) -> Any:
        """
        Fetch data from the oracle.

        Args:
            key (str): The key for the data to retrieve.

        Returns:
            Any: The retrieved data or None if not found.
        """
        value = self.data_store.get(key)
        if value is not None:
            print(f"Oracle: Retrieved data for key '{key}': '{value}'.")
        else:
            print(f"Oracle: No data found for key '{key}'.")
        return value

    def validate_data(self, key: str, value: Any) -> bool:
        """
        Validate the data against the stored value.

        Args:
            key (str): The key for the data.
            value (Any): The value to validate.

        Returns:
            bool: True if the value matches the stored data, False otherwise.
        """
        stored_value = self.data_store.get(key)
        is_valid = stored_value == value
        print(f"Oracle: Validation for key '{key}' with value '{value}': {is_valid}.")
        return is_valid

    def create_block(self, key: str, value: Any) -> Dict[str, Any]:
        """
        Create a new block for the blockchain.

        Args:
            key (str): The key for the data.
            value (Any): The value to store in the block.

        Returns:
            Dict[str, Any]: The new block containing the key, value, and hash.
        """
        block = {
            'key': key,
            'value': value,
            'previous_hash': self.get_latest_block_hash(),
            'hash': self.hash_data(key, value)
        }
        return block

    def get_latest_block_hash(self) -> str:
        """
        Get the hash of the latest block in the blockchain.

        Returns:
            str: The hash of the latest block or '0' if no blocks exist.
        """
        if not self.blockchain:
            return '0'
        return self.blockchain[-1]['hash']

    @staticmethod
    def hash_data(key: str, value: Any) -> str:
        """
        Create a SHA-256 hash of the key and value.

        Args:
            key (str): The key for the data.
            value (Any): The value to hash.

        Returns:
            str: The SHA-256 hash of the key and value.
        """
        data = json.dumps({'key': key, 'value': value}, sort_keys=True).encode()
        return hashlib.sha256(data).hexdigest()

# Example usage
if __name__ == "__main__":
    oracle = QuantumOracle()

    # Update data in the oracle
    oracle.update_data("quantum_key_1", "super_secret_key_123")

    # Fetch data from the oracle
    oracle.fetch_data("quantum_key_1")

    # Validate data
    oracle.validate_data("quantum_key_1", "super_secret_key_123")
    oracle.validate_data("quantum_key_1", "wrong_key")
