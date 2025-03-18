# dmec/config.py

"""
Configuration settings for the Dark Matter Energy Converter (DMEC)
"""

class Config:
    # Detector settings
    DETECTOR_SENSITIVITY = 0.95  # Sensitivity of the dark matter detector
    DETECTION_INTERVAL = 1.0      # Time interval (in seconds) for detection

    # Energy conversion settings
    ENERGY_PER_INTERACTION = 1.0   # Energy generated per detected interaction (in arbitrary units)

    # Communication settings
    COMMUNICATION_PROTOCOL = "MQTT"  # Protocol for communication with edge nodes
    MQTT_BROKER_URL = "mqtt://broker.example.com"
    MQTT_TOPIC = "dmec/energy_output"

    # Logging settings
    LOGGING_ENABLED = True
    LOGGING_LEVEL = "DEBUG"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

    @staticmethod
    def display_config():
        print("DMEC Configuration:")
        for key, value in Config.__dict__.items():
            if not key.startswith('__'):
                print(f"{key}: {value}")
