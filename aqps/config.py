import os

class Config:
    """
    Configuration class to hold API URLs, keys, and other constants.
    """

    # Base URLs for external services
    SATELLITE_API_URL = os.getenv('SATELLITE_API_URL', 'http://micius-satellite-api.com')
    BLOCKCHAIN_API_URL = os.getenv('BLOCKCHAIN_API_URL', 'http://example-blockchain-api.com')

    # Quantum key settings
    QUANTUM_KEY = os.getenv('QUANTUM_KEY', 'default_quantum_key')  # Replace with actual key management

    # Logging settings
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')

    @staticmethod
    def display_config():
        """
        Display the current configuration settings.
        """
        print("Current Configuration:")
        print(f"Satellite API URL: {Config.SATELLITE_API_URL}")
        print(f"Blockchain API URL: {Config.BLOCKCHAIN_API_URL}")
        print(f"Quantum Key: {Config.QUANTUM_KEY}")
        print(f"Logging Level: {Config.LOGGING_LEVEL}")

if __name__ == "__main__":
    # Example usage
    Config.display_config()
