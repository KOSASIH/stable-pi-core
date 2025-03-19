import socket
import logging
import json
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NodeDiscovery:
    def __init__(self, host: str, port: int):
        """Initialize the node discovery service."""
        self.host = host
        self.port = port
        self.known_peers = set()  # Set to store known peers
        self.discovery_interval = 10  # Interval for broadcasting discovery messages
        logging.info(f"Node discovery initialized on {self.host}:{self.port}")

    def start_discovery(self):
        """Start the discovery process in a separate thread."""
        threading.Thread(target=self.broadcast_discovery, daemon=True).start()
        logging.info("Node discovery process started.")

    def broadcast_discovery(self):
        """Broadcast discovery messages to the network."""
        while True:
            message = {
                "type": "discovery",
                "node_id": f"{self.host}:{self.port}"
            }
            self.send_discovery_message(message)
            time.sleep(self.discovery_interval)

    def send_discovery_message(self, message):
        """Send a discovery message to the broadcast address."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(json.dumps(message).encode(), ('<broadcast>', self.port))
            logging.info(f"Broadcasted discovery message: {message}")

    def listen_for_discovery_responses(self):
        """Listen for discovery responses from other nodes."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((self.host, self.port))
            logging.info("Listening for discovery responses...")
            while True:
                data, address = sock.recvfrom(1024)
                self.handle_discovery_response(data.decode(), address)

    def handle_discovery_response(self, message: str, address: tuple):
        """Handle incoming discovery responses from other nodes."""
        try:
            message_data = json.loads(message)
            if message_data.get("type") == "discovery":
                peer_id = message_data.get("node_id")
                self.known_peers.add(peer_id)
                logging.info(f"Discovered new peer: {peer_id} from {address}")
        except json.JSONDecodeError:
            logging.error("Received invalid discovery message.")

# Example usage
if __name__ == "__main__":
    discovery_service = NodeDiscovery(host='127.0.0.1', port=5001)
    discovery_service.start_discovery()

    # Start listening for discovery responses
    discovery_service.listen_for_discovery_responses()
