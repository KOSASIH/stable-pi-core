from sqlalchemy import Column, String, Integer, Float, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from datetime import datetime
import enum

Base = declarative_base()

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)  # ISO currency code
    method = Column(String(50), nullable=False)    # Payment method (e.g., 'coinbase', 'bitpay')
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount}, currency={self.currency}, status={self.status})>"

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

    def update_status(self, new_status):
        """Update the payment status."""
        if new_status not in PaymentStatus:
            raise ValueError("Invalid payment status")
        self.status = new_status

    @classmethod
    def create_payment(cls, session, amount, currency, method):
        """Create a new payment record."""
        payment = cls(amount=amount, currency=currency, method=method)
        session.add(payment)
        session.commit()
        return payment

    @classmethod
    def get_payment_by_id(cls, session, payment_id):
        """Retrieve a payment by its ID."""
        return session.query(cls).filter_by(id=payment_id).first()
