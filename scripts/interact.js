// Import the Hardhat runtime environment
const hre = require("hardhat");

async function main() {
    // Replace with your deployed PiConverter contract address
    const piConverterAddress = "0xYourPiConverterAddress"; // Replace with the actual address
    const PiConverter = await hre.ethers.getContractFactory("PiConverter");
    const piConverter = await PiConverter.attach(piConverterAddress);

    // Example interaction: Get the current conversion rate
    const currentRate = await piConverter.getConversionRate();
    console.log("Current Conversion Rate:", currentRate.toString());

    // Example interaction: Set a new conversion rate
    const newRate = 150; // New conversion rate
    const setRateTx = await piConverter.setConversionRate(newRate);
    await setRateTx.wait();
    console.log("New Conversion Rate set to:", newRate);

    // Example interaction: Perform a conversion
    const amountToConvert = 10; // Amount to convert
    const convertedAmount = await piConverter.convert(amountToConvert);
    console.log(`Converted ${amountToConvert} units to:`, convertedAmount.toString());
}

// Execute the main function and handle errors
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("Error interacting with PiConverter:", error);
        process.exit(1);
    });
