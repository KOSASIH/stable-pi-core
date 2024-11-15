import pytest
from brownie import Stablecoin, accounts

@pytest.fixture
def stablecoin():
    return Stablecoin.deploy({'from': accounts[0]})

def test_initial_supply(stablecoin):
    assert stablecoin.totalSupply() == 1_000_000 * 10 ** 18
    assert stablecoin.balanceOf(accounts[0]) == 1_000_000 * 10 ** 18

def test_mint(stablecoin):
    stablecoin.mint(accounts[1], 100 * 10 ** 18, {'from': accounts[0]})
    assert stablecoin.balanceOf(accounts[1]) == 100 * 10 ** 18

def test_burn(stablecoin):
    stablecoin.burn(50 * 10 ** 18, {'from': accounts[0]})
    assert stablecoin.balanceOf(accounts[0]) == (1_000_000 * 10 ** 18 - 50 * 10 ** 18)

def test_transfer_ownership(stablecoin):
    stablecoin.transferOwnership(accounts[1], {'from': accounts[0]})
    assert stablecoin.owner() == accounts[1]

def test_burn_insufficient_balance(stablecoin):
    with pytest.raises(ValueError):
        stablecoin.burn(1 * 10 ** 18, {'from': accounts[1]})  # Account 1 has no balance
