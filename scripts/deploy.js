// Import the Hardhat runtime environment
const hre = require("hardhat");

async function main() {
    // Get the contract factory for PiConverter
    const PiConverter = await hre.ethers.getContractFactory("PiConverter");

    // Define initial parameters
    const initialRate = 100; // Initial conversion rate
    const initialFeePercentage = 2; // Initial fee percentage
    const feeCollector = "0xYourFeeCollectorAddress"; // Replace with the actual fee collector address

    // Validate fee collector address
    if (!hre.ethers.utils.isAddress(feeCollector)) {
        console.error("Invalid fee collector address");
        process.exit(1);
    }

    // Deploy the contract with initial parameters
    console.log("Deploying PiConverter with the following parameters:");
    console.log(`Initial Rate: ${initialRate}`);
    console.log(`Initial Fee Percentage: ${initialFeePercentage}`);
    console.log(`Fee Collector Address: ${feeCollector}`);

    const piConverter = await PiConverter.deploy(initialRate, initialFeePercentage, feeCollector);

    // Wait for the deployment to be mined
    await piConverter.deployed();

    console.log("PiConverter deployed to:", piConverter.address);
}

// Execute the main function and handle errors
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("Error deploying PiConverter:", error);
        process.exit(1);
    });
