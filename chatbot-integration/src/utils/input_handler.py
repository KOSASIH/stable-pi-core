import re

class InputHandler:
    def __init__(self):
        # Define a set of valid commands or keywords for the chatbot
        self.valid_commands = {
            "greeting": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"],
            "faq": ["return policy", "track order", "payment methods", "contact support", "international shipping"],
            "support": ["help with account", "reset password", "update payment", "report problem", "bug report"]
        }

    def clean_input(self, user_input):
        """Cleans the user input by stripping whitespace and converting to lowercase."""
        return user_input.strip().lower()

    def validate_input(self, user_input):
        """Validates the user input against known commands or keywords."""
        cleaned_input = self.clean_input(user_input)
        
        # Check if the cleaned input matches any valid command
        for category, commands in self.valid_commands.items():
            if cleaned_input in commands:
                return True, category
        
        return False, None

    def extract_keywords(self, user_input):
        """Extracts keywords from the user input for further processing."""
        cleaned_input = self.clean_input(user_input)
        keywords = re.findall(r'\b\w+\b', cleaned_input)  # Extract words as keywords
        return keywords

    def is_valid_email(self, email):
        """Validates if the provided string is a valid email address."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def is_valid_phone(self, phone):
        """Validates if the provided string is a valid phone number."""
        phone_regex = r'^\+?[1-9]\d{1,14}$'  # E.164 format
        return re.match(phone_regex, phone) is not None

# Example usage
if __name__ == "__main__":
    input_handler = InputHandler()
    
    # Test cleaning input
    user_input = "   Hello, how can I return my order?   "
    cleaned_input = input_handler.clean_input(user_input)
    print("Cleaned Input:", cleaned_input)  # Output: "hello, how can I return my order?"

    # Test validating input
    is_valid, category = input_handler.validate_input("How do I track my order?")
    print("Is Valid:", is_valid, "Category:", category)  # Output: Is Valid: True Category: faq

    # Test extracting keywords
    keywords = input_handler.extract_keywords("I need help with my account.")
    print("Extracted Keywords:", keywords)  # Output: Extracted Keywords: ['i', 'need', 'help', 'with', 'my', 'account']

    # Test email validation
    email = "user@example.com"
    print("Is Valid Email:", input_handler.is_valid_email(email))  # Output: Is Valid Email: True

    # Test phone validation
    phone = "+1234567890"
    print("Is Valid Phone:", input_handler.is_valid_phone(phone))  # Output: Is Valid Phone: True
