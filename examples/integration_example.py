import requests
from utils.config import Config

# Load configuration
config = Config('config.json')
api_url = config.get('api_url')  # Assuming you have an API URL in your config

def create_proposal(description):
    """Create a proposal in the governance system."""
    response = requests.post(f"{api_url}/create_proposal", json={'description': description})
    if response.status_code == 200:
        print("Proposal created successfully:", response.json())
    else:
        print("Failed to create proposal:", response.status_code, response.text)

def mint_tokens(recipient, amount):
    """Mint tokens for a specified recipient."""
    response = requests.post(f"{api_url}/mint", json={'recipient': recipient, 'amount': amount})
    if response.status_code == 200:
        print("Tokens minted successfully:", response.json())
    else:
        print("Failed to mint tokens:", response.status_code, response.text)

# Example usage
if __name__ == "__main__":
    # Create a proposal
    create_proposal("Increase token supply to meet demand.")

    # Mint tokens for a recipient
    recipient_address = '0xRecipientAddressHere'
    mint_amount = 100  # Amount of tokens to mint
    mint_tokens(recipient_address, mint_amount)
