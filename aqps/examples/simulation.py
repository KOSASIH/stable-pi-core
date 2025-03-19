import random
import time
from aqps.qkd_client import QKDClient
from aqps.edge_node import EdgeNode
from aqps.encryption import Encryption
from aqps.config import Config

def simulate_space_conditions():
    # Simulate the delay and noise typical in space communication
    time.sleep(random.uniform(0.5, 2.0))  # Simulate variable latency
    if random.random() < 0.1:  # 10% chance of noise
        raise Exception("Simulated noise in communication")

def main():
    # Initialize the QKD client
    qkd_client = QKDClient(Config.SATELLITE_API_URL)

    # Request a quantum key
    try:
        quantum_key = qkd_client.request_quantum_key()
        print(f"Quantum Key: {quantum_key}")
    except Exception as e:
        print(f"Error retrieving quantum key: {e}")
        return

    # Initialize the encryption module
    encryption = Encryption(quantum_key)

    # Example data to encrypt
    data_to_encrypt = "Sensitive information for simulation"

    # Simulate space conditions
    try:
        simulate_space_conditions()
        
        # Encrypt the data
        encrypted_data = encryption.encrypt_data(data_to_encrypt)
        print(f"Encrypted Data: {encrypted_data}")

        # Simulate space conditions again
        simulate_space_conditions()

        # Decrypt the data
        decrypted_data = encryption.decrypt_data(encrypted_data)
        print(f"Decrypted Data: {decrypted_data}")

        # Initialize the edge node
        edge_node = EdgeNode(quantum_key)

        # Process data with the edge node
        processed_data = edge_node.process_data(data_to_encrypt)
        print(f"Processed Data: {processed_data}")

    except Exception as e:
        print(f"Simulation error: {e}")

if __name__ == "__main__":
    main()
