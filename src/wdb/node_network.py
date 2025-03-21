# wdb/node_network.py

import asyncio
import random
from .logger import Logger

class NodeNetworkError(Exception):
    """Custom exception for Node Network errors."""
    pass

class Node:
    def __init__(self, node_id, location):
        self.node_id = node_id
        self.location = location
        self.is_active = True
        self.logger = Logger()

    def check_health(self):
        """
        Simulates a health check for the node.
        
        Returns:
            bool: True if the node is healthy, False otherwise.
        """
        # Simulate health check with a random outcome
        self.is_active = random.choice([True, False])
        self.logger.log(f"Health check for {self.node_id}: {'Active' if self.is_active else 'Inactive'}")
        return self.is_active

class NodeNetwork:
    def __init__(self):
        self.nodes = {}
        self.logger = Logger()

    def add_node(self, node_id, location):
        """
        Adds a new node to the network.
        
        Args:
            node_id (str): The unique identifier for the node.
            location (str): The location of the node.
        """
        if node_id in self.nodes:
            raise NodeNetworkError(f"Node {node_id} already exists.")
        self.nodes[node_id] = Node(node_id, location)
        self.logger.log(f"Node {node_id} added at {location}.")

    def remove_node(self, node_id):
        """
        Removes a node from the network.
        
        Args:
            node_id (str): The unique identifier for the node to be removed.
        """
        if node_id not in self.nodes:
            raise NodeNetworkError(f"Node {node_id} does not exist.")
        del self.nodes[node_id]
        self.logger.log(f"Node {node_id} removed from the network.")

    async def monitor_nodes(self):
        """
        Periodically checks the health of all nodes in the network.
        """
        while True:
            self.logger.log("Monitoring node health...")
            for node_id, node in self.nodes.items():
                node.check_health()
            await asyncio.sleep(5)  # Check health every 5 seconds

    def get_node_location(self, node_id):
        """
        Retrieves the location of a specific node.
        
        Args:
            node_id (str): The unique identifier for the node.

        Returns:
            str: The location of the node or an error message if not found.
        """
        node = self.nodes.get(node_id)
        if node:
            self.logger.log(f"Location of {node_id}: {node.location}")
            return node.location
        else:
            self.logger.log(f"Node {node_id} not found.")
            return "Node not found."

    def list_nodes(self):
        """
        Lists all nodes in the network along with their status.
        
        Returns:
            dict: A dictionary of node IDs and their active status.
        """
        node_status = {node_id: node.is_active for node_id, node in self.nodes.items()}
        self.logger.log(f"Current nodes in the network: {node_status}")
        return node_status
