# dmec/config.py

import json
import os
import logging

class Config:
    # Default configuration settings
    DEFAULTS = {
        "DETECTOR_SENSITIVITY": 0.95,  # Sensitivity of the dark matter detector
        "DETECTION_INTERVAL": 1.0,      # Time interval (in seconds) for detection
        "ENERGY_PER_INTERACTION": 1.0,   # Energy generated per detected interaction (in arbitrary units)
        "COMMUNICATION_PROTOCOL": "MQTT",  # Protocol for communication with edge nodes
        "MQTT_BROKER_URL": "mqtt://broker.example.com",
        "MQTT_TOPIC": "dmec/energy_output",
        "LOGGING_ENABLED": True,
        "LOGGING_LEVEL": "DEBUG",  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
        "DATA_STORAGE_FORMAT": "json",  # Options: json, csv
        "DATA_FILENAME": "energy_data.json",
        "CSV_FILENAME": "energy_data.csv"
    }

    CONFIG_FILE = 'config.json'  # Path to the configuration file

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
        if not (0 <= config_data.get("DETECTOR_SENSITIVITY", cls.DEFAULTS["DETECTOR_SENSITIVITY"]) <= 1):
            raise ValueError("DETECTOR_SENSITIVITY must be between 0 and 1.")
        if config_data.get("DETECTION_INTERVAL", cls.DEFAULTS["DETECTION_INTERVAL"]) <= 0:
            raise ValueError("DETECTION_INTERVAL must be greater than 0.")
        if config_data.get("ENERGY_PER_INTERACTION", cls.DEFAULTS["ENERGY_PER_INTERACTION"]) <= 0:
            raise ValueError("ENERGY_PER_INTERACTION must be greater than 0.")

    @classmethod
    def update_config(cls, config_data):
        """Update the configuration with loaded values."""
        for key, value in config_data.items():
            if key in cls.DEFAULTS:
                cls.DEFAULTS[key] = value

    @classmethod
    def display_config(cls):
        """Display the current configuration settings."""
        logging.info("DMEC Configuration:")
        for key, value in cls.DEFAULTS.items():
            logging.info(f"{key}: {value}")

# Load the configuration when the module is imported
Config.load_config()
