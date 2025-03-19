// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts/utils/StorageSlot.sol";
import "@openzeppelin/contracts/utils/Address.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract UpgradeableProxy is Initializable, UUPSUpgradeable, AccessControl, ReentrancyGuard {
    // Define roles
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

    // Storage slot for the implementation address
    bytes32 internal constant _IMPLEMENTATION_SLOT = keccak256("my.proxy.implementation");
    bytes32 internal constant _VERSION_SLOT = keccak256("my.proxy.version");

    // Event emitted when the implementation is upgraded
    event Upgraded(address indexed implementation, string version);

    // Initialize the proxy with the initial implementation and admin
    function initialize(address initialImplementation, address admin) public initializer {
        _setImplementation(initialImplementation);
        _setupRole(ADMIN_ROLE, admin);
        _setVersion("1.0.0"); // Set initial version
    }

    // Fallback function to delegate calls to the implementation
    fallback() external payable {
        _delegate(_getImplementation());
    }

    receive() external payable {
        // Allow receiving Ether
    }

    // Function to get the current implementation address
    function _getImplementation() internal view returns (address) {
        return StorageSlot.getAddressSlot(_IMPLEMENTATION_SLOT).value;
    }

    // Function to set the implementation address
    function _setImplementation(address newImplementation) internal {
        require(Address.isContract(newImplementation), "New implementation is not a contract");
        StorageSlot.getAddressSlot(_IMPLEMENTATION_SLOT).value = newImplementation;
    }

    // Function to upgrade the implementation
    function upgradeTo(address newImplementation, string memory newVersion) external onlyRole(ADMIN_ROLE) nonReentrant {
        _setImplementation(newImplementation);
        _setVersion(newVersion);
        emit Upgraded(newImplementation, newVersion);
    }

    // Function to get the current version
    function getVersion() external view returns (string memory) {
        return _getVersion();
    }

    // Internal function to get the version
    function _getVersion() internal view returns (string memory) {
        return StorageSlot.getStringSlot(_VERSION_SLOT).value;
    }

    // Internal function to set the version
    function _setVersion(string memory newVersion) internal {
        StorageSlot.getStringSlot(_VERSION_SLOT).value = newVersion;
    }

    // Internal function to delegate calls to the implementation
    function _delegate(address implementation) internal {
        require(Address.isContract(implementation), "Delegate to non-contract");
        assembly {
            // Copy msg.data. We take full control of memory in this inline assembly
            // and we allocate a memory area for the data to copy.
            calldatacopy(0, 0, calldatasize())
            // Call the implementation
            // out and outsize are 0 because we don't know the size yet
            let result := delegatecall(gas(), implementation, 0, calldatasize(), 0, 0)
            // Copy the returned data
            returndatacopy(0, 0, returndatasize())
            switch result
            // delegatecall returns 0 on error
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }
}
