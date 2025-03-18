import logging
from encryption import encrypt_data, decrypt_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EdgeNode:
    def __init__(self, quantum_key):
        """
        Initialize the EdgeNode with a quantum key.

        :param quantum_key: The quantum key used for encryption and decryption
        """
        self.quantum_key = quantum_key

    def process_data(self, data):
        """
        Process the incoming data by encrypting it with the quantum key.

        :param data: The data to be processed
        :return: Encrypted data
        """
        logging.info("Processing data...")
        encrypted_data = encrypt_data(data, self.quantum_key)
        logging.info("Data processed and encrypted successfully.")
        return encrypted_data

    def retrieve_data(self, encrypted_data):
        """
        Retrieve the original data by decrypting it with the quantum key.

        :param encrypted_data: The encrypted data to be decrypted
        :return: Original data
        """
        logging.info("Retrieving data...")
        original_data = decrypt_data(encrypted_data, self.quantum_key)
        logging.info("Data retrieved and decrypted successfully.")
        return original_data

if __name__ == "__main__":
    # Example usage
    quantum_key = "example_quantum_key"  # Replace with an actual quantum key
    edge_node = EdgeNode(quantum_key)

    data_to_process = "Sensitive information"
    encrypted_data = edge_node.process_data(data_to_process)
    print(f"Encrypted Data: {encrypted_data}")

    retrieved_data = edge_node.retrieve_data(encrypted_data)
    print(f"Retrieved Data: {retrieved_data}")
