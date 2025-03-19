// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract EscrowContract is AccessControl {
    using SafeMath for uint256;

    // Roles
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant ESCROW_ROLE = keccak256("ESCROW_ROLE");

    // Escrow structure
    struct Escrow {
        address buyer;
        address seller;
        uint256 amount;
        bool isCompleted;
        bool isDisputed;
        uint256 createdAt;
        uint256 resolvedAt;
    }

    // Mapping of escrow agreements
    mapping(uint256 => Escrow) public escrows;
    uint256 public escrowCount;

    // Events
    event EscrowCreated(uint256 indexed escrowId, address indexed buyer, address indexed seller, uint256 amount);
    event EscrowCompleted(uint256 indexed escrowId);
    event EscrowDisputed(uint256 indexed escrowId);
    event EscrowResolved(uint256 indexed escrowId, address indexed winner);

    constructor() {
        _setupRole(ADMIN_ROLE, msg.sender);
        _setupRole(ESCROW_ROLE, msg.sender);
    }

    // Create a new escrow agreement
    function createEscrow(address seller) external payable {
        require(msg.value > 0, "Amount must be greater than 0");
        require(seller != address(0), "Invalid seller address");

        escrowCount++;
        escrows[escrowCount] = Escrow({
            buyer: msg.sender,
            seller: seller,
            amount: msg.value,
            isCompleted: false,
            isDisputed: false,
            createdAt: block.timestamp,
            resolvedAt: 0
        });

        emit EscrowCreated(escrowCount, msg.sender, seller, msg.value);
    }

    // Complete the escrow agreement
    function completeEscrow(uint256 escrowId) external {
        Escrow storage escrow = escrows[escrowId];
        require(msg.sender == escrow.buyer || msg.sender == escrow.seller, "Not authorized");
        require(!escrow.isCompleted, "Escrow already completed");
        require(!escrow.isDisputed, "Escrow is disputed");

        escrow.isCompleted = true;
        payable(escrow.seller).transfer(escrow.amount);
        emit EscrowCompleted(escrowId);
    }

    // Dispute the escrow agreement
    function disputeEscrow(uint256 escrowId) external {
        Escrow storage escrow = escrows[escrowId];
        require(msg.sender == escrow.buyer || msg.sender == escrow.seller, "Not authorized");
        require(!escrow.isCompleted, "Escrow already completed");
        require(!escrow.isDisputed, "Escrow is already disputed");

        escrow.isDisputed = true;
        emit EscrowDisputed(escrowId);
    }

    // Resolve the dispute
    function resolveDispute(uint256 escrowId, address winner) external onlyRole(ADMIN_ROLE) {
        Escrow storage escrow = escrows[escrowId];
        require(escrow.isDisputed, "No dispute to resolve");
        require(!escrow.isCompleted, "Escrow already completed");

        escrow.isCompleted = true;
        escrow.resolvedAt = block.timestamp;

        // Transfer funds to the winner
        payable(winner).transfer(escrow.amount);
        emit EscrowResolved(escrowId, winner);
    }

    // Get escrow details
    function getEscrowDetails(uint256 escrowId) external view returns (
        address buyer,
        address seller,
        uint256 amount,
        bool isCompleted,
        bool isDisputed,
        uint256 createdAt,
        uint256 resolvedAt
    ) {
        Escrow storage escrow = escrows[escrowId];
        return (
            escrow.buyer,
            escrow.seller,
            escrow.amount,
            escrow.isCompleted,
            escrow.isDisputed,
            escrow.createdAt,
            escrow.resolvedAt
        );
    }
}
