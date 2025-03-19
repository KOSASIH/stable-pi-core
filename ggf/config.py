# ggf/config.py

import json
import os
import logging

class Config:
    # Default configuration settings
    DEFAULTS = {
        "LOGGING_ENABLED": True,
        "LOGGING_LEVEL": "INFO",  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
        "VOTING_TIMEOUT": 3600,  # Voting timeout in seconds
        "MIN_VOTES_REQUIRED": 10,  # Minimum votes required for a decision
        "CONFIG_FILE": "ggf_config.json",  # Path to the configuration file
        "MAX_PROPOSALS": 100,  # Maximum number of proposals allowed
        "COMMUNICATION_PROTOCOL": "Tachyonic",  # Communication protocol to use
        "SPACE_TIME_SYNC_ENABLED": True  # Enable space-time synchronization
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
        if config_data.get("VOTING_TIMEOUT", cls.DEFAULTS["VOTING_TIMEOUT"]) <= 0:
            raise ValueError("VOTING_TIMEOUT must be a positive integer.")
        if config_data.get("MIN_VOTES_REQUIRED", cls.DEFAULTS["MIN_VOTES_REQUIRED"]) <= 0:
            raise ValueError("MIN_VOTES_REQUIRED must be a positive integer.")
        if config_data.get("MAX_PROPOSALS", cls.DEFAULTS["MAX_PROPOSALS"]) <= 0:
            raise ValueError("MAX_PROPOSALS must be a positive integer.")
        if config_data.get("COMMUNICATION_PROTOCOL") not in ["Tachyonic", "Standard"]:
            raise ValueError("COMMUNICATION_PROTOCOL must be either 'Tachyonic' or 'Standard'.")

    @classmethod
    def update_config(cls, config_data):
        """Update the configuration with loaded values."""
        for key, value in config_data.items():
            if key in cls.DEFAULTS:
                cls.DEFAULTS[key] = value

    @classmethod
    def display_config(cls):
        """Display the current configuration settings."""
        logging.info("GGF Configuration:")
        for key, value in cls.DEFAULTS.items():
            logging.info(f"{key}: {value}")

# Load the configuration when the module is imported
Config.load_config()
