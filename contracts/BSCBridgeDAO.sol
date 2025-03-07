// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract BSCBridgeDAO is Ownable {
    IERC20 public token; // The ERC20 token used for unlocking and locking

    enum LockStatus { Pending, Released }
    
    struct LockedToken {
        address user;
        uint256 amount;
        string sourceChain;
        LockStatus status;
    }

    // Mapping to track locked tokens
    mapping(uint256 => LockedToken) public lockedTokens;
    uint256 public lockedTokenCount;

    event TokensUnlocked(address indexed user, uint256 amount);
    event TokensLocked(address indexed user, uint256 amount, string sourceChain, uint256 indexed lockId);
    event LockStatusUpdated(uint256 indexed lockId, LockStatus status);

    constructor(address _token) {
        require(_token != address(0), "Token address cannot be zero");
        token = IERC20(_token);
    }

    // Function to unlock tokens on BSC (to be called by the bridge)
    function unlockTokens(address user, uint256 amount) external onlyOwner {
        require(amount > 0, "Amount must be greater than zero");
        token.transfer(user, amount);
        emit TokensUnlocked(user, amount);
    }

    // Function to lock tokens (to be called by the Ethereum bridge)
    function lockTokens(uint256 amount, string memory sourceChain) external {
        require(amount > 0, "Amount must be greater than zero");
        require(token.balanceOf(msg.sender) >= amount, "Insufficient balance");
        
        // Transfer tokens to the contract
        token.transferFrom(msg.sender, address(this), amount);
        
        // Record the locked token
        lockedTokens[lockedTokenCount] = LockedToken({
            user: msg.sender,
            amount: amount,
            sourceChain: sourceChain,
            status: LockStatus.Pending
        });
        
        emit TokensLocked(msg.sender, amount, sourceChain, lockedTokenCount);
        lockedTokenCount++;
    }

    // Function to update the status of a locked token (to be called by the bridge)
    function updateLockStatus(uint256 lockId, LockStatus status) external onlyOwner {
        require(lockId < lockedTokenCount, "Invalid lock ID");
        lockedTokens[lockId].status = status;
        emit LockStatusUpdated(lockId, status);
    }

    // Function to get the details of a locked token
    function getLockedToken(uint256 lockId) external view returns (address user, uint256 amount, string memory sourceChain, LockStatus status) {
        require(lockId < lockedTokenCount, "Invalid lock ID");
        LockedToken storage lockedToken = lockedTokens[lockId];
        return (lockedToken.user, lockedToken.amount, lockedToken.sourceChain, lockedToken.status);
    }

    // Function to get the balance of the contract
    function getBalance() external view returns (uint256) {
        return token.balanceOf(address(this));
    }
}
