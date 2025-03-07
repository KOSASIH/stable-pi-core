import json
from web3 import Web3
from solcx import compile_source
import os

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

def main():
    # Connect to the Ethereum network (e.g., Ganache)
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Change to your provider
    assert w3.isConnected(), "Failed to connect to the Ethereum network"

    # Compile the contract
    compiled_sol = compile_source(DAO_CONTRACT_SOURCE)
    contract_interface = compiled_sol['<stdin>:DAO']

    # Set up the account to deploy the contract
    account = w3.eth.accounts[0]  # Use the first account from Ganache
    w3.eth.defaultAccount = account

    # Deploy the contract
    voting_period = 7 * 24 * 60 * 60  # 7 days in seconds
    quorum = 2  # Minimum votes required for execution
    dao_contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    
    # Create the transaction
    tx_hash = dao_contract.constructor(voting_period, quorum).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    print(f"DAO contract deployed at address: {tx_receipt.contractAddress}")

    # Optionally save the contract address and ABI for future interactions
    with open('dao_contract_info.json', 'w') as f:
        json.dump({
            'address': tx_receipt.contractAddress,
            'abi': contract_interface['abi']
        }, f)

if __name__ == '__main__':
    main()
