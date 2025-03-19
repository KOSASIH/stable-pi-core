# tcp/data_packet.py

import json
import logging

# Configure logging for the Data Packet
logger = logging.getLogger(__name__)

class DataPacket:
    def __init__(self, sender_id, receiver_id, data, packet_id=None):
        self.packet_id = packet_id  # Unique identifier for the packet
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.data = data
        self.timestamp = self.get_current_timestamp()

    def get_current_timestamp(self):
        """Get the current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()

    def to_dict(self):
        """Convert the DataPacket to a dictionary."""
        packet_dict = {
            "packet_id": self.packet_id,
            "sender": self.sender_id,
            "receiver": self.receiver_id,
            "data": self.data,
            "timestamp": self.timestamp
        }
        logger.debug(f"DataPacket converted to dict: {packet_dict}")
        return packet_dict

    def to_json(self):
        """Convert the DataPacket to a JSON string."""
        packet_json = json.dumps(self.to_dict())
        logger.debug(f"DataPacket converted to JSON: {packet_json}")
        return packet_json

    @classmethod
    def from_json(cls, json_string):
        """Create a DataPacket from a JSON string."""
        try:
            packet_dict = json.loads(json_string)
            logger.debug(f"DataPacket created from JSON: {packet_dict}")
            return cls(
                packet_id=packet_dict.get("packet_id"),
                sender_id=packet_dict["sender"],
                receiver_id=packet_dict["receiver"],
                data=packet_dict["data"]
            )
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to create DataPacket from JSON: {e}")
            return None

    def validate(self):
        """Validate the DataPacket structure."""
        if not self.sender_id or not self.receiver_id or not self.data:
            logger.error("DataPacket validation failed: Missing required fields.")
            return False
        logger.info("DataPacket validation successful.")
        return True

    def __str__(self):
        """String representation of the DataPacket."""
        return f"DataPacket(packet_id={self.packet_id}, sender={self.sender_id}, receiver={self.receiver_id}, data={self.data}, timestamp={self.timestamp})"
