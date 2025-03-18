import os

class Config:
    """
    Configuration settings for the core system of the Interplanetary Transaction Protocol (ITP).
    """

    # Logging configuration
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')  # Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    LOGGING_FILE = os.getenv('LOGGING_FILE', 'stable_pi_core.log')  # Log file name

    # Synchronization settings
    SYNC_INTERVAL = int(os.getenv('SYNC_INTERVAL', 60))  # Time interval for synchronization in seconds

    # Consensus settings
    CONSENSUS_TIMEOUT = int(os.getenv('CONSENSUS_TIMEOUT', 5))  # Timeout for consensus in seconds
    CONSENSUS_RETRY_LIMIT = int(os.getenv('CONSENSUS_RETRY_LIMIT', 3))  # Maximum retry attempts for consensus

    # Transaction settings
    MAX_TRANSACTION_AMOUNT = float(os.getenv('MAX_TRANSACTION_AMOUNT', 1e6))  # Maximum transaction amount
    MIN_TRANSACTION_AMOUNT = float(os.getenv('MIN_TRANSACTION_AMOUNT', 0.01))  # Minimum transaction amount

    # Smart contract settings
    ENABLE_SMART_CONTRACTS = bool(int(os.getenv('ENABLE_SMART_CONTRACTS', 1)))  # Enable or disable smart contracts

    @classmethod
    def display_config(cls):
        """
        Display the current configuration settings.
        """
        print("Current Configuration Settings:")
        print(f"Logging Level: {cls.LOGGING_LEVEL}")
        print(f"Logging Format: {cls.LOGGING_FORMAT}")
        print(f"Logging File: {cls.LOGGING_FILE}")
        print(f"Synchronization Interval: {cls.SYNC_INTERVAL} seconds")
        print(f"Consensus Timeout: {cls.CONSENSUS_TIMEOUT} seconds")
        print(f"Consensus Retry Limit: {cls.CONSENSUS_RETRY_LIMIT}")
        print(f"Max Transaction Amount: {cls.MAX_TRANSACTION_AMOUNT}")
        print(f"Min Transaction Amount: {cls.MIN_TRANSACTION_AMOUNT}")
        print(f"Smart Contracts Enabled: {cls.ENABLE_SMART_CONTRACTS}")

if __name__ == "__main__":
    # Example usage of the configuration settings
    Config.display_config()
