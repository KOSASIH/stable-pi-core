import unittest
import numpy as np
from edge_computing.data_processing import process_data, aggregate_data, filter_data, normalize_data

class TestDataProcessing(unittest.TestCase):
    def test_process_data_mean(self):
        """Test processing data with mean operation."""
        data = np.array([1, 2, 3, 4, 5])
        result = process_data(data, operation='mean')
        self.assertEqual(result, 3.0)

    def test_process_data_sum(self):
        """Test processing data with sum operation."""
        data = np.array([1, 2, 3, 4, 5])
        result = process_data(data, operation='sum')
        self.assertEqual(result, 15)

    def test_process_data_max(self):
        """Test processing data with max operation."""
        data = np.array([1, 2, 3, 4, 5])
        result = process_data(data, operation='max')
        self.assertEqual(result, 5)

    def test_process_data_min(self):
        """Test processing data with min operation."""
        data = np.array([1, 2, 3, 4, 5])
        result = process_data(data, operation='min')
        self.assertEqual(result, 1)

    def test_aggregate_data(self):
        """Test aggregating multiple data arrays."""
        data1 = np.array([1, 2, 3])
        data2 = np.array([4, 5, 6])
        aggregated = aggregate_data([data1, data2])
        expected = np.array([1, 2, 3, 4, 5, 6])
        np.testing.assert_array_equal(aggregated, expected)

    def test_filter_data(self):
        """Test filtering data based on a threshold."""
        data = np.array([1, 2, 3, 4, 5])
        filtered = filter_data(data, threshold=3)
        expected = np.array([4, 5])
        np.testing.assert_array_equal (filtered, expected)

    def test_normalize_data(self):
        """Test normalizing data to a range of [0, 1]."""
        data = np.array([1, 2, 3, 4, 5])
        normalized = normalize_data(data)
        expected = np.array([0, 0.25, 0.5, 0.75, 1])
        np.testing.assert_array_almost_equal(normalized, expected)

if __name__ == '__main__':
    unittest.main()
