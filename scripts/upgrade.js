// scripts/upgrade.js

const { ethers } = require("hardhat");

async function main() {
    // Get the address of the deployed proxy contract
    const proxyAddress = "YOUR_PROXY_CONTRACT_ADDRESS"; // Replace with your actual proxy address

    // Get the new implementation contract
    const NewImplementation = await ethers.getContractFactory("NewImplementation");
    const newImplementation = await NewImplementation.deploy();
    await newImplementation.deployed();
    console.log("New Implementation deployed to:", newImplementation.address);

    // Get the proxy contract instance
    const Proxy = await ethers.getContractAt("Proxy", proxyAddress);

    // Upgrade the implementation in the proxy contract
    const upgradeTx = await Proxy.upgrade(newImplementation.address);
    await upgradeTx.wait();
    console.log("Proxy upgraded to new implementation at:", newImplementation.address);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
