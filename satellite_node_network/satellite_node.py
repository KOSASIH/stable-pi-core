import json
import random
import logging

class SatelliteNode:
    """
    Class representing a satellite node in the space-based node network.

    Attributes:
        node_id (str): Unique identifier for the satellite node.
        location (str): Geographical location of the satellite node.
        connected_nodes (list): List of connected satellite nodes.
        data_storage (dict): Dictionary to store data processed by the node.
    """

    def __init__(self, node_id, location):
        """
        Initializes a SatelliteNode instance.

        Args:
            node_id (str): Unique identifier for the satellite node.
            location (str): Geographical location of the satellite node.
        """
        self.node_id = node_id
        self.location = location
        self.connected_nodes = []
        self.data_storage = {}
        logging.info(f"SatelliteNode {self.node_id} initialized at {self.location}.")

    def connect_to_node(self, other_node):
        """
        Connects this node to another satellite node.

        Args:
            other_node (SatelliteNode): The satellite node to connect to.
        """
        if other_node not in self.connected_nodes:
            self.connected_nodes.append(other_node)
            other_node.connected_nodes.append(self)  # Ensure bidirectional connection
            logging.info(f"Node {self.node_id} connected to Node {other_node.node_id}.")

    def disconnect_from_node(self, other_node):
        """
        Disconnects this node from another satellite node.

        Args:
            other_node (SatelliteNode): The satellite node to disconnect from.
        """
        if other_node in self.connected_nodes:
            self.connected_nodes.remove(other_node)
            other_node.connected_nodes.remove(self)  # Ensure bidirectional disconnection
            logging.info(f"Node {self.node_id} disconnected from Node {other_node.node_id}.")

    def process_data(self, data):
        """
        Processes incoming data and stores the result.

        Args:
            data (dict): The data to be processed.
        
        Returns:
            dict: The processed data.
        """
        # Simulate data processing (e.g., transformation, filtering)
        processed_data = {key: value * random.uniform(0.5, 1.5) for key, value in data.items()}
        self.data_storage.update(processed_data)
        logging.info(f"Node {self.node_id} processed data: {processed_data}.")
        return processed_data

    def get_connected_nodes(self):
        """
        Returns a list of connected nodes.

        Returns:
            list: List of connected SatelliteNode instances.
        """
        return [node.node_id for node in self.connected_nodes]

    def to_json(self):
        """
        Serializes the node information to JSON format.

        Returns:
            str: JSON representation of the node.
        """
        return json.dumps({
            'node_id': self.node_id,
            'location': self.location,
            'connected_nodes': self.get_connected_nodes(),
            'data_storage': self.data_storage
        })

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    node1 = SatelliteNode(node_id="Node1", location="Orbit 1")
    node2 = SatelliteNode(node_id="Node2", location="Orbit 2")

    node1.connect_to_node(node2)
    data = {'temperature': 25, 'humidity': 60}
    processed_data = node1.process_data(data)
    print(node1.to_json())
