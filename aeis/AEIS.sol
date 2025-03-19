// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract AstroEconomicIncentiveSystem is ERC20, AccessControl, Pausable {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant CONTRIBUTOR_ROLE = keccak256("CONTRIBUTOR_ROLE");

    mapping(address => uint256) public contributions;

    event ContributionRecorded(address indexed contributor, uint256 amount);
    event TokensDistributed(address indexed contributor, uint256 reward);

    constructor(uint256 initialSupply) ERC20("Astro Economic Incentive Token", "AEIT") {
        _mint(msg.sender, initialSupply * 10 ** decimals());
        _setupRole(ADMIN_ROLE, msg.sender);
        _setupRole(CONTRIBUTOR_ROLE, msg.sender);
    }

    modifier onlyAdmin() {
        require(hasRole(ADMIN_ROLE, msg.sender), "Caller is not an admin");
        _;
    }

    modifier onlyContributor() {
        require(hasRole(CONTRIBUTOR_ROLE, msg.sender), "Caller is not a contributor");
        _;
    }

    function recordContribution(address contributor, uint256 amount) public onlyContributor whenNotPaused {
        require(amount > 0, "Contribution must be greater than zero");
        contributions[contributor] += amount;
        emit ContributionRecorded(contributor, amount);
    }

    function distributeTokens(address contributor) public onlyAdmin whenNotPaused {
        uint256 reward = calculateReward(contributor);
        require(reward > 0, "No rewards available");
        require(balanceOf(address(this)) >= reward, "Insufficient contract balance");

        _transfer(address(this), contributor, reward);
        emit TokensDistributed(contributor, reward);
        
        // Reset contributions after distribution
        contributions[contributor] = 0;
    }

    function calculateReward(address contributor) internal view returns (uint256) {
        // Example: Reward is 10% of contributions
        return contributions[contributor] / 10;
    }

    function getContribution(address contributor) public view returns (uint256) {
        return contributions[contributor];
    }

    function pause() public onlyAdmin {
        _pause();
    }

    function unpause() public onlyAdmin {
        _unpause();
    }

    function withdrawTokens(uint256 amount) public onlyAdmin {
        require(amount <= balanceOf(address(this)), "Insufficient balance");
        _transfer(address(this), msg.sender, amount);
    }
}
