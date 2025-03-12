# tests/test_payment.py

import pytest
from payment.payment_service import PaymentService
from payment.transaction import Transaction

@pytest.fixture
def payment_service():
    return PaymentService()

def test_create_transaction(payment_service):
    transaction = payment_service.create_transaction(user_id='user123', amount=100, currency='USD')
    assert transaction is not None
    assert transaction.user_id == 'user123'
    assert transaction.amount == 100
    assert transaction.currency == 'USD'
    assert transaction.status == 'pending'

def test_process_payment(payment_service):
    transaction = payment_service.create_transaction(user_id='user123', amount=100, currency='USD')
    completed_transaction = payment_service.process_payment(transaction)
    assert completed_transaction.status == 'completed'

def test_get_transaction_history(payment_service):
    payment_service.create_transaction(user_id='user123', amount=100, currency='USD')
    payment_service.create_transaction(user_id='user123', amount=200, currency='USD')
    history = payment_service.get_transaction_history(user_id='user123')
    assert len(history) == 2
