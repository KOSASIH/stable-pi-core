import unittest
import numpy as np
import pandas as pd
from ai_predictive_governance.model import PredictiveModel

class TestPredictiveModel(unittest.TestCase):
    def setUp(self):
        """Set up a PredictiveModel instance for testing."""
        self.input_shape = (1, 2)  # Example input shape
        self.model = PredictiveModel(input_shape=self.input_shape)

        # Sample data for training
        self.data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [5, 4, 3, 2, 1],
            'target': [1, 2, 3, 4, 5]
        })

    def test_train_model(self):
        """Test the training of the predictive model."""
        self.model.train(self.data, target_column='target', epochs=1)  # Train for 1 epoch for testing
        self.assertIsNotNone(self.model.model)  # Ensure the model is created

    def test_prepare_data(self):
        """Test the data preparation for LSTM."""
        X, y = self.model.prepare_data(self.data, target_column='target')
        self.assertEqual(X.shape, (4, 1, 2))  # 4 samples, 1 time step, 2 features
        self.assertEqual(y.shape, (4,))  # 4 target values

    def test_evaluate_model(self):
        """Test the evaluation of the predictive model."""
        self.model.train(self.data, target_column='target', epochs=1)  # Train the model
        mse = self.model.evaluate(self.data, target_column='target')
        self.assertIsInstance(mse, float)  # Ensure the evaluation returns a float

if __name__ == "__main__":
    unittest.main()
