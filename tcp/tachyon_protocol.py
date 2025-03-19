# tcp/tachyon_protocol.py

import json
import logging

# Configure logging for the Tachyon Protocol
logger = logging.getLogger(__name__)

class TachyonProtocol:
    def __init__(self, version="1.0"):
        self.version = version
        logger.info(f"Tachyon Protocol version {self.version} initialized.")

    def create_message(self, sender_id, receiver_id, data):
        """Create a formatted message for transmission."""
        message = {
            "version": self.version,
            "sender": sender_id,
            "receiver": receiver_id,
            "data": data
        }
        logger.debug(f"Message created: {message}")
        return json.dumps(message)

    def parse_message(self, message):
        """Parse a received message and return its components."""
        try:
            parsed_message = json.loads(message)
            logger.debug(f"Message parsed: {parsed_message}")
            return parsed_message
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse message: {e}")
            return None

    def validate_message(self, message):
        """Validate the structure of the received message."""
        required_fields = ["version", "sender", "receiver", "data"]
        for field in required_fields:
            if field not in message:
                logger.error(f"Message validation failed: Missing field '{field}'")
                return False
        logger.info("Message validation successful.")
        return True

    def handle_message(self, message):
        """Handle an incoming message based on its content."""
        parsed_message = self.parse_message(message)
        if parsed_message and self.validate_message(parsed_message):
            sender = parsed_message["sender"]
            receiver = parsed_message["receiver"]
            data = parsed_message["data"]
            logger.info(f"Handling message from {sender} to {receiver}: {data}")
            # Here you can add logic to process the data
            return True
        return False

    def get_protocol_info(self):
        """Return information about the protocol."""
        return {
            "version": self.version,
            "description": "Tachyonic Communication Protocol for high-speed data transmission."
        }
