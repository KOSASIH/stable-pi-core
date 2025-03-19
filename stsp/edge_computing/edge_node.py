# stsp/edge_computing/edge_node.py

import logging
import json
import time

class EdgeNode:
    """
    Represents an edge computing node that processes data locally.
    """

    def __init__(self, node_id, processing_power):
        """
        Initialize the EdgeNode instance.

        :param node_id: Unique identifier for the edge node.
        :param processing_power: The processing power of the edge node (in arbitrary units).
        """
        self.node_id = node_id
        self.processing_power = processing_power
        self.data_queue = []
        logging.info("EdgeNode initialized with ID: %s and Processing Power: %d", node_id, processing_power)

    def receive_data(self, data):
        """
        Receive data for processing.

        :param data: The data to be processed.
        """
        self.data_queue.append(data)
        logging.info("Data received at EdgeNode %s: %s", self.node_id, data)

    def process_data(self):
        """
        Process the data in the queue.
        
        :return: Processed results.
        """
        if not self.data_queue:
            logging.warning("No data to process in EdgeNode %s.", self.node_id)
            return None

        # Simulate data processing
        processed_results = []
        for data in self.data_queue:
            time.sleep(1 / self.processing_power)  # Simulate processing time based on power
            processed_result = self._simulate_processing(data)
            processed_results.append(processed_result)
            logging.info("Processed data at EdgeNode %s: %s", self.node_id, processed_result)

        # Clear the queue after processing
        self.data_queue.clear()
        return processed_results

    def _simulate_processing(self, data):
        """
        Simulate processing of the data.

        :param data: The data to process.
        :return: Simulated processed result.
        """
        # Here we just return the data with a simple transformation for demonstration
        return {"original": data, "processed": data.upper()}  # Example transformation

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    edge_node = EdgeNode(node_id="EdgeNode_1", processing_power=5)

    # Simulate receiving data
    edge_node.receive_data("sensor_data_1")
    edge_node.receive_data("sensor_data_2")

    # Process the received data
    results = edge_node.process_data()
    print(f"Processed Results: {results}")
