# tests/test_generative_ai/test_feature_generation.py

import unittest
from unittest.mock import MagicMock
from src.generative_ai.feature_generation import FeatureGenerator

class TestFeatureGenerator(unittest.TestCase):
    def setUp(self):
        """Set up the FeatureGenerator instance for testing."""
        self.mock_model = MagicMock()
        self.feature_generator = FeatureGenerator(ai_model=self.mock_model)

    def test_generate_feature(self):
        """Test the feature generation functionality."""
        user_input = "I need a feature for better user engagement."
        expected_output = "New feature suggestion based on user input."
        
        # Mock the AI model's generate_text method
        self.mock_model.generate_text.return_value = expected_output
        
        # Generate the feature
        generated_feature = self.feature_generator.generate_feature(user_input)
        
        # Assert that the generated feature matches the expected output
        self.assertEqual(generated_feature, expected_output)
        self.mock_model.generate_text.assert_called_once()

    def test_generate_feature_with_context(self):
        """Test feature generation with additional context."""
        user_input = "I need a feature for better user engagement."
        context = {"target_audience": "young adults", "platform": "mobile"}
        expected_output = "New feature suggestion based on user input and context."
        
        # Mock the AI model's generate_text method
        self.mock_model.generate_text.return_value = expected_output
        
        # Generate the feature with context
        generated_feature = self.feature_generator.generate_feature(user_input, context)
        
        # Assert that the generated feature matches the expected output
        self.assertEqual(generated_feature, expected_output)
        self.mock_model.generate_text.assert_called_once()

    def test_create_prompt(self):
        """Test the prompt creation functionality."""
        user_input = "I need a feature for better user engagement."
        context = {"target_audience": "young adults", "platform": "mobile"}
        
        # Create the expected prompt
        expected_prompt = "Based on the following context: target_audience: young adults platform: mobile, generate a feature for: I need a feature for better user engagement."
        
        # Call the private method _create_prompt
        prompt = self.feature_generator._create_prompt(user_input, context)
        
        # Assert that the created prompt matches the expected prompt
        self.assertEqual(prompt, expected_prompt)

    def test_generate_feature_error(self):
        """Test error handling during feature generation."""
        user_input = "I need a feature for better user engagement."
        
        # Simulate an error in the AI model's generate_text method
        self.mock_model.generate_text.side_effect = Exception("API error")
        
        with self.assertRaises(Exception) as context:
            self.feature_generator.generate_feature(user_input)
        
        self.assertEqual(str(context.exception), "API error")

if __name__ == '__main__':
    unittest.main()
