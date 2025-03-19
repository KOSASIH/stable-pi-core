import logging
import threading
from p2p import P2PNetwork

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Node:
    def __init__(self, node_id: str, host: str, port: int):
        """Initialize a node in the network."""
        self.node_id = node_id
        self.host = host
        self.port = port
        self.p2p_network = P2PNetwork(host, port)  # Initialize P2P network
        logging.info(f"Node {self.node_id} initialized at {self.host}:{self.port}")

    def start(self):
        """Start the P2P network for this node."""
        self.p2p_network.start()
        logging.info(f"Node {self.node_id} started and listening for connections.")

    def connect_to_peer(self, peer_address: tuple):
        """Connect this node to a specified peer."""
        logging.info(f"Node {self.node_id} attempting to connect to peer: {peer_address}")
        self.p2p_network.send_message(peer_address, {"type": "connect", "node_id": self.node_id})

    def broadcast(self, message):
        """Broadcast a message to all connected peers."""
        logging.info(f"Node {self.node_id} broadcasting message: {message}")
        self.p2p_network.broadcast(message)

    def handle_message(self, message):
        """Handle incoming messages from peers."""
        logging.info(f"Node {self.node_id} received message: {message}")
        if message.get("type") == "heartbeat":
            logging.info(f"Heartbeat received from {message.get('node_id')}")
        elif message.get("type") == "connect":
            self.handle_connect(message)

    def handle_connect(self, message):
        """Handle a connection request from another node."""
        logging.info(f"Node {self.node_id} connected to {message.get('node_id')}")

# Example usage
if __name__ == "__main__":
    node = Node(node_id="Node1", host='127.0.0.1', port=5000)
    node.start()

    # Simulate connecting to a peer
    peer_address = ('127.0.0.1', 5001)  # Example peer address
    node.connect_to_peer(peer_address)

    # Keep the main thread alive
    while True:
        pass
