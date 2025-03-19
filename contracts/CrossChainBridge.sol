// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

contract CrossChainBridge is AccessControl, ReentrancyGuard {
    using ECDSA for bytes32;

    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR_ROLE");

    event TransferInitiated(address indexed from, address indexed to, uint256 amount, string targetChain, address token);
    event TransferCompleted(address indexed to, uint256 amount, string sourceChain, address token);
    event TransferFailed(bytes32 indexed transferId, string reason);
    event OperatorUpdated(address indexed operator, bool isActive);

    struct Transfer {
        address from;
        address to;
        uint256 amount;
        string targetChain;
        address token;
        bool completed;
    }

    mapping(bytes32 => Transfer) public transfers;
    mapping(address => bool) public operators;

    constructor() {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _setupRole(ADMIN_ROLE, msg.sender);
        _setupRole(OPERATOR_ROLE, msg.sender);
    }

    modifier onlyOperator() {
        require(operators[msg.sender], "Not an operator");
        _;
    }

    function setOperator(address _operator, bool _isActive) external onlyRole(ADMIN_ROLE) {
        operators[_operator] = _isActive;
        emit OperatorUpdated(_operator, _isActive);
    }

    function initiateTransfer(address _to, uint256 _amount, string calldata _targetChain, address _token) external nonReentrant {
        require(_amount > 0, "Amount must be greater than zero");
        require(IERC20(_token).transferFrom(msg.sender, address(this), _amount), "Transfer failed");

        bytes32 transferId = keccak256(abi.encodePacked(msg.sender, _to, _amount, _targetChain, _token, block.timestamp));
        
        transfers[transferId] = Transfer(msg.sender, _to, _amount, _targetChain, _token, false);
        
        emit TransferInitiated(msg.sender, _to, _amount, _targetChain, _token);
    }

    function completeTransfer(bytes32 _transferId, bytes calldata _signature) external onlyOperator nonReentrant {
        Transfer storage transfer = transfers[_transferId];
        require(!transfer.completed, "Transfer already completed");

        // Verify the signature
        bytes32 messageHash = keccak256(abi.encodePacked(_transferId));
        address signer = messageHash.toEthSignedMessageHash().recover(_signature);
        require(hasRole(OPERATOR_ROLE, signer), "Invalid signature");

        transfer.completed = true;
        require(IERC20(transfer.token).transfer(transfer.to, transfer.amount), "Transfer to recipient failed");

        emit TransferCompleted(transfer.to, transfer.amount, transfer.targetChain, transfer.token);
    }

    function failTransfer(bytes32 _transferId, string calldata reason) external onlyOperator {
        Transfer storage transfer = transfers[_transferId];
        require(!transfer.completed, "Transfer already completed");

        transfer.completed = true; // Mark as completed to prevent re-entrancy
        emit TransferFailed(_transferId, reason);
    }

    function getTransferInfo(bytes32 _transferId) external view returns (Transfer memory) {
        return transfers[_transferId];
    }

    function emergencyWithdraw(address _token, uint256 _amount) external onlyRole(ADMIN_ROLE) {
        require(IERC20(_token).transfer(msg.sender, _amount), "Emergency withdrawal failed");
    }
}
