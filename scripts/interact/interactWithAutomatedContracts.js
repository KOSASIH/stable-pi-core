// scripts/interact/interactWithAutomatedContracts.js

const { ethers } = require("hardhat");
require("dotenv").config(); // Load environment variables from .env file
const readline = require("readline");

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

async function main() {
    const [signer] = await ethers.getSigners(); // Get the signer (the account that will interact with the contracts)

    // Retrieve contract addresses from environment variables
    const automatedSupplyManagerAddress = process.env.AUTOMATED_SUPPLY_MANAGER_ADDRESS;
    const piCoinDynamicPeggingAddress = process.env.PI_COIN_DYNAMIC_PEGGING_ADDRESS;

    // Validate environment variables
    if (!automatedSupplyManagerAddress || !piCoinDynamicPeggingAddress) {
        console.error("Please set AUTOMATED_SUPPLY_MANAGER_ADDRESS and PI_COIN_DYNAMIC_PEGGING_ADDRESS in your .env file");
        process.exit(1);
    }

    // Interact with AutomatedSupplyManager
    const AutomatedSupplyManager = await ethers.getContractAt("AutomatedSupplyManager", automatedSupplyManagerAddress);
    console.log("Interacting with AutomatedSupplyManager at:", automatedSupplyManagerAddress);

    // Interact with PiCoinDynamicPegging
    const PiCoinDynamicPegging = await ethers.getContractAt("PiCoinDynamicPegging", piCoinDynamicPeggingAddress);
    console.log("Interacting with PiCoinDynamicPegging at:", piCoinDynamicPeggingAddress);

    // Prompt user for action
    rl.question("Choose an action: (1) Adjust Supply (2) Adjust Peg (3) Exit: ", async (action) => {
        try {
            if (action === "1") {
                // Trigger supply adjustment
                const supplyManagerTx = await AutomatedSupplyManager.adjustSupply();
                await supplyManagerTx.wait();
                console.log("Supply adjustment triggered:", supplyManagerTx.hash);
            } else if (action === "2") {
                // Adjust peg
                const pegAdjustmentTx = await PiCoinDynamicPegging.adjustPeg();
                await pegAdjustmentTx.wait();
                console.log("Peg adjustment triggered:", pegAdjustmentTx.hash);
            } else if (action === "3") {
                console.log("Exiting...");
                rl.close();
                return;
            } else {
                console.log("Invalid action. Please choose 1, 2, or 3.");
            }
        } catch (error) {
            console.error("Error during interaction:", error);
        } finally {
            rl.close();
        }
    });
}

// Execute the interaction script
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("Error interacting with automated contracts:", error);
        process.exit(1);
    });
