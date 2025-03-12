import random

def handle_greeting_intent(user_input):
    """
    Handles the greeting intent based on user input.
    
    Args:
        user_input (str): The input text from the user.
    
    Returns:
        str: A response message for the greeting intent.
    """
    # Define a list of possible greeting responses
    greetings = [
        "Hello! How can I assist you today?",
        "Hi there! What can I do for you?",
        "Greetings! How may I help you?",
        "Hey! What brings you here today?",
        "Hello! How can I make your day better?"
    ]

    # Check if the user input contains common greeting phrases
    if any(greet in user_input.lower() for greet in ["hello", "hi", "hey", "greetings", "what's up"]):
        return random.choice(greetings)
    
    # If no greeting detected, return a default response
    return "I'm here to help! How can I assist you today?"
