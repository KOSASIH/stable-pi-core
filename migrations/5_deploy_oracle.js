// migrations/5_deploy_oracle.js

const Oracle = artifacts.require("Oracle");

module.exports = async function (deployer, network, accounts) {
    try {
        // Deploy the Oracle contract
        await deployer.deploy(Oracle);
        const oracleInstance = await Oracle.deployed();

        // Log the deployment
        console.log(`Oracle contract deployed at: ${oracleInstance.address}`);

        // Set up initial roles
        const adminRole = await oracleInstance.ADMIN_ROLE();
        const oracleRole = await oracleInstance.ORACLE_ROLE();

        // Grant the deployer the admin role
        await oracleInstance.grantRole(adminRole, accounts[0]);
        console.log(`Admin role granted to: ${accounts[0]}`);

        // Optionally, you can add additional accounts as oracles
        const additionalOracles = [accounts[1], accounts[2]]; // Example: Add the next two accounts as oracles

        for (const oracle of additionalOracles) {
            await oracleInstance.grantRole(oracleRole, oracle);
            console.log(`Oracle role granted to: ${oracle}`);
        }

        // Emit an event for successful deployment (if you have an event in the contract)
        // await oracleInstance.emitDeploymentEvent(oracleInstance.address); // Uncomment if you have an event

    } catch (error) {
        console.error("Error during Oracle contract deployment:", error);
    }
};
