import unittest
import pandas as pd
from ai_predictive_governance.data_preprocessing import DataPreprocessor

class TestDataPreprocessor(unittest.TestCase):
    def setUp(self):
        """Set up a DataPreprocessor instance for testing."""
        # Sample data for testing
        self.raw_data = {
            "timestamp": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"],
            "value": [10, 20, None, 40],
            "category": ["A", "B", "A", "B"]
        }
        self.dataframe = pd.DataFrame(self.raw_data)
        self.data_preprocessor = DataPreprocessor(data=self.dataframe)

    def test_clean_data(self):
        """Test the cleaning of data."""
        cleaned_data = self.data_preprocessor.clean_data()
        self.assertEqual(len(cleaned_data), 4)  # Should still have 4 rows
        self.assertFalse(cleaned_data['value'].isnull().any())  # No null values should remain

    def test_normalize_data(self):
        """Test normalization of numerical data."""
        cleaned_data = self.data_preprocessor.clean_data()
        normalized_data = self.data_preprocessor.normalize_data(cleaned_data)

        # Check if normalization is done correctly
        self.assertAlmostEqual(normalized_data['value'].mean(), 0, places=1)
        self.assertAlmostEqual(normalized_data['value'].std(), 1, places=1)

    def test_preprocess(self):
        """Test the complete preprocessing pipeline."""
        preprocessed_data = self.data_preprocessor.preprocess()
        self.assertEqual(len(preprocessed_data), 4)  # Should still have 4 rows
        self.assertFalse(preprocessed_data['value'].isnull().any())  # No null values should remain
        self.assertAlmostEqual(preprocessed_data['value'].mean(), 0, places=1)
        self.assertAlmostEqual(preprocessed_data['value'].std(), 1, places=1)

if __name__ == "__main__":
    unittest.main()
