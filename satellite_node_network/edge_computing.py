import logging
import numpy as np

class EdgeComputing:
    """
    Class for managing edge computing functionalities for satellite nodes.

    Attributes:
        node_id (str): Unique identifier for the satellite node.
    """

    def __init__(self, node_id):
        """
        Initializes an EdgeComputing instance.

        Args:
            node_id (str): Unique identifier for the satellite node.
        """
        self.node_id = node_id
        logging.info(f"EdgeComputing initialized for Node {self.node_id}.")

    def process_data(self, raw_data):
        """
        Processes raw data received from sensors or other nodes.

        Args:
            raw_data (dict): The raw data to be processed.

        Returns:
            dict: The processed data.
        """
        logging.info(f"Node {self.node_id} received raw data: {raw_data}")
        
        # Example processing: Normalize numerical data
        processed_data = {}
        for key, value in raw_data.items():
            if isinstance(value, (int, float)):
                processed_data[key] = self.normalize(value)
            else:
                processed_data[key] = value  # Keep non-numeric data unchanged
        
        logging.info(f"Node {self.node_id} processed data: {processed_data}")
        return processed_data

    def normalize(self, value):
        """
        Normalizes a numerical value to a range of 0 to 1.

        Args:
            value (float): The value to normalize.

        Returns:
            float: The normalized value.
        """
        # Example normalization logic (this could be adjusted based on actual data ranges)
        normalized_value = (value - 0) / (100 - 0)  # Assuming the range is 0 to 100
        return max(0, min(1, normalized_value))  # Clamp to [0, 1]

    def store_data(self, processed_data):
        """
        Stores processed data locally.

        Args:
            processed_data (dict): The processed data to store.
        """
        # Here you would implement logic to store data, e.g., in a database or local storage
        logging.info(f"Node {self.node_id} storing processed data: {processed_data}")

    def communicate_with_node(self, other_node, data):
        """
        Communicates processed data to another node.

        Args:
            other_node (SatelliteNode): The node to communicate with.
            data (dict): The data to send.
        """
        # Simulate sending data to another node
        logging.info(f"Node {self.node_id} sending data to Node {other_node.node_id}: {data}")
        # In a real implementation, you would use a network protocol to send the data

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    edge_computing_node = EdgeComputing(node_id="Node1")
    
    raw_data = {
        'temperature': 75,
        'humidity': 50,
        'status': 'active'
    }
    
    processed_data = edge_computing_node.process_data(raw_data)
    edge_computing_node.store_data(processed_data)
