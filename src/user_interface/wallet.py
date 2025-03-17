# src/user_interface/wallet.py

import logging

# Set up logging for the wallet module
logger = logging.getLogger(__name__)

class Wallet:
    def __init__(self, user_id):
        """
        Initialize the Wallet.

        Parameters:
        - user_id (str): The ID of the user associated with the wallet.
        """
        self.user_id = user_id
        self.balance = 0.0  # Initial balance
        logger.info(f"Wallet initialized for user: {self.user_id}")

    def deposit(self, amount):
        """
        Deposit an amount into the wallet.

        Parameters:
        - amount (float): The amount to deposit.

        Raises:
        - ValueError: If the amount is negative.
        """
        if amount < 0:
            logger.error("Deposit amount must be positive.")
            raise ValueError("Deposit amount must be positive.")
        
        self.balance += amount
        logger.info(f"Deposited {amount} to wallet. New balance: {self.balance}")

    def withdraw(self, amount):
        """
        Withdraw an amount from the wallet.

        Parameters:
        - amount (float): The amount to withdraw.

        Raises:
        - ValueError: If the amount is negative or exceeds the balance.
        """
        if amount < 0:
            logger.error("Withdrawal amount must be positive.")
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            logger.error("Insufficient balance for withdrawal.")
            raise ValueError("Insufficient balance for withdrawal.")
        
        self.balance -= amount
        logger.info(f"Withdrew {amount} from wallet. New balance: {self.balance}")

    def get_balance(self):
        """
        Get the current balance of the wallet.

        Returns:
        - float: The current balance.
        """
        logger.info(f"Current balance for user {self.user_id}: {self.balance}")
        return self.balance
