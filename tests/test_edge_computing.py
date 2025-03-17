import unittest
from synthetic_biology.edge_computing import EdgeProcessor
from datetime import datetime
import random

class TestEdgeProcessor(unittest.TestCase):
    def setUp(self):
        """Set up an EdgeProcessor instance for testing."""
        self.edge_processor = EdgeProcessor()

    def test_receive_data(self):
        """Test receiving data from biosensors."""
        test_data = {
            "sensor_id": "biosensor_001",
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "value": random.uniform(0, 100),
            "unit": "units"
        }
        self.edge_processor.receive_data(test_data)
        self.assertEqual(len(self.edge_processor.sensor_data), 1)
        self.assertEqual(self.edge_processor.sensor_data[0]["sensor_id"], "biosensor_001")

    def test_aggregate_data(self):
        """Test data aggregation from received biosensor data."""
        for _ in range(5):
            test_data = {
                "sensor_id": "biosensor_001",
                "timestamp": datetime.utcnow().isoformat() + 'Z',
                "value": random.uniform(0, 100),
                "unit": "units"
            }
            self.edge_processor.receive_data(test_data)

        aggregated_data = self.edge_processor.aggregate_data()
        self.assertIn("mean", aggregated_data)
        self.assertIn("std_dev", aggregated_data)
        self.assertIn("count", aggregated_data)
        self.assertEqual(aggregated_data["count"], 5)

    def test_analyze_data(self):
        """Test data analysis for anomalies."""
        # Adding normal data
        for _ in range(5):
            test_data = {
                "sensor_id": "biosensor_001",
                "timestamp": datetime.utcnow().isoformat() + 'Z',
                "value": random.uniform(0, 50),  # Normal values
                "unit": "units"
            }
            self.edge_processor.receive_data(test_data)

        # Adding an anomaly
        anomaly_data = {
            "sensor_id": "biosensor_001",
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "value": 100,  # Anomalous value
            "unit": "units"
        }
        self.edge_processor.receive_data(anomaly_data)

        analysis_results = self.edge_processor.analyze_data()
        self.assertIn("total_entries", analysis_results)
        self.assertIn("anomalies", analysis_results)
        self.assertEqual(analysis_results["total_entries"], 6)
        self.assertEqual(len(analysis_results["anomalies"]), 1)  # One anomaly should be detected

    def test_clear_data(self):
        """Test clearing the stored sensor data after processing."""
        test_data = {
            "sensor_id": "biosensor_001",
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "value": random.uniform(0, 100),
            "unit": "units"
        }
        self.edge_processor.receive_data(test_data)
        self.assertEqual(len(self.edge_processor.sensor_data), 1)

        self.edge_processor.clear_data()
        self.assertEqual(len(self.edge_processor.sensor_data), 0)

    def test_process_data(self):
        """Test the complete data processing workflow."""
        for _ in range(5):
            test_data = {
                "sensor_id": "biosensor_001",
                "timestamp": datetime.utcnow().isoformat() + 'Z',
                "value": random.uniform(0, 100),
                "unit": "units"
            }
            self.edge_processor.receive_data(test_data)

        processed_data = self.edge_processor.process_data()
        self.assertIn("aggregated_data", processed_data)
        self.assertIn("analysis_results", processed_data)
        self.assertGreater(processed_data["aggregated_data"]["count"], 0)

if __name__ == "__main__":
    unittest.main()
