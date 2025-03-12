import unittest
from src.responses.greeting_responses import GreetingResponses  # Assuming you have a GreetingResponses class
from src.responses.faq_responses import FAQResponses  # Assuming you have a FAQResponses class
from src.responses.support_responses import SupportResponses  # Assuming you have a SupportResponses class

class TestGreetingResponses(unittest.TestCase):
    def setUp(self):
        """Set up the test case with a GreetingResponses instance."""
        self.greeting_responses = GreetingResponses()

    def test_get_greeting(self):
        """Test getting a random greeting response."""
        response = self.greeting_responses.get_greeting()
        self.assertIsInstance(response, str)  # Check if the response is a string

    def test_get_contextual_greeting(self):
        """Test getting a contextual greeting based on time of day."""
        response = self.greeting_responses.get_contextual_greeting()
        self.assertIsInstance(response, str)  # Check if the response is a string

class TestFAQResponses(unittest.TestCase):
    def setUp(self):
        """Set up the test case with a FAQResponses instance."""
        self.faq_responses = FAQResponses()

    def test_get_faq_response(self):
        """Test getting a response for a known FAQ question."""
        response = self.faq_responses.get_faq_response("What is your return policy?")
        self.assertIn("return policy", response.lower())  # Check if the response contains relevant information

    def test_get_faq_response_unknown(self):
        """Test getting a response for an unknown FAQ question."""
        response = self.faq_responses.get_faq_response("Unknown question?")
        self.assertEqual(response, "I'm sorry, but I don't have an answer to that question. Please contact support for more information.")

class TestSupportResponses(unittest.TestCase):
    def setUp(self):
        """Set up the test case with a SupportResponses instance."""
        self.support_responses = SupportResponses()

    def test_get_support_response(self):
        """Test getting a response for a known support query."""
        response = self.support_responses.get_support_response("I need help with my order.")
        self.assertIn("help with my order", response.lower())  # Check if the response contains relevant support information

    def test_get_support_response_unknown(self):
        """Test getting a response for an unknown support query."""
        response = self.support_responses.get_support_response("Unknown issue?")
        self.assertEqual(response, "I'm sorry, but I can't assist with that issue. Please contact our support team for further assistance.")

if __name__ == "__main__":
    unittest.main()
