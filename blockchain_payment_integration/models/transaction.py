from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
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

    @classmethod
    def create_transaction(cls, session, payment_id, transaction_id, amount, currency, status):
        """Create a new transaction record."""
        transaction = cls(payment_id=payment_id, transaction_id=transaction_id, amount=amount, currency=currency, status=status)
        session.add(transaction)
        session.commit()
        return transaction
