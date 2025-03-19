// scripts/deploy/deployAutomatedContracts.js

const { ethers } = require("hardhat");
require("dotenv").config(); // Load environment variables from .env file

async function main() {
    // Retrieve contract addresses and parameters from environment variables
    const tokenAddress = process.env.TOKEN_ADDRESS; // ERC20 token address
    const priceFeedAddress = process.env.PRICE_FEED_ADDRESS; // Price feed address
    const exchangeAddress = process.env.EXCHANGE_ADDRESS; // Exchange address for trading

    // Validate environment variables
    if (!tokenAddress || !priceFeedAddress || !exchangeAddress) {
        console.error("Please set TOKEN_ADDRESS, PRICE_FEED_ADDRESS, and EXCHANGE_ADDRESS in your .env file");
        process.exit(1);
    }

    // Deploy AutomatedSupplyManager
    const AutomatedSupplyManager = await ethers.getContractFactory("AutomatedSupplyManager");
    const automatedSupplyManager = await AutomatedSupplyManager.deploy(
        tokenAddress,
        priceFeedAddress,
        314159 * 10**18, // Target price in wei (assuming 18 decimals)
        5, // Adjustment factor (5%)
        3600 // Adjustment cooldown (1 hour)
    );
    await automatedSupplyManager.deployed();
    console.log("AutomatedSupplyManager deployed to:", automatedSupplyManager.address);

    // Deploy AutomatedTradingBot
    const AutomatedTradingBot = await ethers.getContractFactory("AutomatedTradingBot");
    const automatedTradingBot = await AutomatedTradingBot.deploy(
        priceFeedAddress,
        tokenAddress,
        exchangeAddress
    );
    await automatedTradingBot.deployed();
    console.log("AutomatedTradingBot deployed to:", automatedTradingBot.address);

    // Deploy AutomatedEscrow
    const AutomatedEscrow = await ethers.getContractFactory("AutomatedEscrow");
    const automatedEscrow = await AutomatedEscrow.deploy();
    await automatedEscrow.deployed();
    console.log("AutomatedEscrow deployed to:", automatedEscrow.address);
}

// Execute the deployment script
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("Error deploying contracts:", error);
        process.exit(1);
    });
