import unittest
import numpy as np
from emotion_responsive_ai.voice_emotion_analysis import VoiceEmotionAnalysis

class TestVoiceEmotionAnalysis(unittest.TestCase):
    def setUp(self):
        """Set up a VoiceEmotionAnalysis instance for testing."""
        self.voice_emotion_analyzer = VoiceEmotionAnalysis(use_affectiva=True)  # Change to False for Google Cloud Vision

    def test_analyze_voice_happy(self):
        """Test analysis of a happy voice."""
        # Create a dummy audio file path (this should point to a real audio file for actual tests)
        happy_audio_file = 'test_audio/happy.wav'  # Placeholder path
        emotions = self.voice_emotion_analyzer.analyze_voice(happy_audio_file)
        self.assertGreater(emotions['happiness'], 0.5, "Happiness should be detected.")

    def test_analyze_voice_sad(self):
        """Test analysis of a sad voice."""
        sad_audio_file = 'test_audio/sad.wav'  # Placeholder path
        emotions = self.voice_emotion_analyzer.analyze_voice(sad_audio_file)
        self.assertGreater(emotions['sadness'], 0.5, "Sadness should be detected.")

    def test_analyze_voice_angry(self):
        """Test analysis of an angry voice."""
        angry_audio_file = 'test_audio/angry.wav'  # Placeholder path
        emotions = self.voice_emotion_analyzer.analyze_voice(angry_audio_file)
        self.assertGreater(emotions['anger'], 0.5, "Anger should be detected.")

    def test_analyze_voice_surprised(self):
        """Test analysis of a surprised voice."""
        surprised_audio_file = 'test_audio/surprised.wav'  # Placeholder path
        emotions = self.voice_emotion_analyzer.analyze_voice(surprised_audio_file)
        self.assertGreater(emotions['surprise'], 0.5, "Surprise should be detected.")

    def test_analyze_voice_fear(self):
        """Test analysis of a fearful voice."""
        fearful_audio_file = 'test_audio/fear.wav'  # Placeholder path
        emotions = self.voice_emotion_analyzer.analyze_voice(fearful_audio_file)
        self.assertGreater(emotions['fear'], 0.5, "Fear should be detected.")

    def test_analyze_voice_disgust(self):
        """Test analysis of a disgusted voice."""
        disgusted_audio_file = 'test_audio/disgust.wav'  # Placeholder path
        emotions = self.voice_emotion_analyzer.analyze_voice(disgusted_audio_file)
        self.assertGreater(emotions['disgust'], 0.5, "Disgust should be detected.")

    def test_analyze_voice_invalid_input(self):
        """Test analysis with invalid input."""
        with self.assertRaises(Exception):
            self.voice_emotion_analyzer.analyze_voice(None)  # Pass None to simulate invalid input

if __name__ == "__main__":
    unittest.main()
