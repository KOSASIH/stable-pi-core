# tcp/main.py

import asyncio
import logging
import json
from cryptography.fernet import Fernet
from tachyon_node import TachyonNode
from tachyon_protocol import TachyonProtocol

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TCPApplication:
    def __init__(self):
        self.nodes = {}
        self.protocol = TachyonProtocol()
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)

    async def add_node(self, node_id, address):
        """Add a new Tachyonic Node to the network."""
        if node_id in self.nodes:
            logger.warning(f"Node {node_id} already exists.")
            return

        node = TachyonNode(node_id, address, self.protocol)
        self.nodes[node_id] = node
        await node.start()
        logger.info(f"Node {node_id} added at {address}")

    async def remove_node(self, node_id):
        """Remove a Tachyonic Node from the network."""
        if node_id in self.nodes:
            await self.nodes[node_id].stop()
            del self.nodes[node_id]
            logger.info(f"Node {node_id} removed from the network.")
        else:
            logger.warning(f"Node {node_id} not found.")

    async def send_data(self, sender_id, receiver_id, data):
        """Send encrypted data from one node to another."""
        sender = self.nodes.get(sender_id)
        receiver = self.nodes.get(receiver_id)

        if sender and receiver:
            encrypted_data = self.encrypt_data(data)
            await sender.send_data(receiver, encrypted_data)
            logger.info(f"Data sent from {sender_id} to {receiver_id}: {data}")
        else:
            logger.error("Sender or Receiver not found.")

    def encrypt_data(self, data):
        """Encrypt data using Fernet symmetric encryption."""
        json_data = json.dumps(data).encode()
        encrypted_data = self.cipher.encrypt(json_data)
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        """Decrypt data using Fernet symmetric encryption."""
        decrypted_data = self.cipher.decrypt(encrypted_data)
        return json.loads(decrypted_data)

    async def run(self):
        """Run the TCP application."""
        # Example of adding nodes and sending data
        await self.add_node("Node1", "localhost:8001")
        await self.add_node("Node2", "localhost:8002")

        await self.send_data("Node1", "Node2", {"message": "Hello from Node1!"})

        # Keep the application running
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    app = TCPApplication()
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        logger.info("TCP Application stopped.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
