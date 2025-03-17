import unittest
import pandas as pd
from ai_predictive_governance.model import PredictiveModel
from ai_predictive_governance.predictions import generate_recommendations

class TestPredictions(unittest.TestCase):
    def setUp(self):
        """Set up a PredictiveModel instance and sample data for testing."""
        self.input_shape = (1, 2)  # Example input shape
        self.model = PredictiveModel(input_shape=self.input_shape)

        # Sample data for training
        self.data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [5, 4, 3, 2, 1],
            'target': [1, 2, 3, 4, 5]
        })
        self.model.train(self.data, target_column='target', epochs=1)  # Train the model

    def test_generate_recommendations(self):
        """Test the generation of recommendations."""
        predictions_data = self.data[['feature1', 'feature2']]
        recommendations = generate_recommendations(self.model, predictions_data, target_column='target', num_recommendations=3)

        self.assertEqual(len(recommendations), 3)  # Check that we get the expected number of recommendations
        for recommendation in recommendations:
            self.assertIn("current_value", recommendation)
            self.assertIn("predicted_value", recommendation)
            self.assertIn("recommendation", recommendation)

if __name__ == "__main__":
    unittest.main()
