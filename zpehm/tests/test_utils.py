import unittest
import numpy as np
from zpehm.src.utils import (
    joules_to_electronvolts,
    electronvolts_to_joules,
    normalize_vector,
    mean,
    variance
)

class TestUtils(unittest.TestCase):

    def test_joules_to_electronvolts(self):
        """Test conversion from Joules to electronvolts."""
        joules = 1.0
        expected_eV = joules / 1.60218e-19
        self.assertAlmostEqual(joules_to_electronvolts(joules), expected_eV, places=6)

    def test_electronvolts_to_joules(self):
        """Test conversion from electronvolts to Joules."""
        eV = 1.0
        expected_joules = eV * 1.60218e-19
        self.assertAlmostEqual(electronvolts_to_joules(eV), expected_joules, places=6)

    def test_normalize_vector(self):
        """Test normalization of a vector."""
        vector = np.array([3, 4])
        normalized = normalize_vector(vector)
        expected_normalized = np.array([0.6, 0.8])  # 3/5, 4/5
        np.testing.assert_array_almost_equal(normalized, expected_normalized)

    def test_normalize_zero_vector(self):
        """Test normalization of a zero vector raises an error."""
        zero_vector = np.array([0, 0])
        with self.assertRaises(ValueError):
            normalize_vector(zero_vector)

    def test_mean(self):
        """Test calculation of the mean."""
        values = [1, 2, 3, 4, 5]
        expected_mean = 3.0
        self.assertEqual(mean(values), expected_mean)

    def test_mean_empty_list(self):
        """Test that mean calculation raises an error for an empty list."""
        with self.assertRaises(ValueError):
            mean([])

    def test_variance(self):
        """Test calculation of the variance."""
        values = [1, 2, 3, 4, 5]
        expected_variance = 2.0
        self.assertEqual(variance(values), expected_variance)

    def test_variance_empty_list(self):
        """Test that variance calculation raises an error for an empty list."""
        with self.assertRaises(ValueError):
            variance([])

if __name__ == "__main__":
    unittest.main()
