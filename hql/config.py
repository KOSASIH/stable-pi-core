# hql/config.py

import json
import os
import logging

class Config:
    # Default configuration settings
    DEFAULTS = {
        "DATA_STORAGE_FORMAT": "json",  # Options: json, csv
        "LEDGER_FILENAME": "hql_data.json",  # Default filename for the ledger data
        "LOGGING_ENABLED": True,
        "LOGGING_LEVEL": "DEBUG",  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
        "QUANTUM_ENCODING_METHOD": "basic",  # Options: basic, advanced
        "MAX_DATA_ENTRIES": 10000,  # Maximum number of entries in the ledger
        "DATA_RETENTION_PERIOD": 30,  # Days to retain data
    }

    CONFIG_FILE = 'hql_config.json'  # Path to the configuration file

    @classmethod
    def load_config(cls):
        """Load configuration from a JSON file."""
        if os.path.exists(cls.CONFIG_FILE):
            with open(cls.CONFIG_FILE, 'r') as f:
                config_data = json.load(f)
                cls.validate_config(config_data)
                cls.update_config(config_data)
        else:
            logging.warning(f"Configuration file '{cls.CONFIG_FILE}' not found. Using default settings.")

    @classmethod
    def validate_config(cls, config_data):
        """Validate the loaded configuration values."""
        if config_data.get("LOGGING_LEVEL") not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError("LOGGING_LEVEL must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL.")
        if config_data.get("MAX_DATA_ENTRIES", cls.DEFAULTS["MAX_DATA_ENTRIES"]) <= 0:
            raise ValueError("MAX_DATA_ENTRIES must be a positive integer.")
        if config_data.get("DATA_RETENTION_PERIOD", cls.DEFAULTS["DATA_RETENTION_PERIOD"]) < 0:
            raise ValueError("DATA_RETENTION_PERIOD must be a non-negative integer.")

    @classmethod
    def update_config(cls, config_data):
        """Update the configuration with loaded values."""
        for key, value in config_data.items():
            if key in cls.DEFAULTS:
                cls.DEFAULTS[key] = value

    @classmethod
    def display_config(cls):
        """Display the current configuration settings."""
        logging.info("HQL Configuration:")
        for key, value in cls.DEFAULTS.items():
            logging.info(f"{key}: {value}")

# Load the configuration when the module is imported
Config.load_config()
