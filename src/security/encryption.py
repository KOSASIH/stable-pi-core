# src/security/encryption.py

import logging
from cryptography.fernet import Fernet

# Set up logging for the encryption module
logger = logging.getLogger(__name__)

class Encryption:
    def __init__(self):
        """Initialize the Encryption class and generate a key."""
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        logger.info("Encryption initialized with a new key.")

    def encrypt(self, data):
        """
        Encrypt the given data.

        Parameters:
        - data (str): The data to encrypt.

        Returns:
        - str: The encrypted data.
        """
        encrypted_data = self.cipher.encrypt(data.encode())
        logger.info("Data encrypted successfully.")
        return encrypted_data.decode()

    def decrypt(self, encrypted_data):
        """
        Decrypt the given encrypted data.

        Parameters:
        - encrypted_data (str): The data to decrypt.

        Returns:
        - str: The decrypted data.
        """
        decrypted_data = self.cipher.decrypt(encrypted_data.encode())
        logger.info("Data decrypted successfully.")
        return decrypted_data.decode()

    def get_key(self):
        """
        Get the encryption key.

        Returns:
        - str: The encryption key.
        """
        return self.key.decode()
