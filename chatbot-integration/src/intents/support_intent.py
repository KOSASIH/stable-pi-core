# src/intents/support_intent.py

import json
import logging
from utils.response_generator import generate_response
from utils.input_handler import validate_input

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupportIntentHandler:
    def __init__(self):
        self.support_queries = {
            "password_reset": self.handle_password_reset,
            "order_status": self.handle_order_status,
            "technical_issue": self.handle_technical_issue,
            "refund_request": self.handle_refund_request,
            "general_inquiry": self.handle_general_inquiry,
        }

    def handle_support_query(self, user_input):
        """
        Main method to handle support queries based on user input.
        """
        logger.info("Received user input: %s", user_input)

        # Validate user input
        if not validate_input(user_input):
            return generate_response("I'm sorry, I didn't understand that. Can you please rephrase?")

        # Identify the intent
        intent = self.identify_intent(user_input)
        if intent in self.support_queries:
            return self.support_queries[intent](user_input)
        else:
            return generate_response("I'm here to help, but I need more information about your issue.")

    def identify_intent(self, user_input):
        """
        Identify the intent of the user input.
        """
        # Simple keyword matching for intent recognition
        if "reset password" in user_input.lower():
            return "password_reset"
        elif "order status" in user_input.lower():
            return "order_status"
        elif "technical issue" in user_input.lower() or "app not working" in user_input.lower():
            return "technical_issue"
        elif "refund" in user_input.lower() or "return" in user_input.lower():
            return "refund_request"
        else:
            return "general_inquiry"

    def handle_password_reset(self, user_input):
        """
        Handle password reset requests.
        """
        logger.info("Handling password reset request.")
        return generate_response("To reset your password, please follow the link sent to your email.")

    def handle_order_status(self, user_input):
        """
        Handle order status inquiries.
        """
        logger.info("Handling order status inquiry.")
        return generate_response("Please provide your order number to check the status.")

    def handle_technical_issue(self, user_input):
        """
        Handle technical issue reports.
        """
        logger.info("Handling technical issue report.")
        return generate_response("I'm sorry to hear you're having technical issues. Can you describe the problem in detail?")

    def handle_refund_request(self, user_input):
        """
        Handle refund requests.
        """
        logger.info("Handling refund request.")
        return generate_response("To process your refund, please provide your order number and the reason for the refund.")

    def handle_general_inquiry(self, user_input):
        """
        Handle general inquiries.
        """
        logger.info("Handling general inquiry.")
        return generate_response("I'm here to help! What would you like to know?")

# Example usage
if __name__ == "__main__":
    handler = SupportIntentHandler()
    user_query = "I need help with resetting my password."
    response = handler.handle_support_query(user_query)
    print(response)
