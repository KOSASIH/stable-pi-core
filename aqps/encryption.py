from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Encryption:
    def __init__(self, key):
        """
        Initialize the Encryption class with a quantum key.

        :param key: The quantum key used for encryption and decryption
        """
        self.key = self._prepare_key(key)

    def _prepare_key(self, key):
        """
        Prepare the key for AES encryption by ensuring it is 16 bytes long.

        :param key: The original quantum key
        :return: A 16-byte key for AES
        """
        # Ensure the key is 16 bytes long (AES-128)
        return key.encode('utf-8')[:16].ljust(16, b'\0')

    def encrypt_data(self, data):
        """
        Encrypt the given data using AES encryption.

        :param data: The data to be encrypted
        :return: The encrypted data as a base64 encoded string
        """
        cipher = AES.new(self.key, AES.MODE_CBC)
        iv = cipher.iv
        encrypted = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        encrypted_data = base64.b64encode(iv + encrypted).decode('utf-8')
        logging.info("Data encrypted successfully.")
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        """
        Decrypt the given encrypted data using AES decryption.

        :param encrypted_data: The encrypted data as a base64 encoded string
        :return: The original data
        """
        raw_data = base64.b64decode(encrypted_data)
        iv = raw_data[:16]  # Extract the IV from the beginning
        encrypted = raw_data[16:]  # The rest is the encrypted data
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        original_data = decrypted.decode('utf-8')
        logging.info("Data decrypted successfully.")
        return original_data

# Example usage
if __name__ == "__main__":
    quantum_key = "example_quantum_key"  # Replace with an actual quantum key
    encryption = Encryption(quantum_key)

    data_to_encrypt = "Sensitive information"
    encrypted_data = encryption.encrypt_data(data_to_encrypt)
    print(f"Encrypted Data: {encrypted_data}")

    retrieved_data = encryption.decrypt_data(encrypted_data)
    print(f"Retrieved Data: {retrieved_data}")
