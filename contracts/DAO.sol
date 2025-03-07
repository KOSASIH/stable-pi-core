// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DAO {
    struct Proposal {
        string description; // Description of the proposal
        uint256 voteCount;  // Number of votes received
        uint256 creationTime; // Time when the proposal was created
        mapping(address => bool) voters; // Track if an address has voted
        bool executed;      // Status of the proposal execution
    }

    address public admin; // Admin of the contract
    Proposal[] public proposals; // Array of proposals
    uint256 public proposalCount; // Total number of proposals
    uint256 public votingPeriod; // Duration for voting
    uint256 public quorum; // Minimum votes required for execution

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

    modifier withinVotingPeriod(uint256 _proposalId) {
        require(block.timestamp <= proposals[_proposalId].creationTime + votingPeriod, "Voting period has ended");
        _;
    }

    constructor(uint256 _votingPeriod, uint256 _quorum) {
        admin = msg.sender; // Set the contract deployer as the admin
        votingPeriod = _votingPeriod; // Set the voting period
        quorum = _quorum; // Set the quorum requirement
    }

    function createProposal(string memory _description) public onlyAdmin {
        Proposal storage newProposal = proposals.push();
        newProposal.description = _description;
        newProposal.voteCount = 0;
        newProposal.creationTime = block.timestamp; // Set the creation time
        newProposal.executed = false;
        proposalCount++;

        emit ProposalCreated(proposalCount - 1, _description);
    }

    function vote(uint256 _proposalId) public 
        proposalExists(_proposalId) 
        notVoted(_proposalId) 
        notExecuted(_proposalId) 
        withinVotingPeriod(_proposalId) 
    {
        Proposal storage proposal = proposals[_proposalId];
        proposal.voters[msg.sender] = true; // Mark the voter
        proposal.voteCount++; // Increment the vote count

        emit Voted(_proposalId, msg.sender);
    }

    function executeProposal(uint256 _proposalId) public 
        proposalExists(_proposalId) 
        notExecuted(_proposalId) 
    {
        Proposal storage proposal = proposals[_proposalId];
        require(proposal.voteCount >= quorum, "Not enough votes to execute proposal");

        // Logic to execute the proposal goes here
        // For example, transferring funds, changing state, etc.

        proposal.executed = true; // Mark the proposal as executed

        emit ProposalExecuted(_proposalId);
    }

    function getProposal(uint256 _proposalId) public view 
        proposalExists(_proposalId) 
        returns (string memory, uint256, bool, uint256) 
    {
        Proposal storage proposal = proposals[_proposalId];
        return (proposal.description, proposal.voteCount, proposal.executed, proposal.creationTime);
    }

    function getProposalCount() public view returns (uint256) {
        return proposalCount;
    }
}
