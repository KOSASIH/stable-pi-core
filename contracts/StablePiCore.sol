// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Proxy.sol"; // Import the Proxy contract
import "./NewImplementation.sol"; // Import the new implementation contract

contract StablePiCore {
    // State variable to hold the proxy contract address
    Proxy private proxy;
    // Address of the contract owner
    address private owner;

    // Event to log the creation of the StablePiCore contract
    event StablePiCoreCreated(address indexed proxyAddress);
    // Event to log upgrades
    event ImplementationUpgraded(address indexed newImplementation);

    // Modifier to restrict access to the owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    // Constructor to deploy the proxy with the initial implementation
    constructor() {
        owner = msg.sender; // Set the contract deployer as the owner
        NewImplementation initialImplementation = new NewImplementation();
        proxy = new Proxy(address(initialImplementation));
        emit StablePiCoreCreated(address(proxy));
    }

    // Function to get the current implementation address from the proxy
    function getImplementation() external view returns (address) {
        return proxy.getImplementation();
    }

    // Function to upgrade the implementation contract
    function upgradeImplementation(address newImplementation) external onlyOwner {
        require(newImplementation != address(0), "Invalid implementation address");
        proxy.upgrade(newImplementation);
        emit ImplementationUpgraded(newImplementation);
    }

    // Function to interact with the implementation contract through the proxy
    function setValue(uint256 _value) external {
        (bool success, ) = address(proxy).call(abi.encodeWithSignature("setValue(uint256)", _value));
        require(success, "Failed to set value");
    }

    function getValue() external view returns (uint256) {
        (bool success, bytes memory data) = address(proxy).staticcall(abi.encodeWithSignature("getValue()"));
        require(success, "Failed to get value");
        return abi.decode(data, (uint256));
    }

    function incrementValue() external {
        (bool success, ) = address(proxy).call(abi.encodeWithSignature("incrementValue()"));
        require(success, "Failed to increment value");
    }

    function decrementValue() external {
        (bool success, ) = address(proxy).call(abi.encodeWithSignature("decrementValue()"));
        require(success, "Failed to decrement value");
    }

    function resetValue() external {
        (bool success, ) = address(proxy).call(abi.encodeWithSignature("resetValue()"));
        require(success, "Failed to reset value");
    }

    function multiplyValue(uint256 factor) external {
        (bool success, ) = address(proxy).call(abi.encodeWithSignature("multiplyValue(uint256)", factor));
        require(success, "Failed to multiply value");
    }

    function divideValue(uint256 divisor) external {
        (bool success, ) = address(proxy).call(abi.encodeWithSignature("divideValue(uint256)", divisor));
        require(success, "Failed to divide value");
    }

    function squareValue() external {
        (bool success, ) = address(proxy).call(abi.encodeWithSignature("squareValue()"));
        require(success, "Failed to square value");
    }

    // Function to get the owner of the contract
    function getOwner() external view returns (address) {
        return owner;
    }
}
