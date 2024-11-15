import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    """Function to set up a logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create a file handler
    handler = logging.FileHandler(log_file)
    handler.setLevel(level)
    
    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(handler)
    
    return logger

# Example usage
if __name__ == "__main__":
    log = setup_logger('api_logger', 'api.log')
    log.info('Logger is set up and ready to use.')
