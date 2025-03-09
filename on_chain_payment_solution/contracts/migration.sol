// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Migrations {
    address public owner;
    uint public lastCompletedMigration;

    event MigrationCompleted(uint completed);
    event MigrationUpgraded(address newAddress);

    modifier onlyOwner() {
        require(msg.sender == owner, "Caller is not the owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function setCompleted(uint completed) public onlyOwner {
        lastCompletedMigration = completed;
        emit MigrationCompleted(completed);
    }

    function upgrade(address newAddress) public onlyOwner {
        Migrations upgraded = Migrations(newAddress);
        upgraded.setCompleted(lastCompletedMigration);
        emit MigrationUpgraded(newAddress);
    }

    function getLastCompletedMigration() public view returns (uint) {
        return lastCompletedMigration;
    }
}
