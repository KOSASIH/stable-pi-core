import unittest
import numpy as np
from emotion_responsive_ai.emotion_detection import EmotionDetection

class TestEmotionDetection(unittest.TestCase):
    def setUp(self):
        """Set up an EmotionDetection instance for testing."""
        self.emotion_detector = EmotionDetection(use_affectiva=True)  # Change to False for Google Cloud Vision

    def test_detect_emotion_happy(self):
        """Test detection of happiness."""
        # Create a dummy frame that simulates a happy expression
        happy_frame = np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder for an actual image
        emotions = self.emotion_detector.detect_emotion(happy_frame)
        self.assertGreater(emotions['happiness'], 0.5, "Happiness should be detected.")

    def test_detect_emotion_sad(self):
        """Test detection of sadness."""
        # Create a dummy frame that simulates a sad expression
        sad_frame = np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder for an actual image
        emotions = self.emotion_detector.detect_emotion(sad_frame)
        self.assertGreater(emotions['sadness'], 0.5, "Sadness should be detected.")

    def test_detect_emotion_anger(self):
        """Test detection of anger."""
        # Create a dummy frame that simulates an angry expression
        angry_frame = np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder for an actual image
        emotions = self.emotion_detector.detect_emotion(angry_frame)
        self.assertGreater(emotions['anger'], 0.5, "Anger should be detected.")

    def test_detect_emotion_surprise(self):
        """Test detection of surprise."""
        # Create a dummy frame that simulates a surprised expression
        surprise_frame = np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder for an actual image
        emotions = self.emotion_detector.detect_emotion(surprise_frame)
        self.assertGreater(emotions['surprise'], 0.5, "Surprise should be detected.")

    def test_detect_emotion_fear(self):
        """Test detection of fear."""
        # Create a dummy frame that simulates a fearful expression
        fear_frame = np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder for an actual image
        emotions = self.emotion_detector.detect_emotion(fear_frame)
        self.assertGreater(emotions['fear'], 0.5, "Fear should be detected.")

    def test_detect_emotion_disgust(self):
        """Test detection of disgust."""
        # Create a dummy frame that simulates a disgusted expression
        disgust_frame = np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder for an actual image
        emotions = self.emotion_detector.detect_emotion(disgust_frame)
        self.assertGreater(emotions['disgust'], 0.5, "Disgust should be detected.")

    def test_detect_emotion_invalid_input(self):
        """Test detection with invalid input."""
        with self.assertRaises(Exception):
            self.emotion_detector.detect_emotion(None)  # Pass None to simulate invalid input

if __name__ == "__main__":
    unittest.main()
