# src/security/authentication.py

import logging
from werkzeug.security import generate_password_hash, check_password_hash

# Set up logging for the authentication module
logger = logging.getLogger(__name__)

class Authentication:
    def __init__(self):
        """Initialize the Authentication class."""
        logger.info("Authentication module initialized.")

    def hash_password(self, password):
        """
        Hash a password for secure storage.

        Parameters:
        - password (str): The password to hash.

        Returns:
        - str: The hashed password.
        """
        hashed_password = generate_password_hash(password)
        logger.info("Password hashed successfully.")
        return hashed_password

    def verify_password(self, password, hashed_password):
        """
        Verify a password against a hashed password.

        Parameters:
        - password (str): The password to verify.
        - hashed_password (str): The hashed password to check against.

        Returns:
        - bool: True if the password matches, False otherwise.
        """
        is_valid = check_password_hash(hashed_password, password)
        logger.info("Password verification successful." if is_valid else "Password verification failed.")
        return is_valid
