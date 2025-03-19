"""
edge_node - Class for managing edge nodes in an edge computing architecture.

This module provides a class for modeling an edge node that can
receive, process, and store data from the photonic transmission layer.
"""

import numpy as np

class EdgeNode:
    def __init__(self, node_id: str, processing_capacity: float):
        """
        Initializes an EdgeNode instance.

        Parameters:
            node_id (str): The unique identifier for the edge node.
            processing_capacity (float): The processing capacity of the node in operations per second.
        """
        self.node_id = node_id
        self.processing_capacity = processing_capacity
        self.data_storage = []

    def receive_data(self, data: np.ndarray):
        """
        Receives data from the photonic transmission layer.

        Parameters:
            data (np.ndarray): The data to be processed.
        """
        print(f"EdgeNode {self.node_id} received data: {data}")
        self.data_storage.append(data)

    def process_data(self):
        """
        Processes the received data based on the node's processing capacity.

        Returns:
            list: A list of processed results.
        """
        processed_results = []
        for data in self.data_storage:
            # Simulate data processing (e.g., averaging the data)
            if len(data) > 0:
                result = np.mean(data)  # Example processing: calculate the mean
                processed_results.append(result)
                print(f"EdgeNode {self.node_id} processed data: {data} -> Result: {result}")
            else:
                print(f"EdgeNode {self.node_id} received empty data.")
        
        # Clear the storage after processing
        self.data_storage.clear()
        return processed_results

    def __str__(self):
        return (f"EdgeNode(node_id={self.node_id}, "
                f"processing_capacity={self.processing_capacity} ops/s, "
                f"data_storage_size={len(self.data_storage)})")

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     edge_node = EdgeNode(node_id="Node1", processing_capacity=1e6)
#     print(edge_node)
#     
#     # Simulate receiving data
#     edge_node.receive_data(np.array([1, 2, 3, 4, 5]))
#     edge_node.receive_data(np.array([10, 20, 30]))
#     
#     # Process the received data
#     results = edge_node.process_data()
#     print("Processed Results:", results)
