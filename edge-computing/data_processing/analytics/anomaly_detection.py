import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration for thresholds
def load_thresholds():
    """
    Load thresholds for anomaly detection from a configuration file or define them here.
    
    Returns:
        dict: A dictionary containing threshold values for temperature and humidity.
    """
    return {
        'temperature': {
            'upper_limit': 28.0,  # Upper limit for temperature
            'lower_limit': 18.0   # Lower limit for temperature
        },
        'humidity': {
            'upper_limit': 70.0,  # Upper limit for humidity
            'lower_limit': 30.0   # Lower limit for humidity
        }
    }

def detect_anomaly(data):
    """
    Detect anomalies in the sensor data based on predefined thresholds.
    
    Parameters:
        data (dict): The sensor data containing temperature and humidity.
        
    Returns:
        bool: True if an anomaly is detected, False otherwise.
    """
    thresholds = load_thresholds()
    
    temperature = data.get('temperature')
    humidity = data.get('humidity')

    # Check for temperature anomalies
    if temperature is not None:
        if temperature > thresholds['temperature']['upper_limit']:
            logging.warning(f"Anomaly detected: Temperature {temperature} exceeds upper limit.")
            return True
        elif temperature < thresholds['temperature']['lower_limit']:
            logging.warning(f"Anomaly detected: Temperature {temperature} below lower limit.")
            return True

    # Check for humidity anomalies
    if humidity is not None:
        if humidity > thresholds['humidity']['upper_limit']:
            logging.warning(f"Anomaly detected: Humidity {humidity} exceeds upper limit.")
            return True
        elif humidity < thresholds['humidity']['lower_limit']:
            logging.warning(f"Anomaly detected: Humidity {humidity} below lower limit.")
            return True

    return False
