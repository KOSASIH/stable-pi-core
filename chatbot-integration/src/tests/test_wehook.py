import unittest
from src.webhook import WebhookHandler  # Assuming you have a WebhookHandler class in webhook.py

class TestWebhookHandler(unittest.TestCase):
    def setUp(self):
        """Set up the test case with a WebhookHandler instance."""
        self.webhook_handler = WebhookHandler()

    def test_handle_valid_request(self):
        """Test handling a valid request."""
        request_data = {
            "queryResult": {
                "queryText": "Hello",
                "parameters": {},
                "intent": {
                    "displayName": "greeting"
                }
            }
        }
        response = self.webhook_handler.handle_request(request_data)
        self.assertIn("Hello", response)  # Check if the response contains a greeting

    def test_handle_invalid_request(self):
        """Test handling an invalid request."""
        request_data = {}
        response = self.webhook_handler.handle_request(request_data)
        self.assertEqual(response, "Invalid request")  # Check for appropriate error message

    def test_handle_unknown_intent(self):
        """Test handling an unknown intent."""
        request_data = {
            "queryResult": {
                "queryText": "Unknown intent",
                "parameters": {},
                "intent": {
                    "displayName": "unknown"
                }
            }
        }
        response = self.webhook_handler.handle_request(request_data)
        self.assertEqual(response, "I'm sorry, I didn't understand that.")  # Check for unknown intent response

if __name__ == "__main__":
    unittest.main()
