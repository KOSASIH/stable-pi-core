# ebs/config.py

import json
import os
import logging

class Config:
    # Default configuration settings
    DEFAULTS = {
        "LOGGING_ENABLED": True,
        "LOGGING_LEVEL": "DEBUG",  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
        "SIGNAL_DETECTION_THRESHOLD": 0.1,  # Probability threshold for signal detection
        "MAX_SYNC_ATTEMPTS": 5,  # Maximum attempts to sync with external network
        "AI_SECURITY_ENABLED": True,  # Enable or disable AI security analysis
        "CONFIG_FILE": "ebs_config.json"  # Path to the configuration file
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
        if not (0 <= config_data.get("SIGNAL_DETECTION_THRESHOLD", cls.DEFAULTS["SIGNAL_DETECTION_THRESHOLD"]) <= 1):
            raise ValueError("SIGNAL_DETECTION_THRESHOLD must be between 0 and 1.")
        if config_data.get("MAX_SYNC_ATTEMPTS", cls.DEFAULTS["MAX_SYNC_ATTEMPTS"]) <= 0:
            raise ValueError("MAX_SYNC_ATTEMPTS must be a positive integer.")

    @classmethod
    def update_config(cls, config_data):
        """Update the configuration with loaded values."""
        for key, value in config_data.items():
            if key in cls.DEFAULTS:
                cls.DEFAULTS[key] = value

    @classmethod
    def display_config(cls):
        """Display the current configuration settings."""
        logging.info("EBS Configuration:")
        for key, value in cls.DEFAULTS.items():
            logging.info(f"{key}: {value}")

# Load the configuration when the module is imported
Config.load_config()
