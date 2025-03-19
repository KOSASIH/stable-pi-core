# src/generative_ai/feature_generation.py

import logging

# Set up logging for the feature generation module
logger = logging.getLogger(__name__)

class FeatureGenerator:
    def __init__(self, ai_model):
        """
        Initialize the Feature Generator.

        Parameters:
        - ai_model (GenerativeAIModel): An instance of the GenerativeAIModel for generating features.
        """
        self.ai_model = ai_model
        logger.info("FeatureGenerator initialized.")

    def generate_feature(self, user_input, context=None):
        """
        Generate a new feature based on user input and optional context.

        Parameters:
        - user_input (str): The input provided by the user to guide feature generation.
        - context (dict, optional): Additional context to refine the feature generation.

        Returns:
        - str: The generated feature description.

        Raises:
        - Exception: If feature generation fails.
        """
        try:
            logger.info(f"Generating feature based on user input: {user_input}")
            prompt = self._create_prompt(user_input, context)
            generated_feature = self.ai_model.generate_text(prompt)
            logger.info("Feature generation successful.")
            return generated_feature
        except Exception as e:
            logger.error(f"Error generating feature: {e}")
            raise

    def _create_prompt(self, user_input, context):
        """
        Create a prompt for the AI model based on user input and context.

        Parameters:
        - user_input (str): The input provided by the user.
        - context (dict, optional): Additional context for feature generation.

        Returns:
        - str: The constructed prompt for the AI model.
        """
        if context:
            context_str = " ".join(f"{key}: {value}" for key, value in context.items())
            prompt = f"Based on the following context: {context_str}, generate a feature for: {user_input}"
        else:
            prompt = f"Generate a feature for: {user_input}"
        
        logger.debug(f"Constructed prompt: {prompt}")
        return prompt
