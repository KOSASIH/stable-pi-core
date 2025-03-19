import unittest
from data_processing.analytics.anomaly_detection import detect_anomaly
from data_processing.analytics.pattern_recognition import PatternRecognizer

class TestAnomalyDetection(unittest.TestCase):
    def setUp(self):
        self.thresholds = {
            'temperature': {'upper_limit': 28.0, 'lower_limit': 18.0},
            'humidity': {'upper_limit': 70.0, 'lower_limit': 30.0}
        }

    def test_anomaly_high_temperature(self):
        data = {'temperature': 30.0, 'humidity': 50.0}
        result = detect_anomaly(data)
        self.assertTrue(result, "Anomaly should be detected for high temperature.")

    def test_anomaly_low_temperature(self):
        data = {'temperature': 15.0, 'humidity': 50.0}
        result = detect_anomaly(data)
        self.assertTrue(result, "Anomaly should be detected for low temperature.")

    def test_anomaly_high_humidity(self):
        data = {'temperature': 25.0, 'humidity': 80.0}
        result = detect_anomaly(data)
        self.assertTrue(result, "Anomaly should be detected for high humidity.")

    def test_anomaly_low_humidity(self):
        data = {'temperature': 25.0, 'humidity': 20.0}
        result = detect_anomaly(data)
        self.assertTrue(result, "Anomaly should be detected for low humidity.")

    def test_no_anomaly(self):
        data = {'temperature': 25.0, 'humidity': 50.0}
        result = detect_anomaly(data)
        self.assertFalse(result, "No anomaly should be detected.")

class TestPatternRecognition(unittest.TestCase):
    def setUp(self):
        self.recognizer = PatternRecognizer(window_size=5)

    def test_moving_average(self):
        for i in range(10):
            self.recognizer.add_data(20 + i, 50 + i)
        patterns = self.recognizer.recognize_patterns()
        self.assertAlmostEqual(patterns['temperature_moving_average'], 24.0, places=1)
        self.assertAlmostEqual(patterns['humidity_moving_average'], 54.0, places=1)

if __name__ == '__main__':
    unittest.main()
