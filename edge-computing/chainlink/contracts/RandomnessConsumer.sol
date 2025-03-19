// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract RandomnessConsumer is VRFConsumerBase {
    // Chainlink VRF parameters
    bytes32 internal keyHash;
    uint256 internal fee;

    // Mapping to store random results
    mapping(bytes32 => uint256) public randomResults;

    // Events
    event RandomNumberRequested(bytes32 indexed requestId);
    event RandomNumberReceived(bytes32 indexed requestId, uint256 randomNumber);

    constructor(address _vrfCoordinator, address _linkToken, bytes32 _keyHash, uint256 _fee) 
        VRFConsumerBase(_vrfCoordinator, _linkToken) {
        keyHash = _keyHash;
        fee = _fee; // Fee in LINK to request randomness
    }

    // Request a random number
    function requestRandomNumber() external returns (bytes32 requestId) {
        require(LINK.balanceOf(address(this)) >= fee, "Not enough LINK to pay fee");
        requestId = requestRandomness(keyHash, fee);
        emit RandomNumberRequested(requestId);
    }

    // Callback function used by VRF Coordinator
    function fulfillRandomness(bytes32 requestId, uint256 randomness) internal override {
        randomResults[requestId] = randomness;
        emit RandomNumberReceived(requestId, randomness);
    }

    // Function to retrieve the random number for a specific request ID
    function getRandomNumber(bytes32 requestId) external view returns (uint256) {
        require(randomResults[requestId] != 0, "Random number not yet generated");
        return randomResults[requestId];
    }

    // Function to withdraw LINK tokens from the contract
    function withdrawLINK() external {
        uint256 balance = LINK.balanceOf(address(this));
        require(balance > 0, "No LINK to withdraw");
        require(LINK.transfer(msg.sender, balance), "Transfer failed");
    }
}
