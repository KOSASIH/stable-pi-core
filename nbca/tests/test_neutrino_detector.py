# nbca/tests/test_neutrino_detector.py

import unittest
from nbca.neutrino_detector import NeutrinoDetector
import logging

class TestNeutrinoDetector(unittest.TestCase):
    def setUp(self):
        """Set up a new NeutrinoDetector instance for each test."""
        self.detector = NeutrinoDetector(detector_type="IceCube")

    def test_set_detection_threshold(self):
        """Test setting a valid detection threshold."""
        self.detector.set_detection_threshold(0.2)
        self.assertEqual(self.detector.detection_threshold, 0.2)

    def test_set_invalid_detection_threshold(self):
        """Test setting an invalid detection threshold."""
        with self.assertRaises(ValueError):
            self.detector.set_detection_threshold(1.5)

    def test_detect_event_with_threshold(self):
        """Test neutrino event detection with a set threshold."""
        self.detector.set_detection_threshold(0.1)
        event = self.detector.detect_event()
        self.assertTrue(event is None or isinstance(event, dict))

    def test_event_id_generation(self):
        """Test unique event ID generation."""
        event_id = self.detector.generate_event_id()
        self.assertTrue(event_id.startswith("NEUTRINO-"))

if __name__ == '__main__':
    unittest.main()
