// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";

contract Migrations is AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant MIGRATOR_ROLE = keccak256("MIGRATOR_ROLE");

    // Address of the contract owner
    address public owner;

    // Last completed migration
    uint public last_completed_migration;

    event MigrationCompleted(uint completed);

    modifier onlyAdmin() {
        require(hasRole(ADMIN_ROLE, msg.sender), "Not an admin");
        _;
    }

    modifier onlyMigrator() {
        require(hasRole(MIGRATOR_ROLE, msg.sender), "Not a migrator");
        _;
    }

    constructor() {
        owner = msg.sender;
        _setupRole(ADMIN_ROLE, msg.sender);
        _setupRole(MIGRATOR_ROLE, msg.sender);
    }

    // Function to set the completed migration
    function setCompleted(uint completed) public onlyMigrator {
        last_completed_migration = completed;
        emit MigrationCompleted(completed);
    }

    // Function to add a new migrator
    function addMigrator(address account) external onlyAdmin {
        grantRole(MIGRATOR_ROLE, account);
    }

    // Function to remove a migrator
    function removeMigrator(address account) external onlyAdmin {
        revokeRole(MIGRATOR_ROLE, account);
    }

    // Function to get the current migration status
    function getMigrationStatus() external view returns (uint) {
        return last_completed_migration;
    }
}
