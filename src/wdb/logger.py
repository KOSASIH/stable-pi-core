# wdb/logger.py

import logging
import logging.handlers
import asyncio
import json
import os

class AsyncLogger:
    def __init__(self, log_file='wdb.log', max_bytes=5 * 1024 * 1024, backup_count=5):
        self.logger = logging.getLogger("WDBLogger")
        self.logger.setLevel(logging.DEBUG)

        # Create a rotating file handler
        handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Create a console handler for output to the console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    async def log(self, level, message, **kwargs):
        """
        Asynchronously logs a message with the specified logging level.
        
        Args:
            level (str): The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            message (str): The message to log.
            **kwargs: Additional context to log.
        """
        log_message = {
            'message': message,
            'context': kwargs
        }
        log_message_json = json.dumps(log_message)

        # Log at the appropriate level
        if level == 'DEBUG':
            self.logger.debug(log_message_json)
        elif level == 'INFO':
            self.logger.info(log_message_json)
        elif level == 'WARNING':
            self.logger.warning(log_message_json)
        elif level == 'ERROR':
            self.logger.error(log_message_json)
        elif level == 'CRITICAL':
            self.logger.critical(log_message_json)
        else:
            self.logger.info(log_message_json)  # Default to INFO if level is unknown

    async def close(self):
        """
        Closes the logger and releases any resources.
        """
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)

# Example usage of the AsyncLogger
async def main():
    logger = AsyncLogger()

    await logger.log('INFO', 'Wormhole Data Bridge initialized.')
    await logger.log('DEBUG', 'Debugging information.', context={'module': 'main'})
    await logger.log('WARNING', 'This is a warning message.')
    await logger.log('ERROR', 'An error occurred.', error='SampleError')
    await logger.log('CRITICAL', 'Critical error encountered!')

    await logger.close()

if __name__ == '__main__':
    asyncio.run(main())
