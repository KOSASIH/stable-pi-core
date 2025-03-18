import json
import os
import logging

# Configure logging
logging.basicConfig(filename='config.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Config:
    def __init__(self, config_file='config.json'):
        """
        Initialize the configuration with default values or load from a file.
        
        :param config_file: Path to the configuration file.
        """
        self.config_file = config_file
        self.settings = {
            "base_efficiency": 0.85,
            "harvesting_rate": 1.0,
            "energy_threshold": 0.5,
            "max_energy_capacity": 100.0,
            "logging_level": "INFO"
        }
        self.load_config()

    def load_config(self):
        """
        Load configuration settings from a JSON file.
        """
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                try:
                    self.settings.update(json.load(file))
                    logging.info("Configuration loaded successfully.")
                except json.JSONDecodeError as e:
                    logging.error(f"Error loading configuration: {e}")
                    raise

    def validate_settings(self):
        """
        Validate the configuration settings to ensure they are within acceptable ranges.
        """
        if not (0 <= self.settings["base_efficiency"] <= 1):
            logging.error("Base efficiency must be between 0 and 1.")
            raise ValueError("Base efficiency must be between 0 and 1.")
        if self.settings["harvesting_rate"] <= 0:
            logging.error("Harvesting rate must be greater than 0.")
            raise ValueError("Harvesting rate must be greater than 0.")
        if self.settings["energy_threshold"] < 0:
            logging.error("Energy threshold must be non-negative.")
            raise ValueError("Energy threshold must be non-negative.")
        if self.settings["max_energy_capacity"] <= 0:
            logging.error("Max energy capacity must be greater than 0.")
            raise ValueError("Max energy capacity must be greater than 0.")

    def get_setting(self, key):
        """
        Get a configuration setting by key.
        
        :param key: The key of the setting to retrieve.
        :return: The value of the setting.
        """
        return self.settings.get(key)

    def set_setting(self, key, value):
        """
        Set a configuration setting by key.
        
        :param key: The key of the setting to set.
        :param value: The value to set.
        """
        self.settings[key] = value
        logging.info(f"Setting updated: {key} = {value}")

if __name__ == "__main__":
    # Example usage of the Config class
    try:
        config = Config()
        config.validate_settings()
        print("Configuration settings:")
        for key, value in config.settings.items():
            print(f"{key}: {value}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
