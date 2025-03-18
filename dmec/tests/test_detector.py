# dmec/tests/test_detector.py

import unittest
from dmec.detector import DarkMatterDetector
from dmec.config import Config

class TestDarkMatterDetector(unittest.TestCase):
    def setUp(self):
        """Set up a new DarkMatterDetector instance for each test."""
        self.detector = DarkMatterDetector()

    def test_initial_energy_output(self):
        """Test that the initial energy output is zero."""
        self.assertEqual(self.detector.get_energy_output(), 0)

    def test_detect_interaction(self):
        """Test the interaction detection logic."""
        # Set sensitivity to 0 (no interactions should be detected)
        self.detector.set_sensitivity(0)
        interactions = sum(self.detector.detect_interaction() for _ in range(1000))
        self.assertEqual(interactions, 0)

        # Set sensitivity to 1 (all interactions should be detected)
        self.detector.set_sensitivity(1)
        interactions = sum(self.detector.detect_interaction() for _ in range(1000))
        self.assertGreater(interactions, 0)

    def test_set_sensitivity(self):
        """Test setting the sensitivity of the detector."""
        self.detector.set_sensitivity(0.5)
        self.assertEqual(self.detector.sensitivity, 0.5)

        with self.assertRaises(ValueError):
            self.detector.set_sensitivity(1.5)  # Invalid sensitivity

if __name__ == '__main__':
    unittest.main()
