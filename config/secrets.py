# config/secrets.py

import os

class Secrets:
    """
    Sensitive information for the application.
    """
    def __init__(self):
        self.API_KEY = os.getenv("API_KEY", "your_api_key_here")  # Replace with your actual API key
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///default.db")  # Example for SQLite

    def display_secrets(self):
        """
        Display the current sensitive information (for debugging purposes only).
        """
        print("Current Sensitive Information:")
        print(f"API_KEY: {self.API_KEY}")
        print(f"DATABASE_URL: {self.DATABASE_URL}")

# Example usage
if __name__ == "__main__":
    secrets = Secrets()
    secrets.display_secrets()
