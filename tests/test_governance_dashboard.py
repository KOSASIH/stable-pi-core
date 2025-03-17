import unittest
from unittest.mock import patch, MagicMock
from ai_predictive_governance.governance_dashboard import GovernanceDashboard
from ai_predictive_governance.model import PredictiveModel
from flask import json

class TestGovernanceDashboard(unittest.TestCase):
    def setUp(self):
        """Set up a GovernanceDashboard instance for testing."""
        self.input_shape = (1, 2)  # Example input shape
        self.model = PredictiveModel(input_shape=self.input_shape)
        self.dashboard = GovernanceDashboard(self.model)

    @patch('ai_predictive_governance.governance_dashboard.generate_recommendations')
    def test_index_route(self):
        """Test the index route of the dashboard."""
        with self.dashboard.app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<!doctype html>', response.data)  # Check for HTML content

    @patch('ai_predictive_governance.governance_dashboard.generate_recommendations')
    def test_recommendations_route(self, mock_generate):
        """Test the recommendations route of the dashboard."""
        # Mock the recommendations
        mock_generate.return_value = [
            {"current_value": 1, "predicted_value": 2, "recommendation": "Increase"},
            {"current_value": 2, "predicted_value": 1, "recommendation": "Decrease"}
        ]

        with self.dashboard.app.test_client() as client:
            response = client.post('/recommendations', json={
                "target_column": "target",
                "num_recommendations": 2,
                "predictions_data": self.model.prepare_data(self.model.data, target_column='target')[0].tolist()
            })
            self.assertEqual(response.status_code, 200)
            recommendations = json.loads(response.data)
            self.assertEqual(len(recommendations), 2)
            self.assertIn("current_value", recommendations[0])
            self.assertIn("predicted_value", recommendations[0])
            self.assertIn("recommendation", recommendations[0])

    @patch('ai_predictive_governance.governance_dashboard.generate_recommendations')
    def test_recommendations_route_invalid_data(self, mock_generate):
        """Test the recommendations route with invalid data."""
        with self.dashboard.app.test_client() as client:
            response = client.post('/recommendations', json={})
            self.assertEqual(response.status_code, 400)  # Check for bad request

if __name__ == "__main__":
    unittest.main()
