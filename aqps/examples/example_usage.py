from aqps.qkd_client import QKDClient
from aqps.edge_node import EdgeNode
from aqps.encryption import Encryption
from aqps.blockchain_integration import BlockchainIntegration
from aqps.config import Config

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
    data_to_encrypt = "Sensitive information"
    
    # Encrypt the data
    encrypted_data = encryption.encrypt_data(data_to_encrypt)
    print(f"Encrypted Data: {encrypted_data}")

    # Decrypt the data
    decrypted_data = encryption.decrypt_data(encrypted_data)
    print(f"Decrypted Data: {decrypted_data}")

    # Initialize the edge node
    edge_node = EdgeNode(quantum_key)

    # Process data with the edge node
    processed_data = edge_node.process_data(data_to_encrypt)
    print(f"Processed Data: {processed_data}")

    # Log transaction to the blockchain
    blockchain = BlockchainIntegration(Config.BLOCKCHAIN_API_URL)
    transaction_data = {
        "quantum_key": quantum_key,
        "encrypted_data": encrypted_data,
        "timestamp": "2023-10-01T12:00:00Z"
    }

    try:
        transaction_id = blockchain.log_transaction(transaction_data)
        print(f"Transaction ID: {transaction_id}")
    except Exception as e:
        print(f"Error logging transaction: {e}")

if __name__ == "__main__":
    main()
