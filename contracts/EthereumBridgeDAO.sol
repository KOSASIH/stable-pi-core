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

    enum LockStatus { Pending, Released }

    struct LockedToken {
        address user;
        uint256 amount;
        string destinationChain;
        LockStatus status;
    }

    IERC20 public token; // The ERC20 token used for locking and unlocking
    Proposal[] public proposals;
    uint256 public proposalCount;
    uint256 public votingPeriod; // Duration for voting
    uint256 public quorum; // Minimum votes required for execution

    // Mapping to track locked tokens
    mapping(uint256 => LockedToken) public lockedTokens;
    uint256 public lockedTokenCount;

    event ProposalCreated(uint256 proposalId, string description);
    event Voted(uint256 proposalId, address voter);
    event ProposalExecuted(uint256 proposalId);
    event TokensLocked(address indexed user, uint256 amount, string destinationChain, uint256 indexed lockId);
    event TokensUnlocked(address indexed user, uint256 amount);
    event LockStatusUpdated(uint256 indexed lockId, LockStatus status);

    constructor(address _token, uint256 _votingPeriod, uint256 _quorum) {
        require(_token != address(0), "Token address cannot be zero");
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

    // Function to create a new proposal
    function createProposal(string memory _description) external onlyOwner {
        Proposal storage newProposal = proposals.push();
        newProposal.description = _description;
        newProposal.voteCount = 0;
        newProposal.executed = false;
        proposalCount++;

        emit ProposalCreated(proposalCount - 1, _description);
    }

    // Function to vote on a proposal
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

    // Function to execute a proposal
    function executeProposal(uint256 _proposalId) external 
        proposalExists(_proposalId) 
        notExecuted(_proposalId) 
    {
        Proposal storage proposal = proposals[_proposalId];
        require(proposal.voteCount >= quorum, "Not enough votes to execute proposal");

        proposal.executed = true;

        emit ProposalExecuted(_proposalId);
    }

    // Function to lock tokens for cross-chain transfer
    function lockTokens(uint256 amount, string memory destinationChain) external {
        require(amount > 0, "Amount must be greater than zero");
        require(token.balanceOf(msg.sender) >= amount, "Insufficient balance");

        // Transfer tokens to the contract
        token.transferFrom(msg.sender, address(this), amount);

        // Record the locked token
        lockedTokens[lockedTokenCount] = LockedToken({
            user: msg.sender,
            amount: amount,
            destinationChain: destinationChain,
            status: LockStatus.Pending
        });

        emit TokensLocked(msg.sender, amount, destinationChain, lockedTokenCount);
        lockedTokenCount++;
    }

    // Function to unlock tokens (to be called by the BSC bridge)
    function unlockTokens(address user, uint256 amount) external onlyOwner {
        require(amount > 0, "Amount must be greater than zero");
        token.transfer(user, amount);
        emit TokensUnlocked(user, amount);
    }

    // Function to update the status of a locked token
    function updateLockStatus(uint256 lockId, LockStatus status) external onlyOwner {
        require(lockId < lockedTokenCount, "Invalid lock ID");
        lockedTokens[lockId].status = status;
        emit LockStatusUpdated(lockId, status);
    }

    // Function to get the details of a locked token
    function getLockedToken(uint256 lockId) external view returns (address user, uint256 amount, string memory destinationChain, LockStatus status) {
        require(lockId < lockedTokenCount, "Invalid lock ID");
        LockedToken storage lockedToken = lockedTokens[lockId];
        return (lockedToken.user, lockedToken.amount, lockedToken.destinationChain, lockedToken.status);
    }

    // Function to get the balance of the contract
    function getBalance() external view returns (uint256) {
        return token.balanceOf(address(this));
    }

    // Function to get the total number of proposals
    function getProposalCount() external view returns (uint256) {
        return proposalCount;
    }

    // Function to get details of a specific proposal
    function getProposal(uint256 _proposalId) external view 
        proposalExists(_proposalId) 
        returns (string memory, uint256, bool) 
    {
        Proposal storage proposal = proposals[_proposalId];
        return (proposal.description, proposal.voteCount, proposal.executed);
    }
}
