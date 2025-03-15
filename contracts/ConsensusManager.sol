// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/structs/EnumerableSet.sol";

contract ConsensusManager is Ownable {
    using EnumerableSet for EnumerableSet.AddressSet;

    // Enum for consensus types
    enum ConsensusType { PoS, DPoS, Lightweight }

    // Current consensus mechanism
    ConsensusType public currentConsensus;

    // Set of validators
    EnumerableSet.AddressSet private validators;

    // Mapping of validator addresses to their stakes
    mapping(address => uint256) public stakes;

    // Total stake in the network
    uint256 public totalStake;

    // Events
    event ConsensusSwitched(ConsensusType newConsensus);
    event ValidatorAdded(address indexed validator, uint256 stake);
    event ValidatorRemoved(address indexed validator);
    event StakeUpdated(address indexed validator, uint256 newStake);

    constructor() {
        currentConsensus = ConsensusType.PoS; // Default consensus mechanism
    }

    // Function to switch consensus mechanism
    function switchConsensus(ConsensusType newConsensus) external onlyOwner {
        currentConsensus = newConsensus;
        emit ConsensusSwitched(newConsensus);
    }

    // Function to add a validator
    function addValidator(address validator, uint256 stake) external onlyOwner {
        require(validator != address(0), "Invalid validator address");
        require(stake > 0, "Stake must be greater than zero");

        if (!validators.contains(validator)) {
            validators.add(validator);
        }

        stakes[validator] += stake;
        totalStake += stake;

        emit ValidatorAdded(validator, stake);
        emit StakeUpdated(validator, stakes[validator]);
    }

    // Function to remove a validator
    function removeValidator(address validator) external onlyOwner {
        require(validators.contains(validator), "Validator not found");

        uint256 stake = stakes[validator];
        totalStake -= stake;

        validators.remove(validator);
        delete stakes[validator];

        emit ValidatorRemoved(validator);
    }

    // Function to get the current validators
    function getValidators() external view returns (address[] memory) {
        return validators.values();
    }

    // Function to get the total stake
    function getTotalStake() external view returns (uint256) {
        return totalStake;
    }

    // Function to get the current consensus type
    function getCurrentConsensus() external view returns (ConsensusType) {
        return currentConsensus;
    }
}
