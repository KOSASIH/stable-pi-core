# tokenization/token_generator.py

import hashlib
import os
import json
from cryptography.fernet import Fernet
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TokenGenerator:
    def __init__(self, encryption_key=None):
        """
        Initialize the TokenGenerator with an optional encryption key.
        
        :param encryption_key: A key for encrypting and decrypting data. If None, a new key will be generated.
        """
        if encryption_key is None:
            self.encryption_key = Fernet.generate_key()
            logging.info("Generated new encryption key.")
        else:
            self.encryption_key = encryption_key
        
        self.cipher = Fernet(self.encryption_key)

    def generate_token(self, data):
        """
        Generate a unique token for the given data.
        
        :param data: The data to tokenize (e.g., biological data).
        :return: A token representing the data.
        """
        # Convert data to JSON string
        data_json = json.dumps(data, sort_keys=True).encode()
        
        # Create a hash of the data
        token = hashlib.sha256(data_json).hexdigest()
        logging.info(f"Generated token: {token} for data: {data}")
        return token

    def encrypt_data(self, data):
        """
        Encrypt the given data using the encryption key.
        
        :param data: The data to encrypt.
        :return: Encrypted data.
        """
        data_json = json.dumps(data).encode()
        encrypted_data = self.cipher.encrypt(data_json)
        logging.info("Data encrypted successfully.")
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        """
        Decrypt the given encrypted data.
        
        :param encrypted_data: The encrypted data to decrypt.
        :return: Decrypted data.
        """
        decrypted_data = self.cipher.decrypt(encrypted_data)
        logging.info("Data decrypted successfully.")
        return json.loads(decrypted_data)

if __name__ == "__main__":
    # Example usage
    token_generator = TokenGenerator()

    # Sample biological data
    biological_data = {
        "id": "bio_001",
        "type": "DNA",
        "sequence": "ATCGTAGCTAGCTAGCTAGC",
        "timestamp": 1633072800
    }

    # Generate token
    token = token_generator.generate_token(biological_data)

    # Encrypt data
    encrypted_data = token_generator.encrypt_data(biological_data)

    # Decrypt data
    decrypted_data = token_generator.decrypt_data(encrypted_data)

    print(f"Token: {token}")
    print(f"Encrypted Data: {encrypted_data}")
    print(f"Decrypted Data: {decrypted_data}")
