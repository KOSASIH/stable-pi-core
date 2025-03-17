# src/generative_ai/model.py

import openai
import os

class GenerativeAIModel:
    def __init__(self, model_type='gpt-3.5-turbo'):
        self.model_type = model_type
        self.api_key = os.getenv('OPENAI_API_KEY')  # Ensure the API key is set in environment variables
        openai.api_key = self.api_key

    def generate_text(self, prompt):
        """Generate text using the specified model."""
        response = openai.ChatCompletion.create(
            model=self.model_type,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']

    def generate_image(self, prompt):
        """Generate an image using DALL-E."""
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response['data'][0]['url']
