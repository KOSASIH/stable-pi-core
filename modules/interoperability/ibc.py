import logging
import json
import time
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Packet:
    """Represents a packet for inter-blockchain communication."""
    def __init__(self, source_zone, destination_zone, data, packet_id=None):
        self.source_zone = source_zone
        self.destination_zone = destination_zone
        self.data = data  # Data can be a transaction, event, etc.
        self.packet_id = packet_id or self.generate_packet_id()  # Unique identifier for the packet
        self.timestamp = time.time()  # Timestamp for the packet

    def generate_packet_id(self):
        """Generate a unique packet ID."""
        return f"{self.source_zone}-{int(self.timestamp)}"

    def to_dict(self):
        """Convert the packet to a dictionary for serialization."""
        return {
            'source_zone': self.source_zone,
            'destination_zone': self.destination_zone,
            'data': self.data,
            'packet_id': self.packet_id,
            'timestamp': self.timestamp,
        }

    @classmethod
    def from_dict(cls, packet_dict):
        """Create a Packet instance from a dictionary."""
        return cls(
            source_zone=packet_dict['source_zone'],
            destination_zone=packet_dict['destination_zone'],
            data=packet_dict['data'],
            packet_id=packet_dict['packet_id'],
        )

class IBC:
    """Handles inter-blockchain communication."""
    def __init__(self):
        self.channels = defaultdict(list)  # Dictionary to manage channels between zones
        self.retry_limit = 3  # Number of retries for sending packets

    def create_channel(self, zone_name):
        """Create a communication channel for a zone."""
        if zone_name not in self.channels:
            self.channels[zone_name] = []
            logging.info(f"Channel created for zone: {zone_name}")
        else:
            logging.warning(f"Channel already exists for zone: {zone_name}")

    def send_packet(self, packet):
        """Send a packet to the destination zone with retries."""
        logging.info(f"Sending packet from {packet.source_zone} to {packet.destination_zone}: {packet.packet_id}")
        attempts = 0
        while attempts < self.retry_limit:
            if packet.destination_zone in self.channels:
                self.channels[packet.destination_zone].append(packet)
                logging.info(f"Packet sent: {json.dumps(packet.to_dict())}")
                return True
            else:
                attempts += 1
                logging.error(f"Destination zone {packet.destination_zone} does not have an active channel. Retrying...")
                time.sleep(1)  # Wait before retrying
        logging.error(f"Failed to send packet {packet.packet_id} after {self.retry_limit} attempts.")
        return False

    def receive_packet(self, packet):
        """Receive a packet and process it."""
        logging.info(f"Receiving packet in {packet.destination_zone}: {json.dumps(packet.to_dict())}")
        if self.validate_packet(packet):
            self.process_packet(packet)
        else:
            logging.error(f"Invalid packet received in {packet.destination_zone}: {packet.packet_id}")

    def validate_packet(self, packet):
        """Validate the received packet."""
        # Implement validation logic (e.g., check signatures, format)
        if not isinstance(packet.data, dict):
            logging.error(f"Packet data is not valid: {packet.data}")
            return False
        return True  # Placeholder for actual validation logic

    def process_packet(self, packet):
        """Process the received packet."""
        logging.info(f"Processing packet data: {packet.data}")
        # Implement logic to handle the packet data, such as executing a transaction or updating state
        # Example: if packet.data.get('type') == 'smart_contract':
        #     self.smart_contracts.execute(packet.data['contract_id'], packet.data['context'])

    def get_channel_packets(self, zone_name):
        """Retrieve all packets for a specific zone."""
        if zone_name in self.channels:
            return self.channels[zone_name]
        else:
            logging.warning(f"No channel found for zone: {zone_name}")
            return []

    def clear_channel_packets(self, zone_name):
        """Clear all packets for a specific zone."""
        if zone_name in self.channels:
            self.channels[zone_name] = []
            logging.info(f"Cleared packets for zone: {zone_name}")
        else:
            logging.warning(f"No channel found for zone: {zone_name}")

# Example usage
if __name__ == "__main__":
    ibc = IBC()
    ibc.create_channel("ZoneA")
    ibc.create_channel("ZoneB")

    packet = Packet(source_zone="ZoneA", destination_zone="ZoneB", data={"transaction": "transfer", "amount": 100})
    ibc.send_packet(packet)

    # Simulate receiving the packet
    ibc.receive_packet(packet)
