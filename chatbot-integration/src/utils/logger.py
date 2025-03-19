import logging
import os

class Logger:
    def __init__(self, log_file='app.log', log_level=logging.DEBUG):
        """Initializes the logger with specified log file and log level."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # Create a file handler to log messages to a file
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)

        # Create a console handler to log messages to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Create a formatter for the log messages
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        """Logs a debug message."""
        self.logger.debug(message)

    def info(self, message):
        """Logs an informational message."""
        self.logger.info(message)

    def warning(self, message):
        """Logs a warning message."""
        self.logger.warning(message)

    def error(self, message):
        """Logs an error message."""
        self.logger.error(message)

    def critical(self, message):
        """Logs a critical message."""
        self.logger.critical(message)

# Example usage
if __name__ == "__main__":
    # Create a logger instance
    logger = Logger(log_file='application.log', log_level=logging.DEBUG)

    # Log messages of various severity levels
    logger.debug("This is a debug message.")
    logger.info("This is an informational message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
