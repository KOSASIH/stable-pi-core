# tests/test_utils.py

import unittest
import pandas as pd
import numpy as np
from utils.helpers import preprocess_data, validate_data, split_data

class TestUtils(unittest.TestCase):
    def test_preprocess_data(self):
        raw_data = {
            'feature1': [1, 2, np.nan],
            'feature2': [4, 5, 6],
            'target': [0, 1, 0]
        }
        processed_data = preprocess_data(pd.DataFrame(raw_data))
        self.assertFalse(processed_data['feature1'].isnull().any())  # Ensure no NaN values

    def test_validate_data(self):
        valid_data = {
            'feature1': [1, 2, 3],
            'feature2': [4, 5, 6],
            'target': [0, 1, 0]
        }
        self.assertTrue(validate_data(pd.DataFrame(valid_data)))  # Should return True for valid data

    def test_split_data(self):
        data = {
            'feature1': [1, 2, 3, 4],
            'feature2': [5, 6, 7, 8],
            'target': [0, 1, 0, 1]
        }
        train_data, test_data = split_data(pd.DataFrame(data), test_size=0.25)
        self.assertEqual(len(train_data), 3)  # 75% of 4 is 3
        self.assertEqual(len(test_data), 1)    # 25% of 4 is 1

if __name__ == '__main__':
    unittest.main()
