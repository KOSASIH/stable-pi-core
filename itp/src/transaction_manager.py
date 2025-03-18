import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TransactionManager:
    def __init__(self):
        """
        Initialize the Transaction Manager.
        """
        self.transactions = []  # List of transactions awaiting processing
        self.executed_transactions = []  # List of executed transactions
        logging.info("Transaction Manager initialized.")

    def create_transaction(self, sender, receiver, amount, contract=None):
        """
        Create a new transaction.
        
        :param sender: The sender's identifier.
        :param receiver: The receiver's identifier.
        :param amount: The amount to be transferred.
        :param contract: Optional smart contract to execute with the transaction.
        :return: The created transaction object.
        """
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'contract': contract,
            'status': 'pending'
        }
        self.transactions.append(transaction)
        logging.info(f"Transaction created: {transaction}")
        return transaction

    def validate_transaction(self, transaction):
        """
        Validate a transaction before execution.
        
        :param transaction: The transaction to validate.
        :return: Boolean indicating validity.
        """
        # Placeholder for actual validation logic
        if transaction['amount'] <= 0:
            logging.warning("Invalid transaction amount.")
            return False
        return True

    def execute_transaction(self, transaction):
        """
        Execute a validated transaction.
        
        :param transaction: The transaction to execute.
        """
        if self.validate_transaction(transaction):
            # Logic to transfer funds (placeholder)
            transaction['status'] = 'executed'
            logging.info(f"Executing transaction: {transaction}")

            # Execute smart contract if provided
            if transaction['contract']:
                self.execute_contract(transaction['contract'], transaction)

            # Update balances, etc. (placeholder logic)
            logging.info(f"Transaction executed successfully: {transaction}")
            self.executed_transactions.append(transaction)
        else:
            logging.warning("Transaction validation failed.")

    def execute_contract(self, contract, transaction):
        """
        Execute a smart contract associated with the transaction.
        
        :param contract: The smart contract to execute.
        :param transaction: The transaction associated with the contract.
        """
        # Placeholder for smart contract execution logic
        logging.info(f"Executing smart contract: {contract} for transaction: {transaction}")

    def process_transactions(self):
        """
        Process all transactions in the transaction pool.
        """
        for transaction in self.transactions:
            if transaction['status'] == 'pending':
                self.execute_transaction(transaction)

    def get_all_transactions(self):
        """
        Retrieve all transactions.
        
        :return: List of all transactions.
        """
        return self.transactions

    def get_executed_transactions(self):
        """
        Retrieve all executed transactions.
        
        :return: List of all executed transactions.
        """
        return self.executed_transactions

if __name__ == "__main__":
    # Example usage of the Transaction Manager
    tm = TransactionManager()
    transaction = tm.create_transaction("PlanetA", "PlanetB", 100)
    tm.process_transactions()
    print(tm.get_all_transactions())
    print(tm.get_executed_transactions())
