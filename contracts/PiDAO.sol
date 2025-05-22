// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract PiDAO is Ownable {
    using Counters for Counters.Counter;

    struct Proposal {
        uint256 value;
        uint256 voteCount;
        uint256 endTime;
        bool executed;
        mapping(address => bool) hasVoted;
    }

    Counters.Counter private proposalIdCounter;
    mapping(uint256 => Proposal) public proposals;
    uint256 public constant GCV_VALUE = 314159 * 10**18; // $314,159
    uint256 public quorum; // Minimum votes required to pass a proposal

    event ProposalCreated(uint256 indexed proposalId, uint256 value, uint256 endTime);
    event Voted(uint256 indexed proposalId, address indexed voter);
    event ProposalExecuted(uint256 indexed proposalId, uint256 value);

    constructor(uint256 _quorum) {
        require(_quorum > 0, "Quorum must be greater than 0");
        quorum = _quorum;
    }

    function proposeValue(uint256 value) public {
        require(value == GCV_VALUE, "Value must be $314,159");
        
        proposalIdCounter.increment();
        uint256 proposalId = proposalIdCounter.current();
        
        Proposal storage newProposal = proposals[proposalId];
        newProposal.value = value;
        newProposal.endTime = block.timestamp + 7 days; // Voting period of 7 days

        emit ProposalCreated(proposalId, value, newProposal.endTime);
    }

    function vote(uint256 proposalId) public {
        Proposal storage proposal = proposals[proposalId];
        
        require(block.timestamp < proposal.endTime, "Voting period has ended");
        require(!proposal.hasVoted[msg.sender], "You have already voted on this proposal");

        proposal.voteCount += 1;
        proposal.hasVoted[msg.sender] = true;

        emit Voted(proposalId, msg.sender);

        // Check if the proposal has reached quorum
        if (proposal.voteCount >= quorum) {
            executeProposal(proposalId);
        }
    }

    function executeProposal(uint256 proposalId) internal {
        Proposal storage proposal = proposals[proposalId];
        
        require(block.timestamp >= proposal.endTime, "Voting period has not ended");
        require(!proposal.executed, "Proposal has already been executed");

        proposal.executed = true;

        // Logic to affirm the GCV value can be added here
        // For example, updating a state variable or triggering an event

        emit ProposalExecuted(proposalId, proposal.value);
    }

    function getProposal(uint256 proposalId) public view returns (uint256 value, uint256 voteCount, uint256 endTime, bool executed) {
        Proposal storage proposal = proposals[proposalId];
        return (proposal.value, proposal.voteCount, proposal.endTime, proposal.executed);
    }

    function setQuorum(uint256 newQuorum) public onlyOwner {
        require(newQuorum > 0, "Quorum must be greater than 0");
        quorum = newQuorum;
    }
}
