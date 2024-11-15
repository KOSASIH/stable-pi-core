import pytest
from brownie import Stablecoin, Governance, accounts

@pytest.fixture(scope="module")
def stablecoin():
    return Stablecoin.deploy({'from': accounts[0]})

@pytest.fixture(scope="module")
def governance():
    return Governance.deploy({'from': accounts[0]})

def test_stablecoin_integration(stablecoin):
    stablecoin.mint(accounts[1], 100 * 10 ** 18, {'from': accounts[0]})
    assert stablecoin.balanceOf(accounts[1]) == 100 * 10 ** 18

def test_governance_integration(governance):
    governance.createProposal("Increase token supply", {'from': accounts[0]})
    proposal = governance.proposals(1)
    assert proposal.description() == "Increase token supply"
