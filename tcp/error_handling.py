# tcp/error_handling.py

import logging

# Configure logging for Error Handling
logger = logging.getLogger(__name__)

class ProtocolError(Exception):
    """Custom exception for protocol-related errors."""
    def __init__(self, message):
        super().__init__(message)
        logger.error(f"ProtocolError: {message}")

class NodeError(Exception):
    """Custom exception for node-related errors."""
    def __init__(self, message):
        super().__init__(message)
        logger.error(f"NodeError: {message}")

class DataPacketError(Exception):
    """Custom exception for data packet-related errors."""
    def __init__(self, message):
        super().__init__(message)
        logger.error(f"DataPacketError: {message}")

class ErrorHandler:
    """Class for handling errors in the Tachyonic Communication Protocol."""

    @staticmethod
    def handle_protocol_error(message):
        """Handle protocol errors."""
        raise ProtocolError(message)

    @staticmethod
    def handle_node_error(message):
        """Handle node errors."""
        raise NodeError(message)

    @staticmethod
    def handle_data_packet_error(message):
        """Handle data packet errors."""
        raise DataPacketError(message)

    @staticmethod
    def log_error(message):
        """Log a generic error message."""
        logger.error(f"Error: {message}")

    @staticmethod
    def log_warning(message):
        """Log a warning message."""
        logger.warning(f"Warning: {message}")

    @staticmethod
    def log_info(message):
        """Log an informational message."""
        logger.info(f"Info: {message}")

# Example usage of the ErrorHandler
if __name__ == "__main__":
    error_handler = ErrorHandler()
    try:
        # Simulate a protocol error
        error_handler.handle_protocol_error("Invalid message format.")
    except ProtocolError as e:
        logger.info(f"Caught an error: {e}")
