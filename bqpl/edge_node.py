# bqpl/edge_node.py

import numpy as np
from bqpl.quantum_resistant_encryption import QuantumResistantEncryption
from bqpl.biosensor import Biosensor
import logging

class EdgeNode:
    """
    Represents an edge node for processing biological data.
    """

    def __init__(self, node_id, encryption_params):
        """
        Initialize the edge node.

        :param node_id: Unique identifier for the edge node.
        :param encryption_params: Parameters for quantum-resistant encryption.
        """
        self.node_id = node_id
        self.encryption = QuantumResistantEncryption(**encryption_params)
        self.biosensor = Biosensor()
        logging.basicConfig(level=logging.INFO)

    def collect_data(self):
        """
        Collect data from the biosensor.
        """
        data = self.biosensor.read_data()
        logging.info(f"Edge Node {self.node_id}: Collected data: {data}")
        return data

    def process_data(self, data):
        """
        Process the collected data by encrypting it.

        :param data: The data to process (binary string).
        :return: The encrypted ciphertext.
        """
        logging.info(f"Edge Node {self.node_id}: Processing data...")
        ciphertext = self.encryption.encrypt(data)
        logging.info(f"Edge Node {self.node_id}: Encrypted data: {ciphertext}")
        return ciphertext

    def decrypt_data(self, ciphertext):
        """
        Decrypt the ciphertext to retrieve the original data.

        :param ciphertext: The encrypted data to decrypt.
        :return: The decrypted plaintext.
        """
        decrypted_data = self.encryption.decrypt(ciphertext)
        logging.info(f"Edge Node {self.node_id}: Decrypted data: {decrypted_data}")
        return decrypted_data

# Example usage
if __name__ == "__main__":
    # Define encryption parameters
    encryption_params = {
        'p': 3,
        'q': 32,
        'N': 11
    }

    # Create an edge node
    edge_node = EdgeNode(node_id="EdgeNode_1", encryption_params=encryption_params)

    # Collect data from the biosensor
    collected_data = edge_node.collect_data()

    # Process the collected data
    encrypted_data = edge_node.process_data(collected_data)

    # Decrypt the data
    decrypted_data = edge_node.decrypt_data(encrypted_data)
