import random

class SupportResponses:
    def __init__(self):
        # Predefined support responses
        self.support_queries = {
            "I need help with my account.": [
                "I'm here to help! Please provide me with your account details so I can assist you.",
                "Sure! What specific issue are you facing with your account?",
                "I can help with that. Can you please describe the problem you're experiencing?"
            ],
            "How do I reset my password?": [
                "To reset your password, go to the login page and click on 'Forgot Password'. Follow the instructions sent to your email.",
                "You can reset your password by clicking on the 'Forgot Password' link on the login page.",
                "To reset your password, please check your email for the reset link after clicking 'Forgot Password'."
            ],
            "I want to update my payment information.": [
                "You can update your payment information in the 'Account Settings' section under 'Payment Methods'.",
                "To update your payment details, log in to your account and navigate to 'Payment Information'.",
                "Please go to 'Account Settings' and select 'Payment Methods' to update your payment information."
            ],
            "How can I report a problem?": [
                "To report a problem, please contact our support team at support@example.com with details of the issue.",
                "You can report any issues by emailing us at support@example.com or using the contact form on our website.",
                "For reporting problems, please reach out to our support team via email at support@example.com."
            ],
            "What should I do if I encounter a bug?": [
                "If you encounter a bug, please report it to our support team with a description of the issue and steps to reproduce it.",
                "To report a bug, please send an email to support@example.com with details about the bug.",
                "We appreciate your feedback! Please let us know about any bugs by contacting support@example.com."
            ]
        }

    def get_support_response(self, query):
        """Returns a random response for a given support query."""
        query = query.strip()
        if query in self.support_queries:
            return random.choice(self.support_queries[query])
        else:
            return "I'm sorry, but I don't have an answer to that query. Please contact our support team for further assistance."

    def list_support_queries(self):
        """Returns a list of available support queries."""
        return list(self.support_queries.keys())

# Example usage
if __name__ == "__main__":
    support_responses = SupportResponses()
    
    # Example support queries
    print(support_responses.get_support_response("I need help with my account."))  # Random response for account help
    print(support_responses.get_support_response("How do I reset my password?"))    # Random response for password reset
    print(support_responses.get_support_response("I want to update my payment information."))  # Random response for payment update
    print(support_responses.get_support_response("Unknown query?"))  # Response for an unknown query
    print("Available Support Queries:", support_responses.list_support_queries())  # List of available support queries
