# crhai/config.py

import json
import os
import logging

class Config:
    # Default configuration settings
    DEFAULTS = {
        "LOGGING_ENABLED": True,
        "LOGGING_LEVEL": "INFO",  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
        "MODEL_COUNT": 3,  # Number of redundant AI models
        "EDGE_COMPUTING_ENABLED": True,  # Enable edge computing
        "CONFIG_FILE": "crhai_config.json",  # Path to the configuration file
        "RADIATION_HARDENING_MATERIAL": "NASA-Approved",  # Material used for radiation hardening
        "AI_MODEL_TYPE": "Neural Network",  # Type of AI model to use
        "PROCESSING_TIMEOUT": 5  # Timeout for processing data in seconds
    }

    @classmethod
    def load_config(cls):
        """Load configuration from a JSON file."""
        if os.path.exists(cls.DEFAULTS["CONFIG_FILE"]):
            with open(cls.DEFAULTS["CONFIG_FILE"], 'r') as f:
                config_data = json.load(f)
                cls.validate_config(config_data)
                cls.update_config(config_data)
        else:
            logging.warning(f"Configuration file '{cls.DEFAULTS['CONFIG_FILE']}' not found. Using default settings.")

    @classmethod
    def validate_config(cls, config_data):
        """Validate the loaded configuration values."""
        if config_data.get("LOGGING_LEVEL") not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError("LOGGING_LEVEL must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL.")
        if config_data.get("MODEL_COUNT", cls.DEFAULTS["MODEL_COUNT"]) <= 0:
            raise ValueError("MODEL_COUNT must be a positive integer.")
        if config_data.get("PROCESSING_TIMEOUT", cls.DEFAULTS["PROCESSING_TIMEOUT"]) <= 0:
            raise ValueError("PROCESSING_TIMEOUT must be a positive integer.")

    @classmethod
    def update_config(cls, config_data):
        """Update the configuration with loaded values."""
        for key, value in config_data.items():
            if key in cls.DEFAULTS:
                cls.DEFAULTS[key] = value

    @classmethod
    def display_config(cls):
        """Display the current configuration settings."""
        logging.info("CRHAI Configuration:")
        for key, value in cls.DEFAULTS.items():
            logging.info(f"{key}: {value}")

# Load the configuration when the module is imported
Config.load_config()
