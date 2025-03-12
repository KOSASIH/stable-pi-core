import random
from datetime import datetime

class GreetingResponses:
    def __init__(self):
        # Predefined greeting responses
        self.greetings = [
            "Hello! How can I assist you today?",
            "Hi there! What can I do for you?",
            "Greetings! How may I help you?",
            "Hey! What brings you here today?",
            "Welcome! How can I assist you?",
            "Good day! How can I help you?",
            "Hi! What questions do you have for me?",
            "Hello! I'm here to help you with anything you need."
        ]
        
        # Contextual greetings based on time of day
        self.morning_greetings = [
            "Good morning! How can I brighten your day?",
            "Rise and shine! What can I assist you with this morning?",
            "Morning! Ready to tackle the day? How can I help?"
        ]
        
        self.afternoon_greetings = [
            "Good afternoon! How can I assist you this fine day?",
            "Afternoon! What can I do for you?",
            "Hello! Hope your day is going well. How can I help?"
        ]
        
        self.evening_greetings = [
            "Good evening! How can I assist you tonight?",
            "Evening! What can I help you with as the day winds down?",
            "Hello! How can I make your evening better?"
        ]

    def get_greeting(self):
        """Returns a random greeting response."""
        return random.choice(self.greetings)

    def get_contextual_greeting(self):
        """Returns a greeting based on the current time of day."""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            return random.choice(self.morning_greetings)
        elif 12 <= current_hour < 18:
            return random.choice(self.afternoon_greetings)
        elif 18 <= current_hour < 22:
            return random.choice(self.evening_greetings)
        else:
            return "Hello! I'm here 24/7 to assist you."

# Example usage
if __name__ == "__main__":
    greeting_responses = GreetingResponses()
    print(greeting_responses.get_greeting())  # Random greeting
    print(greeting_responses.get_contextual_greeting())  # Contextual greeting based on time
