# tests/test_zkp.py

import pytest
from payment.zkp_payment import ZKPPayment
from payment.transaction import Transaction

@pytest.fixture
def transaction():
    return Transaction(user_id='user123', amount=100, currency='USD')

def test_generate_proof(transaction):
    zkp = ZKPPayment()
    proof = zkp.generate_proof(transaction)
    assert proof is not None
    assert isinstance(proof, str)

def test_verify_proof(transaction):
    zkp = ZKPPayment()
    proof = zkp.generate_proof(transaction)
    is_valid = zkp.verify_proof(proof, transaction)
    assert is_valid is True

def test_verify_proof_invalid(transaction):
    zkp = ZKPPayment()
    invalid_proof = "invalid_proof_string"
    is_valid = zkp.verify_proof(invalid_proof, transaction)
    assert is_valid is False
