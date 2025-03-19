// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Proxy {
    // Storage for the implementation address
    address private implementation;
    // Storage for the contract owner
    address private owner;

    // Event to log upgrades
    event Upgraded(address indexed newImplementation);

    // Constructor to set the initial implementation and owner
    constructor(address _implementation) {
        require(_implementation != address(0), "Implementation address cannot be zero");
        implementation = _implementation;
        owner = msg.sender;
    }

    // Modifier to restrict access to the owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    // Function to upgrade the implementation contract
    function upgrade(address _newImplementation) external onlyOwner {
        require(_newImplementation != address(0), "New implementation address cannot be zero");
        require(_newImplementation != implementation, "New implementation must be different");
        
        implementation = _newImplementation;
        emit Upgraded(_newImplementation);
    }

    // Fallback function to delegate calls to the implementation contract
    fallback() external payable {
        address _impl = implementation;
        require(_impl != address(0), "Implementation not set");

        assembly {
            // Copy the function call data to memory
            calldatacopy(0, 0, calldatasize())
            // Delegate the call to the implementation
            let result := delegatecall(gas(), _impl, 0, calldatasize(), 0, 0)
            // Get the size of the returned data
            let size := returndatasize()
            // Copy the returned data to memory
            returndatacopy(0, 0, size)
            // Return the data to the caller
            switch result
            case 0 { revert(0, size) }
            default { return(0, size) }
        }
    }

    // Function to get the current implementation address
    function getImplementation() external view returns (address) {
        return implementation;
    }

    // Function to get the owner of the contract
    function getOwner() external view returns (address) {
        return owner;
    }
}
