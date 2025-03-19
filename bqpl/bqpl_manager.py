# bqpl/bqpl_manager.py

import logging
from bqpl.edge_node import EdgeNode
from bqpl.biosensor import Biosensor

class BQPLManager:
    """
    Manages interactions between components of the Bio-Quantum Privacy Layer (BQPL).
    """

    def __init__(self, node_id, sensor_id, encryption_params):
        """
        Initialize the BQPL Manager.

        :param node_id: Unique identifier for the edge node.
        :param sensor_id: Unique identifier for the biosensor.
        :param encryption_params: Parameters for quantum-resistant encryption.
        """
        self.edge_node = EdgeNode(node_id, encryption_params)
        self.biosensor = Biosensor(sensor_id)
        logging.basicConfig(level=logging.INFO)

    def collect_and_process_data(self):
        """
        Collect data from the biosensor and process it through the edge node.
        """
        # Step 1: Collect data from the biosensor
        data = self.biosensor.read_data()
        
        # Convert the collected data to a binary string for encryption
        binary_data = self.convert_data_to_binary(data)

        # Step 2: Process the data (encrypt it)
        encrypted_data = self.edge_node.process_data(binary_data)

        return encrypted_data

    def convert_data_to_binary(self, data):
        """
        Convert collected biological data to a binary string.

        :param data: The collected biological data.
        :return: A binary string representation of the data.
        """
        # For simplicity, we will convert heart rate and temperature to a binary string
        heart_rate_binary = format(data['heart_rate'], '08b')  # 8 bits for heart rate
        temperature_binary = format(int((data['temperature'] - 36) * 100), '08b')  # Scale temperature

        # Combine the binary representations
        binary_string = heart_rate_binary + temperature_binary
        logging.info(f"Converted data to binary: {binary_string}")
        return binary_string

    def decrypt_data(self, encrypted_data):
        """
        Decrypt the encrypted data using the edge node.

        :param encrypted_data: The encrypted data to decrypt.
        :return: The decrypted plaintext data.
        """
        decrypted_data = self.edge_node.decrypt_data(encrypted_data)
        return decrypted_data

# Example usage
if __name__ == "__main__":
    # Define encryption parameters
    encryption_params = {
        'p': 3,
        'q': 32,
        'N': 11
    }

    # Create a BQPL Manager instance
    bqpl_manager = BQPLManager(node_id="EdgeNode_1", sensor_id="Biosensor_1", encryption_params=encryption_params)

    # Collect and process data
    encrypted_data = bqpl_manager.collect_and_process_data()
    print(f"Encrypted Data: {encrypted_data}")

    # Decrypt the data
    decrypted_data = bqpl_manager.decrypt_data(encrypted_data)
    print(f"Decrypted Data: {decrypted_data}")
