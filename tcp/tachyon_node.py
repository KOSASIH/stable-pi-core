# tcp/tachyon_node.py

import asyncio
import logging

# Configure logging for the Tachyon Node
logger = logging.getLogger(__name__)

class TachyonNode:
    def __init__(self, node_id, address, protocol):
        self.node_id = node_id
        self.address = address
        self.protocol = protocol
        self.connected_nodes = set()
        self.is_running = False

    async def start(self):
        """Start the Tachyon Node and listen for incoming messages."""
        self.is_running = True
        logger.info(f"Tachyon Node {self.node_id} starting at {self.address}")
        # Simulate listening for incoming messages
        asyncio.create_task(self.listen_for_messages())

    async def stop(self):
        """Stop the Tachyon Node."""
        self.is_running = False
        logger.info(f"Tachyon Node {self.node_id} stopping.")

    async def listen_for_messages(self):
        """Simulate listening for incoming messages."""
        while self.is_running:
            await asyncio.sleep(5)  # Simulate waiting for messages
            # Here you would normally receive messages from a network socket
            # For demonstration, we will simulate receiving a message
            simulated_message = {"sender": "Node2", "data": "Hello from Node2!"}
            await self.handle_received_data(simulated_message)

    async def handle_received_data(self, message):
        """Handle incoming data."""
        sender = message["sender"]
        data = message["data"]
        logger.info(f"Node {self.node_id} received data from {sender}: {data}")
        # Here you can add logic to process the received data

    async def send_data(self, receiver, data):
        """Send data to another Tachyonic Node."""
        if not self.is_running:
            logger.warning(f"Node {self.node_id} is not running. Cannot send data.")
            return

        logger.info(f"Node {self.node_id} sending data to {receiver.node_id}.")
        # Simulate sending data to the receiver
        await receiver.handle_received_data({"sender": self.node_id, "data": data})

    def connect_to(self, other_node):
        """Connect to another Tachyonic Node."""
        self.connected_nodes.add(other_node.node_id)
        logger.info(f"Node {self.node_id} connected to {other_node.node_id}.")

    def disconnect_from(self, other_node):
        """Disconnect from another Tachyonic Node."""
        self.connected_nodes.discard(other_node.node_id)
        logger.info(f"Node {self.node_id} disconnected from {other_node.node_id}.")
