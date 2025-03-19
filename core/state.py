import logging
from collections import defaultdict
from transaction import Transaction

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class State:
    def __init__(self):
        # Using a defaultdict to manage account balances
        self.balances = defaultdict(float)

    def update_state(self, transaction: Transaction) -> bool:
        """Update the state based on a transaction."""
        if self.validate_transaction(transaction):
            # Deduct the amount from the sender's balance
            self.balances[transaction.sender] -= transaction.amount
            # Add the amount to the recipient's balance
            self.balances[transaction.recipient] += transaction.amount
            logging.info(f"State updated: {transaction.sender} -> {transaction.recipient}: {transaction.amount}")
            return True
        else:
            logging.error(f"Transaction validation failed for: {transaction.transaction_id}")
            return False

    def validate_transaction(self, transaction: Transaction) -> bool:
        """Validate a transaction before updating the state."""
        # Check if the sender has enough balance
        if self.balances[transaction.sender] < transaction.amount:
            logging.error(f"Insufficient funds for transaction: {transaction.transaction_id}")
            return False
        return True

    def get_balance(self, address: str) -> float:
        """Get the balance of a specific address."""
        return self.balances[address]

    def __repr__(self) -> str:
        return f"State(balances={dict(self.balances)})"

# Example usage
if __name__ == "__main__":
    # Create a state instance
    state = State()

    # Simulate adding initial balances
    state.balances["AlicePublicKey"] = 100.0
    state.balances["BobPublicKey"] = 50.0

    # Create a sample transaction
    transaction = Transaction(sender="AlicePublicKey", recipient="BobPublicKey", amount=30, signature="SampleSignature")

    # Update the state with the transaction
    if state.update_state(transaction):
        print(f"Transaction successful. New balance for Alice: {state.get_balance('AlicePublicKey')}, New balance for Bob: {state.get_balance('BobPublicKey')}")
    else:
        print("Transaction failed.")
