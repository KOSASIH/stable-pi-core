// Import the Hardhat runtime environment
const hre = require("hardhat");

async function main() {
    // Get the contract factory for PiConverter
    const PiConverter = await hre.ethers.getContractFactory("PiConverter");

    // Define initial parameters
    const initialRate = process.env.INITIAL_RATE || 100; // Initial conversion rate
    const initialFeePercentage = process.env.INITIAL_FEE_PERCENTAGE || 2; // Initial fee percentage
    const feeCollector = process.env.FEE_COLLECTOR; // Fee collector address from environment variable

    // Validate fee collector address
    if (!feeCollector || !hre.ethers.utils.isAddress(feeCollector)) {
        console.error("Invalid fee collector address");
        process.exit(1);
    }

    // Validate initial parameters
    if (initialRate <= 0) {
        console.error("Initial rate must be greater than zero");
        process.exit(1);
    }

    if (initialFeePercentage < 0 || initialFeePercentage > 100) {
        console.error("Fee percentage must be between 0 and 100");
        process.exit(1);
    }

    // Deploy the contract with initial parameters
    console.log("Deploying PiConverter with the following parameters:");
    console.log(`Initial Rate: ${initialRate}`);
    console.log(`Initial Fee Percentage: ${initialFeePercentage}`);
    console.log(`Fee Collector Address: ${feeCollector}`);

    const piConverter = await upgrades.deployProxy(PiConverter, [initialRate, initialFeePercentage, feeCollector], { initializer: 'initialize' });

    // Wait for the deployment to be mined
    await piConverter.deployed();

    console.log("PiConverter deployed to:", piConverter.address);

    // Emit an event for successful deployment
    console.log(`PiConverter successfully deployed at ${piConverter.address} with initial rate ${initialRate} and fee percentage ${initialFeePercentage}`);
}

// Execute the main function and handle errors
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("Error deploying PiConverter:", error);
        process.exit(1);
    });
