import json
import os

class Config:
    """
    Class for managing configuration settings for the satellite network.

    Attributes:
        config_file (str): Path to the configuration file.
        settings (dict): Dictionary to store configuration settings.
    """

    def __init__(self, config_file='config.json'):
        """
        Initializes a Config instance.

        Args:
            config_file (str): Path to the configuration file.
        """
        self.config_file = config_file
        self.settings = {}
        self.load_config()

    def load_config(self):
        """Loads configuration settings from a JSON file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                self.settings = json.load(file)
                print(f"Configuration loaded: {self.settings}")
        else:
            print(f"Configuration file {self.config_file} not found. Using default settings.")
            self.set_default_config()

    def set_default_config(self):
        """Sets default configuration settings."""
        self.settings = {
            'node_capacity': 100,  # Maximum number of nodes
            'communication_protocol': 'quantum',  # Default communication protocol
            'max_data_size': 1024,  # Maximum data size in bytes
            'quantum_key_length': 128,  # Length of the quantum key
            'location': 'geostationary',  # Default node location
            'logging_level': 'INFO'  # Default logging level
        }
        self.save_config()

    def save_config(self):
        """Saves the current configuration settings to a JSON file."""
        with open(self.config_file, 'w') as file:
            json.dump(self.settings, file, indent=4)
            print(f"Configuration saved: {self.settings}")

    def get_setting(self, key):
        """
        Retrieves a configuration setting.

        Args:
            key (str): The key of the setting to retrieve.

        Returns:
            The value of the setting, or None if the key does not exist.
        """
        return self.settings.get(key, None)

    def set_setting(self, key, value):
        """
        Sets a configuration setting.

        Args:
            key (str): The key of the setting to set.
            value: The value to set for the setting.
        """
        self.settings[key] = value
        self.save_config()

# Example usage
if __name__ == "__main__":
    config = Config()
    print("Node Capacity:", config.get_setting('node_capacity'))
    config.set_setting('node_capacity', 150)
    print("Updated Node Capacity:", config.get_setting('node_capacity'))
