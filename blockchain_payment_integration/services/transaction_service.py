from models.transaction import Transaction  # Assuming you have a Transaction model defined
import logging

logger = logging.getLogger(__name__)

class TransactionService:
    def __init__(self, session):
        self.session = session

    def create_transaction(self, payment_id, transaction_id, amount, currency, status):
        """Create a new transaction record."""
        transaction = Transaction.create_transaction(self.session, payment_id, transaction_id, amount, currency, status)
        logger.info("Transaction created successfully: %s", transaction_id)
        return transaction

    def get_transaction_by_id(self, transaction_id):
        """Retrieve a transaction by its ID."""
        transaction = self.session.query(Transaction).filter_by(id=transaction_id).first()
        if transaction:
            logger.info("Transaction retrieved: %s", transaction.transaction_id)
            return transaction
        else:
            logger.warning("Transaction not found: %s", transaction_id)
            return None

    def get_transactions_by_payment_id(self, payment_id):
        """Retrieve all transactions associated with a specific payment ID."""
        transactions = self.session.query(Transaction).filter_by(payment_id=payment_id).all()
        logger.info("Retrieved %d transactions for payment ID: %s", len(transactions), payment_id)
        return transactions

    def delete_transaction(self, transaction_id):
        """Delete a transaction record."""
        transaction = self.get_transaction_by_id(transaction_id)
        if transaction:
            self.session.delete(transaction)
            self.session.commit()
            logger.info("Transaction deleted successfully: %s", transaction_id)
            return True
        else:
            logger.warning("Transaction not found for deletion: %s", transaction_id)
            return False
