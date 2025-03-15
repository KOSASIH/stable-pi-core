// migrations/2_deploy_consensus_manager.js

const ConsensusManager = artifacts.require("ConsensusManager");

module.exports = async function (deployer, network, accounts) {
    try {
        // Deploy the ConsensusManager contract
        await deployer.deploy(ConsensusManager);
        const consensusManagerInstance = await ConsensusManager.deployed();

        // Log the deployment
        console.log(`ConsensusManager contract deployed at: ${consensusManagerInstance.address}`);

        // Optionally, you can set the initial consensus type if needed
        // await consensusManagerInstance.switchConsensus(0); // 0 for PoS, 1 for DPoS, etc.

        // Emit an event for successful deployment (if you have an event in the contract)
        // await consensusManagerInstance.emitDeploymentEvent(consensusManagerInstance.address); // Uncomment if you have an event

    } catch (error) {
        console.error("Error during ConsensusManager contract deployment:", error);
    }
};
