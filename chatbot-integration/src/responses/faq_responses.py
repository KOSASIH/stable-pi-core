import random

class FAQResponses:
    def __init__(self):
        # Predefined FAQ responses
        self.faqs = {
            "What is your return policy?": [
                "Our return policy allows you to return items within 30 days of purchase.",
                "You can return any item within 30 days for a full refund, provided it is in its original condition.",
                "We accept returns within 30 days. Please ensure the item is unused and in its original packaging."
            ],
            "How can I track my order?": [
                "You can track your order using the tracking link sent to your email after purchase.",
                "To track your order, please visit our tracking page and enter your order number.",
                "You will receive a tracking number via email once your order has shipped. Use it to track your order."
            ],
            "What payment methods do you accept?": [
                "We accept all major credit cards, PayPal, and bank transfers.",
                "You can pay using Visa, MasterCard, American Express, or PayPal.",
                "We accept various payment methods including credit cards and PayPal for your convenience."
            ],
            "How do I contact customer support?": [
                "You can reach our customer support team via email at support@example.com or call us at 1-800-555-0199.",
                "For assistance, please contact our support team at support@example.com or through our live chat.",
                "You can contact customer support by emailing support@example.com or using the contact form on our website."
            ],
            "Do you ship internationally?": [
                "Yes, we offer international shipping to select countries. Please check our shipping policy for details.",
                "We do ship internationally! Please review our shipping options during checkout.",
                "International shipping is available. Check our website for a list of countries we ship to."
            ]
        }

    def get_faq_response(self, question):
        """Returns a random response for a given FAQ question."""
        question = question.strip()
        if question in self.faqs:
            return random.choice(self.faqs[question])
        else:
            return "I'm sorry, but I don't have an answer to that question. Please contact support for more information."

    def list_faqs(self):
        """Returns a list of available FAQ questions."""
        return list(self.faqs.keys())

# Example usage
if __name__ == "__main__":
    faq_responses = FAQResponses()
    
    # Example FAQ questions
    print(faq_responses.get_faq_response("What is your return policy?"))  # Random response for return policy
    print(faq_responses.get_faq_response("How can I track my order?"))    # Random response for order tracking
    print(faq_responses.get_faq_response("What payment methods do you accept?"))  # Random response for payment methods
    print(faq_responses.get_faq_response("Unknown question?"))  # Response for an unknown question
    print("Available FAQs:", faq_responses.list_faqs())  # List of available FAQs
