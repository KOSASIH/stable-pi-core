import random
from datetime import datetime

class ResponseGenerator:
    def __init__(self):
        # Predefined templates for dynamic responses
        self.greeting_templates = [
            "Hello, {name}! How can I assist you today?",
            "Hi, {name}! What can I do for you?",
            "Greetings, {name}! How may I help you?",
            "Hey, {name}! What brings you here today?",
            "Welcome, {name}! How can I assist you?",
        ]

        self.farewell_templates = [
            "Thank you for reaching out, {name}. Have a great day!",
            "Goodbye, {name}! If you have more questions, feel free to ask.",
            "Take care, {name}! I'm here if you need anything else.",
            "See you later, {name}! Don't hesitate to return if you need help.",
        ]

        self.faq_templates = {
            "return policy": [
                "Our return policy allows you to return items within 30 days of purchase. Would you like more details?",
                "You can return any item within 30 days for a full refund, provided it is in its original condition. Need help with a return?",
            ],
            "track order": [
                "To track your order, please visit our tracking page and enter your order number. Would you like the link?",
                "You can track your order using the tracking link sent to your email after purchase. Do you need assistance with that?",
            ],
            "payment methods": [
                "We accept all major credit cards, PayPal, and bank transfers. Would you like to know more about a specific method?",
                "You can pay using Visa, MasterCard, American Express, or PayPal. Do you have a preferred payment method?",
            ],
        }

    def generate_greeting(self, user_name):
        """Generates a personalized greeting response."""
        template = random.choice(self.greeting_templates)
        return template.format(name=user_name)

    def generate_farewell(self, user_name):
        """Generates a personalized farewell response."""
        template = random.choice(self.farewell_templates)
        return template.format(name=user_name)

    def generate_faq_response(self, question):
        """Generates a response for a given FAQ question."""
        question = question.lower()
        if question in self.faq_templates:
            template = random.choice(self.faq_templates[question])
            return template
        else:
            return "I'm sorry, but I don't have an answer to that question. Please contact support for more information."

    def generate_dynamic_response(self, user_input, user_name=None):
        """Generates a dynamic response based on user input."""
        cleaned_input = user_input.lower()
        
        if "hello" in cleaned_input or "hi" in cleaned_input:
            return self.generate_greeting(user_name or "there")
        elif "bye" in cleaned_input or "goodbye" in cleaned_input:
            return self.generate_farewell(user_name or "there")
        elif any(keyword in cleaned_input for keyword in self.faq_templates.keys()):
            return self.generate_faq_response(cleaned_input)
        else:
            return "I'm here to help! Can you please provide more details?"

# Example usage
if __name__ == "__main__":
    response_generator = ResponseGenerator()
    
    # Example dynamic responses
    print(response_generator.generate_greeting("Alice"))  # Personalized greeting
    print(response_generator.generate_farewell("Alice"))  # Personalized farewell
    print(response_generator.generate_faq_response("What is your return policy?"))  # FAQ response
    print(response_generator.generate_dynamic_response("Hello, I need help with my order.", "Alice"))  # Dynamic response
    print(response_generator.generate_dynamic_response("Goodbye!"))  # Farewell response
