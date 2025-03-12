// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "./VotingMechanism.sol";

contract GovernanceContract is AccessControl {
    using SafeMath for uint256;

    bytes32 public constant PROPOSER_ROLE = keccak256("PROPOSER_ROLE");
    bytes32 public constant VOTER_ROLE = keccak256("VOTER_ROLE");

    VotingMechanism public votingMechanism;

    struct Proposal {
        uint256 id;
        string description;
        address proposer;
        uint256 voteCount;
        bool executed;
        uint256 creationTime;
        uint256 votingEndTime;
        uint256 quorum; // Minimum votes required for proposal to be executed
    }

    Proposal[] public proposals;

    event ProposalCreated(uint256 indexed proposalId, string description, address indexed proposer, uint256 votingEndTime);
    event ProposalExecuted(uint256 indexed proposalId);
    event ProposalCanceled(uint256 indexed proposalId);

    constructor(address _votingMechanism) {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _setupRole(PROPOSER_ROLE, msg.sender);
        _setupRole(VOTER_ROLE, msg.sender);
        votingMechanism = VotingMechanism(_votingMechanism);
    }

    function createProposal(string memory description, uint256 duration, uint256 quorum) external onlyRole(PROPOSER_ROLE) {
        require(duration > 0, "Voting duration must be greater than 0");
        require(quorum > 0, "Quorum must be greater than 0");

        uint256 proposalId = proposals.length;
        proposals.push(Proposal({
            id: proposalId,
            description: description,
            proposer: msg.sender,
            voteCount: 0,
            executed: false,
            creationTime: block.timestamp,
            votingEndTime: block.timestamp.add(duration),
            quorum: quorum
        }));

        emit ProposalCreated(proposalId, description, msg.sender, block.timestamp.add(duration));
    }

    function vote(uint256 proposalId) external onlyRole(VOTER_ROLE) {
        require(proposalId < proposals.length, "Proposal does not exist");
        require(!proposals[proposalId].executed, "Proposal already executed");
        require(block.timestamp < proposals[proposalId].votingEndTime, "Voting period has ended");

        // Call the voting mechanism to handle the voting logic
        votingMechanism.vote(proposalId, msg.sender);
        proposals[proposalId].voteCount = proposals[proposalId].voteCount.add(1);
    }

    function executeProposal(uint256 proposalId) external {
        require(proposalId < proposals.length, "Proposal does not exist");
        require(!proposals[proposalId].executed, "Proposal already executed");
        require(block.timestamp >= proposals[proposalId].votingEndTime, "Voting period has not ended");
        require(proposals[proposalId].voteCount >= proposals[proposalId].quorum, "Not enough votes to execute proposal");

        // Execute the proposal logic here (e.g., change a state variable, etc.)
        proposals[proposalId].executed = true;

        emit ProposalExecuted(proposalId);
    }

    function cancelProposal(uint256 proposalId) external onlyRole(PROPOSER_ROLE) {
        require(proposalId < proposals.length, "Proposal does not exist");
        require(!proposals[proposalId].executed, "Proposal already executed");
        require(block.timestamp < proposals[proposalId].votingEndTime, "Voting period has ended");

        delete proposals[proposalId]; // Remove the proposal
        emit ProposalCanceled(proposalId);
    }

    function getProposal(uint256 proposalId) external view returns (Proposal memory) {
        require(proposalId < proposals.length, "Proposal does not exist");
        return proposals[proposalId];
    }

    function getActiveProposals() external view returns (Proposal[] memory) {
        uint256 activeCount = 0;
        for (uint256 i = 0; i < proposals.length; i++) {
            if (!proposals[i].executed && block.timestamp < proposals[i].votingEndTime) {
                activeCount++;
            }
        }

        Proposal[] memory activeProposals = new Proposal[](activeCount);
        uint256 index = 0;
        for (uint256 i = 0; i < proposals.length; i++) {
            if (!proposals[i].executed && block.timestamp < proposals[i].votingEndTime) {
                activeProposals[index] = proposals[i];
                index++;
            }
        }

        return activeProposals }

    function getProposalCount() external view returns (uint256) {
        return proposals.length;
    }
}
