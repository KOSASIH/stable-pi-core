// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract EthereumBridgeDAO is Ownable {
    struct Proposal {
        string description;
        uint256 voteCount;
        mapping(address => bool) voters;
        bool executed;
    }

    IERC20 public token; // The ERC20 token used for voting
    Proposal[] public proposals;
    uint256 public proposalCount;
    uint256 public votingPeriod; // Duration for voting
    uint256 public quorum; // Minimum votes required for execution

    event ProposalCreated(uint256 proposalId, string description);
    event Voted(uint256 proposalId, address voter);
    event ProposalExecuted(uint256 proposalId);
    event TokensLocked(address indexed user, uint256 amount, string destinationChain);

    constructor(address _token, uint256 _votingPeriod, uint256 _quorum) {
        token = IERC20(_token);
        votingPeriod = _votingPeriod;
        quorum = _quorum;
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

    function createProposal(string memory _description) external onlyOwner {
        Proposal storage newProposal = proposals.push();
        newProposal.description = _description;
        newProposal.voteCount = 0;
        newProposal.executed = false;
        proposalCount++;

        emit ProposalCreated(proposalCount - 1, _description);
    }

    function vote(uint256 _proposalId) external 
        proposalExists(_proposalId) 
        notVoted(_proposalId) 
        notExecuted(_proposalId) 
    {
        Proposal storage proposal = proposals[_proposalId];
        proposal.voters[msg.sender] = true;
        proposal.voteCount++;

        emit Voted(_proposalId, msg.sender);
    }

    function executeProposal(uint256 _proposalId) external 
        proposalExists(_proposalId) 
        notExecuted(_proposalId) 
    {
        Proposal storage proposal = proposals[_proposalId];
        require(proposal.voteCount >= quorum, "Not enough votes to execute proposal");

        proposal.executed = true;

        emit ProposalExecuted(_proposalId);
    }

    function lockTokens(uint256 amount, string memory destinationChain) external {
        require(token.balanceOf(msg.sender) >= amount, "Insufficient balance");
        token.transferFrom(msg.sender, address(this), amount);
        emit TokensLocked(msg.sender, amount, destinationChain);
    }

    // Function to unlock tokens (to be called by the bridge)
    function unlockTokens(address user, uint256 amount) external onlyOwner {
        token.transfer(user, amount);
    }

    function getProposal(uint256 _proposalId) external view 
        proposalExists(_proposalId) 
        returns (string memory, uint256, bool) 
    {
        Proposal storage proposal = proposals[_proposalId];
        return (proposal.description, proposal.voteCount, proposal.executed);
    }

    function getProposalCount() external view returns (uint256) {
        return proposalCount;
    }
}
