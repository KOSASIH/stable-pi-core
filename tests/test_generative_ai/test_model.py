# tests/test_generative_ai/test_model.py

import unittest
from unittest.mock import patch, MagicMock
from src.generative_ai.model import GenerativeAIModel

class TestGenerativeAIModel(unittest.TestCase):
    def setUp(self):
        """Set up the GenerativeAIModel instance for testing."""
        self.model = GenerativeAIModel(model_type='gpt-3.5-turbo')

    @patch('src.generative_ai.model.openai.ChatCompletion.create')
    def test_generate_text(self, mock_chat_completion):
        """Test the text generation functionality."""
        # Mock the response from the OpenAI API
        mock_chat_completion.return_value = {
            'choices': [{'message': {'content': 'This is a generated response.'}}]
        }
        
        prompt = "What is the future of AI?"
        response = self.model.generate_text(prompt)
        
        # Assert that the response matches the expected output
        self.assertEqual(response, 'This is a generated response.')
        mock_chat_completion.assert_called_once_with(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )

    @patch('src.generative_ai.model.openai.Image.create')
    def test_generate_image(self, mock_image_create):
        """Test the image generation functionality."""
        # Mock the response from the OpenAI API
        mock_image_create.return_value = {
            'data': [{'url': 'http://example.com/generated_image.png'}]
        }
        
        prompt = "A futuristic city skyline"
        response = self.model.generate_image(prompt)
        
        # Assert that the response matches the expected output
        self.assertEqual(response, 'http://example.com/generated_image.png')
        mock_image_create.assert_called_once_with(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

    @patch('src.generative_ai.model.openai.ChatCompletion.create')
    def test_generate_text_error(self, mock_chat_completion):
        """Test error handling during text generation."""
        # Simulate an API error
        mock_chat_completion.side_effect = Exception("API error")
        
        with self.assertRaises(Exception) as context:
            self.model.generate_text("What is the future of AI?")
        
        self.assertEqual(str(context.exception), "API error")

    @patch('src.generative_ai.model.openai.Image.create')
    def test_generate_image_error(self, mock_image_create):
        """Test error handling during image generation."""
        # Simulate an API error
        mock_image_create.side_effect = Exception("API error")
        
        with self.assertRaises(Exception) as context:
            self.model.generate_image("A futuristic city skyline")
        
        self.assertEqual(str(context.exception), "API error")

if __name__ == '__main__':
    unittest.main()
