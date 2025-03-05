// Import the Hardhat runtime environment
const hre = require("hardhat");

async function main() {
    // Get the contract factory for PiConverter
    const PiConverter = await hre.ethers.getContractFactory("PiConverter");

    // Deploy the contract with initial parameters
    const initialRate = 100; // Initial conversion rate
    const initialFeePercentage = 2; // Initial fee percentage
    const feeCollector = "0xYourFeeCollectorAddress"; // Replace with the actual fee collector address

    const piConverter = await PiConverter.deploy(initialRate, initialFeePercentage, feeCollector);

    // Wait for the deployment to be mined
    await piConverter.deployed();

    console.log("PiConverter deployed to:", piConverter.address);
}

// Execute the main function and handle errors
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
