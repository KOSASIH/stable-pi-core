import socket
import threading
import json
import logging
import ssl
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class P2PNetwork:
    def __init__(self, host: str, port: int):
        """Initialize the P2P network."""
        self.host = host
        self.port = port
        self.peers = set()  # Set of connected peers
        self.server = self.create_server_socket()
        self.key = Fernet.generate_key()  # Generate a key for encryption
        self.cipher = Fernet(self.key)
        logging.info(f"P2P network initialized on {self.host}:{self.port}")

    def create_server_socket(self):
        """Create a secure server socket."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        return server_socket

    def start(self):
        """Start the server to accept incoming connections."""
        threading.Thread(target=self.accept_connections, daemon=True).start()
        logging.info("P2P network server started.")

    def accept_connections(self):
        """Accept incoming connections from peers."""
        while True:
            client_socket, address = self.server.accept()
            logging.info(f"Connection established with {address}")
            self.peers.add(address)
            threading.Thread(target=self.handle_peer, args=(client_socket,), daemon=True).start()

    def handle_peer(self, client_socket):
        """Handle communication with a connected peer."""
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    decrypted_message = self.decrypt_message(message)
                    if self.validate_message(decrypted_message):
                        self.process_message(json.loads(decrypted_message))
                    else:
                        logging.warning("Received invalid message.")
                else:
                    break
            except Exception as e:
                logging.error(f"Error handling peer: {e}")
                break
        client_socket.close()

    def process_message(self, message):
        """Process incoming messages from peers."""
        logging.info(f"Received message: {message}")

    def send_message(self, peer_address, message):
        """Send a message to a specific peer."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(peer_address)
                encrypted_message = self.encrypt_message(json.dumps(message))
                sock.sendall(encrypted_message.encode())
                logging.info(f"Sent message to {peer_address}: {message}")
        except Exception as e:
            logging.error(f"Failed to send message to {peer_address}: {e}")

    def encrypt_message(self, message: str) -> str:
        """Encrypt a message using Fernet symmetric encryption."""
        return self.cipher.encrypt(message.encode()).decode()

    def decrypt_message(self, encrypted_message: str) -> str:
        """Decrypt a message using Fernet symmetric encryption."""
        return self.cipher.decrypt(encrypted_message.encode()).decode()

    def validate_message(self, message: dict) -> bool:
        """Validate the incoming message structure."""
        # Implement validation logic (e.g., check required fields)
        return isinstance(message, dict) and 'type' in message

    def broadcast(self, message):
        """Broadcast a message to all peers in the network."""
        for peer in self.peers:
            self.send_message(peer, message)

    def heartbeat(self):
        """Send heartbeat messages to connected peers to check their status."""
        while True:
            for peer in list(self.peers):
                try:
                    self.send_message(peer, {"type": "heartbeat"})
                except Exception as e:
                    logging.warning(f"Peer {peer} is unresponsive. Removing from peers.")
                    self.peers.remove(peer)
            time.sleep(10)  # Send heartbeat every 10 seconds

# Example usage
if __name__ == "__main__":
    p2p_network = P2PNetwork(host='127.0.0.1', port=5000 )
    p2p_network.start()

    # Start the heartbeat mechanism in a separate thread
    threading.Thread(target=p2p_network.heartbeat, daemon=True).start()

    # Keep the main thread alive
    while True:
        pass
