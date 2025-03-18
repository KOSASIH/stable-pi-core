# ebs/tests/test_signal_detector.py

import unittest
from ebs.signal_detector import SignalDetector
import logging

class TestSignalDetector(unittest.TestCase):
    def setUp(self):
        """Set up a new SignalDetector instance for each test."""
        self.detector = SignalDetector()

    def test_set_detection_threshold(self):
        """Test setting a valid detection threshold."""
        self.detector.set_detection_threshold(0.2)
        self.assertEqual(self.detector.detection_threshold, 0.2)

    def test_set_invalid_detection_threshold(self):
        """Test setting an invalid detection threshold."""
        with self.assertRaises(ValueError):
            self.detector.set_detection_threshold(1.5)

    def test_detect_signal_with_threshold(self):
        """Test signal detection with a set threshold."""
        self.detector.set_detection_threshold(0.1)
        detected_signals = self.detector.listen_for_signals(duration=1)
        self.assertTrue(any("Quantum Signal Detected!" in signal for signal in detected_signals) or len(detected_signals) == 0)

if __name__ == '__main__':
    unittest.main()
