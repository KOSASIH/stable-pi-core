# src/utils/config_loader.py

import os
import json
import yaml
import logging

# Set up logging for the config loader
logger = logging.getLogger(__name__)

class ConfigLoader:
    def __init__(self, config_file=None):
        """
        Initialize the ConfigLoader.

        Parameters:
        - config_file (str): Path to the configuration file (JSON or YAML).
        """
        self.config_file = config_file
        self.config = {}
        logger.info("ConfigLoader initialized.")

        if config_file:
            self.load_config(config_file)

    def load_config(self, config_file):
        """
        Load configuration from a specified file.

        Parameters:
        - config_file (str): Path to the configuration file (JSON or YAML).

        Raises:
        - ValueError: If the file format is unsupported or if loading fails.
        """
        try:
            if config_file.endswith('.json'):
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
                    logger.info(f"Configuration loaded from JSON file: {config_file}")
            elif config_file.endswith('.yaml') or config_file.endswith('.yml'):
                with open(config_file, 'r') as f:
                    self.config = yaml.safe_load(f)
                    logger.info(f"Configuration loaded from YAML file: {config_file}")
            else:
                logger.error("Unsupported configuration file format. Use .json or .yaml/.yml.")
                raise ValueError("Unsupported configuration file format. Use .json or .yaml/.yml.")
        except Exception as e:
            logger.error(f"Failed to load configuration from {config_file}: {e}")
            raise

    def get(self, key, default=None):
        """
        Get a configuration value by key.

        Parameters:
        - key (str): The key of the configuration value to retrieve.
        - default: The default value to return if the key is not found.

        Returns:
        - The configuration value or the default value if the key is not found.
        """
        value = self.config.get(key, default)
        logger.info(f"Retrieved config value for '{key}': {value}")
        return value

    def load_env_variables(self):
        """
        Load configuration values from environment variables.

        This method assumes that environment variables are named in uppercase
        and match the keys in the configuration.
        """
        for key in self.config.keys():
            env_value = os.getenv(key.upper())
            if env_value is not None:
                self.config[key] = env_value
                logger.info(f"Loaded environment variable for '{key}': {env_value}")

    def save_config(self, config_file=None):
        """
        Save the current configuration to a specified file.

        Parameters:
        - config_file (str): Path to the configuration file (JSON or YAML). If None, uses the original config_file.
        """
        if config_file is None:
            config_file = self.config_file

        try:
            if config_file.endswith('.json'):
                with open(config_file, 'w') as f:
                    json.dump(self.config, f, indent=4)
                    logger.info(f"Configuration saved to JSON file: {config_file}")
            elif config_file.endswith('.yaml') or config_file.endswith('.yml'):
                with open(config_file, 'w') as f:
                    yaml.dump(self.config, f)
                    logger.info(f"Configuration saved to YAML file: {config_file}")
            else:
                logger.error("Unsupported configuration file format. Use .json or .yaml/.yml.")
                raise ValueError("Unsupported configuration file format. Use .json or .yaml/.yml.")
        except Exception as e:
            logger.error(f"Failed to save configuration to {config_file}: {e}")
            raise
