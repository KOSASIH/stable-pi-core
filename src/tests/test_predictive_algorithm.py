# tests/test_predictive_algorithm.py

import unittest
import numpy as np
import pandas as pd
from wdb.predictive_algorithm import PredictiveAlgorithm

class TestPredictiveAlgorithm(unittest.TestCase):
    def setUp(self):
        self.algorithm = PredictiveAlgorithm()

    def test_train_and_predict(self):
        historical_data = pd.DataFrame({
            'time': [1, 2, 3, 4, 5],
            'data_volume': [100, 150, 200, 250, 300]
        })
        self.algorithm.train(historical_data)
        predictions = self.algorithm.predict([6, 7, 8])
        expected_predictions = np.array([350, 400, 450])
        np.testing.assert_array_almost_equal(predictions, expected_predictions)

if __name__ == '__main__':
    unittest.main()
