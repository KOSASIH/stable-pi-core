import logging
import json
import os
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataAvailability:
    def __init__(self, storage_path='data_storage.json', encryption_key=None):
        self.storage_path = storage_path
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        self.load_data()

    def load_data(self):
        """Load data from the storage file."""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as file:
                encrypted_data = json.load(file)
                self.storage = {key: self.decrypt_value(value) for key, value in encrypted_data.items()}
                logging.info("Data loaded successfully.")
        else:
            self.storage = {}
            logging.info("No existing data found. Starting with an empty storage.")

    def save_data(self):
        """Save data to the storage file."""
        with open(self.storage_path, 'w') as file:
            encrypted_data = {key: self.encrypt_value(value) for key, value in self.storage.items()}
            json.dump(encrypted_data, file)
            logging.info("Data saved successfully.")

    def encrypt_value(self, value):
        """Encrypt a value for storage."""
        return self.cipher.encrypt(value.encode()).decode()

    def decrypt_value(self, value):
        """Decrypt a value retrieved from storage."""
        return self.cipher.decrypt(value.encode()).decode()

    def store_data(self, key, value):
        """Store data with a specified key."""
        self.storage[key] = value
        self.save_data()
        logging.info(f"Data stored: {key} -> {value}")

    def retrieve_data(self, key):
        """Retrieve data by key."""
        value = self.storage.get(key)
        if value is not None:
            logging.info(f"Data retrieved: {key} -> {value}")
            return value
        else:
            logging.warning(f"Data not found for key: {key}")
            return None

    def check_data_availability(self, key):
        """Check if data is available for a specified key."""
        available = key in self.storage
        logging.info(f"Data availability for key '{key}': {available}")
        return available

    def delete_data(self, key):
        """Delete data associated with a specified key."""
        if key in self.storage:
            del self.storage[key]
            self.save_data()
            logging.info(f"Data deleted for key: {key}")
        else:
            logging.warning(f"Attempted to delete non-existent key: {key}")

# Example usage
if __name__ == "__main__":
    data_availability = DataAvailability()
    data_availability.store_data("example_key", "example_value")
    retrieved_value = data_availability.retrieve_data("example_key")
    availability = data_availability.check_data_availability("example_key")
    data_availability.delete_data("example_key")
