import pytest
from web3 import Web3
from solcx import compile_source

# Sample Solidity code for the DAO contract
DAO_CONTRACT_SOURCE = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DAO {
    struct Proposal {
        string description;
        uint256 voteCount;
        mapping(address => bool) voters;
        bool executed;
    }

    address public admin;
    Proposal[] public proposals;
    uint256 public proposalCount;
    uint256 public votingPeriod;
    uint256 public quorum;

    event ProposalCreated(uint256 proposalId, string description);
    event Voted(uint256 proposalId, address voter);
    event ProposalExecuted(uint256 proposalId);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can call this function");
        _;
    }

    modifier proposalExists(uint256 _proposalId) {
        require(_proposalId < proposalCount, "Proposal does not exist");
        _;
    }

    modifier notVoted(uint256 _proposalId) {
        require(!proposals[_proposalId].voters[msg.sender], "You have already voted");
        _;
    }

    modifier notExecuted(uint256 _proposalId) {
        require(!proposals[_proposalId].executed, "Proposal already executed");
        _;
    }

    constructor(uint256 _votingPeriod, uint256 _quorum) {
        admin = msg.sender;
        votingPeriod = _votingPeriod;
        quorum = _quorum;
    }

    function createProposal(string memory _description) public onlyAdmin {
        Proposal storage newProposal = proposals.push();
        newProposal.description = _description;
        newProposal.voteCount = 0;
        newProposal.executed = false;
        proposalCount++;

        emit ProposalCreated(proposalCount - 1, _description);
    }

    function vote(uint256 _proposalId) public 
        proposalExists(_proposalId) 
        notVoted(_proposalId) 
        notExecuted(_proposalId) 
    {
        Proposal storage proposal = proposals[_proposalId];
        proposal.voters[msg.sender] = true;
        proposal.voteCount++;

        emit Voted(_proposalId, msg.sender);
    }

    function executeProposal(uint256 _proposalId) public 
        proposalExists(_proposalId) 
        notExecuted(_proposalId) 
    {
        Proposal storage proposal = proposals[_proposalId];
        require(proposal.voteCount >= quorum, "Not enough votes to execute proposal");

        proposal.executed = true;

        emit ProposalExecuted(_proposalId);
    }

    function getProposal(uint256 _proposalId) public view 
        proposalExists(_proposalId) 
        returns (string memory, uint256, bool) 
    {
        Proposal storage proposal = proposals[_proposalId];
        return (proposal.description, proposal.voteCount, proposal.executed);
    }

    function getProposalCount() public view returns (uint256) {
        return proposalCount;
    }
}
'''

@pytest.fixture
def dao_contract(web3):
    # Compile the contract
    compiled_sol = compile_source(DAO_CONTRACT_SOURCE)
    contract_interface = compiled_sol['<stdin>:DAO']

    # Deploy the contract
    DAOContract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = DAOContract.constructor(7 days, 2).transact({'from': web3.eth.accounts[0]})
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    return web3.eth.contract(address=tx_receipt.contractAddress, abi=contract_interface['abi'])

def test_create_proposal(dao_contract):
    # Arrange
    admin = dao_contract.functions.admin().call()
    proposal_description = "Proposal 1"

    # Act
    tx_hash = dao_contract.functions.createProposal(proposal_description).transact({'from': admin})
    web3.eth.waitForTransactionReceipt(tx_hash)

    # Assert
    proposal_count = dao_contract.functions.getProposalCount().call()
    assert proposal_count == 1

    description, vote_count, executed = dao_contract.functions.getProposal(0).call()
    assert description == proposal_description
    assert vote_count == 0
    assert not executed

def test_vote(dao_contract):
    # Arrange
    admin = dao_contract.functions.admin().call()
    proposal_description = "Proposal 2"
    dao_contract.functions.createProposal(proposal_description).transact({'from': admin})

    # Act
    tx_hash = dao_contract.functions.vote(0).transact({'from': web3.eth.accounts[1]})
    web3.eth.waitForTransactionReceipt(tx_hash)

    # Assert
    description, vote_count, executed = dao_contract.functions.getProposal(0).call()
    assert vote_count == 1

def test_execute_proposal(dao_contract):
    # Arrange
    admin = dao_contract.functions.admin().call()
    proposal_description = "Proposal 3"
    dao_contract.functions.createProposal(proposal_description).transact({'from': admin})
    dao_contract.functions.vote(0).transact({'from': web3.eth.accounts[1]})

    # Act
    tx_hash = dao_contract.functions.executeProposal(0).transact({'from': admin})
    web3.eth.waitForTransactionReceipt(tx_hash)

    # Assert
    description, vote_count, executed = dao_contract.functions.getProposal(0).call()
    assert executed is True

def test_double_vote(dao_contract):
    # Arrange
    admin = dao_contract.functions.admin().call()
    proposal_description = "Proposal 4"
    dao_contract.functions.createProposal(proposal_description).transact({'from': admin})

    # Act
    dao_contract.functions.vote(0).transact({'from': web3.eth.accounts[1]})
    
    # Assert that voting again fails
    with pytest.raises(Exception):
        dao_contract.functions.vote(0).transact({'from': web3 .eth.accounts[1]})

def test_execute_nonexistent_proposal(dao_contract):
    # Arrange
    admin = dao_contract.functions.admin().call()

    # Act & Assert
    with pytest.raises(Exception):
        dao_contract.functions.executeProposal(999).transact({'from': admin})

def test_execute_proposal_without_quorum(dao_contract):
    # Arrange
    admin = dao_contract.functions.admin().call()
    proposal_description = "Proposal 5"
    dao_contract.functions.createProposal(proposal_description).transact({'from': admin})

    # Act & Assert
    with pytest.raises(Exception):
        dao_contract.functions.executeProposal(0).transact({'from': admin})

def test_get_proposal_count(dao_contract):
    # Arrange
    admin = dao_contract.functions.admin().call()
    dao_contract.functions.createProposal("Proposal 6").transact({'from': admin})
    dao_contract.functions.createProposal("Proposal 7").transact({'from': admin})

    # Act
    proposal_count = dao_contract.functions.getProposalCount().call()

    # Assert
    assert proposal_count == 2
