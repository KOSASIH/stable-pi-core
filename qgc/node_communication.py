# qgc/node_communication.py

import logging
import json
import random
import time
import threading
from queue import Queue

class NodeCommunication:
    """
    Facilitates secure communication between nodes for data sharing in the Quantum Gravitational Consensus (QGC) system.
    """

    def __init__(self, node_id):
        """
        Initialize the node communication protocol.

        :param node_id: Unique identifier for the node.
        """
        self.node_id = node_id
        self.connected_nodes = []
        self.message_queue = Queue()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.start_message_listener()

    def start_message_listener(self):
        """Start a thread to listen for incoming messages."""
        listener_thread = threading.Thread(target=self.process_incoming_messages, daemon=True)
        listener_thread.start()

    def connect_to_node(self, target_node):
        """
        Connect to another node.

        :param target_node: The target node to connect to.
        """
        if target_node not in self.connected_nodes:
            self.connected_nodes.append(target_node)
            self.logger.info(f"Node {self.node_id} connected to Node {target_node.node_id}")

    def send_measurement(self, measurement, target_node):
        """
        Send a gravitational measurement to a target node.

        :param measurement: The gravitational measurement to send.
        :param target_node: The target node to send the measurement to.
        """
        if target_node not in self.connected_nodes:
            self.logger.error(f"Node {self.node_id} is not connected to Node {target_node.node_id}.")
            return

        message = {
            "sender": self.node_id,
            "measurement": measurement,
            "timestamp": time.time()
        }
        self.logger.info(f"Node {self.node_id} sending measurement to Node {target_node.node_id}: {measurement:.4f} m/s^2")
        target_node.receive_measurement(json.dumps(message))

    def receive_measurement(self, message):
        """
        Receive a gravitational measurement from another node.

        :param message: The message containing the measurement data.
        """
        self.message_queue.put(message)  # Queue the message for processing

    def process_incoming_messages(self):
        """Process incoming messages from the queue."""
        while True:
            message = self.message_queue.get()
            if message is None:  # Exit signal
                break
            self.handle_message(message)

    def handle_message(self, message):
        """Handle the received message."""
        try:
            data = json.loads(message)
            sender = data["sender"]
            measurement = data["measurement"]
            timestamp = data["timestamp"]
            self.logger.info(f"Node {self.node_id} received measurement from Node {sender}: {measurement:.4f} m/s^2 at {timestamp}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode message: {message}. Error: {e}")
        except Exception as e:
            self.logger.error(f"An error occurred while handling the message: {e}")

    def broadcast_measurement(self, measurement):
        """
        Broadcast a gravitational measurement to all connected nodes.

        :param measurement: The gravitational measurement to broadcast.
        """
        for node in self.connected_nodes:
            self.send_measurement(measurement, node)

# Example usage
if __name__ == "__main__":
    class MockNode:
        """ A mock node class for testing the communication protocol. """
        def __init__(self, node_id):
            self.node_id = node_id
            self.communication = NodeCommunication(node_id)

        def receive_measurement(self, message):
            self.communication.receive_measurement(message)

    # Create mock nodes
    node1 = MockNode("Node_1")
    node2 = MockNode("Node_2")

    # Connect nodes
    node1.communication.connect_to_node(node2.communication)

    # Simulate sending a measurement
    measurement = random.uniform(9.78, 9.82)  # Simulated gravitational measurement
    node1.communication.send_measurement(measurement, node2.communication)

    # Broadcast a measurement
    node1.communication.broadcast_measurement(measurement)

    # Allow some time for message processing
    time.sleep(2)
