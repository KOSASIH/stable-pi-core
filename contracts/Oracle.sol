// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract Oracle is AccessControl {
    using SafeMath for uint256;

    // Define roles
    bytes32 public constant ORACLE_ROLE = keccak256("ORACLE_ROLE");
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

    // Event to emit when new data is submitted
    event DataUpdated(string indexed dataType, string data, address indexed oracle, uint256 timestamp);

    // Struct to hold the data
    struct Data {
        string data;
        uint256 timestamp;
        address[] oracles;
        uint256 confirmations;
    }

    // Mapping to store data by type
    mapping(string => Data) private dataStore;

    // Maximum confirmations required for data to be considered valid
    uint256 public constant MAX_CONFIRMATIONS = 3;

    constructor() {
        _setupRole(ADMIN_ROLE, msg.sender);
        _setupRole(ORACLE_ROLE, msg.sender); // Initially, the deployer is an oracle
    }

    // Modifier to check if the sender is an oracle
    modifier onlyOracle() {
        require(hasRole(ORACLE_ROLE, msg.sender), "Caller is not an oracle");
        _;
    }

    // Function to submit data from an oracle
    function submitData(string memory dataType, string memory data) external onlyOracle {
        require(bytes(dataType).length > 0, "Data type cannot be empty");
        require(bytes(data).length > 0, "Data cannot be empty");

        Data storage dataEntry = dataStore[dataType];

        // Check if the data is already submitted
        if (dataEntry.timestamp == 0) {
            // New data entry
            dataEntry.data = data;
            dataEntry.timestamp = block.timestamp;
            dataEntry.oracles.push(msg.sender);
            dataEntry.confirmations = 1;
        } else {
            // Existing data entry, check for duplicates
            for (uint256 i = 0; i < dataEntry.oracles.length; i++) {
                require(dataEntry.oracles[i] != msg.sender, "Oracle has already submitted data for this type");
            }
            // Update data and increment confirmations
            dataEntry.confirmations = dataEntry.confirmations.add(1);
            dataEntry.oracles.push(msg.sender);
        }

        // Emit an event for the new data
        emit DataUpdated(dataType, data, msg.sender, block.timestamp);

        // Check if we have enough confirmations
        if (dataEntry.confirmations >= MAX_CONFIRMATIONS) {
            // Data is considered valid, further actions can be taken here
            // For example, you could trigger another event or call another contract
        }
    }

    // Function to retrieve data by type
    function getData(string memory dataType) external view returns (string memory, uint256, address[] memory) {
        Data memory dataEntry = dataStore[dataType];
        require(bytes(dataEntry.data).length > 0, "No data found for this type");

        return (dataEntry.data, dataEntry.timestamp, dataEntry.oracles);
    }

    // Function to delete data (only for admin)
    function deleteData(string memory dataType) external onlyRole(ADMIN_ROLE) {
        require(bytes(dataType).length > 0, "Data type cannot be empty");
        require(bytes(dataStore[dataType].data).length > 0, "No data found for this type");

        delete dataStore[dataType];
    }

    // Function to add an oracle (only for admin)
    function addOracle(address oracle) external onlyRole(ADMIN_ROLE) {
        grantRole(ORACLE_ROLE, oracle);
    }

    // Function to remove an oracle (only for admin)
    function removeOracle(address oracle) external onlyRole(ADMIN_ROLE) {
        revokeRole(ORACLE_ROLE, oracle);
    }
}
