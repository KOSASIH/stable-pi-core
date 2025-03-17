import numpy as np
from typing import List, Dict, Any
from datetime import datetime

class EdgeProcessor:
    """
    A class to process data from biosensors at the edge.

    Attributes:
        sensor_data (List[Dict[str, Any]]): A list to store data from biosensors.
    """

    def __init__(self):
        self.sensor_data = []

    def receive_data(self, data: Dict[str, Any]):
        """
        Receives data from a biosensor and stores it for processing.

        Args:
            data (Dict[str, Any]): The data received from a biosensor.
        """
        self.sensor_data.append(data)

    def aggregate_data(self) -> Dict[str, Any]:
        """
        Aggregates data from all received biosensor data.

        Returns:
            Dict[str, Any]: A dictionary containing aggregated data.
        """
        if not self.sensor_data:
            return {}

        # Example aggregation: Calculate mean and standard deviation of sensor values
        values = [entry['value'] for entry in self.sensor_data if 'value' in entry]
        aggregated_data = {
            "mean": np.mean(values),
            "std_dev": np.std(values),
            "count": len(values),
            "timestamp": datetime.now().isoformat()
        }
        return aggregated_data

    def analyze_data(self) -> Dict[str, Any]:
        """
        Analyzes the received biosensor data and returns insights.

        Returns:
            Dict[str, Any]: A dictionary containing analysis results.
        """
        if not self.sensor_data:
            return {"message": "No data to analyze."}

        # Example analysis: Identify anomalies based on a threshold
        threshold = 75  # Example threshold
        anomalies = [entry for entry in self.sensor_data if entry['value'] > threshold]

        analysis_results = {
            "total_entries": len(self.sensor_data),
            "anomalies": anomalies,
            "timestamp": datetime.now().isoformat()
        }
        return analysis_results

    def clear_data(self):
        """Clears the stored sensor data after processing."""
        self.sensor_data.clear()

    def process_data(self) -> Dict[str, Any]:
        """
        Processes the received data by aggregating and analyzing it.

        Returns:
            Dict[str, Any]: A dictionary containing aggregated and analyzed data.
        """
        aggregated = self.aggregate_data()
        analysis = self.analyze_data()
        self.clear_data()  # Clear data after processing

        return {
            "aggregated_data": aggregated,
            "analysis_results": analysis
        }
