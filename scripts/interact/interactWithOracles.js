// scripts/interact/interactWithOracles.js

const { ethers } = require("hardhat");
require("dotenv").config(); // Load environment variables from .env file
const readline = require("readline");

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

async function main() {
    const [signer] = await ethers.getSigners(); // Get the signer (the account that will interact with the oracles)

    // Retrieve oracle contract address from environment variables
    const oracleContractAddress = process.env.ORACLE_CONTRACT_ADDRESS;

    // Validate environment variable
    if (!oracleContractAddress) {
        console.error("Please set ORACLE_CONTRACT_ADDRESS in your .env file");
        process.exit(1);
    }

    // Interact with Oracle contract
    const OracleContract = await ethers.getContractAt("OracleContract", oracleContractAddress);
    console.log("Interacting with Oracle contract at:", oracleContractAddress);

    // Prompt user for action
    rl.question("Choose an action: (1) Get Price (2) Get Data (3) Exit: ", async (action) => {
        try {
            if (action === "1") {
                // Get price from oracle
                const price = await OracleContract.getPrice();
                console.log("Current price from oracle:", price.toString());
            } else if (action === "2") {
                // Get specific data from oracle
                const data = await OracleContract.getData();
                console.log("Data retrieved from oracle:", data);
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
        console.error("Error interacting with oracle:", error);
        process.exit(1);
    });
