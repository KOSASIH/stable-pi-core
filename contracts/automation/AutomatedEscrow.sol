// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract AutomatedEscrow is AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant ESCROW_MANAGER_ROLE = keccak256("ESCROW_MANAGER_ROLE");

    struct Escrow {
        address buyer;
        address seller;
        uint256 amount;
        bool isReleased;
        bool isDisputed;
        uint256 createdAt;
        uint256 releaseTime; // Time after which the escrow can be released automatically
    }

    mapping(uint256 => Escrow) public escrows;
    uint256 public escrowCount;

    event EscrowCreated(uint256 indexed escrowId, address indexed buyer, address indexed seller, uint256 amount, uint256 releaseTime);
    event EscrowReleased(uint256 indexed escrowId);
    event EscrowDisputed(uint256 indexed escrowId);
    event EscrowResolved(uint256 indexed escrowId, bool releaseToSeller);

    constructor() {
        _setupRole(ADMIN_ROLE, msg.sender);
        _setupRole(ESCROW_MANAGER_ROLE, msg.sender);
    }

    function createEscrow(address seller, uint256 amount, uint256 releaseDelay) external {
        require(amount > 0, "Amount must be greater than 0");
        require(releaseDelay > 0, "Release delay must be greater than 0");

        escrowCount++;
        escrows[escrowCount] = Escrow({
            buyer: msg.sender,
            seller: seller,
            amount: amount,
            isReleased: false,
            isDisputed: false,
            createdAt: block.timestamp,
            releaseTime: block.timestamp + releaseDelay
        });

        emit EscrowCreated(escrowCount, msg.sender, seller, amount, releaseTime);
    }

    function releaseEscrow(uint256 escrowId) external {
        Escrow storage escrow = escrows[escrowId];
        require(escrow.buyer == msg.sender || escrow.seller == msg.sender, "Only involved parties can release escrow");
        require(!escrow.isReleased, "Escrow already released");
        require(!escrow.isDisputed, "Escrow is disputed");
        require(block.timestamp >= escrow.releaseTime, "Release time has not been reached");

        // Logic to transfer tokens from the buyer to the seller
        // Example: IERC20(token).transfer(escrow.seller, escrow.amount);
        escrow.isReleased = true;

        emit EscrowReleased(escrowId);
    }

    function disputeEscrow(uint256 escrowId) external {
        Escrow storage escrow = escrows[escrowId];
        require(escrow.buyer == msg.sender || escrow.seller == msg.sender, "Only involved parties can dispute");
        require(!escrow.isReleased, "Escrow already released");
        require(!escrow.isDisputed, "Escrow already disputed");

        escrow.isDisputed = true;

        emit EscrowDisputed(escrowId);
    }

    function resolveDispute(uint256 escrowId, bool releaseToSeller) external onlyRole(ADMIN_ROLE) {
        Escrow storage escrow = escrows[escrowId];
        require(escrow.isDisputed, "Escrow is not disputed");

        if (releaseToSeller) {
            // Logic to transfer tokens to the seller
            // Example: IERC20(token).transfer(escrow.seller, escrow.amount);
        } else {
            // Logic to refund the buyer
            // Example: IERC20(token).transfer(escrow.buyer, escrow.amount);
        }

        escrow.isReleased = true;
        escrow.isDisputed = false; // Reset dispute status

        emit EscrowResolved(escrowId, releaseToSeller);
    }

    function getEscrowDetails(uint256 escrowId) external view returns (Escrow memory) {
        return escrows[escrowId];
    }
}
