# wdb/data_transfer.py

import asyncio
import zlib
from cryptography.fernet import Fernet
from .logger import Logger

class DataTransferError(Exception):
    """Custom exception for Data Transfer errors."""
    pass

class DataTransferProtocol:
    def __init__(self, encryption_key=None):
        self.transfers = []
        self.logger = Logger()
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)

    def compress_data(self, data):
        """
        Compresses the data using zlib.
        
        Args:
            data (str): The data to be compressed.

        Returns:
            bytes: The compressed data.
        """
        compressed_data = zlib.compress(data.encode())
        self.logger.log("Data compressed successfully.")
        return compressed_data

    def encrypt_data(self, data):
        """
        Encrypts the data using Fernet symmetric encryption.
        
        Args:
            data (bytes): The data to be encrypted.

        Returns:
            bytes: The encrypted data.
        """
        encrypted_data = self.cipher.encrypt(data)
        self.logger.log("Data encrypted successfully.")
        return encrypted_data

    async def initiate_transfer(self, source, destination, data):
        """
        Initiates the transfer process from source to destination.
        
        Args:
            source (str): The source node.
            destination (str): The destination node.
            data (str): The data to be transferred.

        Returns:
            str: The result of the transfer.
        """
        self.logger.log(f"Initiating transfer from {source} to {destination}.")
        try:
            # Compress and encrypt the data
            compressed_data = self.compress_data(data)
            encrypted_data = self.encrypt_data(compressed_data)

            # Simulate transfer delay
            await asyncio.sleep(1)  # Simulate network delay

            # Store the transfer details
            self.transfers.append((source, destination, encrypted_data))
            self.logger.log(f"Transfer from {source} to {destination} completed successfully.")
            return "Transfer successful."
        except Exception as e:
            raise DataTransferError(f"Error during data transfer: {str(e)}")

    def get_encryption_key(self):
        """
        Returns the encryption key used for data transfer.
        
        Returns:
            bytes: The encryption key.
        """
        return self.encryption_key
