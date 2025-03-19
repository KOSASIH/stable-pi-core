# src/generative_ai/model.py

import openai
import os
import logging

# Set up logging for the model module
logger = logging.getLogger(__name__)

class GenerativeAIModel:
    def __init__(self, model_type='gpt-3.5-turbo'):
        """
        Initialize the Generative AI Model.

        Parameters:
        - model_type (str): The type of model to use (default is 'gpt-3.5-turbo').
        """
        self.model_type = model_type
        self.api_key = os.getenv('OPENAI_API_KEY')  # Ensure the API key is set in environment variables
        openai.api_key = self.api_key

        logger.info(f"Generative AI Model initialized with model type: {self.model_type}")

    def generate_text(self, prompt, max_tokens=150):
        """
        Generate text using the specified model.

        Parameters:
        - prompt (str): The input prompt for text generation.
        - max_tokens (int): The maximum number of tokens to generate (default is 150).

        Returns:
        - str: The generated text response.
        """
        try:
            logger.info(f"Generating text for prompt: {prompt}")
            response = openai.ChatCompletion.create(
                model=self.model_type,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            generated_text = response['choices'][0]['message']['content']
            logger.info("Text generation successful.")
            return generated_text
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise

    def generate_image(self, prompt, size="1024x1024"):
        """
        Generate an image using DALL-E.

        Parameters:
        - prompt (str): The input prompt for image generation.
        - size (str): The size of the generated image (default is "1024x1024").

        Returns:
        - str: The URL of the generated image.
        """
        try:
            logger.info(f"Generating image for prompt: {prompt}")
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size=size
            )
            image_url = response['data'][0]['url']
            logger.info("Image generation successful.")
            return image_url
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            raise
