# tests/test_neuromorphic_analytics/test_npae.py

import unittest
from src.neuromorphic_analytics.npae import NeuromorphicPredictiveAnalyticsEngine
from src.neuromorphic_analytics.model import SpikingNeuralNetworkModel
from unittest.mock import patch

class TestNPAE(unittest.TestCase):
    def setUp(self):
        """Set up the Neuromorphic Predictive Analytics Engine for testing."""
        model_params = {'num_neurons': 10, 'threshold': 1.0, 'decay': 0.9}
        data_sources = ['source1', 'source2']
        self.npae = NeuromorphicPredictiveAnalyticsEngine(model_params, data_sources)

    @patch('src.neuromorphic_analytics.data_pipeline.DataPipeline.collect_data')
    @patch('src.neuromorphic_analytics.data_pipeline.DataPipeline.preprocess_data')
    def test_process_data(self, mock_preprocess_data, mock_collect_data):
        """Test the data processing functionality."""
        mock_collect_data.return_value = [0.5, 0.7, 0.2]
        mock_preprocess_data.return_value = [0.5, 0.7, 0.2]

        predictions = self.npae.process_data()
        self.assertEqual(len(predictions), 3)  # Expecting 3 predictions
        self.assertTrue(all(isinstance(pred, int) for pred in predictions))  # Predictions should be integers (0 or 1)

    @patch('src.neuromorphic_analytics.model.SpikingNeuralNetworkModel.evaluate')
    def test_evaluate_model(self, mock_evaluate):
        """Test the model evaluation functionality."""
        mock_evaluate.return_value = 0.85  # Simulate an accuracy of 85%
        accuracy = self.npae.evaluate_model([[0.5]], [1])
        self.assertEqual(accuracy, 0.85)  # Check if the returned accuracy matches the mock

if __name__ == '__main__':
    unittest.main()
