# src/intents/faq_intent.py

import json
import logging
from utils.response_generator import generate_response
from utils.logger import setup_logger

# Set up logging
logger = setup_logger()

class FAQIntent:
    def __init__(self, faqs_file='data/faqs.json'):
        self.faqs = self.load_faqs(faqs_file)

    def load_faqs(self, faqs_file):
        """Load FAQs from a JSON file."""
        try:
            with open(faqs_file, 'r') as file:
                faqs = json.load(file)
            logger.info("FAQs loaded successfully.")
            return faqs
        except Exception as e:
            logger.error(f"Error loading FAQs: {e}")
            return {}

    def get_answer(self, user_query):
        """Retrieve the answer for a given user query."""
        logger.info(f"Received user query: {user_query}")
        for faq in self.faqs:
            if user_query.lower() in faq['question'].lower():
                logger.info(f"Match found: {faq['question']}")
                return generate_response(faq['answer'])
        logger.warning("No match found for the user query.")
        return generate_response("I'm sorry, I couldn't find an answer to your question.")

    def handle_intent(self, user_query):
        """Handle the FAQ intent based on user query."""
        logger.info("Handling FAQ intent.")
        answer = self.get_answer(user_query)
        return answer

# Example usage
if __name__ == "__main__":
    faq_intent = FAQIntent()
    user_query = "What is your return policy?"
    response = faq_intent.handle_intent(user_query)
    print(response)
