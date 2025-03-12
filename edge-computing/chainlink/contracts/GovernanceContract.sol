// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract GovernanceContract is AccessControl {
    using Counters for Counters.Counter;

    // Roles
    bytes32 public constant PROPOSER_ROLE = keccak256("PROPOSER_ROLE");
    bytes32 public constant VOTER_ROLE = keccak256("VOTER_ROLE");

    // Proposal states
    enum ProposalState { Pending, Active, Executed, Canceled }

    // Proposal structure
    struct Proposal {
        string description;
        uint256 voteCount;
        uint256 endTime;
        ProposalState state;
        mapping(address => bool) voters;
    }

    // Proposal counter
    Counters.Counter private proposalCounter;

    // Mapping of proposals
    mapping(uint256 => Proposal) public proposals;

    // Events
    event ProposalCreated(uint256 indexed proposalId, string description, uint256 endTime);
    event Voted(uint256 indexed proposalId, address indexed voter);
    event ProposalExecuted(uint256 indexed proposalId);
    event ProposalCanceled(uint256 indexed proposalId);

    constructor() {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _setupRole(PROPOSER_ROLE, msg.sender);
        _setupRole(VOTER_ROLE, msg.sender);
    }

    // Create a new proposal
    function createProposal(string memory description, uint256 duration) external onlyRole(PROPOSER_ROLE) {
        require(duration > 0, "Duration must be greater than 0");

        uint256 proposalId = proposalCounter.current();
        proposalCounter.increment();

        Proposal storage newProposal = proposals[proposalId];
        newProposal.description = description;
        newProposal.endTime = block.timestamp + duration;
        newProposal.state = ProposalState.Active;

        emit ProposalCreated(proposalId, description, newProposal.endTime);
    }

    // Vote on a proposal
    function vote(uint256 proposalId) external onlyRole(VOTER_ROLE) {
        Proposal storage proposal = proposals[proposalId];

        require(proposal.state == ProposalState.Active, "Proposal is not active");
        require(block.timestamp < proposal.endTime, "Voting has ended");
        require(!proposal.voters[msg.sender], "You have already voted");

        proposal.voters[msg.sender] = true;
        proposal.voteCount++;

        emit Voted(proposalId, msg.sender);
    }

    // Execute a proposal
    function executeProposal(uint256 proposalId) external {
        Proposal storage proposal = proposals[proposalId];

        require(proposal.state == ProposalState.Active, "Proposal is not active");
        require(block.timestamp >= proposal.endTime, "Voting has not ended");

        proposal.state = ProposalState.Executed;

        // Execute the proposal logic here
        // For example, changing a state variable or calling another contract

        emit ProposalExecuted(proposalId);
    }

    // Cancel a proposal
    function cancelProposal(uint256 proposalId) external onlyRole(PROPOSER_ROLE) {
        Proposal storage proposal = proposals[proposalId];

        require(proposal.state == ProposalState.Active, "Proposal is not active");

        proposal.state = ProposalState.Canceled;

        emit ProposalCanceled(proposalId);
    }

    // Get proposal details
    function getProposal(uint256 proposalId) external view returns (
        string memory description,
        uint256 voteCount,
        uint256 endTime,
        ProposalState state
    ) {
        Proposal storage proposal = proposals[proposalId];
        return (proposal.description, proposal.voteCount, proposal.endTime, proposal.state);
    }
}
