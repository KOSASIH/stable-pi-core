import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os
import sys
import json

def setup_logging():
    """Set up logging configuration."""
    log_level = os.getenv('LOG_LEVEL', 'DEBUG').upper()
    log_file = os.getenv('LOG_FILE', 'blockchain_payment_integration.log')
    mailhost = os.getenv('MAIL_HOST')
    mailport = int(os.getenv('MAIL_PORT', 25))
    fromaddr = os.getenv('MAIL_FROM')
    toaddrs = os.getenv('MAIL_TO', '').split(',')
    credentials = (os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD')) if os.getenv('MAIL_USERNAME') else None
    secure = None if os.getenv('MAIL_USE_TLS') != '1' else ()

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create a file handler that logs messages to a file
    file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    file_handler.setLevel(log_level)

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Create an SMTP handler for error notifications
    if mailhost and fromaddr and toaddrs:
        mail_handler = SMTPHandler(
            mailhost=(mailhost, mailport),
            fromaddr=fromaddr,
            toaddrs=toaddrs,
            subject='Application Error',
            credentials=credentials,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        logger.addHandler(mail_handler)

    # Create a formatter for structured logging
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Log the startup message
    logger.info("Logging is set up. Log level: %s", log_level)

# Call the setup_logging function to configure logging
setup_logging()
