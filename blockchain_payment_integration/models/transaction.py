from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from datetime import datetime

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey('payments.id'), nullable=False)
    transaction_id = Column(String(100), nullable=False)  # ID from the payment provider
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)  # ISO currency code
    status = Column(String(50), nullable=False)    # Status of the transaction
    created_at = Column(DateTime, default=datetime.utcnow)

    payment = relationship("Payment", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, transaction_id={self.transaction_id}, amount={self.amount}, status={self.status})>"

    @validates('amount')
    def validate_amount(self, key, amount):
        """Validate that the amount is positive."""
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        return amount

    @validates('currency')
    def validate_currency(self, key, currency):
        """Validate that the currency is a valid ISO code."""
        if len(currency) != 3:
            raise ValueError("Currency must be a 3-letter ISO code.")
        return currency.upper()

    @classmethod
    def create_transaction(cls, session, payment_id, transaction_id, amount, currency, status):
        """Create a new transaction record."""
        transaction = cls(payment_id=payment_id, transaction_id=transaction_id, amount=amount, currency=currency, status=status)
        session.add(transaction)
        session.commit()
        return transaction

    @classmethod
    def get_transaction_by_id(cls, session, transaction_id):
        """Retrieve a transaction by its ID."""
        return session.query(cls).filter _by(id=transaction_id).first()

    @classmethod
    def update_transaction_status(cls, session, transaction_id, new_status):
        """Update the status of a transaction."""
        transaction = cls.get_transaction_by_id(session, transaction_id)
        if transaction:
            transaction.status = new_status
            session.commit()
            return transaction
        raise ValueError("Transaction not found.")
