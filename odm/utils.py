# odm/utils.py

import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)

def log_info(message):
    """Log an informational message."""
    logging.info(f"{datetime.now()}: {message}")

def log_error(message):
    """Log an error message."""
    logging.error(f"{datetime.now()}: {message}")

def validate_data(data, required_fields):
    """Validate that the required fields are present in the data."""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    return True

def encrypt_data(data, key):
    """Encrypt data using a simple XOR cipher (for demonstration purposes)."""
    return ''.join(chr(ord(c) ^ key) for c in data)

def decrypt_data(data, key):
    """Decrypt data using a simple XOR cipher (for demonstration purposes)."""
    return ''.join(chr(ord(c) ^ key) for c in data)
