import unittest
import numpy as np
from emotion_responsive_ai.emotion_detection import EmotionDetection
from emotion_responsive_ai.ar_vr_integration import ARVRIntegration

class TestARVRIntegration(unittest.TestCase):
    def setUp(self):
        """Set up an ARVRIntegration instance for testing."""
        self.emotion_detector = EmotionDetection(use_affectiva=True)  # Change to False for Google Cloud Vision
        self.arvr_integration = ARVRIntegration(self.emotion_detector)

    def test_update_ar_vr_experience_happy(self):
        """Test AR-VR experience update for happy emotion."""
        # Create a dummy frame that simulates a happy expression
        happy_frame = np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder for an actual image
        emotions = {'happiness': 0.8, 'sadness': 0.1, 'anger': 0.1, 'surprise': 0.0, 'disgust': 0.0, 'fear': 0.0}
        
        # Mock the emotion detection method
        self.emotion_detector.detect_emotion = lambda x: emotions
        
        with self.assertLogs('emotion_responsive_ai.ar_vr_integration', level='INFO') as log:
            self.arvr_integration.update_ar_vr_experience(happy_frame)
            self.assertIn("Displaying happy content.", log.output[0])

    def test_update_ar_vr_experience_sad(self):
        """Test AR-VR experience update for sad emotion."""
        sad_frame = np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder for an actual image
        emotions = {'happiness': 0.1, 'sadness': 0.8, 'anger': 0.1, 'surprise': 0.0, 'disgust': 0.0, 'fear': 0.0}
        
        # Mock the emotion detection method
        self.emotion_detector.detect_emotion = lambda x: emotions
        
        with self.assertLogs('emotion_responsive_ai.ar_vr_integration', level='INFO') as log:
            self.arvr_integration.update_ar_vr_experience(sad_frame)
            self.assertIn("Displaying sad content.", log.output[0])

    def test_update_ar_vr_experience_angry(self):
        """Test AR-VR experience update for angry emotion."""
        angry_frame = np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder for an actual image
        emotions = {'happiness': 0.1, 'sadness': 0.1, 'anger': 0.8, 'surprise': 0.0, 'disgust': 0.0, 'fear': 0.0}
        
        # Mock the emotion detection method
        self.emotion_detector.detect_emotion = lambda x: emotions
        
        with self.assertLogs('emotion_responsive_ai.ar_vr_integration', level='INFO') as log:
            self.arvr_integration.update_ar_vr_experience(angry_frame)
            self.assertIn("Displaying angry content.", log.output[0])

    def test_update_ar_vr_experience_surprised(self):
        """Test AR-VR experience update for surprised emotion."""
        surprised_frame = np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder for an actual image
        emotions = {'happiness': 0.1, 'sadness': 0.1, 'anger': 0.1, 'surprise': 0.8, 'disgust': 0.0, 'fear': 0.0}
        
        # Mock the emotion detection method
        self.emotion_detector.detect_emotion = lambda x: emotions
        
        with self.assertLogs('emotion_responsive_ai.ar_vr_integration', level='INFO') as log:
            self.arvr_integration.update_ar_vr_experience(surprised_frame)
            self.assertIn("Displaying surprised content.", log.output[0])

    def test_update_ar_vr_experience_fearful(self):
        """Test AR-VR experience update for fearful emotion."""
        fearful_frame = np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder for an actual image
        emotions = {'happiness': 0.1, 'sadness': 0.1, 'anger': 0.1, 'surprise': 0.0, 'disgust': 0.0, 'fear': 0.8}
        
        # Mock the emotion detection method
        self.emotion_detector.detect_emotion = lambda x: emotions
        
        with self.assertLogs('emotion_responsive_ai.ar_vr_integration', level='INFO') as log:
            self.arvr_integration.update_ar_vr_experience(fearful_frame)
            self.assertIn("Displaying fearful content.", log.output[0])

    def test_update_ar_vr_experience_neutral(self):
        """Test AR-VR experience update for neutral emotion."""
        neutral_frame = np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder for an actual image
        emotions = {'happiness': 0.1, 'sadness': 0.1, 'anger': 0.1, 'surprise': 0.0, 'disgust': 0.0, 'fear': 0.1}
        
        # Mock the emotion detection method
        self.emotion_detector.detect_emotion = lambda x: emotions
        
        with self.assertLogs('emotion_responsive_ai.ar_vr_integration', level='INFO') as log:
            self.arvr_integration.update_ar_vr_experience(neutral_frame)
            self.assertIn("Displaying neutral content.", log.output[0])

if __name__ == "__main__":
    unittest.main()
