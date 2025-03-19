// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract VotingMechanism is AccessControl {
    using SafeMath for uint256;

    bytes32 public constant DELEGATOR_ROLE = keccak256("DELEGATOR_ROLE");

    struct Vote {
        address voter;
        uint256 proposalId;
        bool hasVoted;
        bool voteChoice; // true for 'yes', false for 'no'
    }

    mapping(uint256 => mapping(address => Vote)) public votes; // proposalId => (voter => Vote)
    mapping(address => address) public delegates; // voter => delegate

    event Voted(uint256 indexed proposalId, address indexed voter, bool voteChoice);
    event Delegated(address indexed delegator, address indexed delegate);

    constructor() {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    function vote(uint256 proposalId, address voter, bool voteChoice) external onlyRole(DELEGATOR_ROLE) {
        require(!votes[proposalId][voter].hasVoted, "Voter has already voted");
        
        votes[proposalId][voter] = Vote({
            voter: voter,
            proposalId: proposalId,
            hasVoted: true,
            voteChoice: voteChoice
        });

        emit Voted(proposalId, voter, voteChoice);
    }

    function delegateVote(address delegate) external {
        require(delegate != msg.sender, "Cannot delegate to self");
        delegates[msg.sender] = delegate;

        emit Delegated(msg.sender, delegate);
    }

    function getVote(uint256 proposalId, address voter) external view returns (Vote memory) {
        return votes[proposalId][voter];
    }

    function getDelegate(address voter) external view returns (address) {
        return delegates[voter];
    }

    function executeDelegatedVote(uint256 proposalId) external {
        address delegate = delegates[msg.sender];
        require(delegate != address(0), "No delegate found");

        Vote memory delegatedVote = votes[proposalId][delegate];
        require(delegatedVote.hasVoted, "Delegate has not voted");

        votes[proposalId][msg.sender] = Vote({
            voter: msg.sender,
            proposalId: proposalId,
            hasVoted: true,
            voteChoice: delegatedVote.voteChoice
        });

        emit Voted(proposalId, msg.sender, delegatedVote.voteChoice);
    }
}
