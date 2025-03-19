// scripts/deploy/deployOracles.js

const { ethers } = require("hardhat");
require("dotenv").config(); // Load environment variables from .env file

async function main() {
    // Retrieve parameters from environment variables
    const decimals = process.env.ORACLE_DECIMALS || 18; // Default to 18 decimals if not set
    const description = process.env.ORACLE_DESCRIPTION || "Price Feed Oracle for PiCoin"; // Default description

    // Deploy PriceFeedOracle
    const PriceFeedOracle = await ethers.getContractFactory("PriceFeedOracle");
    const priceFeedOracle = await PriceFeedOracle.deploy(decimals, description);
    await priceFeedOracle.deployed();
    console.log("PriceFeedOracle deployed to:", priceFeedOracle.address);

    // Additional oracles can be deployed here if needed
    // const AnotherOracle = await ethers.getContractFactory("AnotherOracle");
    // const anotherOracle = await AnotherOracle.deploy(...);
    // await anotherOracle.deployed();
    // console.log("AnotherOracle deployed to:", anotherOracle.address);
}

// Execute the deployment script
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("Error deploying oracles:", error);
        process.exit(1);
    });
