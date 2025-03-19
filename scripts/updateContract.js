// updateContract.js
require('dotenv').config();
const { ethers, upgrades } = require('hardhat');

async function main() {
    // Ensure the user has provided the contract name and proxy address
    const contractName = process.argv[2];
    const proxyAddress = process.argv[3];

    if (!contractName || !proxyAddress) {
        console.error("Usage: node updateContract.js <ContractName> <ProxyAddress>");
        process.exit(1);
    }

    // Get the contract factory for the new implementation
    const Contract = await ethers.getContractFactory(contractName);

    console.log(`Updating contract at proxy address: ${proxyAddress} with new implementation: ${contractName}`);

    // Upgrade the contract
    try {
        const upgraded = await upgrades.upgradeProxy(proxyAddress, Contract);
        await upgraded.deployed();
        console.log(`Contract upgraded successfully! New implementation address: ${upgraded.address}`);
    } catch (error) {
        console.error("Error upgrading contract:", error);
        process.exit(1);
    }
}

// Execute the script
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
