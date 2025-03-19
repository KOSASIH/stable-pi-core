# tests/test_neuromorphic_analytics/test_data_pipeline.py

import unittest
from src.neuromorphic_analytics.data_pipeline import DataPipeline

class TestDataPipeline(unittest.TestCase):
    def setUp(self):
        """Set up the Data Pipeline for testing."""
        self.data_sources = ['source1', 'source2']
        self.data_pipeline = DataPipeline(self.data_sources)

    def test_collect_data(self):
        """Test the data collection functionality."""
        collected_data = self.data_pipeline.collect_data()
        self.assertEqual(len(collected_data), len(self.data_sources) * 5)  # Expecting 5 data points from each source

    def test_preprocess_data(self):
        """Test the data preprocessing functionality."""
        raw_data = [0.1, 0.5, 0.9]
        preprocessed_data = self.data_pipeline.preprocess_data(raw_data)
        self.assertEqual(len(preprocessed_data), len(raw_data))  # Check if the length remains the same
        self.assertTrue(all(0 <= data <= 1 for data in preprocessed_data))  # Check if all data is normalized

if __name__ == '__main__':
    unittest.main()
