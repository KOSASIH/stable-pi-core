import unittest
from src.intents.greeting_intent import GreetingIntent  # Assuming you have a GreetingIntent class

class TestGreetingIntent(unittest.TestCase):
    def setUp(self):
        """Set up the test case with a GreetingIntent instance."""
        self.greeting_intent = GreetingIntent()

    def test_handle_greeting(self):
        """Test handling a greeting intent."""
        user_input = "Hello"
        response = self.greeting_intent.handle(user_input)
        self.assertIn("Hello", response)  # Check if the response contains a greeting

    def test_handle_farewell(self):
        """Test handling a farewell intent."""
        user_input = "Goodbye"
        response = self.greeting_intent.handle(user_input)
        self.assertIn("Goodbye", response)  # Check if the response contains a farewell

if __name__ == "__main__":
    unittest.main()
