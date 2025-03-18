// Import the necessary artifacts
const OrbitalDataMarketplace = artifacts.require("OrbitalDataMarketplace");

module.exports = async function (deployer, network, accounts) {
    try {
        // Log the network being used for deployment
        console.log(`Deploying to network: ${network}`);
        
        // Deploy the OrbitalDataMarketplace contract
        const instance = await deployer.deploy(OrbitalDataMarketplace, {
            gas: 5000000, // Set a gas limit for the deployment
            from: accounts[0] // Use the first account for deployment
        });

        console.log("OrbitalDataMarketplace contract deployed successfully at address:", instance.address);
    } catch (error) {
        console.error("Error deploying OrbitalDataMarketplace contract:", error);
    }
};
