// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract Governance is Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private proposalIdCounter;

    struct Proposal {
        uint256 id;
        string description;
        uint256 voteCount;
        mapping(address => bool) voters;
        bool executed;
    }

    mapping(uint256 => Proposal) public proposals;

    event ProposalCreated(uint256 id, string description);
    event Voted(uint256 proposalId, address voter);
    event ProposalExecuted(uint256 proposalId);

    function createProposal(string memory description) external onlyOwner {
        proposalIdCounter.increment();
        uint256 proposalId = proposalIdCounter.current();

        Proposal storage newProposal = proposals[proposalId];
        newProposal.id = proposalId;
        newProposal.description = description;

        emit ProposalCreated(proposalId, description);
    }

    function vote(uint256 proposalId) external {
        Proposal storage proposal = proposals[proposalId];
        require(!proposal.voters[msg.sender], "You have already voted.");
        require(!proposal.executed, "Proposal has already been executed.");

        proposal.voters[msg.sender] = true;
        proposal.voteCount += 1;

        emit Voted(proposalId, msg.sender);
    }

    function executeProposal(uint256 proposalId) external onlyOwner {
        Proposal storage proposal = proposals[proposalId];
        require(!proposal.executed, "Proposal has already been executed.");

        // Here you can implement the logic to execute the proposal
        // For example, changing a state variable or transferring funds

        proposal.executed = true;
        emit ProposalExecuted(proposalId);
    }
}
