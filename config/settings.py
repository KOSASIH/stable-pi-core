# config/settings.py

import os

class Settings:
    """
    Configuration settings for the application.
    """
    def __init__(self):
        self.DEBUG = os.getenv("DEBUG", "False") == "True"
        self.BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL", "http://localhost:5000/api")
        self.BIOSENSOR_API_URL = os.getenv("BIOSENSOR_API_URL", "http://localhost:5001/api")
        self.ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "default_encryption_key")  # Replace with a secure key

    def display_settings(self):
        """
        Display the current configuration settings.
        """
        print("Current Configuration Settings:")
        print(f"DEBUG: {self.DEBUG}")
        print(f"BLOCKCHAIN_URL: {self.BLOCKCHAIN_URL}")
        print(f"BIOSENSOR_API_URL: {self.BIOSENSOR_API_URL}")
        print(f"ENCRYPTION_KEY: {self.ENCRYPTION_KEY}")

# Example usage
if __name__ == "__main__":
    settings = Settings()
    settings.display_settings()
