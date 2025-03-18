# nbca/config.py

import json
import os
import logging

class Config:
    # Default configuration settings
    DEFAULTS = {
        "LOGGING_ENABLED": True,
        "LOGGING_LEVEL": "DEBUG",  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
        "NEUTRINO_DETECTION_THRESHOLD": 0.1,  # Probability threshold for neutrino detection
        "MAX_COMMUNICATION_ATTEMPTS": 5,  # Maximum attempts to communicate
        "CONFIG_FILE": "nbca_config.json",  # Path to the configuration file
        "NEUTRINO_DETECTOR_TYPE": "IceCube",  # Type of neutrino detector
        "QUANTUM_PROCESSOR_TYPE": "Photonic",  # Type of quantum processor
        "DATA_FORMAT": "JSON"  # Format for data transmission
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
        if not (0 <= config_data.get("NEUTRINO_DETECTION_THRESHOLD", cls.DEFAULTS["NEUTRINO_DETECTION_THRESHOLD"]) <= 1):
            raise ValueError("NEUTRINO_DETECTION_THRESHOLD must be between 0 and 1.")
        if config_data.get("MAX_COMMUNICATION_ATTEMPTS", cls.DEFAULTS["MAX_COMMUNICATION_ATTEMPTS"]) <= 0:
            raise ValueError("MAX_COMMUNICATION_ATTEMPTS must be a positive integer.")
        if config_data.get("NEUTRINO_DETECTOR_TYPE") not in ["IceCube", "Super-Kamiokande", "Other"]:
            raise ValueError("NEUTRINO_DETECTOR_TYPE must be one of: IceCube, Super-Kamiokande, Other.")
        if config_data.get("QUANTUM_PROCESSOR_TYPE") not in ["Photonic", "Trapped Ion", "Other"]:
            raise ValueError("QUANTUM_PROCESSOR_TYPE must be one of: Photonic, Trapped Ion, Other.")
        if config_data.get("DATA_FORMAT") not in ["JSON", "XML", "Binary"]:
            raise ValueError("DATA_FORMAT must be one of: JSON, XML, Binary.")

    @classmethod
    def update_config(cls, config_data):
        """Update the configuration with loaded values."""
        for key, value in config_data.items():
            if key in cls.DEFAULTS:
                cls.DEFAULTS[key] = value

    @classmethod
    def display_config(cls):
        """Display the current configuration settings."""
        logging.info("NBCA Configuration:")
        for key, value in cls.DEFAULTS.items():
            logging.info(f"{key}: {value}")

# Load the configuration when the module is imported
Config.load_config()
