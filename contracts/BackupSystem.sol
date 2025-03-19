// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract BackupSystem is ReentrancyGuard, Ownable {
    struct Asset {
        string name;
        uint256 amount;
        uint256 timestamp;
    }

    mapping(address => Asset[]) private userAssets;

    event AssetAdded(address indexed user, string name, uint256 amount, uint256 timestamp);
    event AssetRemoved(address indexed user, string name, uint256 amount, uint256 timestamp);

    modifier assetExists(uint256 _index) {
        require(_index < userAssets[msg.sender].length, "Asset does not exist");
        _;
    }

    function addAsset(string memory _name, uint256 _amount) public nonReentrant {
        require(_amount > 0, "Amount must be greater than zero");
        
        userAssets[msg.sender].push(Asset({
            name: _name,
            amount: _amount,
            timestamp: block.timestamp
        }));

        emit AssetAdded(msg.sender, _name, _amount, block.timestamp);
    }

    function removeAsset(uint256 _index) public nonReentrant assetExists(_index) {
        Asset memory assetToRemove = userAssets[msg.sender][_index];

        // Move the last asset into the place to delete
        userAssets[msg.sender][_index] = userAssets[msg.sender][userAssets[msg.sender].length - 1];
        userAssets[msg.sender].pop();

        emit AssetRemoved(msg.sender, assetToRemove.name, assetToRemove.amount, block.timestamp);
    }

    function getAssets() public view returns (Asset[] memory) {
        return userAssets[msg.sender];
    }

    function getAssetCount() public view returns (uint256) {
        return userAssets[msg.sender].length;
    }
}
