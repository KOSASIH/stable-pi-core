import pytest
from utils.helpers import is_valid_address, to_wei, from_wei

def test_is_valid_address():
    assert is_valid_address('0x32Be343B94f860124dC4fEe278FDCBD38C102D88') is True
    assert is_valid_address('invalid_address') is False

def test_to_wei():
    assert to_wei(1, 'ether') == 1000000000000000000
    assert to_wei(0.1, 'ether') == 100000000000000000

def test_from_wei():
    assert from_wei(1000000000000000000, 'ether') == 1.0
    assert from_wei(100000000000000000, 'ether') == 0.1
