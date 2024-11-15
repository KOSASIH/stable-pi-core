import pytest
from brownie import Governance, accounts

@pytest.fixture
def governance():
    return Governance.deploy({'from': accounts[0]})

def test_create_proposal(governance):
    governance.createProposal("Increase token supply", {'from': accounts[0]})
    proposal = governance.proposals(1)
    assert proposal.description() == "Increase token supply"
    assert proposal.voteCount() == 0

def test_vote(governance):
    governance.createProposal("Increase token supply", {'from': accounts[0]})
    governance.vote(1, {'from': accounts[1]})
    proposal = governance.proposals(1)
    assert proposal.voteCount() == 1
    assert proposal.voters(accounts[1]) == True

def test_vote_twice(governance):
    governance.createProposal("Increase token supply", {'from': accounts[0]})
    governance.vote(1, {'from': accounts[1]})
    with pytest.raises(ValueError):
        governance.vote(1, {'from': accounts[1]})  # Voting again should fail

def test_execute_proposal(governance):
    governance.createProposal("Increase token supply", {'from': accounts[0]})
    governance.vote(1, {'from': accounts[1]})
    governance.executeProposal(1, {'from': accounts[0]})
    proposal = governance.proposals(1)
    assert proposal.executed() == True

def test_execute_nonexistent_proposal(governance):
    with pytest.raises(ValueError):
        governance.executeProposal(999, {'from': accounts[0]})  # Nonexistent proposal
